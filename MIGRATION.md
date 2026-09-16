# Monorepo Migration Guide

This document is for maintainers who are moving existing per-integration
repositories into this monorepo.

User-facing usage and installation docs belong in [README.md](./README.md).

## Goal

Import each existing repository into `packages/` while preserving full git
history, then standardize workspace configuration so everything builds and tests
together.

## Prerequisites

- Run commands from the root of this repository.
- Ensure your working tree is clean before each subtree import.
- Confirm target package names match root `pyproject.toml` extras and
    `tool.uv.sources` entries.

## 1. Import repositories with history

Use `git subtree add` for each package.

```bash
# Shared core first.
git subtree add --prefix=packages/core \
  https://github.com/integrify-sdk/integrify-core-python.git main

# Integrations.
git subtree add --prefix=packages/epoint \
  https://github.com/integrify-sdk/integrify-epoint-python.git main
git subtree add --prefix=packages/kapitalbank \
  https://github.com/integrify-sdk/integrify-kapitalbank-python.git main
git subtree add --prefix=packages/azericard \
  https://github.com/integrify-sdk/integrify-azericard-python.git main
git subtree add --prefix=packages/clopos \
  https://github.com/integrify-sdk/integrify-clopos-python.git main
git subtree add --prefix=packages/lsim \
  https://github.com/integrify-sdk/integrify-lsim-python.git main
git subtree add --prefix=packages/postaguvercini \
    https://github.com/integrify-sdk/integrify-postaguvercini-python.git main
```

Why subtree:

- Preserves commit history from each old repo.
- Keeps a clean package boundary under `packages/<distribution-name>/`.
- Allows temporary sync with old repos via `git subtree pull` during transition.

## 2. Normalize each imported package

For each imported member package:

1. Keep package-local structure (`src/integrify/<name>/`, tests, local metadata).
2. Keep publish-time dependency constraints in `[project.dependencies]`
     (for example `integrify-core>=x.y.z`).
3. Remove duplicated repository-level tooling only after root-level equivalents
     exist (CI, lint config, pre-commit, release automation).
4. Ensure package `name` matches the distribution naming convention:
     `integrify-<integration>`.

## 3. Verify root workspace wiring

In root `pyproject.toml`, ensure each imported package appears in:

- `[project.optional-dependencies]`
- `all` extra
- `[tool.uv.sources]` as `{ workspace = true }`

Then run:

```bash
uv sync
uv run pytest
uv run ruff check .
```

## 4. Release model after migration

- `integrify` remains the umbrella distribution.
- Member distributions are still published independently.

Example:

```bash
uv build --package integrify-epoint
uv publish
```

## 5. Optional transition phase

If old repositories are still receiving commits briefly, pull updates using:

```bash
git subtree pull --prefix=packages/epoint \
    https://github.com/integrify-sdk/integrify-epoint-python.git main
```

Stop this once the old repository is frozen.

## Migration tracker (template)

Use this checklist to track progress:

- [ ] integrify-core imported
- [ ] integrify-epoint imported
- [ ] integrify-kapitalbank imported
- [ ] integrify-azericard imported
- [ ] integrify-clopos imported
- [ ] integrify-lsim imported
- [ ] integrify-postaguvercini imported
- [ ] root extras updated
- [ ] root uv sources updated
- [ ] workspace sync and tests passing
