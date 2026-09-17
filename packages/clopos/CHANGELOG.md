# Changelog

All notable changes to `integrify-clopos` are documented here. The format is based
on [Keep a Changelog](https://keepachangelog.com/) and this project follows
[Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-08-11

### Added

- Full type hints and autocomplete for the async client (`CloposAsyncRequest`) via sync/async overloads.
- **Price lists**: `get_price_lists` (`GET price-lists`, returns `PriceList`) and `get_price_list_prices` (`GET price-lists/prices`, returns `PriceListPrice`).
- **Receipts**: `close_receipt` (`POST receipts/{id}/close`) and `get_receipt_stock_operations` (`GET receipts/{id}/stock-operations`, returns `ReceiptStockOperation`).

### Changed

- Migrated to Clopos Open API **v2** (base URL `https://integrations.clopos.com/open-api/v2/`).
- Authentication now uses `integrator_id` (env var `CLOPOS_INTEGRATOR_ID`) instead of `venue_id`.
- v2 requests send only the `x-token` header; `x-brand` is no longer sent and `x-venue` is now optional (overrides the venue encoded in the JWT).
- `AuthResponse` now includes the `expires_at` field.
- Updated handlers for the stateless handler API in `integrify-core` 1.2.0.

### Removed

- **Receipts**: `create_receipt`, `update_receipt` and `delete_receipt` — no longer part of Open API v2.

### Chore

- Requires `integrify-core>=1.2.0`.

### Notes

- Nested relation objects on the new schemas (`PriceList.prices` product/list relations, `ReceiptStockOperation.product`/`stock`) are typed as `dict` where the exact nested shapes were not verifiable from the API docs.

## [0.0.1] - 2025-12-01

### Added

- Initial integration with full API support (not production-tested).

[0.1.0]: https://github.com/integrify-sdk/integrify-python/compare/clopos-0.0.1...clopos-0.1.0
[0.0.1]: https://github.com/integrify-sdk/integrify-python/releases/tag/clopos-0.0.1
