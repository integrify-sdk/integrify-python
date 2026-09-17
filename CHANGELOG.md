<!-- markdownlint-disable MD024 -->

# Changelog

All notable changes to `integrify` (the umbrella package) are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/) and this
project follows [Semantic Versioning](https://semver.org/).

## [3.0.0] - 2026-08-13

Re-architected from a single monolithic package into an **umbrella package over a
monorepo of independently-published integrations**. The top-level `integrify`
distribution ships no integration code of its own — install only what you need:

- `pip install integrify` — shared core only
- `pip install integrify[epoint]` — core + EPoint
- `pip install integrify[epoint,lsim]` — core + selected integrations
- `pip install integrify[all]` — every integration

Import paths are unchanged (`integrify.epoint`, `integrify.kapitalbank`, …).

### Changed

- Split into an umbrella plus per-integration distributions (`integrify-epoint`, `integrify-core`, …), each pulled in through its extra.

### Removed

- **Breaking:** replaced the previous monolithic `integrify` (last release 2.2.2); integrations must now be opted into via extras.
- **Breaking:** dropped Python 3.9 (end-of-life) — now requires Python >= 3.10.

## [2.2.0] - 2025-03-03

### Added

- LSIM integration
- PostaGuvercini integration ([kazimovzaman2](https://github.com/kazimovzaman2))
- `_UNSET` logic to distinguish between unset and `None` values

### Changed

- Migrated from Poetry to uv
- Switched the Makefile to the Python `duty` library
- Dry-run responses are now a `TypedDict` instead of a plain `dict`

### Fixed

- GET requests were sending data in the body instead of as query params
- Replaced remaining mock requests with live ones
- Outdated Kapital test-card documentation ([AlifaghaSalmanov](https://github.com/AlifaghaSalmanov))

## [2.1.1] - 2025-01-27

### Added

- Dry-run functionality per request

### Fixed

- API URL generation for async requests

## [2.1.0] - 2025-01-17

### Added

- KapitalBank integration ([kazimovzaman2](https://github.com/kazimovzaman2))
- Dry-run functionality per request class

### Removed

- Support for Python 3.8

## [2.0.1] - 2024-10-28

### Added

- More detailed documentation

### Changed

- Reworked the whole request/response structure for better handling
- Increased test coverage

## [1.0.3] - 2024-10-07

### Fixed

- Replaced `StrEnum` with `str, Enum` for Python <3.11 compatibility

## [1.0.1] - 2024-09-28

### Fixed

- Updated version for PyPI

## [1.0.0] - 2024-09-27

### Added

- EPoint integration
- EPoint documentation

[3.0.0]: https://github.com/integrify-sdk/integrify-python/compare/v2.2.2...integrify-3.0.0
[2.2.0]: https://github.com/integrify-sdk/integrify-python/compare/v2.1.1...v2.2.0
[2.1.1]: https://github.com/integrify-sdk/integrify-python/compare/v2.1.0...v2.1.1
[2.1.0]: https://github.com/integrify-sdk/integrify-python/compare/v2.0.1...v2.1.0
[2.0.1]: https://github.com/integrify-sdk/integrify-python/compare/v1.0.3...v2.0.1
[1.0.3]: https://github.com/integrify-sdk/integrify-python/compare/v1.0.1...v1.0.3
[1.0.1]: https://github.com/integrify-sdk/integrify-python/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/integrify-sdk/integrify-python/releases/tag/v1.0.0
