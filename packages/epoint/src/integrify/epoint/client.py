from collections.abc import Coroutine
from typing import TYPE_CHECKING, Any, Generic, overload
from typing import SupportsFloat as Numeric

from integrify.api import APIClient, _Async, _Mode, _Sync
from integrify.epoint import env
from integrify.epoint.handlers import (
    ApplePayPayloadHandler,
    ApplePaySessionPayloadHandler,
    CreateTokenPaymentPayloadHandler,
    CreateWidgetPayloadHandler,
    GetTransactionStatusPayloadHandler,
    GooglePayPayloadHandler,
    PayAndSaveCardPayloadHandler,
    PaymentPayloadHandler,
    PayoutPayloadHandler,
    PayWithSavedCardPayloadHandler,
    RefundPayloadHandler,
    SaveCardPayloadHandler,
    SplitPayAndSaveCardPayloadHandler,
    SplitPayPayloadHandler,
    SplitPayWithSavedCardPayloadHandler,
)
from integrify.epoint.schemas.response import (
    BaseResponseSchema,
    MinimalResponseSchema,
    RedirectUrlResponseSchema,
    RedirectUrlWithCardIdResponseSchema,
    SplitPayWithSavedCardResponseSchema,
    TokenPaymentResponseSchema,
    TokenPayResponseSchema,
    TransactionStatusResponseSchema,
    WidgetResponseSchema,
)
from integrify.schemas import APIResponse
from integrify.utils import UNSET, Unset

__all__ = ['EPointAsyncRequest', 'EPointClientClass', 'EPointRequest']


class EPointClientClass(APIClient, Generic[_Mode]):
    """EPoint sorğular üçün baza class"""

    def __init__(
        self,
        name='EPoint',
        base_url: str | None = env.API.BASE_URL,
        default_handler=None,
        sync: bool = True,
        dry: bool = False,
    ):
        super().__init__(name, base_url, default_handler, sync, dry)

        self.add_url('pay', env.API.PAY, verb='POST')
        self.add_handler('pay', PaymentPayloadHandler)

        self.add_url('get_transaction_status', env.API.GET_STATUS, verb='POST')
        self.add_handler('get_transaction_status', GetTransactionStatusPayloadHandler)

        self.add_url('save_card', env.API.SAVE_CARD, verb='POST')
        self.add_handler('save_card', SaveCardPayloadHandler)

        self.add_url('pay_with_saved_card', env.API.PAY_WITH_SAVED_CARD, verb='POST')
        self.add_handler('pay_with_saved_card', PayWithSavedCardPayloadHandler)

        self.add_url('pay_and_save_card', env.API.PAY_AND_SAVE_CARD, verb='POST')
        self.add_handler('pay_and_save_card', PayAndSaveCardPayloadHandler)

        self.add_url('payout', env.API.PAYOUT, verb='POST')
        self.add_handler('payout', PayoutPayloadHandler)

        self.add_url('refund', env.API.REFUND, verb='POST')
        self.add_handler('refund', RefundPayloadHandler)

        self.add_url('split_pay', env.API.SPLIT_PAY, verb='POST')
        self.add_handler('split_pay', SplitPayPayloadHandler)

        self.add_url('split_pay_with_saved_card', env.API.SPLIT_PAY_WITH_SAVED_CARD, verb='POST')
        self.add_handler('split_pay_with_saved_card', SplitPayWithSavedCardPayloadHandler)

        self.add_url('split_pay_and_save_card', env.API.SPLIT_PAY_AND_SAVE_CARD, verb='POST')
        self.add_handler('split_pay_and_save_card', SplitPayAndSaveCardPayloadHandler)

        # Apple Pay & Google Pay
        self.add_url('create_widget', env.API.CREATE_WIDGET, verb='POST')
        self.add_handler('create_widget', CreateWidgetPayloadHandler)

        self.add_url('create_token_payment', env.API.CREATE_TOKEN_PAYMENT, verb='POST')
        self.add_handler('create_token_payment', CreateTokenPaymentPayloadHandler)

        self.add_url('apple_pay_session', env.API.APPLE_PAY_SESSION, verb='POST')
        self.add_handler('apple_pay_session', ApplePaySessionPayloadHandler)

        self.add_url('apple_pay', env.API.APPLE_PAY, verb='POST')
        self.add_handler('apple_pay', ApplePayPayloadHandler)

        self.add_url('google_pay', env.API.GOOGLE_PAY, verb='POST')
        self.add_handler('google_pay', GooglePayPayloadHandler)

    if TYPE_CHECKING:
        # pylint: disable=missing-function-docstring,unused-argument

        @overload
        def pay(
            self: 'EPointClientClass[_Sync]',
            amount: Numeric,
            currency: str,
            order_id: str,
            description: Unset[str] = UNSET,
            **extra: Any,
        ) -> APIResponse[RedirectUrlResponseSchema]:
            """Ödəniş sorğusu

            **Endpoint:** */api/1/request*

            Example:
                ```python
                from integrify.epoint import EPointRequest

                EPointRequest.pay(amount=100, currency='AZN', order_id='12345678', description='Ödəniş')
                ```

            **Cavab formatı**: [`RedirectUrlResponseSchema`][integrify.epoint.schemas.response.RedirectUrlResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` gəlir. Müştəri həmin URLə daxil
            olub, kart məlumatlarını daxil edib, uğurlu ödəniş etdikdən sonra, backend callback
            APIsinə (EPoint dashboard-ında qeyd etdiyiniz) sorğu daxil olur, və eyni `order_id`
            ilə [`DecodedCallbackDataSchema`][integrify.epoint.schemas.callback.DecodedCallbackDataSchema]
            formatında məlumat gəlir.

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
                order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
                description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
                **extra: Başqa ötürmək istədiyiniz əlavə dəyərlər. Bu dəyərlər callback sorğuda sizə
                            geri göndərilir.
            """  # noqa: E501

        @overload
        def pay(
            self: 'EPointClientClass[_Async]',
            amount: Numeric,
            currency: str,
            order_id: str,
            description: Unset[str] = UNSET,
            **extra: Any,
        ) -> Coroutine[Any, Any, APIResponse[RedirectUrlResponseSchema]]: ...
        def pay(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def get_transaction_status(
            self: 'EPointClientClass[_Sync]',
            transaction_id: str,
        ) -> APIResponse[TransactionStatusResponseSchema]:
            """
            Transaksiya statusunu öyrənmək üçün sorğu

            **Endpoint:** */api/1/get-status*

            Example:
                ```python
                from integrify.epoint import EPointRequest

                EPointRequest.get_transaction_status(transaction_id='texxxxxx')
                ```

            Cavab formatı: [`TransactionStatusResponseSchema`][integrify.epoint.schemas.response.TransactionStatusResponseSchema]

            Args:
                transaction_id: EPoint tərəfindən verilmiş tranzaksiya IDsi.
                                Adətən `te` prefiksi ilə olur.
            """  # noqa: E501

        @overload
        def get_transaction_status(
            self: 'EPointClientClass[_Async]',
            transaction_id: str,
        ) -> Coroutine[Any, Any, APIResponse[TransactionStatusResponseSchema]]: ...
        def get_transaction_status(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def save_card(
            self: 'EPointClientClass[_Sync]',
        ) -> APIResponse[RedirectUrlWithCardIdResponseSchema]:
            """Ödəniş olmadan kartı yadda saxlamaq sorğusu

            **Endpoint:** */api/1/card-registration*

            Example:
                ```python
                from integrify.epoint import EPointRequest

                EPointRequest.save_card()
                ```

            Cavab formatı: [`RedirectUrlWithCardIdResponseSchema`][integrify.epoint.schemas.response.RedirectUrlWithCardIdResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` və `card_id` gəlir.
            Müştəri həmin URLə daxil olub, kart məlumatlarını uğurlu qeyd etdikdən sonra,
            backend callback APIsinə (EPoint dashboard-ında qeyd etdiyiniz) sorğu daxil olur,
            və eyni `card_id` ilə [`DecodedCallbackDataSchema`][integrify.epoint.schemas.callback.DecodedCallbackDataSchema]
            formatında məlumat gəlir.
            """  # noqa: E501

        @overload
        def save_card(
            self: 'EPointClientClass[_Async]',
        ) -> Coroutine[Any, Any, APIResponse[RedirectUrlWithCardIdResponseSchema]]: ...
        def save_card(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def pay_with_saved_card(
            self: 'EPointClientClass[_Sync]',
            amount: Numeric,
            currency: str,
            order_id: str,
            card_id: str,
        ) -> APIResponse[BaseResponseSchema]:
            """Yadda saxlanılmış kartla ödəniş sorğusu

            **Endpoint:** */api/1/execute-pay*

            Example:
                ```python
                from integrify.epoint import EPointRequest

                EPointRequest.pay_with_saved_card(amount=100, currency='AZN', order_id='12345678', card_id='cexxxxxx')
                ```

            Cavab formatı: [`BaseResponseSchema`][integrify.epoint.schemas.response.BaseResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq `BaseResponseSchema` formatında
            cavab gəlir, və ödənişin statusu birbaşa qayıdır: heç bir callback sorğusu gəlmir.

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
                order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
                card_id: Saxlanılmış kartın id-si. Adətən `ce` prefiksi ilə başlayır.
            """  # noqa: E501

        @overload
        def pay_with_saved_card(
            self: 'EPointClientClass[_Async]',
            amount: Numeric,
            currency: str,
            order_id: str,
            card_id: str,
        ) -> Coroutine[Any, Any, APIResponse[BaseResponseSchema]]: ...
        def pay_with_saved_card(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def pay_and_save_card(
            self: 'EPointClientClass[_Sync]',
            amount: Numeric,
            currency: str,
            order_id: str,
            description: str,
        ) -> APIResponse[RedirectUrlWithCardIdResponseSchema]:
            """Ödəniş və kartı yadda saxlama sorğusu

            **Endpoint:** */api/1/card-registration-with-pay*

            Example:
                ```python
                from integrify.epoint import EPointRequest

                EPointRequest.pay_and_save_card(amount=100, currency='AZN', order_id='12345678', description='Ödəniş')
                ```

            Cavab formatı:  [`RedirectUrlWithCardIdResponseSchema`][integrify.epoint.schemas.response.RedirectUrlWithCardIdResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq `redirect_url` və `card_id` gəlir. Müştəri həmin URLə
            daxil olub, kart məlumatlarını daxil edib, uğurlu ödəniş etdikdən sonra, backend callback
            APIsinə (EPoint dashboard-ında qeyd etdiyiniz) sorğu daxil olur, və eyni `order_id` və
            `card_id` ilə [`DecodedCallbackDataSchema`][integrify.epoint.schemas.callback.DecodedCallbackDataSchema]
            formatında məlumat gəlir.

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
                order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
                description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
            """  # noqa: E501

        @overload
        def pay_and_save_card(
            self: 'EPointClientClass[_Async]',
            amount: Numeric,
            currency: str,
            order_id: str,
            description: str,
        ) -> Coroutine[Any, Any, APIResponse[RedirectUrlWithCardIdResponseSchema]]: ...
        def pay_and_save_card(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def payout(
            self: 'EPointClientClass[_Sync]',
            amount: Numeric,
            currency: str,
            order_id: str,
            card_id: str,
            description: Unset[str] = UNSET,
        ) -> APIResponse[BaseResponseSchema]:
            """Hesabınızda olan pulu karta nağdlaşdırmaq sorğusu

            **Endpoint:** */api/1/refund-request*

            Example:
                ```python
                from integrify.epoint import EPointRequest

                EPointRequest.payout(amount=100, currency='AZN', order_id='12345678', card_id='cexxxxxx', description='Ödəniş')
                ```

            Cavab sorğu formatı: [`BaseResponseSchema`][integrify.epoint.schemas.response.BaseResponseSchema]

            Bu sorğunu göndərdikdə, əməliyyat Epoint xidməti tərəfindən işləndikdən və bankdan ödəniş
            statusu alındıqdan sonra cavab `BaseResponseSchema` formatında qayıdacaqdır

            Args:
                amount: Nağdlaşdırmaq miqdarı. Numerik dəyər.
                currency: Nağdlaşdırma məzənnəsi. Mümkün dəyərlər: AZN
                order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
                card_id: Saxlanılmış kartın id-si. Adətən `ce` prefiksi ilə başlayır.
                description: Nağdlaşdırmanın təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
            """  # noqa: E501

        @overload
        def payout(
            self: 'EPointClientClass[_Async]',
            amount: Numeric,
            currency: str,
            order_id: str,
            card_id: str,
            description: Unset[str] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[BaseResponseSchema]]: ...
        def payout(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def refund(
            self: 'EPointClientClass[_Sync]',
            transaction_id: str,
            currency: str,
            amount: Unset[Numeric] = UNSET,
        ) -> APIResponse[MinimalResponseSchema]:
            """Keçmiş ödənişi tam və ya yarımçıq geri qaytarma sorğusu

            **Endpoint:** */api/1/reverse*

            Example:
                ```python
                from integrify.epoint import EPointRequest

                # Full refund
                EPointRequest.refund(transaction_id='texxxxxx', currency='AZN')

                # Partial refund
                EPointRequest.refund(transaction_id='texxxxxx', currency='AZN', amount=50)
                ```

            Cavab formatı: [`MinimalResponseSchema`][integrify.epoint.schemas.response.MinimalResponseSchema]

            Bu sorğunu göndərdikdə, cavab olaraq `status` və `message` gəlir.
            Heç bir callback sorğusu göndərilmir.

            Args:
                transaction_id: EPoint tərəfindən verilmiş tranzaksiya IDsi.
                                Adətən `te` prefiksi ilə olur.
                currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
                amount: Ödəniş məbləği. Məbləğin göndərilməsi yarımçıq geri-qaytarma hesab olunur,
                        əks halda tam geri-qaytarma baş verəcəkdir.
            """  # noqa: E501

        @overload
        def refund(
            self: 'EPointClientClass[_Async]',
            transaction_id: str,
            currency: str,
            amount: Unset[Numeric] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[MinimalResponseSchema]]: ...
        def refund(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def split_pay(
            self: 'EPointClientClass[_Sync]',
            amount: Numeric,
            currency: str,
            order_id: str,
            split_user_id: str,
            split_amount: Numeric,
            description: Unset[str] = UNSET,
            **extra: Any,
        ) -> APIResponse[RedirectUrlResponseSchema]:
            """Ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə sorğusu

            **Endpoint:** */api/1/split-request*

            Example:
                ```python
                from integrify.epoint import EPointRequest

                EPointRequest.split_pay(amount=100, currency='AZN', order_id='123456789', split_user_id='epoint_user_id', split_amount=50, description='split payment')
                ```

            Cavab formatı: [`RedirectUrlResponseSchema`][integrify.epoint.schemas.response.RedirectUrlResponseSchema]

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
                order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
                split_user_id: Ödənişi böləcəyini **EPoint** user-ini IDsi
                split_amount: Bölünən miqdar. Numerik dəyər
                description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
                **extra: Başqa ötürmək istədiyiniz əlavə dəyərlər. Bu dəyərlər callback sorğuda sizə
                            geri göndərilir.
            """  # noqa: E501

        @overload
        def split_pay(
            self: 'EPointClientClass[_Async]',
            amount: Numeric,
            currency: str,
            order_id: str,
            split_user_id: str,
            split_amount: Numeric,
            description: Unset[str] = UNSET,
            **extra: Any,
        ) -> Coroutine[Any, Any, APIResponse[RedirectUrlResponseSchema]]: ...
        def split_pay(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def split_pay_with_saved_card(
            self: 'EPointClientClass[_Sync]',
            amount: Numeric,
            currency: str,
            order_id: str,
            card_id: str,
            split_user_id: str,
            split_amount: Numeric,
            description: Unset[str] = UNSET,
        ) -> APIResponse[SplitPayWithSavedCardResponseSchema]:
            """Saxlanılmış kartla ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə sorğusu

            **Endpoint:** */api/1/split-execute-pay*

            Example:
                ```python
                from integrify.epoint import EPointRequest

                EPointRequest.split_pay_with_saved_card(amount=100, currency='AZN', order_id='123456789', card_id='cexxxxxx', split_user_id='epoint_user_id', split_amount=50, description='split payment')
                ```

            Cavab formatı: [`SplitPayWithSavedCardResponseSchema`][integrify.epoint.schemas.response.SplitPayWithSavedCardResponseSchema]

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
                order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
                card_id: Saxlanılmış kartın id-si. Adətən `ce` prefiksi ilə başlayır.
                split_user_id: Ödənişi böləcəyini **EPoint** user-ini IDsi
                split_amount: Bölünən miqdar. Numerik dəyər
                description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
            """  # noqa: E501

        @overload
        def split_pay_with_saved_card(
            self: 'EPointClientClass[_Async]',
            amount: Numeric,
            currency: str,
            order_id: str,
            card_id: str,
            split_user_id: str,
            split_amount: Numeric,
            description: Unset[str] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[SplitPayWithSavedCardResponseSchema]]: ...
        def split_pay_with_saved_card(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def split_pay_and_save_card(
            self: 'EPointClientClass[_Sync]',
            amount: Numeric,
            currency: str,
            order_id: str,
            split_user_id: str,
            split_amount: Numeric,
            description: Unset[str] = UNSET,
        ) -> APIResponse[RedirectUrlWithCardIdResponseSchema]:
            """Ödənişi başqa EPoint istifadəçisi ilə bölüb ödəmə və kartı saxlama sorğusu

            **Endpoint:** */api/1/split-card-registration-with-pay*

            Example:
                ```python
                from integrify.epoint import EPointRequest

                EPointRequest.split_pay_and_save_card(amount=100, currency='AZN', order_id='123456789', split_user_id='epoint_user_id', split_amount=50, description='split payment')
                ```

            Cavab formatı: [`RedirectUrlWithCardIdResponseSchema`][integrify.epoint.schemas.response.RedirectUrlWithCardIdResponseSchema]

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
                order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
                split_user_id: Ödənişi böləcəyini **EPoint** user-ini IDsi
                split_amount: Bölünən miqdar. Numerik dəyər
                description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol. Məcburi arqument deyil.
            """  # noqa: E501

        @overload
        def split_pay_and_save_card(
            self: 'EPointClientClass[_Async]',
            amount: Numeric,
            currency: str,
            order_id: str,
            split_user_id: str,
            split_amount: Numeric,
            description: Unset[str] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[RedirectUrlWithCardIdResponseSchema]]: ...
        def split_pay_and_save_card(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def create_widget(
            self: 'EPointClientClass[_Sync]',
            amount: Numeric,
            order_id: str,
            description: str,
        ) -> APIResponse[WidgetResponseSchema]:
            """Apple Pay və Google Pay widget-i yaratma sorğusu

            **Endpoint:** */api/1/token/widget*

            Example:
                ```python
                from integrify.epoint import EPointRequest

                EPointRequest.create_widget(amount=2.5, order_id='12345678', description='Ödəniş')
                ```

            **Cavab formatı**: [`WidgetResponseSchema`][integrify.epoint.schemas.response.WidgetResponseSchema]

            Apple Pay/Google Pay-i qoşmağın ən sadə yolu. Cavabda gələn `widget_url`-i saytınızda
            iframe, mobil tətbiqdə isə webview daxilində açın: düymələr və ödəniş axını EPoint
            tərəfindən idarə olunur, əlavə backend endpoint-lərinə ehtiyac yoxdur. Ödəniş bitdikdən
            sonra widget səhifəyə `message` event-i göndərir (`event.data`:
            `{status: 'success', payment: {...}}`). Ödənişin nəticəsini backend-də
            [`get_transaction_status`][integrify.epoint.client.EPointClientClass.get_transaction_status]
            ilə yoxlamaq tövsiyə olunur.

            Düymələri öz dizaynınızla göstərmək istəyirsinizsə,
            [`create_token_payment`][integrify.epoint.client.EPointClientClass.create_token_payment]
            ilə başlayan SDK axınından istifadə edin.

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
                description: Ödənişin təsviri. Maksimal uzunluq: 1000 simvol.
            """  # noqa: E501

        @overload
        def create_widget(
            self: 'EPointClientClass[_Async]',
            amount: Numeric,
            order_id: str,
            description: str,
        ) -> Coroutine[Any, Any, APIResponse[WidgetResponseSchema]]: ...
        def create_widget(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def create_token_payment(
            self: 'EPointClientClass[_Sync]',
            amount: Numeric,
            currency: str,
            order_id: str,
            description: Unset[str] = UNSET,
        ) -> APIResponse[TokenPaymentResponseSchema]:
            """Apple Pay/Google Pay üçün token ödənişi yaratma sorğusu

            **Endpoint:** */api/1/token/payment*

            Example:
                ```python
                from integrify.epoint import EPointRequest

                EPointRequest.create_token_payment(amount=2.5, currency='AZN', order_id='12345678', description='Ödəniş')
                ```

            **Cavab formatı**: [`TokenPaymentResponseSchema`][integrify.epoint.schemas.response.TokenPaymentResponseSchema]

            Apple Pay/Google Pay düymələrini işə salmazdan əvvəl, EPoint-də token ödənişi
            yaradılmalıdır: bütün sonrakı token əməliyyatları bu ödənişə istinad edir. Cavabda gələn
            ödəniş obyektini (ən azı `id` və məbləği) frontend-də `initTokenPay`-ə `payment`
            parametri kimi ötürün. Sonra SDK sizin backend-inizdəki
            [`apple_pay_session`][integrify.epoint.client.EPointClientClass.apple_pay_session],
            [`apple_pay`][integrify.epoint.client.EPointClientClass.apple_pay] və
            [`google_pay`][integrify.epoint.client.EPointClientClass.google_pay] sorğularını
            çağıran endpoint-lərə müraciət edəcək.

            Args:
                amount: Ödəniş miqdarı. Numerik dəyər.
                currency: Ödəniş məzənnəsi. Mümkün dəyərlər: AZN
                order_id: Unikal ID. Maksimal uzunluq: 255 simvol.
                description: Ödənişin təsviri. Məcburi arqument deyil.
            """  # noqa: E501

        @overload
        def create_token_payment(
            self: 'EPointClientClass[_Async]',
            amount: Numeric,
            currency: str,
            order_id: str,
            description: Unset[str] = UNSET,
        ) -> Coroutine[Any, Any, APIResponse[TokenPaymentResponseSchema]]: ...
        def create_token_payment(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def apple_pay_session(
            self: 'EPointClientClass[_Sync]',
            origin: str,
        ) -> APIResponse[dict]:
            """Apple Pay session-u almaq sorğusu

            **Endpoint:** */api/1/token/apple/session*

            Example:
                ```python
                from integrify.epoint import EPointRequest

                EPointRequest.apple_pay_session(origin='https://yoursite.az')
                ```

            **Cavab formatı**: `dict` (Apple merchant session obyekti, olduğu kimi)

            Apple Pay-in əlavə təhlükəsizlik qatı var: SDK ödəniş pəncərəsini açmazdan əvvəl
            sizin backend-inizdəki session endpoint-inə (məs., `/epoint/apple/session`) POST
            sorğusu göndərir. Həmin endpoint bu sorğunu çağırıb, `resp.body`-ni olduğu kimi
            geri qaytarmalıdır.

            Args:
                origin: Ödəniş səhifəsinin açıldığı saytın origin-i (məs., `https://yoursite.az`).
                        Adətən daxil olan sorğunun `Origin` header-indən götürülür.
            """  # noqa: E501

        @overload
        def apple_pay_session(
            self: 'EPointClientClass[_Async]',
            origin: str,
        ) -> Coroutine[Any, Any, APIResponse[dict]]: ...
        def apple_pay_session(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def apple_pay(
            self: 'EPointClientClass[_Sync]',
            payment_id: int | str,
            token: Any,
            billing_contact: Any = None,
        ) -> APIResponse[TokenPayResponseSchema]:
            """Apple Pay ilə ödənişi tamamlama sorğusu

            **Endpoint:** */api/1/token/apple/pay*

            Example:
                ```python
                from integrify.epoint import EPointRequest

                # body: SDK-nın sizin `/epoint/apple` endpoint-inə göndərdiyi JSON
                EPointRequest.apple_pay(
                    payment_id=body['id'],
                    token=body['token'],
                    billing_contact=body.get('billingContact'),
                )
                ```

            **Cavab formatı**: [`TokenPayResponseSchema`][integrify.epoint.schemas.response.TokenPayResponseSchema]

            Session uğurla yaradıldıqdan və istifadəçi Apple Pay pəncərəsində ödənişi
            təsdiqlədikdən sonra (kart seçimi, təsdiq), SDK sizin backend-inizdəki pay
            endpoint-inə (məs., `/epoint/apple`) `id`, `token` və `billingContact` göndərir.
            Həmin endpoint bu sorğunu çağırıb, `resp.body`-ni olduğu kimi geri qaytarmalıdır.
            `public_key` avtomatik əlavə olunur.

            Args:
                payment_id: Token ödənişinin IDsi (SDK sorğusundakı `id`).
                token: Apple Pay token-i (SDK sorğusundakı `token`).
                billing_contact: Ödəyicinin billing məlumatı (SDK sorğusundakı `billingContact`).
            """  # noqa: E501

        @overload
        def apple_pay(
            self: 'EPointClientClass[_Async]',
            payment_id: int | str,
            token: Any,
            billing_contact: Any = None,
        ) -> Coroutine[Any, Any, APIResponse[TokenPayResponseSchema]]: ...
        def apple_pay(self, *args: Any, **kwds: Any) -> Any: ...

        @overload
        def google_pay(
            self: 'EPointClientClass[_Sync]',
            payment_id: int | str,
            token: Any,
            billing_contact: Any = None,
        ) -> APIResponse[TokenPayResponseSchema]:
            """Google Pay ilə ödənişi tamamlama sorğusu

            **Endpoint:** */api/1/token/google/pay*

            Example:
                ```python
                from integrify.epoint import EPointRequest

                # body: SDK-nın sizin `/epoint/google` endpoint-inə göndərdiyi JSON
                EPointRequest.google_pay(
                    payment_id=body['id'],
                    token=body['token'],
                    billing_contact=body.get('billingContact'),
                )
                ```

            **Cavab formatı**: [`TokenPayResponseSchema`][integrify.epoint.schemas.response.TokenPayResponseSchema]

            Apple Pay ilə eynidir, yalnız endpoint fərqlidir və session mərhələsi yoxdur.
            İstifadəçi Google Pay pəncərəsində ödənişi təsdiqlədikdən sonra, SDK sizin
            backend-inizdəki pay endpoint-inə (məs., `/epoint/google`) `id`, `token` və
            `billingContact` göndərir. Həmin endpoint bu sorğunu çağırıb, `resp.body`-ni
            olduğu kimi geri qaytarmalıdır. `public_key` avtomatik əlavə olunur.

            Args:
                payment_id: Token ödənişinin IDsi (SDK sorğusundakı `id`).
                token: Google Pay token-i (SDK sorğusundakı `token`).
                billing_contact: Ödəyicinin billing məlumatı (SDK sorğusundakı `billingContact`).
            """  # noqa: E501

        @overload
        def google_pay(
            self: 'EPointClientClass[_Async]',
            payment_id: int | str,
            token: Any,
            billing_contact: Any = None,
        ) -> Coroutine[Any, Any, APIResponse[TokenPayResponseSchema]]: ...
        def google_pay(self, *args: Any, **kwds: Any) -> Any: ...


EPointRequest: 'EPointClientClass[_Sync]' = EPointClientClass(sync=True)
EPointAsyncRequest: 'EPointClientClass[_Async]' = EPointClientClass(sync=False)
