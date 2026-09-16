# Integrify PostaGuvercini

> [!Caution]
> Bütün sorğular rəsmi dokumentasiyalara uyğun yazılsalar da, Integrify qeyri-rəsmi API klient-dir.

<p align="center">
  <a href="https://integrify.mmzeynalli.dev/"><img width="400" src="https://raw.githubusercontent.com/integrify-sdk/integrify-docs-python/main/docs/az/docs/assets/integrify.png" alt="Integrify"></a>
</p>
<p align="center">
    <em>Integrify API inteqrasiyalarını rahatlaşdıran sorğular kitabaxanasıdır. Bu kitabxana PostaGuvercini inteqrasiyası üçün nəzərdə tutulmuşdur.</em>
</p>

---

**Dokumentasiya**: [https://integrify.mmzeynalli.dev/integrations/postaguvercini/about/](https://integrify.mmzeynalli.dev/integrations/postaguvercini/about/)

**Kod**: [https://github.com/integrify-sdk/integrify-python/tree/main/packages/postaguvercini](https://github.com/integrify-sdk/integrify-python/tree/main/packages/postaguvercini)

---

## Rəsmi Dokumentasiya (v1)

[İngliscə](https://www.poctgoyercini.com/api_json/swagger/ui/index#/)

## Əsas özəlliklər

- Kitabxana həm sync, həm də async sorğu dəyişimini dəstəkləyir.
- Kitabaxanadakı bütün sinif və funksiyalar tamamilə dokumentləşdirilib.
- Kitabaxanadakı bütün sinif və funksiyalar tipləndirildiyindən, "type hinting" aktivdir.
- Sorğuların çoxunun məntiq axını (flowsu) izah edilib.

## Kitabxananın yüklənməsi

<div class="termy">

```console
pip install integrify-epoint
```

</div>

## İstifadəsi

Bu sorğulardan istifadə edə bilmək üçün, düzgün "environment variable"-ları quraşdırmalısınız. Daha ətraflı [burdan](https://integrify.mmzeynalli.dev/integrations/posta-guvercini/env.md) oxuya bilərsiniz.

### Sorğular listi

| Sorğu metodu        | Məqsəd                            |        PostaGuvercini API        |
| :------------------ | :-------------------------------- | :------------------------------: |
| `send_single_sms`   | Tək nömrəyə sms göndərilməsi      |   `/api_json/v1/Sms/Send_1_N`    |
| `send_multiple_sms` | Bir neçə nömrəyə sms göndərilməsi |   `/api_json/v1/Sms/Send_N_N`    |
| `get_status`        | SMS-in statusunu yoxlamaq         |    `/api_json/v1/Sms/Status`     |
| `credit_balance`    | Balansın yoxlanılması             | `/api_json/v1/Sms/CreditBalance` |

> [!Caution]
> Bütün sorğular rəsmi dokumentasiyalara uyğun yazılsalar da, Integrify qeyri-rəsmi API klient-dir.
