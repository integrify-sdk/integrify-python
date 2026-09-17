"""Build the whole docs site: public languages + password-protected private integrations.

Output (Netlify publish dir ``docs/site``)::

    docs/site/                      public az (site root)
    docs/site/en/                   public en
    docs/site/private/<name>/       private integration, az
    docs/site/en/private/<name>/    private integration, en

Everything under ``*/private/*`` is gated by ``netlify/edge-functions/private-docs.ts``.

Where the private sources come from, per entry in ``docs/private.yml``:

1. ``PRIVATE_DOCS_<NAME>_PATH`` env var: a local checkout.
2. ``PRIVATE_DOCS_TOKEN`` env var: fetched from GitHub (read-only token).
3. A sibling checkout next to this repo (``../<repo name>``): local development.
4. Otherwise the entry is skipped (fork PRs, contributors without access), unless
   ``PRIVATE_DOCS_REQUIRED=1``, in which case the build fails.

Usage::

    python scripts/build_docs.py                # everything
    python scripts/build_docs.py --public-only  # skip private integrations
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import zlib
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / 'docs'
SITE = DOCS / 'site'
REGISTRY = DOCS / 'private.yml'
CHECKOUTS = ROOT / '.private'

TRUTHY = {'1', 'true', 'yes', 'on'}
MIN_TEXT_LEN = 40  # search entries shorter than this are too generic to fingerprint
MAX_REPORTED = 20
MIN_DOTS = 2  # only fully-qualified names (pkg.module.Object) are searched for in public text
COPY_IGNORE = {'.git', '.venv', '.venvs', '.cache', '__pycache__', 'node_modules', 'coverage'}


@dataclass
class PrivateBuild:
    name: str
    lang: str
    out: Path
    pages: set[str] = field(default_factory=set)  # where the pages would live publicly
    inventory: set[str] = field(default_factory=set)
    texts: set[str] = field(default_factory=set)


# --------------------------------------------------------------------------- #
#  Helpers                                                                    #
# --------------------------------------------------------------------------- #


def log(msg: str) -> None:
    print(f'[docs] {msg}', flush=True)


def fail(msg: str) -> None:
    print(f'[docs] ERROR: {msg}', file=sys.stderr, flush=True)
    sys.exit(1)


def env_key(name: str) -> str:
    return re.sub(r'[^A-Z0-9]', '_', name.upper())


def rmtree(path: Path) -> None:
    """``shutil.rmtree`` that also removes read-only files (git objects on Windows)."""
    if not path.exists():
        return

    def _retry(func, p, *_):
        os.chmod(p, stat.S_IWRITE)
        func(p)

    if sys.version_info >= (3, 12):
        shutil.rmtree(path, onexc=_retry)
    else:
        shutil.rmtree(path, onerror=_retry)


def zensical_build(config: Path) -> None:
    log(f'zensical build -f {config.relative_to(ROOT)}')
    subprocess.run(
        [sys.executable, '-m', 'zensical', 'build', '-f', str(config), '--strict'],
        cwd=ROOT,
        check=True,
    )


def lang_root(prefix: str) -> Path:
    return SITE / prefix if prefix else SITE


def load_registry() -> dict:
    with REGISTRY.open(encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}
    data.setdefault('private', {})
    if not data.get('site_url') or not data.get('languages'):
        fail(f'{REGISTRY.relative_to(ROOT)} needs `site_url` and `languages`')
    data['site_url'] = data['site_url'].rstrip('/') + '/'
    return data


class _PyName(str):
    """A ``!!python/name:`` value, written back verbatim for Zensical to resolve."""


class _Loader(yaml.SafeLoader):
    pass


class _Dumper(yaml.SafeDumper):
    pass


_Loader.add_multi_constructor(
    'tag:yaml.org,2002:python/name:', lambda _loader, suffix, _node: _PyName(suffix)
)
_Dumper.add_representer(
    _PyName, lambda dumper, v: dumper.represent_scalar(f'tag:yaml.org,2002:python/name:{v}', '')
)


def load_config(path: Path) -> dict:
    with path.open(encoding='utf-8') as f:
        return yaml.load(f, Loader=_Loader) or {}  # SafeLoader subclass


def dump_config(config: dict, path: Path) -> None:
    text = yaml.dump(config, Dumper=_Dumper, sort_keys=False, allow_unicode=True)
    path.write_text(text, encoding='utf-8')


def mkdocstrings_paths(config: dict) -> list[str] | None:
    """The (mutable) mkdocstrings python ``paths`` list of a config, if any."""
    for plugin in config.get('plugins', []):
        if isinstance(plugin, dict) and 'mkdocstrings' in plugin:
            python = plugin['mkdocstrings'].setdefault('handlers', {}).setdefault('python', {})
            return python.setdefault('paths', [])
    return None


# --------------------------------------------------------------------------- #
#  Public site                                                                #
# --------------------------------------------------------------------------- #


def build_public(languages: dict[str, str]) -> None:
    for lang, prefix in languages.items():
        config = DOCS / lang / 'mkdocs.yml'
        built = config.parent / 'site'
        rmtree(built)
        # Zensical's cache keeps objects from earlier builds in objects.inv even after
        # their pages are gone, so a once-leaked private object would stay published.
        rmtree(config.parent / '.cache')
        zensical_build(config)
        target = lang_root(prefix)
        target.mkdir(parents=True, exist_ok=True)
        shutil.copytree(built, target, dirs_exist_ok=True)


# --------------------------------------------------------------------------- #
#  Private sources                                                            #
# --------------------------------------------------------------------------- #


def fetch_from_github(repo: str, ref: str, token: str, dest: Path) -> None:
    """Shallow-fetch ``ref`` (branch, tag or SHA) without writing the token to disk or argv."""
    basic = base64.b64encode(f'x-access-token:{token}'.encode()).decode()
    env = {
        **os.environ,
        'GIT_TERMINAL_PROMPT': '0',
        'GIT_CONFIG_COUNT': '1',
        'GIT_CONFIG_KEY_0': 'http.https://github.com/.extraheader',
        'GIT_CONFIG_VALUE_0': f'AUTHORIZATION: basic {basic}',
    }

    def git(*args: str) -> None:
        subprocess.run(['git', *args], cwd=dest, env=env, check=True)

    dest.mkdir(parents=True)
    git('init', '--quiet')
    git('remote', 'add', 'origin', f'https://github.com/{repo}.git')
    git('fetch', '--quiet', '--depth', '1', 'origin', ref)
    git('checkout', '--quiet', '--detach', 'FETCH_HEAD')


def copy_local(src: Path, dest: Path) -> None:
    def ignore(directory: str, names: list[str]) -> set[str]:
        skipped = COPY_IGNORE.intersection(names)
        # Built output of a standalone private build (docs/<lang>/site)
        if 'site' in names and 'mkdocs.yml' in names:
            skipped.add('site')
        return skipped

    shutil.copytree(src, dest, ignore=ignore)


def resolve_source(name: str, entry: dict) -> Path | None:
    dest = CHECKOUTS / name
    rmtree(dest)
    key = env_key(name)
    repo = entry['repo']

    explicit = os.environ.get(f'PRIVATE_DOCS_{key}_PATH')
    if explicit:
        log(f'{name}: using local checkout {explicit}')
        copy_local(Path(explicit).expanduser().resolve(), dest)
        return dest

    token = os.environ.get('PRIVATE_DOCS_TOKEN')
    if token:
        ref = str(entry.get('ref', 'main'))
        log(f'{name}: fetching {repo}@{ref}')
        fetch_from_github(repo, ref, token, dest)
        return dest

    sibling = ROOT.parent / repo.split('/')[-1]
    if sibling.is_dir():
        log(f'{name}: using sibling checkout {sibling}')
        copy_local(sibling, dest)
        return dest

    return None


# --------------------------------------------------------------------------- #
#  Private builds                                                             #
# --------------------------------------------------------------------------- #


def read_inventory(path: Path) -> set[str]:
    """Object names from a Sphinx v2 ``objects.inv``."""
    if not path.is_file():
        return set()
    raw = path.read_bytes()
    body = raw
    for _ in range(4):  # 4 plain-text header lines, then zlib
        body = body[body.index(b'\n') + 1 :]
    names = set()
    for line in zlib.decompress(body).decode('utf-8').splitlines():
        if line.strip():
            names.add(line.split(' ', 1)[0])
    return names


def read_search(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    data = json.loads(path.read_text(encoding='utf-8'))
    return data.get('items') or data.get('docs') or []


def page_paths(site: Path) -> set[str]:
    return {
        '' if p.parent == site else p.parent.relative_to(site).as_posix() + '/'
        for p in site.rglob('index.html')
    }


def write_root_redirect(site: Path, site_url: str) -> None:
    """Private sites often have no home page; send the section root to the first page."""
    if (site / 'index.html').exists():
        return
    sitemap = site / 'sitemap.xml'
    locs = re.findall(r'<loc>(.*?)</loc>', sitemap.read_text(encoding='utf-8'))
    target = next((loc[len(site_url) :] for loc in locs if loc.startswith(site_url)), None)
    if not target:
        return
    (site / 'index.html').write_text(
        '<!doctype html><meta charset="utf-8">'
        f'<meta http-equiv="refresh" content="0; url={target}">'
        f'<link rel="canonical" href="{target}">'
        f'<a href="{target}">{target}</a>\n',
        encoding='utf-8',
    )


def page_url(md: str) -> str:
    """``a/b.md`` -> ``a/b/``, ``a/index.md`` -> ``a/``, ``index.md`` -> ``''``."""
    stem = md[: -len('.md')]
    if stem == 'index':
        return ''
    return stem[: -len('index')] if stem.endswith('/index') else stem + '/'


def link_public_nav(nav: list, lang_path: str, titles: dict[str, str]) -> list:
    """Public nav with every page turned into an absolute link to the public site."""
    out = []
    for item in nav:
        if isinstance(item, str):
            url = page_url(item) if item.endswith('.md') else item
            label = titles.get(url, url)
            out.append({label: f'/{lang_path}{url}' if item.endswith('.md') else item})
            continue
        ((label, value),) = item.items()
        if isinstance(value, list):
            value = link_public_nav(value, lang_path, titles)
        elif isinstance(value, str) and value.endswith('.md'):
            value = f'/{lang_path}{page_url(value)}'
        out.append({label: value})
    return out


def rebase_private_nav(nav: list, prefix: str, name: str) -> tuple[str | None, list]:
    """Private nav relative to ``prefix``; unwraps a single top-level section."""
    label = None
    if len(nav) == 1 and isinstance(nav[0], dict):
        ((only_label, only_value),) = nav[0].items()
        if isinstance(only_value, list):
            label, nav = only_label, only_value

    def rebase(value: str) -> str:
        if not value.endswith('.md') or not prefix:
            return value
        if not value.startswith(prefix + '/'):
            fail(f'{name}: nav page {value} is outside {prefix}/')
        return value[len(prefix) + 1 :]

    def walk(items: list) -> list:
        out = []
        for item in items:
            if isinstance(item, str):
                out.append(rebase(item))
                continue
            ((key, value),) = item.items()
            out.append({key: walk(value) if isinstance(value, list) else rebase(value)})
        return out

    return label, walk(nav)


def merge_nav(public: list, private: list, label: str, target: str) -> list:
    """Put the private pages in the public nav entry that links to ``target``."""

    def links_to_target(value) -> bool:
        if isinstance(value, list):
            return any(
                isinstance(i, dict) and links_to_target(next(iter(i.values()))) for i in value
            )
        return isinstance(value, str) and value.rstrip('/') == target.rstrip('/')

    merged, found = [], False
    for item in public:
        if isinstance(item, dict):
            ((key, value),) = item.items()
            if links_to_target(value):
                merged.append({key: private})
                found = True
                continue
        merged.append(item)
    if not found:
        merged.append({label: private})
    return merged


def prepare_private_site(
    name: str, entry: dict, lang: str, checkout: Path, registry: dict
) -> tuple[Path, str]:
    """Write ``<checkout>/_site-<lang>/`` (pages, assets, overrides, mkdocs.yml).

    Returns the build directory and the private docs subdirectory that was published.
    """
    template = entry.get('config', 'docs/{lang}/mkdocs.yml').format(lang=lang)
    prefix = registry['languages'][lang]
    lang_path = f'{prefix}/' if prefix else ''
    url_path = f'{lang_path}private/{name}/'

    private_config_path = checkout / template
    if not private_config_path.is_file():
        fail(f'{name}: {template} not found in {entry["repo"]}')
    private_config = load_config(private_config_path)
    if not private_config.get('nav'):
        fail(f'{name}: {template} has no nav')
    private_dir = private_config_path.parent
    private_docs = private_dir / private_config.get('docs_dir', 'docs')
    pages = entry.get('pages')
    if pages is None:
        pages = f'integrations/{name}' if (private_docs / 'integrations' / name).is_dir() else ''

    public_dir = DOCS / lang
    config = load_config(public_dir / 'mkdocs.yml')
    public_docs = public_dir / config.get('docs_dir', 'docs')

    # The private pages at the docs root, plus the public assets and theme overrides
    build_dir = checkout / f'_site-{lang}'
    rmtree(build_dir)
    shutil.copytree(private_docs / pages, build_dir / 'docs')
    if (public_docs / 'assets').is_dir():
        shutil.copytree(public_docs / 'assets', build_dir / 'docs' / 'assets', dirs_exist_ok=True)
    theme = config.setdefault('theme', {})
    if theme.get('custom_dir'):
        shutil.copytree(public_dir / theme['custom_dir'], build_dir / 'overrides')
        theme['custom_dir'] = 'overrides'

    # Public sidebar, with this integration's section holding the private pages
    titles = {
        item['location']: html.unescape(item['title'])
        for item in read_search(lang_root(prefix) / 'search.json')
        if '#' not in item.get('location', '#')
    }
    label, private_nav = rebase_private_nav(private_config['nav'], pages, name)
    public_nav = link_public_nav(config.get('nav', []), lang_path, titles)
    config['nav'] = merge_nav(public_nav, private_nav, label or name, f'/{url_path}')

    # API reference: private sources first, then the public ones for cross-refs
    paths = mkdocstrings_paths(config)
    if paths is not None:
        own = [private_dir / p for p in (mkdocstrings_paths(private_config) or [])]
        paths[:] = [str(p.resolve()) for p in own + [public_dir / p for p in paths]]

    config.update(site_url=registry['site_url'] + url_path, docs_dir='docs', site_dir='site')
    config.setdefault('extra', {})['homepage'] = registry['site_url'] + lang_path
    dump_config(config, build_dir / 'mkdocs.yml')
    return build_dir, pages


def build_private(name: str, entry: dict, checkout: Path, registry: dict) -> list[PrivateBuild]:
    builds = []
    for lang in entry.get('langs', []):
        if lang not in registry['languages']:
            fail(f'{name}: language {lang!r} is not in `languages`')
        prefix = registry['languages'][lang]
        url_path = f'{prefix}/private/{name}/'.lstrip('/')

        build_dir, pages = prepare_private_site(name, entry, lang, checkout, registry)
        built = build_dir / 'site'
        zensical_build(build_dir / 'mkdocs.yml')
        write_root_redirect(built, registry['site_url'] + url_path)

        out = SITE / url_path
        rmtree(out)
        shutil.copytree(built, out)

        base_path = f'{pages}/' if pages else ''
        build = PrivateBuild(name=name, lang=lang, out=out)
        build.pages = {base_path + p for p in page_paths(built)}
        build.inventory = read_inventory(built / 'objects.inv')
        build.texts = {
            item['text'].strip()
            for item in read_search(built / 'search.json')
            if len(item.get('text', '').strip()) >= MIN_TEXT_LEN
        }
        builds.append(build)
        log(f'{name} [{lang}] -> /{url_path}')
    return builds


# --------------------------------------------------------------------------- #
#  Leak check                                                                 #
# --------------------------------------------------------------------------- #


def _leaks_in_language(root: Path, lang: str, builds: list[PrivateBuild], is_private) -> list[str]:
    problems = []
    public_pages = {p for p in page_paths(root) if not is_private(root / p)}
    search = read_search(root / 'search.json')
    search_pages = {str(i.get('location', '')).split('#')[0] for i in search}
    sitemap = (root / 'sitemap.xml').read_text(encoding='utf-8')
    if '/private/' in sitemap:
        problems.append(f'[{lang}] public sitemap mentions /private/')
    sitemap_paths = {
        urlparse(loc).path.strip('/') + '/' for loc in re.findall(r'<loc>(.*?)</loc>', sitemap)
    }

    for b in (b for b in builds if b.lang == lang):
        lang_path = str(b.out.relative_to(SITE).parent.parent)
        lang_path = '' if lang_path == '.' else lang_path + '/'
        for page in sorted(b.pages - public_pages - {''}):
            if page in search_pages:
                problems.append(f'[{lang}] public search index has private page {page}')
            if (lang_path + page) in sitemap_paths:
                problems.append(f'[{lang}] public sitemap lists private page {page}')
        for item in search:
            if item.get('text', '').strip() in b.texts:
                loc = item.get('location')
                problems.append(f'[{lang}] public search entry {loc} repeats {b.name} content')
    return problems


def _qualified_names_in_public_text(builds: list[PrivateBuild], is_private) -> list[str]:
    qualified = {n for b in builds for n in b.inventory if n.count('.') >= MIN_DOTS}
    if not qualified:
        return []
    pattern = re.compile('|'.join(re.escape(n) for n in sorted(qualified, key=len, reverse=True)))
    problems = []
    for path in SITE.rglob('*'):
        if path.suffix not in {'.html', '.json', '.xml', '.txt'} or is_private(path):
            continue
        match = pattern.search(path.read_text(encoding='utf-8', errors='ignore'))
        if match:
            rel = path.relative_to(SITE).as_posix()
            problems.append(f'{rel} mentions private object {match.group(0)}')
    return problems


def check_leaks(builds: list[PrivateBuild], languages: dict[str, str]) -> None:
    """Fail if anything from a private build shows up in the public output."""
    private_dirs = [b.out for b in builds]

    def is_private(path: Path) -> bool:
        return any(path.is_relative_to(d) for d in private_dirs)

    problems: list[str] = []
    public_inventory: set[str] = set()
    for lang, prefix in languages.items():
        root = lang_root(prefix)
        public_inventory |= read_inventory(root / 'objects.inv')
        problems += _leaks_in_language(root, lang, builds, is_private)

    for b in builds:
        problems += [
            f'public objects.inv documents private object {o}'
            for o in sorted(b.inventory & public_inventory)
        ]
    problems += _qualified_names_in_public_text(builds, is_private)

    if problems:
        shown = problems[:MAX_REPORTED]
        if len(problems) > MAX_REPORTED:
            shown.append(f'... and {len(problems) - MAX_REPORTED} more')
        fail('private content leaked into the public site:\n  - ' + '\n  - '.join(shown))
    log('leak check passed')


# --------------------------------------------------------------------------- #
#  Main                                                                       #
# --------------------------------------------------------------------------- #


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('--public-only', action='store_true', help='skip private integrations')
    args = parser.parse_args()

    registry = load_registry()
    required = os.environ.get('PRIVATE_DOCS_REQUIRED', '').lower() in TRUTHY

    rmtree(SITE)
    build_public(registry['languages'])

    builds: list[PrivateBuild] = []
    if not args.public_only:
        for name, entry in registry['private'].items():
            if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', name):
                fail(f'private integration name {name!r} must be lowercase [a-z0-9-]')
            checkout = resolve_source(name, entry)
            if checkout is None:
                msg = f'{name}: no source (set PRIVATE_DOCS_TOKEN)'
                if required:
                    fail(msg)
                log(f'{msg}; skipping')
                continue
            builds.extend(build_private(name, entry, checkout, registry))

    if builds:
        check_leaks(builds, registry['languages'])
    log(f'done -> {SITE.relative_to(ROOT)}')


if __name__ == '__main__':
    try:
        main()
    except subprocess.CalledProcessError as e:
        fail(f'command failed ({e.returncode}): {" ".join(map(str, e.cmd))}')
