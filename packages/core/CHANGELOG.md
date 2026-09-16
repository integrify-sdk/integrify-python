# Changelog

All notable changes to `integrify-core` are documented here. The format is based
on [Keep a Changelog](https://keepachangelog.com/) and this project follows
[Semantic Versioning](https://semver.org/).

## [1.3.0] - 2026-08-17

### Changed

- Widened the `_ResponseT` bound to `BaseModel | dict | list`, so integrations whose
  endpoints return a JSON array at the root can type their responses as
  `APIResponse[list[SomeSchema]]`.

## [1.2.0] - 2026-08-11

### Added

- Handler `req_model`, `resp_model` and `dry` can be declared as class attributes, in addition to `__init__` arguments (backward compatible).
- Sync/async type markers `_Sync`, `_Async` and the `_Mode` `TypeVar`, enabling correctly-typed async clients through overloads.
- Lazy `httpx` client with `close()`/`aclose()` and (async) context-manager support — importing a client no longer opens connections.
- Configurable request `timeout` (default: 10s).

### Changed

- Payload handlers are now **stateless**: the request model is built per-call instead of being stored on the handler, so shared/singleton handlers are safe under concurrent (including async) requests.
- `APIClient` dispatches requests via `__getattr__` instead of `__getattribute__` (faster; only triggered on an attribute miss).

### Fixed

- Non-JSON or empty response bodies no longer raise `JSONDecodeError`; `APIResponse` now decodes defensively.
- `PayloadBaseModel.from_args` now raises on duplicate or excess positional arguments.

## [1.1.1] - 2026-08-08

### Chore

- Raised the maximum supported `httpx` version from 0.28 to 1.
- Added Dependabot.

## [1.1.0] - 2025-10-28

### Added

- `UNSET` constant for distinguishing `None` from missing/unset values, plus `UnsetField`/`UnsetOrNoneField` annotated pydantic fields.
- Requests can now pass the request headers as an argument (see Clopos).
- `_build_request_lambda` hook so subclasses can enforce arguments without overriding `__getattribute__`.

### Chore

- Raised the minimum `pydantic` version from 2.8 to 2.11.

## [1.0.5] - 2025-10-20

### Fixed

- Made `integrify-core` a proper namespace package.

## [1.0.3] - 2025-07-19

### Added

- Initial release — refactored from the [old library](https://github.com/mmzeynalli/integrify) to the new style.

[1.2.0]: https://github.com/integrify-sdk/integrify-python/compare/core-1.1.1...core-1.2.0
[1.1.1]: https://github.com/integrify-sdk/integrify-python/compare/core-1.1.0...core-1.1.1
[1.1.0]: https://github.com/integrify-sdk/integrify-python/compare/core-1.0.5...core-1.1.0
[1.0.5]: https://github.com/integrify-sdk/integrify-python/compare/core-1.0.3...core-1.0.5
[1.0.3]: https://github.com/integrify-sdk/integrify-python/releases/tag/core-1.0.3
