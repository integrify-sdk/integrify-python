from decimal import Decimal
from typing import Any

from integrify.epoint import env
from integrify.schemas import PayloadBaseModel
from pydantic import AliasChoices, Field


class MinimalPaymentRequestSchema(PayloadBaseModel):
    amount: Decimal
    currency: str
    order_id: str


class BasePaymentRequestSchema(MinimalPaymentRequestSchema):
    success_redirect_url: str | None = env.EPOINT_SUCCESS_REDIRECT_URL
    error_redirect_url: str | None = env.EPOINT_FAILED_REDIRECT_URL
    description: str | None = None


##############################################################################
class PaymentRequestSchema(BasePaymentRequestSchema):
    other_attr: dict | None = None


class GetTransactionStatusRequestSchema(PayloadBaseModel):
    transaction: str = Field(validation_alias='transaction_id')


class SaveCardRequestSchema(PayloadBaseModel):
    pass


class PayWithSavedCardRequestSchema(MinimalPaymentRequestSchema):
    card_id: str


class PayAndSaveCardRequestSchema(BasePaymentRequestSchema):
    description: str


class PayoutRequestSchema(MinimalPaymentRequestSchema):
    card_id: str
    description: str | None = None


class RefundRequestSchema(PayloadBaseModel):
    transaction: str = Field(validation_alias='transaction_id')
    currency: str
    amount: Decimal | None = None


class SplitPayRequestSchema(BasePaymentRequestSchema):
    split_user: str = Field(validation_alias='split_user_id')
    split_amount: Decimal
    other_attr: dict | None = None


class SplitPayWithSavedCardRequestSchema(MinimalPaymentRequestSchema):
    card_id: str
    split_user: str = Field(validation_alias='split_user_id')
    split_amount: Decimal
    description: str | None = None


class SplitPayAndSaveCardRequestSchema(BasePaymentRequestSchema):
    split_user: str = Field(validation_alias='split_user_id')
    split_amount: Decimal
    description: str | None = None


##############################################################################
# Apple Pay & Google Pay
class CreateWidgetRequestSchema(PayloadBaseModel):
    amount: Decimal
    order_id: str
    description: str


class CreateTokenPaymentRequestSchema(PayloadBaseModel):
    amount: Decimal
    currency: str
    order_id: str
    description: str | None = None


class ApplePaySessionRequestSchema(PayloadBaseModel):
    origin: str


class BaseTokenPayRequestSchema(PayloadBaseModel):
    id: int | str = Field(validation_alias=AliasChoices('payment_id', 'id'))
    token: Any
    billing_contact: Any = Field(
        default=None,
        validation_alias=AliasChoices('billing_contact', 'billingContact'),
        serialization_alias='billingContact',
    )


class ApplePayRequestSchema(BaseTokenPayRequestSchema):
    pass


class GooglePayRequestSchema(BaseTokenPayRequestSchema):
    pass
