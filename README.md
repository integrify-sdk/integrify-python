# Integrify

<!-- markdownlint-disable MD033 -->
<p align="center">
  <a href="https://integrify.mmzeynalli.dev/"><img width="400" src="https://raw.githubusercontent.com/integrify-sdk/integrify-python/main/docs/assets/integrify.png" alt="Integrify"></a>
</p>

<p align="center">
  <a href="https://pypi.org/project/integrify/"><img alt="PyPI package" src="https://img.shields.io/pypi/v/integrify?color=%2334D058&label=pypi%20package"></a>
  <a href="https://pypi.org/project/integrify/"><img alt="Supported Python versions" src="https://img.shields.io/pypi/pyversions/integrify.svg?color=%2334D058"></a>
  <a href="https://pepy.tech/project/integrify"><img alt="Downloads" src="https://static.pepy.tech/badge/integrify"></a>
  <a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/integrify-sdk/integrify-python"><img alt="Coverage" src="https://coverage-badge.samuelcolvin.workers.dev/integrify-sdk/integrify-python.svg"></a>
  <br>
  <a href="https://www.gnu.org/licenses/mit.en.html"><img alt="License" src="https://img.shields.io/badge/license-MIT-16A34A"></a>
  <a href="https://docs.astral.sh/uv/"><img alt="uv workspace" src="https://img.shields.io/badge/uv-workspace-111827?logo=python&logoColor=white"></a>
  <a href="https://github.com/integrify-sdk/integrify-python"><img alt="Monorepo" src="https://img.shields.io/badge/monorepo-integrations-0F766E"></a>
</p>
<!-- markdownlint-enable MD033 -->

---

Integrify API inteqrasiyalarını rahatlaşdıran Python kitabxanasıdır. Bu repository bütün Integrify paketlərini bir monorepo daxilində birləşdirir: shared core + ayrıca publish olunan integration paketləri.

**English below:** [English section](#english)

## Mündəricat / Table of Contents

- [Integrify](#integrify)
  - [Mündəricat / Table of Contents](#mündəricat--table-of-contents)
  - [Azərbaycanca](#azərbaycanca)
    - [Dokumentasiya](#dokumentasiya)
    - [Əsas özəlliklər](#əsas-özəlliklər)
    - [Kitabxananın yüklənməsi](#kitabxananın-yüklənməsi)
    - [İstifadəsi](#i̇stifadəsi)
      - [Sync nümunə](#sync-nümunə)
      - [Async nümunə](#async-nümunə)
      - [Sorğu cavabı](#sorğu-cavabı)
    - [Dəstəklənən paketlər](#dəstəklənən-paketlər)
  - [English](#english)
    - [Documentation](#documentation)
    - [Key features](#key-features)
    - [Installation](#installation)
    - [Usage](#usage)
      - [Sync example](#sync-example)
      - [Async example](#async-example)
      - [Response object shape](#response-object-shape)
    - [Supported packages](#supported-packages)

---

## Azərbaycanca

### Dokumentasiya

- Dokumentasiya portalı: [https://integrify.mmzeynalli.dev](https://integrify.mmzeynalli.dev)
- Kod bazası: [https://github.com/integrify-sdk/integrify-python](https://github.com/integrify-sdk/integrify-python)

### Əsas özəlliklər

- Hər integration ayrıca paketdir, yalnız lazım olanı yükləyib istifadə edirsiniz.
- Shared `integrify-core` ilə kod təkrarının qarşısı alınır.
- Paketlər birlikdə inkişaf etdirilir, amma ayrı-ayrı publish olunur.
- uv workspace sayəsində bütün member-lər eyni mühitdə test/lint edilir.
- Kitabxana həm sync, həm də async sorğu dəyişimini dəstəkləyir.
- Kitabaxanadakı bütün sinif və funksiyalar tamamilə dokumentləşdirilib.
- Kitabaxanadakı bütün sinif və funksiyalar tipləndirildiyindən, "type hinting" aktivdir.
- Sorğuların çoxunun məntiq axını (flowsu) izah edilib.

### Kitabxananın yüklənməsi

```console
pip install integrify
pip install integrify[epoint]
pip install integrify[epoint,lsim]
pip install integrify[all]
```

### İstifadəsi

#### Sync nümunə

```python
from integrify.epoint import EPointRequest

resp = EPointRequest.pay(
    amount=100,
    currency='AZN',
    order_id='12345678',
    description='Ödəniş',
)
print(resp.ok, resp.body)
```

#### Async nümunə

```python
from integrify.epoint import EPointAsyncRequest

resp = await EPointAsyncRequest.pay(
    amount=100,
    currency='AZN',
    order_id='12345678',
    description='Ödəniş',
)
print(resp.ok, resp.body)
```

#### Sorğu cavabı

```python
class ApiResponse:
    ok: bool
    status_code: int
    headers: dict
    body: object
```

### [Dəstəklənən paketlər](#supported-packages)

Mövcud per-integration repository-lərin bu monorepo-ya köçürülməsi üçün [MIGRATION.md](./MIGRATION.md) faylına baxın.

---

## English

Integrify is a Python toolkit for API integrations. This repository is the monorepo for the Integrify package family: shared core plus independently published integration packages.

### Documentation

- Project docs portal: [https://integrify.mmzeynalli.dev](https://integrify.mmzeynalli.dev)
- Code repository: [https://github.com/integrify-sdk/integrify-python](https://github.com/integrify-sdk/integrify-python)

### Key features

- Each integration is installed independently, so users install only what they need.
- Shared `integrify-core` avoids duplicated base logic.
- Packages are developed together but released independently.
- uv workspace keeps linting and tests unified across members.
- Library supports both sync and async requests
- Every class and type in the library is documented
- Everything in library is type hinted
- Explanation of most of the request flows are explained

### Installation

```console
pip install integrify
pip install integrify[epoint]
pip install integrify[epoint,lsim]
pip install integrify[all]
```

### Usage

#### Sync example

```python
from integrify.epoint import EPointRequest

resp = EPointRequest.pay(
    amount=100,
    currency='AZN',
    order_id='12345678',
    description='Payment',
)
print(resp.ok, resp.body)
```

#### Async example

```python
from integrify.epoint import EPointAsyncRequest

resp = await EPointAsyncRequest.pay(
    amount=100,
    currency='AZN',
    order_id='12345678',
    description='Payment',
)
print(resp.ok, resp.body)
```

#### Response object shape

```python
class ApiResponse:
    ok: bool
    status_code: int
    headers: dict
    body: object
```

For migration steps from older per-integration repositories, see [MIGRATION.md](./MIGRATION.md).

### Supported packages

> [!Caution]
> Bütün sorğular rəsmi dokumentasiyalara uyğun yazılsa da, Integrify qeyri-rəsmi API klient-dir.
>
> Even though all requests are written according to official documentation, Integrify is unofficial library for these integrations

| Service                                                                                                |                                        Core requests/                   Əsas sorğular                                        |                                                 All requests/Bütün sorğular                                                  | Documentation                                                                                                                | Tested in production/Real mühitdə test                                                                                       | Lead developer/Əsas Developer                     |
| ------------------------------------------------------------------------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------: | ---------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| [EPoint](https://github.com/integrify-sdk/integrify-python/tree/main/packages/epoint)                  |                                                              ✅                                                               | ![loading](https://raw.githubusercontent.com/integrify-sdk/integrify-docs-python/main/docs/az/docs/assets/spinner-solid.svg) | [Full](https://integrify.mmzeynalli.dev/integrations/epoint)                                                                 | ✅                                                                                                                            | [Miradil Zeynallı](https://github.com/mmzeynalli) |
| [KapitalBank](https://github.com/integrify-sdk/integrify-python/tree/main/packages/kapitalbank)        |                                                              ✅                                                               |                                                              ✅                                                               | [Full](https://integrify.mmzeynalli.dev/integrations/kapitalbank)                                                            | ✅                                                                                                                            | [Zaman Kazımov](https://github.com/kazimovzaman2) |
| [LSIM](https://github.com/integrify-sdk/integrify-python/tree/main/packages/lsim)                      |                                                              ✅                                                               |                                                              ✅                                                               | [Full](https://integrify.mmzeynalli.dev/integrations/lsim)                                                                   | ✅                                                                                                                            | [Miradil Zeynallı](https://github.com/mmzeynalli) |
| [Posta Guvercini](https://github.com/integrify-sdk/integrify-python/tree/main/packages/postaguvercini) |                                                              ✅                                                               |                                                              ✅                                                               | [Full](https://integrify.mmzeynalli.dev/integrations/posta-guvercini)                                                        | ✅                                                                                                                            | [Zaman Kazımov](https://github.com/kazimovzaman2) |
| [Azericard](https://github.com/integrify-sdk/integrify-python/tree/main/packages/azericard)            |                                                              ✅                                                               | ![loading](https://raw.githubusercontent.com/integrify-sdk/integrify-docs-python/main/docs/az/docs/assets/spinner-solid.svg) | [Full](https://integrify.mmzeynalli.dev/integrations/azericard)                                                              | ![loading](https://raw.githubusercontent.com/integrify-sdk/integrify-docs-python/main/docs/az/docs/assets/spinner-solid.svg) | [Miradil Zeynallı](https://github.com/mmzeynalli) |
| [Clopos](https://github.com/integrify-sdk/integrify-python/tree/main/packages/clopos)                  |                                                              ✅                                                               |                                                              ✅                                                               | [Full](https://integrify.mmzeynalli.dev/en/integrations/clopos)                                                              | ![loading](https://raw.githubusercontent.com/mmzeynalli/integrify/main/docs/az/docs/assets/spinner-solid.svg)                | [Miradil Zeynallı](https://github.com/mmzeynalli) |
| [ECustoms (məxfi)](https://github.com/integrify-sdk/integrify-ecustoms)                                |                                                              ✅                                                               |                                                              ✅                                                               | [Məxfi](https://integrify.mmzeynalli.dev/integrations/ecustoms/)                                                             | ![loading](https://raw.githubusercontent.com/integrify-sdk/integrify-docs-python/main/docs/az/docs/assets/spinner-solid.svg) | [Miradil Zeynallı](https://github.com/mmzeynalli) |
| [Payriff](https://github.com/integrify-sdk/integrify-python/tree/main/packages/payriff)                | ![loading](https://raw.githubusercontent.com/integrify-sdk/integrify-docs-python/main/docs/az/docs/assets/spinner-solid.svg) | ![loading](https://raw.githubusercontent.com/integrify-sdk/integrify-docs-python/main/docs/az/docs/assets/spinner-solid.svg) | ![loading](https://raw.githubusercontent.com/integrify-sdk/integrify-docs-python/main/docs/az/docs/assets/spinner-solid.svg) | ![loading](https://raw.githubusercontent.com/integrify-sdk/integrify-docs-python/main/docs/az/docs/assets/spinner-solid.svg) | [Vahid Həsənzadə](https://github.com/vahidzhe)    |
