# Integrify KapitalBank

> [!Caution]
> Bütün sorğular rəsmi dokumentasiyalara uyğun yazılsalar da, Integrify qeyri-rəsmi API klient-dir.

<p align="center">
  <a href="https://integrify.mmzeynalli.dev/"><img width="400" src="https://raw.githubusercontent.com/integrify-sdk/integrify-docs-python/main/docs/az/docs/assets/integrify.png" alt="Integrify"></a>
</p>
<p align="center">
    <em>Integrify API inteqrasiyalarını rahatlaşdıran sorğular kitabaxanasıdır. Bu kitabxana KapitalBank inteqrasiyası üçün nəzərdə tutulmuşdur.</em>
</p>

---

**Dokumentasiya**: [https://integrify.mmzeynalli.dev/integrations/kapitalbank/about/](https://integrify.mmzeynalli.dev/integrations/kapitalbank/about/)

**Kod**: [https://github.com/integrify-sdk/integrify-python/tree/main/packages/kapitalbank](https://github.com/integrify-sdk/integrify-python/tree/main/packages/kapitalbank)

---

## Rəsmi Dokumentasiya (v1.0.3)

[Azərbaycanca, İngliscə, Rusca](https://pg.kapitalbank.az/docs)

## Əsas özəlliklər

- Kitabxana həm sync, həm də async sorğu dəyişimini dəstəkləyir.
- Kitabaxanadakı bütün sinif və funksiyalar tamamilə dokumentləşdirilib.
- Kitabaxanadakı bütün sinif və funksiyalar tipləndirildiyindən, "type hinting" aktivdir.
- Sorğuların çoxunun məntiq axını (flowsu) izah edilib.

## Kitabxananın yüklənməsi

<div class="termy">

```console
pip install integrify-kapitalbank
```

</div>

## İstifadəsi

Bu sorğulardan istifadə etmək üçün, bu dəyərləri "environment variable"-larına əlavə etməlisiniz: `KAPITAL_USERNAME`, `KAPITAL_PASSWORD`

Əlavə olaraq `KAPITAL_ENV` dəyişənini də təyin etməlisiniz. Default olaraq saxlasaz test mühitindən istifadə edəcəksiniz. Əks halda, `prod` dəyərini təyin etməlisiniz.

Kapital interfeysinin dilini dəyişmək istəyirsinizsə, `KAPITAL_INTERFACE_LANG` "environment variable"-na dəyər verin. Default olaraq, Azərbaycan dili olacaq.

Sorğular uğurlu və ya uğursuz olduqda, spesifik URL-ə yönləndirmək istəyirsinizsə, bu dəyişənlərə də mühit levelində dəyər verin: `KAPITAL_REDIRECT_URL`

### Sorğular listi

| Sorğu metodu              | Məqsəd                                             |            Kapital API            | Callback-ə sorğu atılır |
| :------------------------ | :------------------------------------------------- | :-------------------------------: | :---------------------: |
| `create_order`            | Ödəniş                                             |           `/api/order`            |            ✅            |
| `get_order_information`   | Ödəniş haqda qısa məlumat                          |      `/api/order/{order_id}`      |            ❌            |
| `get_detailed_order_info` | Ödəniş haqda detallı məlumat                       |      `/api/order/{order_id}`      |            ❌            |
| `refund_order`            | Geri ödəniş sorğusu                                | `/api/order/{order_id}/exec-tran` |            ❌            |
| `save_card`               | Kartı saxlamaq üçün ödəniş sorğusu                 |           `/api/order`            |            ✅            |
| `pay_and_save_card`       | Kartı saxlamaq və ödəniş etmək üçün ödəniş sorğusu |           `/api/order`            |            ✅            |
| `full_reverse_order`      | Ödənişi ləğv etmək üçün sorğu                      | `/api/order/{order_id}/exec-tran` |            ❌            |
| `clearing_order`          | Ödənişin təsdiq edilməsi üçün sorğu                | `/api/order/{order_id}/exec-tran` |            ❌            |
| `pay_with_saved_card`     | Ödənişin hissəsini ləğv etmək üçün sorğu           | `/api/order/{order_id}/exec-tran` |            ❌            |

> [!Caution]
> Bütün sorğular rəsmi dokumentasiyalara uyğun yazılsalar da, Integrify qeyri-rəsmi API klient-dir.
