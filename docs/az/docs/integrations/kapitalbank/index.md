# Kapital Bank

???+ warning
    Bu sorğulardan istifadə edə bilmək üçün, düzgün "environment variable"-ları quraşdırmalısınız. Daha ətraflı [burdan](./env.md) oxuya bilərsiniz.

???+ info
    ### Test Card Məlumatları
    | **PAN**          | **ExpDate** | **CVV/CVV2** |
    | ---------------- | ----------- | ------------ |
    | 4169741330151778 | 06/25       | 119          |
    | 5239151747183468 | 11/27       | 602          |

    ### Test Autentifikasiyası
    İstifadəçi adı: TerminalSys/kapital
    Şifrə: kapital123

## Rəsmi Dokumentasiya { #official-documentation }

[AZ, EN, RU](https://pg.kapitalbank.az/docs)

Markdown versiyası (bu saytda): [Kapital Bank E-commerce API](./official/api.md)

## Sürətli başlanğıc { #quickstart }

Sifariş yaratmaq, müştərini bankın ödəniş səhifəsinə yönləndirmək və statusu yoxlamaq:

```python
from integrify.kapitalbank import KapitalRequest

# 1. Sifariş yaradın
resp = KapitalRequest.create_order(amount=10, currency='AZN', description='Sifariş #1')

if resp.ok:
    order = resp.body.data

    # 2. Müştərini bankın ödəniş səhifəsinə yönləndirin
    print(order.redirect_url)

    # 3. Müştəri KAPITAL_REDIRECT_URL-ə qayıtdıqdan sonra statusu yoxlayın
    info = KapitalRequest.get_order_information(order_id=order.id)
    print(info.body.data.status)  # FullyPaid, Declined, Cancelled, ...
else:
    print(resp.body.error)
```

Asinxron istifadə üçün `KapitalAsyncRequest` import edib, eyni metodları `await` ilə çağırın.

## Sorğular listi { #list-of-requests }

| Sorğu metodu                                                                                         | Məqsəd                                             |            Kapital API            |  Callback-ə sorğu atılır  |
| :--------------------------------------------------------------------------------------------------- | :------------------------------------------------- | :-------------------------------: | :-----------------------: |
| [`create_order`][integrify.kapitalbank.client.KapitalClientClass.create_order]                       | Ödəniş                                             |           `/api/order`            | :fontawesome-solid-check: |
| [`get_order_information`][integrify.kapitalbank.client.KapitalClientClass.get_order_information]     | Ödəniş haqda qısa məlumat                          |      `/api/order/{order_id}`      |            :x:            |
| [`get_detailed_order_info`][integrify.kapitalbank.client.KapitalClientClass.get_detailed_order_info] | Ödəniş haqda detallı məlumat                       |      `/api/order/{order_id}`      |            :x:            |
| [`refund_order`][integrify.kapitalbank.client.KapitalClientClass.refund_order]                       | Geri ödəniş sorğusu                                | `/api/order/{order_id}/exec-tran` |            :x:            |
| [`save_card`][integrify.kapitalbank.client.KapitalClientClass.save_card]                             | Kartı saxlamaq üçün ödəniş sorğusu                 |           `/api/order`            | :fontawesome-solid-check: |
| [`pay_and_save_card`][integrify.kapitalbank.client.KapitalClientClass.pay_and_save_card]             | Kartı saxlamaq və ödəniş etmək üçün ödəniş sorğusu |           `/api/order`            | :fontawesome-solid-check: |
| [`full_reverse_order`][integrify.kapitalbank.client.KapitalClientClass.full_reverse_order]           | Ödənişi ləğv etmək üçün sorğu                      | `/api/order/{order_id}/exec-tran` |            :x:            |
| [`clearing_order`][integrify.kapitalbank.client.KapitalClientClass.clearing_order]                   | Ödənişin təsdiq edilməsi üçün sorğu                | `/api/order/{order_id}/exec-tran` |            :x:            |
| [`pay_with_saved_card`][integrify.kapitalbank.client.KapitalClientClass.pay_with_saved_card]         | Ödənişin hissəsini ləğv etmək üçün sorğu           | `/api/order/{order_id}/exec-tran` |            :x:            |
