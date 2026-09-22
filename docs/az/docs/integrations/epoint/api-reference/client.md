# API Client

???+ note

    İstifadəsi göstərilən bütün sorğular sinxrondur. Asinxron versiyasaları istifadə etmək üçün
    bu importu edin və eyni-adlı funksiyaları `await` ilə çağırın:

    ```python
    from integrify.epoint import EPointAsyncRequest
    ```

::: integrify.epoint.client.EPointRequest
    handler: python
    options:
      separate_signature: true

::: integrify.epoint.client.EPointAsyncRequest
    handler: python
    options:
      separate_signature: true

???+ note

    Bunlar artıq hazır yaradılmış klass obyektləridir, birbaşa istifadə üçün nəzərdə tutulub. Əks halda
    bütün sorğuları `EPointRequestClass().save_card()` kimi istifadə etməlisiniz.

::: integrify.epoint.client.EPointClientClass
    handler: python
    options:
      separate_signature: true
      members:
        - pay
        - get_transaction_status
        - save_card
        - pay_with_saved_card
        - pay_and_save_card
        - payout
        - refund
        - split_pay
        - split_pay_with_saved_card
        - split_pay_and_save_card
        - create_widget
        - create_token_payment
        - apple_pay_session
        - apple_pay
        - google_pay
