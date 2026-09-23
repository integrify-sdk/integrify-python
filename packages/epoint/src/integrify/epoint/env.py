import os
from enum import Enum
from warnings import warn

VERSION = '1.0.3'

EPOINT_PUBLIC_KEY: str = os.getenv('EPOINT_PUBLIC_KEY', '')
EPOINT_PRIVATE_KEY: str = os.getenv('EPOINT_PRIVATE_KEY', '')

EPOINT_INTERFACE_LANG: str = os.getenv('EPOINT_INTERFACE_LANG', 'az')
EPOINT_SUCCESS_REDIRECT_URL: str | None = os.getenv('EPOINT_SUCCESS_REDIRECT_URL')
EPOINT_FAILED_REDIRECT_URL: str | None = os.getenv('EPOINT_FAILED_REDIRECT_URL')
EPOINT_LOGGER_NAME: str = os.getenv('EPOINT_LOGGER_NAME', 'epoint')


if not EPOINT_PUBLIC_KEY or not EPOINT_PRIVATE_KEY:  # pragma: no cover
    warn(
        'EPOINT_PUBLIC_KEY/EPOINT_PRIVATE_KEY mühit dəyişənlərinə dəyər verməsəniz '
        'sorğular çalışmayacaq!'
    )


class API(str, Enum):
    """Endpoint constant-ları"""

    BASE_URL = 'https://epoint.az'

    PAY = '/api/1/request'
    GET_STATUS = '/api/1/get-status'
    SAVE_CARD = '/api/1/card-registration'
    PAY_WITH_SAVED_CARD = '/api/1/execute-pay'
    PAY_AND_SAVE_CARD = '/api/1/card-registration-with-pay'
    PAYOUT = '/api/1/refund-request'
    REFUND = '/api/1/reverse'
    SPLIT_PAY = '/api/1/split-request'
    SPLIT_PAY_WITH_SAVED_CARD = '/api/1/split-execute-pay'
    SPLIT_PAY_AND_SAVE_CARD = '/api/1/split-card-registration-with-pay'

    # Apple Pay & Google Pay
    CREATE_WIDGET = '/api/1/token/widget'
    CREATE_TOKEN_PAYMENT = '/api/1/token/payment'  # nosec: B105
    APPLE_PAY_SESSION = '/api/1/token/apple/session'
    APPLE_PAY = '/api/1/token/apple/pay'
    GOOGLE_PAY = '/api/1/token/google/pay'


__all__ = [
    'VERSION',
    'EPOINT_PUBLIC_KEY',
    'EPOINT_PRIVATE_KEY',
    'EPOINT_INTERFACE_LANG',
    'EPOINT_SUCCESS_REDIRECT_URL',
    'EPOINT_FAILED_REDIRECT_URL',
    'EPOINT_LOGGER_NAME',
    'API',
]
