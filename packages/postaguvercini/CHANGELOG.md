# Changelog

All notable changes to `integrify-postaguvercini` are documented here. The format
is based on [Keep a Changelog](https://keepachangelog.com/) and this project
follows [Semantic Versioning](https://semver.org/).

## [1.1.0] - 2026-08-11

### Added

- Full type hints and autocomplete for the async client (`PostaGuverciniAsyncClient`) via sync/async overloads.

### Changed

- Migrated payload handlers to the class-attribute style.

### Fixed

- `ImportError` that prevented the package from importing against `integrify-core>=1.1` (removed `_UNSET`/`Unsettable` names).

### Chore

- Requires `integrify-core>=1.2.0`.

## [1.0.0] - 2025-07-19

### Added

- Initial release — refactored from the [old library](https://github.com/mmzeynalli/integrify) to the new style.

[1.1.0]: https://github.com/integrify-sdk/integrify-python/compare/postaguvercini-1.0.0...postaguvercini-1.1.0
[1.0.0]: https://github.com/integrify-sdk/integrify-python/releases/tag/postaguvercini-1.0.0
