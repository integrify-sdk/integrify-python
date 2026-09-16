# Changelog

All notable changes to `integrify-lsim` are documented here. The format is based
on [Keep a Changelog](https://keepachangelog.com/) and this project follows
[Semantic Versioning](https://semver.org/).

## [1.1.0] - 2026-08-11

### Added

- Full type hints and autocomplete for the async clients (single & bulk) via sync/async overloads.

### Changed

- Migrated single-SMS payload handlers to the class-attribute style.

### Fixed

- The single-SMS report handler no longer crashes on empty or non-numeric report bodies; the response is now built safely.

### Chore

- Requires `integrify-core>=1.2.0`.

## [1.0.0] - 2025-07-19

### Added

- Initial release — refactored from the [old library](https://github.com/mmzeynalli/integrify) to the new style.

[1.1.0]: https://github.com/integrify-sdk/integrify-python/compare/lsim-1.0.0...lsim-1.1.0
[1.0.0]: https://github.com/integrify-sdk/integrify-python/releases/tag/lsim-1.0.0
