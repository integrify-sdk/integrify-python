# Changelog

All notable changes to `integrify-azericard` are documented here. The format is
based on [Keep a Changelog](https://keepachangelog.com/) and this project follows
[Semantic Versioning](https://semver.org/).

## [1.1.0] - 2026-08-11

### Added

- Full type hints and autocomplete for the async client (`AzeriCardAsyncClient`) via sync/async overloads.

### Changed

- Migrated payload handlers to the class-attribute style.
- The RSA signing key is now read and parsed once (cached) instead of on every request.
- `AZERICARD_ENV` is now normalized and warns on unknown values instead of silently using the test gateway.

### Fixed

- `ImportError` against `integrify-core>=1.1` (removed `_UNSET`/`Unsettable` names).

### Security

- HTML auto-submit form values are now HTML-escaped, preventing attribute/markup injection.

### Chore

- Requires `integrify-core>=1.2.0`.

## [1.0.0] - 2025-07-19

### Added

- Initial release — refactored from the [old library](https://github.com/mmzeynalli/integrify) to the new style.

[1.1.0]: https://github.com/integrify-sdk/integrify-python/compare/azericard-1.0.0...azericard-1.1.0
[1.0.0]: https://github.com/integrify-sdk/integrify-python/releases/tag/azericard-1.0.0
