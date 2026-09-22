# EPoint

???+ warning
    Bu sorğulardan istifadə edə bilmək üçün, düzgün "environment variable"-ları quraşdırmalısınız. Daha ətraflı [burdan](./env.md) oxuya bilərsiniz.

## Rəsmi Dokumentasiya (v1.0.3) { #official-documentation }

[Azərbaycanca](https://epointbucket.s3.eu-central-1.amazonaws.com/files/instructions/API%20Epoint%20az.pdf)

[İngliscə](https://epointbucket.s3.eu-central-1.amazonaws.com/files/instructions/API%20Epoint%20en.pdf)

[Rusca](https://epointbucket.s3.eu-central-1.amazonaws.com/files/instructions/API%20Epoint%20ru.pdf)

Markdown versiyaları (bu saytda):

- [EPoint API (v1.0.3)](./official/api.md)
- [Apple Pay & Google Pay (JS SDK)](./official/apple-google-pay.md)

## Sorğular listi { #list-of-requests }

| Sorğu metodu                                                                                       | Məqsəd                                                               |                EPoint API                 |  Callback-ə sorğu atılır  |
| :------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------- | :---------------------------------------: | :-----------------------: |
| [`pay`][integrify.epoint.client.EPointClientClass.pay]                                             | Ödəniş                                                               |             `/api/1/request`              | :fontawesome-solid-check: |
| [`get_transaction_status`][integrify.epoint.client.EPointClientClass.get_transaction_status]       | Ödəniş statusunun yoxlanılması                                       |            `/api/1/get-status`            |            :x:            |
| [`save_card`][integrify.epoint.client.EPointClientClass.save_card]                                 | Ödəniş olmadan kartı yadda saxlamaq                                  |        `/api/1/card-registration`         | :fontawesome-solid-check: |
| [`pay_with_saved_card`][integrify.epoint.client.EPointClientClass.pay_with_saved_card]             | Saxlanılan kartla ödəniş                                             |           `/api/1/execute-pay`            |            :x:            |
| [`pay_and_save_card`][integrify.epoint.client.EPointClientClass.pay_and_save_card]                 | Ödəniş etmə və kartı yadda saxlamaq                                  |    `/api/1/card-registration-with-pay`    | :fontawesome-solid-check: |
| [`payout`][integrify.epoint.client.EPointClientClass.payout]                                       | Vəsaitlərin köçürülməsi                                              |          `/api/1/refund-request`          |            :x:            |
| [`refund`][integrify.epoint.client.EPointClientClass.refund]                                       | Ödənişi tam və ya yarımçıq geri qaytarma                             |             `/api/1/reverse`              |            :x:            |
| [`split_pay`][integrify.epoint.client.EPointClientClass.split_pay]                                 | Ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə                    |          `/api/1/split-request`           | :fontawesome-solid-check: |
| [`split_pay_with_saved_card`][integrify.epoint.client.EPointClientClass.split_pay_with_saved_card] | Saxlanılmış kartla ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə |        `/api/1/split-execute-pay`         |            :x:            |
| [`split_pay_and_save_card`][integrify.epoint.client.EPointClientClass.split_pay_and_save_card]     | Ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə və kartı saxlamaq  | `/api/1/split-card-registration-with-pay` | :fontawesome-solid-check: |
| [`create_widget`][integrify.epoint.client.EPointClientClass.create_widget]                         | Apple Pay/Google Pay widget-i yaratmaq                               |          `/api/1/token/widget`            |            :x:            |
| [`create_token_payment`][integrify.epoint.client.EPointClientClass.create_token_payment]           | Apple Pay/Google Pay üçün token ödənişi yaratmaq                     |          `/api/1/token/payment`           |            :x:            |
| [`apple_pay_session`][integrify.epoint.client.EPointClientClass.apple_pay_session]                 | Apple Pay session-u almaq                                            |       `/api/1/token/apple/session`        |            :x:            |
| [`apple_pay`][integrify.epoint.client.EPointClientClass.apple_pay]                                 | Apple Pay ilə ödənişi tamamlamaq                                     |         `/api/1/token/apple/pay`          |            :x:            |
| [`google_pay`][integrify.epoint.client.EPointClientClass.google_pay]                               | Google Pay ilə ödənişi tamamlamaq                                    |         `/api/1/token/google/pay`         |            :x:            |

## Apple Pay & Google Pay { #apple-pay-google-pay }

Apple Pay və Google Pay-i iki yolla qoşmaq olar:

| Üsul | Nə vaxt | Backend sorğuları |
| :--- | :------ | :---------------- |
| **Widget** | Ən sadə yol: düymələr EPoint-in səhifəsində, iframe/webview daxilində göstərilir | [`create_widget`][integrify.epoint.client.EPointClientClass.create_widget] |
| **JS SDK** | Düymələr birbaşa sizin səhifənizdə, öz dizaynınızla | [`create_token_payment`][integrify.epoint.client.EPointClientClass.create_token_payment], [`apple_pay_session`][integrify.epoint.client.EPointClientClass.apple_pay_session], [`apple_pay`][integrify.epoint.client.EPointClientClass.apple_pay], [`google_pay`][integrify.epoint.client.EPointClientClass.google_pay] |

### Widget { #apple-google-pay-widget }

```python
from integrify.epoint import EPointRequest

resp = EPointRequest.create_widget(amount=2.5, order_id='12345678', description='Ödəniş')
widget_url = resp.body.widget_url  # frontend-ə ötürün
```

`widget_url`-i saytda iframe, mobil tətbiqdə isə webview daxilində açın. Ödəniş bitdikdən sonra
widget səhifəyə `message` event-i göndərir:

```html
<iframe src="{{ widget_url }}" allow="payment"></iframe>

<script>
  window.addEventListener('message', function (event) {
    console.log(event.data); // {status: 'success', payment: {...}}
  });
</script>
```

> **Qeyd**
>
> `event.data` brauzerdən gəldiyi üçün ona tam güvənməyin: ödənişin nəticəsini backend-də
> [`get_transaction_status`][integrify.epoint.client.EPointClientClass.get_transaction_status] ilə yoxlayın.

### JS SDK { #apple-google-pay-sdk }

Bu üsulda düymələr EPoint-in JS SDK-sı (`epoint-token-pay`) vasitəsilə göstərilir.
Axın belədir:

1. **Backend:** [`create_token_payment`][integrify.epoint.client.EPointClientClass.create_token_payment] ilə EPoint-də token ödənişi yaradın.
2. **Frontend:** SDK-nı qoşun, düymələri əlavə edin və `initTokenPay`-i 1-ci addımda gələn ödənişlə çağırın.
3. **Apple Pay:** SDK sizin session endpoint-inizə müraciət edir → [`apple_pay_session`][integrify.epoint.client.EPointClientClass.apple_pay_session].
4. **Ödəniş:** İstifadəçi ödənişi təsdiqlədikdən sonra SDK pay endpoint-inizə `id`, `token` və `billingContact` göndərir → [`apple_pay`][integrify.epoint.client.EPointClientClass.apple_pay] / [`google_pay`][integrify.epoint.client.EPointClientClass.google_pay].

Session və pay endpoint-ləri EPoint-dən gələn cavabı **olduğu kimi** (`resp.body`) qaytarmalıdır.

#### Frontend { #apple-google-pay-frontend }

```html
<script src="https://epoint.az/js/epoint-token-pay.min.js"></script>

<google-pay-button type="pay" color="white"></google-pay-button>
<apple-pay-button type="pay" color="black"></apple-pay-button>

<script>
  initTokenPay({
    payment: { id: 9998887, amount: '2.50' },  // create_token_payment cavabından
    endpoints: {
      apple: { session: '/epoint/apple/session', pay: '/epoint/apple' },
      google: { pay: '/epoint/google' },
    },
    onError: function (error) { console.log({ error }) },
    onSuccess: function (success) { console.log({ success }) },
  });
</script>
```

#### Backend (FastAPI nümunəsi) { #apple-google-pay-backend }

```python
from fastapi import APIRouter, Request
from integrify.epoint import EPointAsyncRequest

router = APIRouter(prefix='/epoint')


@router.post('/apple/session')
async def apple_session(request: Request):
    resp = await EPointAsyncRequest.apple_pay_session(origin=request.headers['origin'])
    return resp.body


@router.post('/apple')
async def apple_pay(request: Request):
    body = await request.json()
    resp = await EPointAsyncRequest.apple_pay(
        payment_id=body['id'],
        token=body['token'],
        billing_contact=body.get('billingContact'),
    )
    return resp.body.model_dump()


@router.post('/google')
async def google_pay(request: Request):
    body = await request.json()
    resp = await EPointAsyncRequest.google_pay(
        payment_id=body['id'],
        token=body['token'],
        billing_contact=body.get('billingContact'),
    )
    return resp.body.model_dump()
```

> **Qeyd**
>
> `apple_pay`/`google_pay` sorğularının cavabında `redirect_url` gələ bilər (məs., 3DS üçün) — SDK bunu özü idarə edir.
> Uğurlu ödənişdən sonra statusu [`get_transaction_status`][integrify.epoint.client.EPointClientClass.get_transaction_status] ilə də yoxlaya bilərsiniz.

## Callback Sorğusu { #callback-request }

Bəzi sorğular müştəri məlumat daxil etdikdən və arxa fonda bank işləmləri bitdikdən sonra, tranzaksiya haqqında məlumat sizin EPoint dashboard-da qeyd etdiyiniz `callback` URL-ə POST sorğusu göndərilir. Data siz adətən sorğu göndərdiyiniz formatda gəlir:

```python
{
    'data': 'base64data'
    'signature': 'sha1signature'
}
```

Bu data-nı `signature`-ni yoxladıqdan sonra, decode etmək lazımdır. Callback üçün API yazdıqda, datanı alıb, `helpers.py`-dakı [`decode_callback_data`][integrify.epoint.helpers.decode_callback_data] funksiyası ilə həm signature yoxlanması həm də datanın decode-unu edə bilərsiniz. Bu funksiya sizə [`DecodedCallbackDataSchema`][integrify.epoint.schemas.callback.DecodedCallbackDataSchema] formatında decode olunmuş datanı qaytarır.

> **Qeyd**
>
> FastAPI istifadəçiləri kiçik "shortcut"-dan istifadə edə bilərlər:
>
> ```python
> from fastapi import Fastapi, APIRouter, Depends
> from integrify.epoint.schemas.callback import DecodedCallbackDataSchema
> from integrify.epoint.helpers import decode_callback_data
>
> router = APIRouter()
>
> @router.post('/epoint/callback')
> async def epoint_callback(data: DecodedCallbackDataSchema = Depends(decode_callback_data)):
>    ...
> ```
>
> Funksiyanı belə yazdıqda, data avtomatik signature-i yoxlanaraq decode edilir.

---

## Callback Data formatı { #callback-data-format }

Nə sorğu göndərməyinizdən asılı olaraq, callback-ə gələn data biraz fərqlənə bilər. [`DecodedCallbackDataSchema`][integrify.epoint.schemas.callback.DecodedCallbackDataSchema] bütün bu dataları özündə cəmləsə də, hansı fieldlərin gəlməyəcəyini (yəni, decode-dan sonra `None` olacağını) bilmək yaxşı olar. Ümumilikdə, mümkün olacaq datalar bunlardır:

| Dəyişən adı      | İzahı                                                                                                   |
| ---------------- | ------------------------------------------------------------------------------------------------------- |
| status           | Success və ya failed əməliyyatının nəticəsi                                                             |
| message          | Ödənişin icra statusu haqqında mesaj                                                                    |
| code             | Bankın cavab kodu. 3 rəqəmli koddan, xəta/uğur mesajına çevrilir.                                       |
| transaction      | Epoint xidmətinin əməliyyat IDsi                                                                        |
| bank_transaction | Bank ödəniş əməliyyatı IDsi                                                                             |
| bank_response    | Ödəniş icrasının nəticəsi ilə bankın cavabı                                                             |
| operation_code   | 001-kart qeydiyyatı\n100- istifadəçi ödənişi                                                            |
| rrn              | Retrieval Reference Number - unikal əməliyyat identifikator. Yalnız uğurlu bir əməliyyat üçün mövcuddur |
| card_mask        | Ödəniş səhifəsində göstərilən istifadəçi adı                                                            |
| card_name        | 123456******1234 formatında əks edilən kart maskası                                                     |
| amount           | Ödəniş məbləği                                                                                          |
| order_id         | Tətbiqinizdə unikal əməliyyat ID                                                                        |
| card_id          | Ödənişləri yerinə yetirmək üçün istifadə edilm lazım olan unikal kart identifikatoru                    |
| split_amount     | İkinci istifadəçi üçün ödəniş məbləği                                                                   |
| other_attr       | Əlavə göndərdiyiniz seçimlər                                                                            |

Sorğudan asılı olaraq, bu data-lar callback-də **GƏLMİR** (yəni, avtomatik `None` dəyəri alır):

| Sorğu metodu              | Callback-də gəlməyəcək datalar                    |
| :------------------------ | :------------------------------------------------ |
| `pay`                     | `card_id`, `split_amount`                         |
| `save_card`               | `order_id`, `transaction`, `amount`, `other_attr` |
| `pay_and_save_card`       | `message`                                         |
| `split_pay`               | -                                                 |
| `split_pay_and_save_card` | `message`                                         |

> **Qeyd**
>
> Qalan bütün data-lar sorğu success olduqda gəlir, əks halda, onlar da `None` dəyəri alır.
