import base64
import json
from datetime import datetime
from decimal import Decimal

import pytest
from httpx import Response
from integrify.epoint.client import EPointClientClass
from pytest_mock import MockerFixture


def _decode(dry_resp: dict) -> dict:
    return json.loads(base64.b64decode(dry_resp['data']['data']))


@pytest.fixture(scope='module')
def epoint_dry_client():
    yield EPointClientClass(dry=True)


def test_create_widget_payload(epoint_dry_client: EPointClientClass, mocker: MockerFixture):
    mocker.patch('integrify.epoint.env.EPOINT_PUBLIC_KEY', 'pub')
    resp = epoint_dry_client.create_widget(amount=2.5, order_id='123', description='Test payment')

    assert resp['url'].endswith('/api/1/token/widget')
    assert resp['data']['signature']
    assert _decode(resp) == {
        'public_key': 'pub',
        'amount': '2.5',
        'order_id': '123',
        'description': 'Test payment',
    }


def test_create_widget_request(
    epoint_client: EPointClientClass,
    epoint_mock_create_widget_response: Response,
    mocker: MockerFixture,
):
    mocker.patch('httpx.Client.request', return_value=epoint_mock_create_widget_response)
    resp = epoint_client.create_widget(amount=2.5, order_id='123', description='Test payment')

    assert resp.ok
    assert resp.body.widget_url == 'https://epoint.az/api/1/token/widget/000001'


def test_create_widget_failed_request(
    epoint_client: EPointClientClass,
    epoint_mock_create_widget_failed_response: Response,
    mocker: MockerFixture,
):
    mocker.patch('httpx.Client.request', return_value=epoint_mock_create_widget_failed_response)
    resp = epoint_client.create_widget(amount=2.5, order_id='123', description='Test payment')

    assert not resp.ok
    assert resp.body.widget_url is None


def test_create_token_payment_payload(epoint_dry_client: EPointClientClass, mocker: MockerFixture):
    mocker.patch('integrify.epoint.env.EPOINT_PUBLIC_KEY', 'pub')
    resp = epoint_dry_client.create_token_payment(
        amount=2.5, currency='AZN', order_id='123', description='Test payment'
    )

    assert resp['url'].endswith('/api/1/token/payment')
    assert resp['data']['signature']
    data = _decode(resp)
    assert data['public_key'] == 'pub'
    assert data['language']
    assert data['order_id'] == '123'
    assert data['description'] == 'Test payment'


def test_apple_pay_session_payload(epoint_dry_client: EPointClientClass, mocker: MockerFixture):
    mocker.patch('integrify.epoint.env.EPOINT_PUBLIC_KEY', 'pub')
    resp = epoint_dry_client.apple_pay_session(origin='https://yoursite.az')

    assert resp['url'].endswith('/api/1/token/apple/session')
    assert _decode(resp) == {'public_key': 'pub', 'origin': 'https://yoursite.az'}


@pytest.mark.parametrize(
    'method, endpoint',
    [('apple_pay', '/api/1/token/apple/pay'), ('google_pay', '/api/1/token/google/pay')],
)
def test_token_pay_payload(
    epoint_dry_client: EPointClientClass,
    mocker: MockerFixture,
    method: str,
    endpoint: str,
):
    mocker.patch('integrify.epoint.env.EPOINT_PUBLIC_KEY', 'pub')
    token = {'paymentData': {'data': 'xxx'}}
    contact = {'givenName': 'Name'}

    resp = getattr(epoint_dry_client, method)(payment_id=1, token=token, billing_contact=contact)
    assert resp['url'].endswith(endpoint)
    assert _decode(resp) == {
        'public_key': 'pub',
        'id': 1,
        'token': token,
        'billingContact': contact,
    }

    # SDK-dan gələn body birbaşa ötürülə bilər (id/billingContact açarları ilə)
    resp2 = getattr(epoint_dry_client, method)(
        **{'id': 1, 'token': token, 'billingContact': contact}
    )
    assert _decode(resp2) == _decode(resp)


def test_create_token_payment_request(
    epoint_client: EPointClientClass,
    epoint_mock_create_token_payment_response: Response,
    mocker: MockerFixture,
):
    mocker.patch('httpx.Client.request', return_value=epoint_mock_create_token_payment_response)
    resp = epoint_client.create_token_payment(amount=2.5, currency='AZN', order_id='111222333')

    assert resp.ok
    assert resp.body.id == 9998887
    assert resp.body.total == Decimal('2.36')
    assert resp.body.created_at == datetime(2024, 10, 16, 12, 9, 10)


def test_create_token_payment_failed_request(
    epoint_client: EPointClientClass,
    epoint_mock_create_token_payment_failed_response: Response,
    mocker: MockerFixture,
):
    mocker.patch(
        'httpx.Client.request', return_value=epoint_mock_create_token_payment_failed_response
    )
    resp = epoint_client.create_token_payment(amount=2.5, currency='AZN', order_id='111222333')

    assert not resp.ok
    assert resp.body.id is None
    assert resp.body.message


def test_apple_pay_session_request(
    epoint_client: EPointClientClass,
    epoint_mock_apple_pay_session_response: Response,
    mocker: MockerFixture,
):
    mocker.patch('httpx.Client.request', return_value=epoint_mock_apple_pay_session_response)
    resp = epoint_client.apple_pay_session(origin='https://yoursite.az')

    assert resp.ok
    assert resp.body['merchantSessionIdentifier']


def test_apple_pay_session_failed_request(
    epoint_client: EPointClientClass,
    epoint_mock_apple_pay_session_failed_response: Response,
    mocker: MockerFixture,
):
    mocker.patch('httpx.Client.request', return_value=epoint_mock_apple_pay_session_failed_response)
    resp = epoint_client.apple_pay_session(origin='https://yoursite.az')

    assert not resp.ok


@pytest.mark.parametrize('method', ['apple_pay', 'google_pay'])
def test_token_pay_request(
    epoint_client: EPointClientClass,
    epoint_mock_token_pay_response: Response,
    mocker: MockerFixture,
    method: str,
):
    mocker.patch('httpx.Client.request', return_value=epoint_mock_token_pay_response)
    resp = getattr(epoint_client, method)(payment_id=1, token='token')

    assert resp.ok
    assert resp.body.status == 'success'
    assert resp.body.result == {'code': '000'}
    assert resp.body.redirect_url is None


@pytest.mark.parametrize('method', ['apple_pay', 'google_pay'])
def test_token_pay_failed_request(
    epoint_client: EPointClientClass,
    epoint_mock_token_pay_failed_response: Response,
    mocker: MockerFixture,
    method: str,
):
    mocker.patch('httpx.Client.request', return_value=epoint_mock_token_pay_failed_response)
    resp = getattr(epoint_client, method)(payment_id=1, token='token')

    assert not resp.ok
    assert resp.body.status == 'error'
