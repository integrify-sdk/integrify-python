# Changelog

All notable changes to `integrify-epoint` are documented here. The format is based
on [Keep a Changelog](https://keepachangelog.com/) and this project follows
[Semantic Versioning](https://semver.org/).

## [1.3.0] - 2026-09-22

### Added

- Apple Pay & Google Pay widget: `create_widget` (`/api/1/token/widget`), returning a `widget_url` to embed in an iframe/webview.
- Apple Pay & Google Pay via EPoint's JS SDK (token payment API): `create_token_payment`, `apple_pay_session`, `apple_pay`, `google_pay`.
- `WidgetResponseSchema`, `TokenPaymentResponseSchema` and `TokenPayResponseSchema` response schemas.

## [1.2.0] - 2026-08-11

### Added

- Full type hints and autocomplete for the async client (`EPointAsyncRequest`) via sync/async overloads.

### Changed

- Migrated payload handlers to the class-attribute style.

### Fixed

- Response/callback parsing no longer crashes on unknown bank response codes (`Code[...]` `KeyError`); unknown codes fall back to the raw code.

### Chore

- Requires `integrify-core>=1.2.0`.

## [1.1.0] - 2025-11-24

### Added

- Support for both the old and new versions of `integrify-core`.

## [1.0.0] - 2025-07-19

### Added

- Initial release — refactored from the [old library](https://github.com/mmzeynalli/integrify) to the new style.

[1.3.0]: https://github.com/integrify-sdk/integrify-python/compare/epoint-1.2.0...epoint-1.3.0
[1.2.0]: https://github.com/integrify-sdk/integrify-python/compare/epoint-1.1.0...epoint-1.2.0
[1.1.0]: https://github.com/integrify-sdk/integrify-python/compare/epoint-1.0.0...epoint-1.1.0
[1.0.0]: https://github.com/integrify-sdk/integrify-python/releases/tag/epoint-1.0.0
