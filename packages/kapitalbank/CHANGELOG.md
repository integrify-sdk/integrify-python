# Changelog

All notable changes to `integrify-kapitalbank` are documented here. The format is
based on [Keep a Changelog](https://keepachangelog.com/) and this project follows
[Semantic Versioning](https://semver.org/).

## [1.1.0] - 2026-08-11

### Added

- Full type hints and autocomplete for the async client (`KapitalAsyncRequest`) via sync/async overloads.

### Changed

- Migrated payload handlers to the class-attribute style.
- `KAPITAL_ENV` is now normalized and warns on unknown values instead of silently using the test gateway.

### Fixed

- `link_card_token` no longer sends a double-encoded (stringified) JSON body; it now sends a proper JSON object.
- Response handling no longer crashes on non-JSON or empty response bodies.
- `ImportError` against `integrify-core>=1.1` (removed `_UNSET`/`Unsettable` names).

### Chore

- Requires `integrify-core>=1.2.0`.

## [1.0.0] - 2025-07-19

### Added

- Initial release — refactored from the [old library](https://github.com/mmzeynalli/integrify) to the new style.

[1.1.0]: https://github.com/integrify-sdk/integrify-python/compare/kapitalbank-1.0.0...kapitalbank-1.1.0
[1.0.0]: https://github.com/integrify-sdk/integrify-python/releases/tag/kapitalbank-1.0.0
