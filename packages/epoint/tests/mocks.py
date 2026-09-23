import pytest
from httpx import Response
from integrify.epoint.schemas.enums import TransactionStatus, TransactionStatusExtended

MESSAGE_SUCCESS = 'Təsdiq edildi'
MESSAGE_SERVER_ERROR = 'Signature did not match'
MESSAGE_TRANSACTION_FAIL = 'Kartda kifayət qədər balans yoxdur'


@pytest.fixture(scope='package')
def epoint_mock_get_transaction_status_success_response():
    return Response(
        status_code=200,
        json={
            'status': TransactionStatusExtended.SUCCESS,
            'message': MESSAGE_SUCCESS,
            'transaction': 'texxxxxxxxxx',
            'bank_transaction': 'base64data',
            'bank_response': '',
            'operation_code': None,
            'rrn': 'RRN-123456789',
            'card_mask': '*******1234',
            'card_name': 'Name Surname',
            'amount': 1,
            'code': '',
            'order_id': 'random_order_id',
            'other_attr': None,
        },
    )


@pytest.fixture(scope='package')
def epoint_mock_get_transaction_status_failed_response():
    # Request is successful, transaction was not
    return Response(
        status_code=200,
        json={
            'status': TransactionStatusExtended.ERROR,
            'message': MESSAGE_TRANSACTION_FAIL,
            'transaction': 'texxxxxxxxxx',
            'bank_transaction': 'base64data',
            'bank_response': '',
            'operation_code': None,
            'rrn': 'RRN-123456789',
            'card_mask': '*******1234',
            'card_name': 'Name Surname',
            'amount': 1,
            'code': '',
            'order_id': 'random_order_id',
            'other_attr': None,
        },
    )


@pytest.fixture(scope='package')
def epoint_mock_bad_signature_response():
    return Response(
        status_code=200,
        json={
            'status': TransactionStatusExtended.SERVER_ERROR,
            'message': MESSAGE_SERVER_ERROR,
        },
    )


@pytest.fixture(scope='package')
def epoint_mock_save_card_response():
    return Response(
        status_code=200,
        json={
            'status': TransactionStatus.SUCCESS,
            'redirect_url': 'https://epoint.az',
            'card_id': 'cexxxxxxxxxx',
        },
    )


@pytest.fixture(scope='package')
def epoint_mock_save_card_failed_response():
    return Response(
        status_code=200,
        json={
            'status': TransactionStatus.ERROR,
            'redirect_url': None,
            'card_id': None,
        },
    )


@pytest.fixture(scope='package')
def epoint_mock_payment_response():
    return Response(
        status_code=200,
        json={
            'status': TransactionStatus.SUCCESS,
            'transaction': 'texxxxxxxxxx',
            'redirect_url': 'https://epoint.az/',
        },
    )


@pytest.fixture(scope='package')
def epoint_mock_pay_and_save_card_response():
    return Response(
        status_code=200,
        json={
            'status': TransactionStatus.SUCCESS,
            'transaction': 'texxxxxxxxxx',
            'redirect_url': 'https://epoint.az/',
            'card_id': 'cexxxxxxxxxx',
        },
    )


@pytest.fixture(scope='package')
def epoint_mock_pay_with_saved_card_response():
    return Response(
        status_code=200,
        json={
            'status': TransactionStatus.SUCCESS,
            'message': 'Approved',
            'transaction': 'texxxxxxxxxx',
            'bank_transaction': 'base64data',
            'bank_response': '',
            'operation_code': None,
            'rrn': 'RRN-123456789',
            'card_mask': '*******1234',
            'card_name': 'Name Surname',
            'amount': 1,
        },
    )


@pytest.fixture(scope='package')
def epoint_mock_payout_response():
    return Response(
        status_code=200,
        json={
            'status': TransactionStatus.SUCCESS,
            'message': 'Approved',
            'transaction': 'texxxxxxxxxx',
            'bank_transaction': 'base64data',
            'bank_response': '',
            'rrn': 'RRN-123456789',
            'card_mask': '*******1234',
            'card_name': 'Name Surname',
            'amount': 1,
        },
    )


@pytest.fixture(scope='package')
def epoint_mock_refund_response():
    return Response(
        status_code=200,
        json={'status': TransactionStatus.SUCCESS, 'message': 'Approved'},
    )


@pytest.fixture(scope='package')
def epoint_mock_split_payment_response():
    return Response(
        status_code=200,
        json={
            'status': TransactionStatus.SUCCESS,
            'transaction': 'texxxxxxxxxx',
            'redirect_url': 'https://epoint.az/',
        },
    )


@pytest.fixture(scope='package')
def epoint_mock_split_pay_with_saved_card_response():
    return Response(
        status_code=200,
        json={
            'status': TransactionStatus.SUCCESS,
            'message': 'Approved',
            'transaction': 'texxxxxxxxxx',
            'bank_transaction': 'base64data',
            'bank_response': '',
            'operation_code': None,
            'rrn': 'RRN-123456789',
            'card_mask': '*******1234',
            'card_name': 'Name Surname',
            'amount': 100,
            'split_amount': 50,
        },
    )


@pytest.fixture(scope='package')
def epoint_mock_split_pay_and_save_card_response():
    return Response(
        status_code=200,
        json={
            'status': TransactionStatus.SUCCESS,
            'transaction': 'texxxxxxxxxx',
            'redirect_url': 'https://epoint.az/',
            'card_id': 'cexxxxxxxxxx',
        },
    )


##############################################################################
# Apple Pay & Google Pay
@pytest.fixture(scope='package')
def epoint_mock_create_widget_response():
    return Response(
        status_code=200,
        json={
            'status': TransactionStatus.SUCCESS,
            'widget_url': 'https://epoint.az/api/1/token/widget/000001',
        },
    )


@pytest.fixture(scope='package')
def epoint_mock_create_widget_failed_response():
    return Response(
        status_code=200,
        json={'status': TransactionStatus.ERROR, 'message': MESSAGE_SERVER_ERROR},
    )


@pytest.fixture(scope='package')
def epoint_mock_create_token_payment_response():
    return Response(
        status_code=200,
        json={
            'id': 9998887,
            'transaction': '12345',
            'rrn': '123',
            'short_link': 'a1b2',
            'bank_order_id': 'aaa111',
            'total': 2.36,
            'card_name': 'Name',
            'card_mask': '4000********1234',
            'description': 'test description',
            'merchant_order_id': '111222333',
            'other_attr': 'other attributes',
            'created_at': '2024-10-16 12:09:10',
            'updated_at': '2024-10-16 15:00:48',
        },
    )


@pytest.fixture(scope='package')
def epoint_mock_create_token_payment_failed_response():
    return Response(
        status_code=200,
        json={'status': TransactionStatus.SERVER_ERROR, 'message': MESSAGE_SERVER_ERROR},
    )


@pytest.fixture(scope='package')
def epoint_mock_apple_pay_session_response():
    return Response(
        status_code=200,
        json={
            'epochTimestamp': 1729080550000,
            'expiresAt': 1729084150000,
            'merchantSessionIdentifier': 'SSH...',
            'nonce': 'abc123',
            'merchantIdentifier': 'merchant.az.epoint',
            'domainName': 'yoursite.az',
            'displayName': 'Your Site',
            'signature': 'base64signature',
        },
    )


@pytest.fixture(scope='package')
def epoint_mock_apple_pay_session_failed_response():
    return Response(
        status_code=200,
        json={'status': TransactionStatus.SERVER_ERROR, 'message': MESSAGE_SERVER_ERROR},
    )


@pytest.fixture(scope='package')
def epoint_mock_token_pay_response():
    return Response(
        status_code=200,
        json={
            'status': TransactionStatus.SUCCESS,
            'message': 'Payment is finished successfully',
            'result': {'code': '000'},
        },
    )


@pytest.fixture(scope='package')
def epoint_mock_token_pay_failed_response():
    return Response(
        status_code=200,
        json={'status': TransactionStatus.ERROR, 'message': MESSAGE_TRANSACTION_FAIL},
    )
