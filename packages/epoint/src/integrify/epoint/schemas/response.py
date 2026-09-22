from datetime import datetime
from decimal import Decimal
from typing import Any

from integrify.epoint.schemas.enums import Code, TransactionStatus, TransactionStatusExtended
from pydantic import BaseModel, field_validator


class MinimalResponseSchema(BaseModel):
    status: TransactionStatus
    """Success və ya failed əməliyyatının nəticəsi"""

    message: str | None = None
    """Ödənişin icra statusu haqqında mesaj"""


class BaseResponseSchema(MinimalResponseSchema):
    # if success
    transaction: str | None = None
    """EPoint xidmətinin əməliyyat IDsi"""

    bank_transaction: str | None = None
    """Bank ödəniş əməliyyatı IDsi"""

    bank_response: str | None = None
    """Ödəniş icrasının nəticəsi ilə bankın cavabı"""

    operation_code: str | None = None
    """001-kart qeydiyyatı\n100- istifadəçi ödənişi"""

    rrn: str | None = None
    """Retrieval Reference Number - unikal əməliyyat identifikatoru.
    Yalnız uğurlu bir əməliyyat üçün mövcuddur"""

    card_mask: str | None = None
    """Ödəniş səhifəsində göstərilən istifadəçi adı"""

    card_name: str | None = None
    """123456******1234 formatında əks edilən kart maskası"""

    amount: Decimal | None = None
    """Ödəniş məbləği"""


class BaseWithCodeSchema(BaseResponseSchema):
    code: str | None = None
    """Bankın 3 rəqəmli cavab kodu."""

    @field_validator('code', mode='before')
    @classmethod
    def code_to_msg(cls, v: str | None = None) -> str | None:
        """3 rəqəmli koddan, xəta/uğur mesajına çevrilir.

        Kod `Code` lüğətində yoxdursa (bank yeni/naməlum kod qaytara bilər),
        `KeyError` atmaq əvəzinə orijinal kod qaytarılır ki, cavab parse-i crash olmasın.
        """
        if not v:
            return None

        return Code.get(v, v)


#################################################################
class RedirectUrlResponseSchema(MinimalResponseSchema):
    # if success
    transaction: str | None = None
    """EPoint xidmətinin əməliyyat IDsi"""

    redirect_url: str | None = None
    """İstifadəçinin kart məlumatlarını daxil etmək üçün yönləndirilməsi lazım olan URL"""


class RedirectUrlWithCardIdResponseSchema(RedirectUrlResponseSchema):
    card_id: str | None = None
    """Ödənişləri yerinə yetirmək üçün istifadə edilməsi
    lazım olan unikal kart identifikatoru"""


class PaymentSchema(BaseWithCodeSchema):
    order_id: str
    """Tətbiqinizdə unikal əməliyyat ID"""

    other_attr: str | None = None
    """Əlavə göndərdiyiniz seçimlər"""


class TransactionStatusResponseSchema(BaseWithCodeSchema):
    status: TransactionStatusExtended
    """Tranzaksiyanın detallı statusu"""

    order_id: str | None = None
    """Tətbiqinizdə unikal əməliyyat ID"""

    other_attr: str | None = None
    """Əlavə göndərdiyiniz seçimlər"""


class SplitPayWithSavedCardResponseSchema(BaseResponseSchema):
    split_amount: Decimal | None = None
    """İkinci istifadəçi üçün ödəniş məbləği."""


#################################################################
# Apple Pay & Google Pay
class WidgetResponseSchema(BaseModel):
    """`/api/1/token/widget` sorğusunun cavabı"""

    status: str
    """Əməliyyatın nəticəsi: `success` və ya `error`"""

    message: str | None = None
    """Xəta baş verdikdə, xəta mesajı"""

    widget_url: str | None = None
    """Apple Pay/Google Pay düymələrinin olduğu widget-in URL-i.
    iframe və ya webview daxilində açılmalıdır."""


class TokenPaymentResponseSchema(BaseModel):
    """`/api/1/token/payment` sorğusunun cavabı: EPoint-də yaradılmış token ödənişi.
    Bu obyekt frontend-də `initTokenPay`-ə `payment` parametri kimi ötürülür."""

    # if error
    status: str | None = None
    """Xəta baş verdikdə, əməliyyatın statusu"""

    message: str | None = None
    """Xəta baş verdikdə, xəta mesajı"""

    # if success
    id: int | None = None
    """Token ödənişinin EPoint-dəki IDsi. Apple/Google Pay sorğularında istifadə olunur."""

    transaction: str | None = None
    """EPoint xidmətinin əməliyyat IDsi"""

    rrn: str | None = None
    """Retrieval Reference Number - unikal əməliyyat identifikatoru"""

    short_link: str | None = None
    """Ödənişin qısa linki"""

    bank_order_id: str | None = None
    """Bank tərəfindəki sifariş IDsi"""

    total: Decimal | None = None
    """Ödənişin yekun məbləği"""

    card_name: str | None = None
    """Ödəniş səhifəsində göstərilən istifadəçi adı"""

    card_mask: str | None = None
    """123456******1234 formatında əks edilən kart maskası"""

    description: str | None = None
    """Ödənişin təsviri"""

    merchant_order_id: str | None = None
    """Tətbiqinizdə unikal əməliyyat ID (sorğuda göndərdiyiniz `order_id`)"""

    other_attr: Any = None
    """Əlavə göndərdiyiniz seçimlər"""

    created_at: datetime | None = None
    """Ödənişin yaradılma tarixi"""

    updated_at: datetime | None = None
    """Ödənişin son yenilənmə tarixi"""


class TokenPayResponseSchema(BaseModel):
    """Apple Pay/Google Pay ödənişinin tamamlanması sorğusunun cavabı"""

    status: str
    """Əməliyyatın nəticəsi. Uğurlu olduqda: `success`"""

    message: str | None = None
    """Ödənişin icra statusu haqqında mesaj"""

    result: Any = None
    """Ödəniş provayderindən (PSP) gələn cavab"""

    redirect_url: str | None = None
    """Yönləndirmə URL-i (məs., 3DS üçün). Hər zaman gəlmir."""
