# Integrify LSIM

> [!Caution]
> Bütün sorğular rəsmi dokumentasiyalara uyğun yazılsalar da, Integrify qeyri-rəsmi API klient-dir.

<p align="center">
  <a href="https://integrify.mmzeynalli.dev/"><img width="400" src="https://raw.githubusercontent.com/integrify-sdk/integrify-docs-python/main/docs/az/docs/assets/integrify.png" alt="Integrify"></a>
</p>
<p align="center">
    <em>Integrify API inteqrasiyalarını rahatlaşdıran sorğular kitabaxanasıdır. Bu kitabxana LSIM inteqrasiyası üçün nəzərdə tutulmuşdur.</em>
</p>

---

**Dokumentasiya**: [https://integrify.mmzeynalli.dev/integrations/lsim/about/](https://integrify.mmzeynalli.dev/integrations/lsim/about/)

**Kod**: [https://github.com/integrify-sdk/integrify-python/tree/main/packages/lsim](https://github.com/integrify-sdk/integrify-python/tree/main/packages/lsim)

---

## Rəsmi Dokumentasiya (v2024.11.22)

[İngliscə](https://integrify.mmzeynalli.dev/integrations/lsim/official/api/)

## Əsas özəlliklər

- Kitabxana həm sync, həm də async sorğu dəyişimini dəstəkləyir.
- Kitabaxanadakı bütün sinif və funksiyalar tamamilə dokumentləşdirilib.
- Kitabaxanadakı bütün sinif və funksiyalar tipləndirildiyindən, "type hinting" aktivdir.
- Sorğuların çoxunun məntiq axını (flowsu) izah edilib.

## Kitabxananın yüklənməsi

<div class="termy">

```console
pip install integrify-lsim
```

</div>

## İstifadəsi

Bu sorğulardan istifadə etmək üçün, bu dəyərləri "environment variable"-larına əlavə etməlisiniz: `LSIM_LOGIN`, `LSIM_PASSWORD`, `LSIM_SENDER_NAME`

### Sorğular listi

### Tək SMS sorğuları

| Sorğu metodu      | Məqsəd                                            |          LSIM API          |
| :---------------- | :------------------------------------------------ | :------------------------: |
| `send_sms_get`    | GET sorğusu ilə SMS göndərilmə                    |    `/quicksms/v1/send`     |
| `send_sms_post`   | POST sorğusu ilə SMS göndərilmə                   |  `/quicksms/v1/smssender`  |
| `check_balance`   | Balansı yoxlamaq                                  |   `/quicksms/v1/balance`   |
| `get_report_get`  | GET sorğusu ilə göndərilmiş SMS haqqında məlumat  |   `/quicksms/v1/report`    |
| `get_report_post` | POST sorğusu ilə göndərilmiş SMS haqqında məlumat | `/quicksms/v1/smsreporter` |

### Toplu SMS sorğuları

| Sorğu metodu                     | Məqsəd                                              |   LSIM API   |
| :------------------------------- | :-------------------------------------------------- | :----------: |
| `bulk_send_one_message`          | Toplu şəkildə hamıya eyni SMS göndərilmə            | `/smxml/api` |
| `bulk_send_different_messages`   | Toplu şəkildə hərəyə fərqli SMS göndərilmə          | `/smxml/api` |
| `get_report`                     | Toplu göndərilmiş SMS-in reportu                    | `/smxml/api` |
| `get_detailed_report`            | Toplu göndərilmiş SMS-in detallı reportu            | `/smxml/api` |
| `get_detailed_report_with_dates` | Toplu göndərilmiş SMS-in detallı və tarixli reportu | `/smxml/api` |
| `check_balance`                  | Balansı yoxlamaq                                    | `/smxml/api` |

> [!Caution]
> Bütün sorğular rəsmi dokumentasiyalara uyğun yazılsalar da, Integrify qeyri-rəsmi API klient-dir.
