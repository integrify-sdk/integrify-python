# EPoint API (v1.0.3)

???+ info
    Bu səhifə EPoint-in rəsmi API dokumentasiyasının (ingiliscə, v1.0.3) Markdown versiyasıdır.
    Orijinal: [API Epoint en.pdf](https://epointbucket.s3.eu-central-1.amazonaws.com/files/instructions/API%20Epoint%20en.pdf).
    Orijinalda kod nümunələri şəkil kimi verildiyi üçün, burada onlar parametr cədvəllərinə
    əsasən yenidən yazılıb. Uyğunsuzluq olarsa, orijinal PDF əsas götürülür.

**Epoint.az** — electronic payment platform. Solution for payment on site.

## Contents

- [Epoint payment page working principle](#working-principle)
- [Formation of API request](#formation-of-api-request)
- [Callback function processing](#callback-function-processing)
- [Checking payment status](#checking-payment-status)
- [Saving a card to make payments without entering card data](#card-registration)
- [Executing a payment with a saved card](#execute-pay)
- [Saving the card with the first payment made](#card-registration-with-pay)
- [Request for disbursement of funds](#refund-request)
- [Cancel operations](#reverse)
- [Split payment request](#split-request)
- [Executing a split payment with a stored card](#split-execute-pay)
- [Saving the card with the first split payment](#split-card-registration-with-pay)
- [Formation of API preauth request](#pre-auth-request)
- [Apple Pay & Google Pay](#apple-pay-google-pay)
- [Google Pay (integration for mobile applications)](#google-pay-mobile)
- [Wallets](#wallets)
- [Invoices](#invoices)
- [Heartbeat API](#heartbeat)
- [Bank Response Codes](#bank-response-codes)

---

Epoint system provides possibility to connect payment acceptance to your site. To add a payment
button to your application you need to connect the payment service in your personal cabinet on our
website.

To set up a merchant in our system you will need to provide us with the following information:

- your website address;
- url of the page of successful payment — `success_url`;
- url of the page for displaying information about unsuccessful payment — `error_url`;
- url to send the result of payment — `result_url`.

After checking this information, you will be given access keys: `public_key` — merchant ID in our
system and `private_key` — secret API access key.

## Epoint payment page working principle { #working-principle }

1. It is necessary to form a request to the Epoint API according to the technical documentation.
2. As a result of executing the request, the client will be redirected to the bank's payment page.
3. The client fills in the card details and confirms the payment.
4. In case of successful payment, the customer will be redirected to `success_url`, or `error_url` otherwise.
5. The result of payment execution with payment details will be sent to the `result_url` specified by you.

## Formation of API request { #formation-of-api-request }

To call the Epoint API, you must send the `data` and `signature` parameters using the POST method to
`https://epoint.az/api/1/request` or redirect the user using the POST method to
`https://epoint.az/api/1/checkout`, where:

- `data` — json string with API parameters encoded with base64 function, `base64_encode(json_string)`,
- `signature` — unique signature for each request, `base64_encode(sha1(private_key + data + private_key, 1))`,
- `base64_encode` — returns a string encoded in MIME base64 format,
- `sha1` — returns a hash of a string of 20 characters (raw binary).

### Formation of data and signature

Parameters `json_string` of the api call:

| Parameter              | Required | Type   | Description                                                                               |
| :--------------------- | :------- | :----- | :---------------------------------------------------------------------------------------- |
| `public_key`           | Required | String | The public key is the identifier of the created merchant. For example: `i000000001`       |
| `amount`               | Required | Number | The amount of the payment. For example: 100, 20.50                                        |
| `currency`             | Required | String | Payment currency. Possible values: `AZN`                                                  |
| `language`             | Required | String | Page display language. Possible values: `az`, `en`, `ru`                                  |
| `order_id`             | Required | String | The unique ID of the transaction in your application. Maximum length 255 characters.     |
| `description`          | Optional | String | Payment description. No more than 1000 characters.                                        |
| `is_installment`       | Optional | Number | Parameter defining the payment type. Possible values: `1` (installment) or `0` (standard) |
| `success_redirect_url` | Optional | String | Redirection link in case of successful payment.                                           |
| `error_redirect_url`   | Optional | String | Redirection link in case of unsuccessful payment.                                         |
| `other_attr`           | Optional | Array  | Additional payment options                                                                |

`json_string` example:

```json
{
    "public_key": "i000000001",
    "amount": "30.75",
    "currency": "AZN",
    "description": "test payment",
    "order_id": "1",
    "language": "az"
}
```

To form a signature, concatenate `private_key + data + private_key` and apply
`base64_encode(sha1(sgn_string, 1))` to the resulting string:

```php
$data = base64_encode(json_encode($json_string));
$signature = base64_encode(sha1($private_key . $data . $private_key, 1));
```

### Sending a request

A form must be generated to send a request to the Epoint page:

```html
<form method="POST" action="https://epoint.az/api/1/checkout" accept-charset="utf-8">
    <input type="hidden" name="data" value="{data}" />
    <input type="hidden" name="signature" value="{signature}" />
    <input type="submit" value="Pay" />
</form>
```

Or send the received `data` and `signature` to `https://epoint.az/api/1/request`. In this case a
json string will be returned with the value of `status` (`success|error`), `transaction` and
`redirect_url` to which the user should be redirected to enter card data.

After entering the card data, the user will be redirected to `success_redirect_url` or
`error_redirect_url` depending on the payment status. Along with this, a POST request will be sent to
`result_url` with payment details and transaction status.

## Callback function processing { #callback-function-processing }

After the transaction is processed by Epoint service and the payment status is received from the
bank, a POST request with two parameters `data` and `signature` will be sent to your server
(`result_url`).

To authenticate a request from the Epoint server, you must:

1. Generate a signature on your server side using the `data` received in the response from Epoint and your `private_key`.
2. The received signature should be compared with the one received from Epoint. If the signatures
   match, then you have received a genuine response from the Epoint server unmodified by a third party.

To decode the `data` value you must execute:

```php
$result = json_decode(base64_decode($data), true);
```

Use the Payment Status API function to get the status of a transaction, which can be done at any time.

Payment result parameters:

| Parameter          | Description                                                                                          |
| :----------------- | :--------------------------------------------------------------------------------------------------- |
| `order_id`         | The unique ID of the transaction in your application.                                                |
| `status`           | Operation result: `success` or `failed`                                                              |
| `code`             | Bank response code                                                                                   |
| `message`          | Payment execution status message                                                                     |
| `transaction`      | Epoint service transaction                                                                           |
| `bank_transaction` | Bank payment transaction                                                                             |
| `bank_response`    | Bank's response, with the result of payment processing                                               |
| `operation_code`   | `001` — card registration, `100` — user payment                                                      |
| `rrn`              | Retrieval Reference Number — a unique transaction identifier. Present only for a successful transaction |
| `card_name`        | User name specified on the payment page                                                              |
| `card_mask`        | User card mask in the format: `123456******1234`                                                     |
| `amount`           | Payment amount                                                                                       |
| `other_attr`       | Additional parameters                                                                                |

## Checking payment status { #checking-payment-status }

To invoke Epoint payment status check, you need to pass the `data` and `signature` parameters by POST
method to `https://epoint.az/api/1/get-status`, where:

- `data` — json string with API parameters encoded by function base64, `base64_encode(json_string)`,
- `signature` — unique signature for each request, `base64_encode(sha1(private_key + data + private_key, 1))`.

`json_string` example:

```json
{
    "public_key": "i000000001",
    "transaction": "te000000001"
}
```

Response parameters:

| Parameter          | Description                                                                                          |
| :----------------- | :--------------------------------------------------------------------------------------------------- |
| `status`           | Payment status                                                                                       |
| `code`             | Bank response code                                                                                   |
| `message`          | Payment execution status message                                                                     |
| `transaction`      | Epoint service transaction                                                                           |
| `bank_transaction` | Bank payment transaction                                                                             |
| `bank_response`    | Bank's response, with the result of payment processing                                               |
| `operation_code`   | `001` — card registration, `100` — user payment                                                      |
| `rrn`              | Retrieval Reference Number — a unique transaction identifier. Present only for a successful transaction |
| `card_name`        | Username specified on the payment page                                                               |
| `card_mask`        | User card mask in `123456******1234` format                                                          |
| `amount`           | Payment amount                                                                                       |
| `other_attr`       | Additional parameters                                                                                |

Payment statuses:

- `new` — payment is registered in the Epoint system;
- `success` — successful payment;
- `returned` — the payment has been refunded;
- `error` — an error occurred during payment;
- `server_error` — status check execution error.

## Saving a card to make payments without entering card data { #card-registration }

To call Epoint API you need to send `data` and `signature` parameters by POST method to
`https://epoint.az/api/1/card-registration`.

The `json_string` parameters of the api call:

| Parameter              | Required | Type   | Description                                                                         |
| :--------------------- | :------- | :----- | :---------------------------------------------------------------------------------- |
| `public_key`           | Required | String | The public key is the identifier of the created merchant. For example: `i000000001` |
| `language`             | Required | String | Page display language. Possible values: `az`, `en`, `ru`                            |
| `refund`               | Optional | Number | Card type: `0` — debit card; `1` — payout card.                                     |
| `description`          | Optional | String | Payment description. No more than 1000 characters.                                  |
| `success_redirect_url` | Optional | String | Redirection link in case of successful payment.                                     |
| `error_redirect_url`   | Optional | String | Redirection link in case of unsuccessful payment.                                   |

The request will return a json string with the `status` value (`success|error`) and `redirect_url` to
which the user should be redirected to enter card data, and `card_id` — a unique card identifier
that will be used to make payments.

The client fills in the card information and confirms the payment. In case of success, the client
will be redirected to `success_url`, or `error_url` otherwise (`success_redirect_url` and
`error_redirect_url`, if specified).

After the transaction is processed by Epoint service and the payment status is received from the
bank, a POST request with two parameters `data` and `signature` will be sent to the `result_url`
specified by you. Verify and decode it as described in
[Callback function processing](#callback-function-processing).

Response parameters:

| Parameter          | Description                                                                                          |
| :----------------- | :--------------------------------------------------------------------------------------------------- |
| `status`           | Operation result: `success` or `failed`                                                              |
| `code`             | `000` — successful operation, `500` — error                                                          |
| `message`          | Operation progress status message                                                                    |
| `card_id`          | The unique card identifier that will be used to make the payment                                    |
| `bank_transaction` | Bank payment transaction                                                                             |
| `bank_response`    | Bank's response, with the result of payment processing                                               |
| `operation_code`   | `001` — card registration, `100` — user payment                                                      |
| `rrn`              | Retrieval Reference Number — a unique transaction identifier. Present only for a successful transaction |
| `card_name`        | Username specified on the payment page                                                               |
| `card_mask`        | User card mask in `123456******1234` format                                                          |

## Executing a payment with a saved card { #execute-pay }

To make a payment with a stored card you need to send `data` and `signature` parameters by POST
method to `https://epoint.az/api/1/execute-pay`.

Parameters `json_string` of API call:

| Parameter     | Required | Type   | Description                                                                         |
| :------------ | :------- | :----- | :---------------------------------------------------------------------------------- |
| `public_key`  | Required | String | The public key is the identifier of the created merchant. For example: `i000000001` |
| `language`    | Required | String | Page display language. Possible values: `az`, `en`, `ru`                            |
| `card_id`     | Required | String | The card ID obtained by saving the card.                                            |
| `order_id`    | Required | String | Unique transaction ID in your application. The maximum length is 255 characters.   |
| `amount`      | Required | Number | Amount of payment. For example: 100, 20.50                                          |
| `currency`    | Required | String | Payment currency. Possible values: `AZN`                                            |
| `description` | Optional | String | Description of the payment. Not more than 1000 characters.                          |

After processing the transaction by the Epoint service and receiving the payment status from the
bank, a response will be returned with the following parameters:

| Parameter          | Description                                                                                          |
| :----------------- | :--------------------------------------------------------------------------------------------------- |
| `status`           | Result of a `success` or `failed` operation                                                          |
| `transaction`      | Epoint transaction ID                                                                                |
| `bank_transaction` | Bank payment transaction                                                                             |
| `bank_response`    | Bank response, with the result of payment processing                                                 |
| `rrn`              | Retrieval Reference Number — unique identifier of the transaction. Present only for successful transaction |
| `card_name`        | User name specified on the payment page                                                              |
| `card_mask`        | User card mask in `123456******1234` format                                                          |
| `amount`           | Amount of payment                                                                                    |
| `message`          | Error message                                                                                        |

## Saving the card with the first payment made { #card-registration-with-pay }

If you use this type of payment, you will be paid for the specified amount along with the card
registration. To call the Epoint API, you need to pass the `data` and `signature` parameters by POST
method to `https://epoint.az/api/1/card-registration-with-pay`.

Parameters for the `json_string` call of the API:

| Parameter              | Required | Type   | Description                                                                         |
| :--------------------- | :------- | :----- | :---------------------------------------------------------------------------------- |
| `public_key`           | Required | String | The public key is the identifier of the created merchant. For example: `i000000001` |
| `language`             | Required | String | Page display language. Possible values: `az`, `en`, `ru`                            |
| `order_id`             | Required | String | Unique transaction ID in your application. The maximum length is 255 characters.   |
| `amount`               | Required | Number | Amount of payment. For example: 100, 20.50                                          |
| `currency`             | Required | String | Payment currency. Possible values: `AZN`                                            |
| `description`          | Optional | String | Description of the payment. Not more than 1000 characters.                          |
| `success_redirect_url` | Optional | String | Redirection link in case of successful payment.                                     |
| `error_redirect_url`   | Optional | String | Redirection link in case of failed payment.                                         |

As a result of the request, a json string with the `status` (`success|error`) value, `transaction`
and `redirect_url` to which the user needs to be redirected to enter card data will be returned, and
`card_id` — the unique identifier of the card that will need to be used to make payments.

The customer fills in the card details and confirms payment. If the payment is successful, the client
will be redirected to `success_url`, or `error_url` otherwise (`success_redirect_url` and
`error_redirect_url` if specified).

After processing the transaction, a POST request with `data` and `signature` parameters will be sent
to the `result_url` indicated by you. Verify and decode it as described in
[Callback function processing](#callback-function-processing).

Response parameters:

| Parameter          | Description                                                                                          |
| :----------------- | :--------------------------------------------------------------------------------------------------- |
| `status`           | Result of a `success` or `failed` operation                                                          |
| `code`             | `000` — successful operation                                                                         |
| `card_id`          | Unique identifier of the card you want to use to make the payment                                   |
| `order_id`         | Unique identifier of the payment in your application                                                 |
| `transaction`      | Epoint transaction ID                                                                                |
| `bank_transaction` | Bank payment transaction                                                                             |
| `bank_response`    | Bank response, with the result of payment processing                                                 |
| `operation_code`   | `200` — card registration with the first payment                                                     |
| `rrn`              | Retrieval Reference Number — unique identifier of the transaction. Present only for successful transaction |
| `card_mask`        | User card mask in `123456******1234` format                                                          |
| `card_name`        | Name of the cardholder                                                                               |
| `amount`           | Amount of payment                                                                                    |
| `other_attr`       | Advanced options                                                                                     |

## Request for disbursement of funds { #refund-request }

To request a payout of funds, you must send a POST request to `https://epoint.az/api/1/refund-request`
with the `data` and `signature` parameters.

API call `json_string` parameters:

| Parameter     | Required | Type   | Description                                                                         |
| :------------ | :------- | :----- | :---------------------------------------------------------------------------------- |
| `public_key`  | Required | String | The public key is the identifier of the created merchant. For example: `i000000001` |
| `language`    | Required | String | Page display language. Possible values: `az`, `en`, `ru`                            |
| `card_id`     | Required | String | The card ID received by the card saving method.                                     |
| `order_id`    | Required | String | Unique transaction ID in your application. The maximum length is 255 characters.   |
| `amount`      | Required | Number | Amount of payment. For example: 100, 20.50                                          |
| `currency`    | Required | String | Payment currency. Possible values: `AZN`                                            |
| `description` | Optional | String | Description of the payment. Not more than 1000 characters.                          |

After processing the transaction by the Epoint service and receiving the payment status from the
bank, a response will be returned with the following parameters:

| Parameter          | Description                                                                                          |
| :----------------- | :--------------------------------------------------------------------------------------------------- |
| `status`           | Result of a `success` or `failed` operation                                                          |
| `transaction`      | Epoint transaction ID                                                                                |
| `bank_transaction` | Bank payment transaction                                                                             |
| `bank_response`    | Bank response, with the result of payment processing                                                 |
| `rrn`              | Retrieval Reference Number — unique identifier of the transaction. Present only for successful transaction |
| `card_mask`        | User card mask in `123456******1234` format                                                          |
| `card_name`        | Name of the cardholder                                                                               |
| `amount`           | Amount of payment                                                                                    |
| `message`          | Error message                                                                                        |

## Cancel operations { #reverse }

To cancel the operation, you must send a POST request to `https://epoint.az/api/1/reverse` with the
`data` and `signature` parameters.

API call `json_string` parameters:

| Parameter     | Required | Type   | Description                                                                         |
| :------------ | :------- | :----- | :---------------------------------------------------------------------------------- |
| `public_key`  | Required | String | The public key is the identifier of the created merchant. For example: `i000000001` |
| `language`    | Required | String | Page display language. Possible values: `az`, `en`, `ru`                            |
| `transaction` | Required | String | Epoint transaction ID.                                                              |
| `amount`      | Optional | Number | Amount of payment. For example: 100, 20.50. You can specify a partial refund.       |
| `currency`    | Required | String | Payment currency. Possible values: `AZN`                                            |

After processing, a response will be returned with the following parameters:

| Parameter | Description                                 |
| :-------- | :------------------------------------------ |
| `status`  | Result of a `success` or `failed` operation |
| `message` | Error message                               |

## Split payment request { #split-request }

To create a split payment, you need to pass the `data` and `signature` parameters by POST method to
`https://epoint.az/api/1/split-request`.

Parameters for the `json_string` call of the API:

| Parameter              | Required | Type   | Description                                                                         |
| :--------------------- | :------- | :----- | :---------------------------------------------------------------------------------- |
| `public_key`           | Required | String | The public key is the identifier of the created merchant. For example: `i000000001` |
| `amount`               | Required | Number | Amount of payment. For example: 100, 20.50                                          |
| `split_user`           | Required | String | The ID of the second user in the Epoint system.                                     |
| `split_amount`         | Required | Number | Payment amount for the second user. For example: 100, 20.50                         |
| `currency`             | Required | String | Payment currency. Possible values: `AZN`                                            |
| `language`             | Required | String | Page display language. Possible values: `az`, `en`, `ru`                            |
| `order_id`             | Required | String | Unique transaction ID in your application. The maximum length is 255 characters.   |
| `description`          | Optional | String | Description of the payment. Not more than 1000 characters.                          |
| `success_redirect_url` | Optional | String | Redirection link in case of successful payment.                                     |
| `error_redirect_url`   | Optional | String | Redirection link in case of failed payment.                                         |
| `other_attr`           | Optional | Array  | Additional payment options                                                          |

In this case, a json string will be returned with the `status` (`success|error`) value, `transaction`
and `redirect_url` to which the user must be redirected to enter card data.

After processing the transaction, a POST request with `data` and `signature` parameters will be sent
to your server (`result_url`). Verify and decode it as described in
[Callback function processing](#callback-function-processing).

Please note that the amount paid for the second merchant will only appear on their payment list.

Payment result parameters:

| Parameter          | Description                                                                                          |
| :----------------- | :--------------------------------------------------------------------------------------------------- |
| `order_id`         | Unique transaction ID in your application                                                            |
| `status`           | Result of a `success` or `failed` operation                                                          |
| `code`             | Bank response code                                                                                   |
| `message`          | Payment status message                                                                               |
| `transaction`      | Epoint service transaction                                                                           |
| `bank_transaction` | Bank payment transaction                                                                             |
| `bank_response`    | Bank response, with the result of payment processing                                                 |
| `operation_code`   | `001` — card registration, `100` — user payment                                                      |
| `rrn`              | Retrieval Reference Number — unique identifier of the transaction. Present only for successful transaction |
| `card_name`        | User name specified on the payment page                                                              |
| `card_mask`        | User card mask in `123456******1234` format                                                          |
| `amount`           | Amount of payment                                                                                    |
| `split_amount`     | Payment amount for the second user                                                                   |
| `other_attr`       | Additional parameters                                                                                |

## Executing a split payment with a stored card { #split-execute-pay }

To pay with a saved card, you must send the `data` and `signature` parameters by POST method to
`https://epoint.az/api/1/split-execute-pay`.

API call `json_string` parameters:

| Parameter      | Required | Type   | Description                                                                         |
| :------------- | :------- | :----- | :---------------------------------------------------------------------------------- |
| `public_key`   | Required | String | The public key is the identifier of the created merchant. For example: `i000000001` |
| `language`     | Required | String | Page display language. Possible values: `az`, `en`, `ru`                            |
| `card_id`      | Required | String | The card ID received by the card saving method.                                     |
| `order_id`     | Required | String | Unique transaction ID in your application. The maximum length is 255 characters.   |
| `amount`       | Required | Number | Amount of payment. For example: 100, 20.50                                          |
| `split_user`   | Required | String | The ID of the second user in the Epoint system.                                     |
| `split_amount` | Required | Number | Payment amount for the second user. For example: 100, 20.50                         |
| `currency`     | Required | String | Payment currency. Possible values: `AZN`                                            |
| `description`  | Optional | String | Description of the payment. Not more than 1000 characters.                          |

After processing, a response will be returned with the following parameters:

| Parameter          | Description                                                                                          |
| :----------------- | :--------------------------------------------------------------------------------------------------- |
| `status`           | Result of a `success` or `failed` operation                                                          |
| `transaction`      | Epoint transaction ID                                                                                |
| `bank_transaction` | Bank payment transaction                                                                             |
| `bank_response`    | Bank response, with the result of payment processing                                                 |
| `rrn`              | Retrieval Reference Number — unique identifier of the transaction. Present only for successful transaction |
| `card_mask`        | User card mask in `123456******1234` format                                                          |
| `card_name`        | User name specified on the payment page                                                              |
| `amount`           | Amount of payment                                                                                    |
| `message`          | Error message                                                                                        |
| `split_amount`     | Payment amount for the second user                                                                   |

## Saving the card with the first split payment { #split-card-registration-with-pay }

If you use this type of payment, you will be paid for the specified amount along with the card
registration. To call the Epoint API, you need to pass the `data` and `signature` parameters by POST
method to `https://epoint.az/api/1/split-card-registration-with-pay`.

Parameters for the `json_string` call of the API:

| Parameter              | Required | Type   | Description                                                                         |
| :--------------------- | :------- | :----- | :---------------------------------------------------------------------------------- |
| `public_key`           | Required | String | The public key is the identifier of the created merchant. For example: `i000000001` |
| `language`             | Required | String | Page display language. Possible values: `az`, `en`, `ru`                            |
| `order_id`             | Required | String | Unique transaction ID in your application. The maximum length is 255 characters.   |
| `amount`               | Required | Number | Amount of payment. For example: 100, 20.50                                          |
| `split_user`           | Required | String | The ID of the second user in the Epoint system.                                     |
| `split_amount`         | Required | Number | Payment amount for the second user. For example: 100, 20.50                         |
| `currency`             | Required | String | Payment currency. Possible values: `AZN`                                            |
| `description`          | Optional | String | Description of the payment. Not more than 1000 characters.                          |
| `success_redirect_url` | Optional | String | Redirection link in case of successful payment.                                     |
| `error_redirect_url`   | Optional | String | Redirection link in case of failed payment.                                         |

As a result of the request, a json string with the `status` (`success|error`) value, `transaction`
and `redirect_url` to which the user needs to be redirected to enter card data will be returned, and
`card_id` — the unique identifier of the card that will need to be used to make payments.

The customer fills in the card details and confirms payment. If the payment is successful, the client
will be redirected to `success_url`, or `error_url` otherwise (`success_redirect_url` and
`error_redirect_url` if specified). After processing, a POST request with `data` and `signature`
parameters will be sent to the `result_url` indicated by you.

Response parameters:

| Parameter          | Description                                                                                          |
| :----------------- | :--------------------------------------------------------------------------------------------------- |
| `status`           | Result of a `success` or `failed` operation                                                          |
| `code`             | `000` — successful operation                                                                         |
| `card_id`          | Unique identifier of the card you want to use to make the payment                                   |
| `order_id`         | Unique identifier of the payment in your application                                                 |
| `transaction`      | Epoint transaction ID                                                                                |
| `bank_transaction` | Bank payment transaction                                                                             |
| `bank_response`    | Bank response, with the result of payment processing                                                 |
| `operation_code`   | `200` — card registration with the first payment                                                     |
| `rrn`              | Retrieval Reference Number — unique identifier of the transaction. Present only for successful transaction |
| `card_mask`        | User card mask in `123456******1234` format                                                          |
| `card_name`        | Name of the cardholder                                                                               |
| `amount`           | Payment amount                                                                                       |
| `split_amount`     | Payment amount for the second user                                                                   |
| `other_attr`       | Advanced options                                                                                     |

## Formation of API preauth request { #pre-auth-request }

To call the Epoint API, you must send the `data` and `signature` parameters using the POST method to
`https://epoint.az/api/1/pre-auth-request`. `data` and `signature` are formed the same way as in
[Formation of API request](#formation-of-api-request).

Parameters `json_string` of the api call:

| Parameter              | Required | Type   | Description                                                                         |
| :--------------------- | :------- | :----- | :---------------------------------------------------------------------------------- |
| `public_key`           | Required | String | The public key is the identifier of the created merchant. For example: `i000000001` |
| `amount`               | Required | Number | The amount of the payment. For example: 100, 20.50                                  |
| `currency`             | Required | String | Payment currency. Possible values: `AZN`                                            |
| `language`             | Required | String | Page display language. Possible values: `az`, `en`, `ru`                            |
| `order_id`             | Required | String | The unique ID of the transaction in your application. Maximum length 255 characters. |
| `description`          | Optional | String | Payment description. No more than 1000 characters.                                  |
| `success_redirect_url` | Optional | String | Redirection link in case of successful payment.                                     |
| `error_redirect_url`   | Optional | String | Redirection link in case of unsuccessful payment.                                   |
| `other_attr`           | Optional | Array  | Additional payment options                                                          |

### Sending a preauth request

Send the received `data` and `signature` to `https://epoint.az/api/1/pre-auth-request`. In this case a
json string will be returned with the value of `status` (`success|error`), `transaction` and
`redirect_url` to which user should be redirected to enter card data.

After entering the card data, the user will be redirected to `success_redirect_url` or
`error_redirect_url` depending on the payment status. Along with this, a POST request will be sent to
`result_url` with payment details and transaction status.

### Complete preauth request

After the transaction is processed by Epoint service and the payment status is received from the
bank, you should complete this payment, otherwise it will not be added to your Epoint balance. Until
then, it will be shown on your pending balance in the business panel.

Everything is the same when you want to complete the preauth request, only the body data differs.
Use the endpoint `https://epoint.az/api/1/pre-auth-complete`.

Parameters `json_string` of the api call:

| Parameter     | Required | Type   | Description                                                                                                         |
| :------------ | :------- | :----- | :------------------------------------------------------------------------------------------------------------------ |
| `public_key`  | Required | String | The public key is the identifier of the created merchant. For example: `i000000001`                                 |
| `amount`      | Required | Number | The amount of the payment. For example: 100, 20.50                                                                  |
| `transaction` | Required | String | Transaction id you got from Epoint (see [Callback function processing](#callback-function-processing)), e.g. `te001111111` |

## Apple Pay & Google Pay { #apple-pay-google-pay }

- **Google Pay:** for web integration.
- **Apple Pay:** for both web and app integration.

See also: [Apple Pay & Google Pay (JS SDK)](apple-google-pay.md) — the separate EPoint document for
integrating the buttons directly into your page.

### Create Widget Url (POST Request)

You need to pass the `data` and `signature` to `https://epoint.az/api/1/token/widget`.

| Parameter     | Required | Type   | Description                                                                         |
| :------------ | :------- | :----- | :---------------------------------------------------------------------------------- |
| `public_key`  | Required | String | The public key is the identifier of the created merchant. For example: `i000000001` |
| `amount`      | Required | Number | Amount of payment. For example: 100, 20.50                                          |
| `order_id`    | Required | String | Unique transaction ID in your application. The maximum length is 255 characters.   |
| `description` | Required | String | Description of the payment. Not more than 1000 characters.                          |

```
data = base64_encode(fields_in_json)
```

Fields in json:

```json
{
    "public_key": "your_public_key_on_epoint",
    "amount": 2.50,
    "order_id": "order id generated by your system",
    "description": "Test payment"
}
```

```
signature_string = private_key + data + private_key
signature = base64_encode(sha1(signature_string))
```

Signature string:

```
signature_string = d3hjsl38sd8kdfhbcea0be04eafde9e8e2bad2fb092deyJwdWJsaWNfa2V5IjoiaTAwMDAwMDAwMSIsImFtb3VudCI6IjMwLjc1IiwiY3VycmVuY3kiOiJBWk4iLCJkZXNjcmlwdGlvbiI6InRlc3QgcGF5bWVudCIsIm9yZGVyX2lkIjoiMSJ9d3hjsl38sd8kdfhbcea0be04eafde9e8e2bad2fb092d
```

Example in PHP (Laravel):

```php
$payload = [
    'public_key' => 'public_key',
    'amount' => 2.50,
    'order_id' => 'order id generated by your system',
    'description' => 'Test payment',
];

$data = base64_encode(json_encode($payload));
$private_key = 'your_private_key';
$signature = base64_encode(sha1($private_key . $data . $private_key, 1));

$request = Http::get("https://epoint.az/api/1/token/widget", [
    'data' => $data,
    'signature' => $signature
]);

$response = $request->json();
```

!!! note
    The heading says POST, while the PHP example in the original uses `Http::get`. Integrify sends POST.

Response:

```json
{
    "status": "success",
    "widget_url": "https://epointv1.test/api/1/token/widget/000001"
}
```

When payment is finished inside of the iframe or webview you can listen to the iframe message:

```javascript
window.addEventListener('message', function(event) {
    console.log(event.data); // {status: 'success', payment: {...}}
});
```

## Google Pay (integration for mobile applications) { #google-pay-mobile }

To integrate Google Pay into your mobile application, you must implement a native integration.

1. Implement native integration following the official Google Pay documentation:
   <https://developers.google.com/pay/api/android/overview>
2. Provide us with screenshots showing:
    - the placement of the Google Pay button in your app interface;
    - the appearance of the Google Pay button.
3. After reviewing the submitted materials, we will provide you with a Merchant ID to complete the integration.

## Wallets { #wallets }

The Wallet API provides the following endpoints:

1. `https://epoint.az/api/1/wallet/status` — to retrieve the list of wallets
2. `https://epoint.az/api/1/wallet/payment` — to create a payment using a wallet

### Wallet status

To retrieve the list of wallets, the `public_key` parameter must be sent to
`https://epoint.az/api/1/wallet/status` using the POST method.

| Parameter    | Required | Type   | Description                                                                         |
| :----------- | :------- | :----- | :---------------------------------------------------------------------------------- |
| `public_key` | Required | String | The public key is the identifier of the created merchant. For example: `i000000001` |

!!! note
    The original contains request submission and dynamic button creation examples (HTML/JS) only as
    images; see the original PDF.

### Wallet payment

To create a payment using a wallet, the `data` and `signature` POST parameters must be sent to
`https://epoint.az/api/1/wallet/payment`.

| Parameter     | Required | Type   | Description                                                                         |
| :------------ | :------- | :----- | :---------------------------------------------------------------------------------- |
| `public_key`  | Required | String | The public key is the identifier of the created merchant. For example: `i000000001` |
| `wallet_id`   | Required | String | Selected wallet ID.                                                                 |
| `amount`      | Required | Number | Amount of payment. For example: 100, 20.50                                          |
| `currency`    | Required | String | Payment currency. Possible values: `AZN`                                            |
| `order_id`    | Required | String | Unique transaction ID in your application. The maximum length is 255 characters.   |
| `description` | Optional | String | Description of the payment. Not more than 1000 characters.                          |
| `language`    | Required | String | Page display language. Possible values: `az`, `en`, `ru`                            |

## Invoices { #invoices }

To call the Invoice API, you need to pass the `data` and `signature` parameters using the POST method
to `https://epoint.az/api/1`. The Invoice API has the following endpoints:

1. `/invoices/create` — creating an invoice
2. `/invoices/update` — updating invoice information
3. `/invoices/view` — viewing invoice information
4. `/invoices/list` — viewing information on all invoices
5. `/invoices/send-sms` — sending an SMS to the invoice recipient
6. `/invoices/send-email` — sending an email to the invoice recipient

Creating and updating an invoice has an additional optional parameter `invoice_images[]`, which
contains images in jpg, png, jpeg, svg, bmp formats.

### /invoices/create

| Parameter            | Required | Type   | Description                                                                         |
| :------------------- | :------- | :----- | :---------------------------------------------------------------------------------- |
| `public_key`         | Required | String | The public key is the identifier of the created merchant. For example: `i000000001` |
| `sum`                | Required | Number | The amount of the payment. For example: 100, 20.50                                  |
| `display`            | Required | Number | Display invoice. Possible values: `1` or `0`                                        |
| `save_as_template`   | Required | Number | Save invoice as template. Possible values: `1` or `0`                               |
| `status_installment` | Optional | Number | Enables installment payments. Possible values: `1` or `0`                           |
| `name`               | Optional | String | Name                                                                                |
| `description`        | Optional | String | Payment description. No more than 1000 characters.                                  |
| `phone`              | Optional | String | Phone                                                                               |
| `email`              | Optional | String | Email                                                                               |
| `inn`                | Optional | String | TIN                                                                                 |
| `contract_number`    | Optional | String | Contract number                                                                     |
| `merchant_order_id`  | Optional | String | Order ID                                                                            |
| `period_from`        | Required | Date   | Invoice start date                                                                  |
| `period_to`          | Required | Date   | Invoice end date                                                                    |

### /invoices/update

| Parameter            | Required | Type   | Description                                                                         |
| :------------------- | :------- | :----- | :---------------------------------------------------------------------------------- |
| `public_key`         | Required | String | The public key is the identifier of the created merchant. For example: `i000000001` |
| `id`                 | Required | Number | ID of the invoice being updated                                                     |
| `sum`                | Required | Number | The amount of the payment. For example: 100, 20.50                                  |
| `display`            | Required | Number | Display invoice. Possible values: `1` or `0`                                        |
| `save_as_template`   | Required | Number | Save invoice as template. Possible values: `1` or `0`                               |
| `status_installment` | Optional | Number | Enables installment payments. Possible values: `1` or `0`                           |
| `name`               | Optional | String | Name                                                                                |
| `description`        | Optional | String | Payment description. No more than 1000 characters.                                  |
| `phone`              | Optional | String | Phone                                                                               |
| `email`              | Optional | String | Email                                                                               |
| `inn`                | Optional | String | TIN                                                                                 |
| `contract_number`    | Optional | String | Contract number                                                                     |
| `merchant_order_id`  | Optional | String | Order ID                                                                            |
| `period_from`        | Required | Date   | Invoice start date                                                                  |
| `period_to`          | Required | Date   | Invoice end date                                                                    |

### /invoices/view

| Parameter    | Required | Type   | Description                                                                         |
| :----------- | :------- | :----- | :---------------------------------------------------------------------------------- |
| `public_key` | Required | String | The public key is the identifier of the created merchant. For example: `i000000001` |
| `id`         | Required | Number | Invoice ID                                                                          |

### /invoices/list

| Parameter    | Required | Type   | Description                                                                         |
| :----------- | :------- | :----- | :---------------------------------------------------------------------------------- |
| `public_key` | Required | String | The public key is the identifier of the created merchant. For example: `i000000001` |
| `type`       | Optional | String | Invoice type — `incoming`, `outgoing`, `static`                                     |
| `order`      | Optional | String | Sorting by ascending, descending                                                    |

### /invoices/send-sms

| Parameter    | Required | Type   | Description                                                                         |
| :----------- | :------- | :----- | :---------------------------------------------------------------------------------- |
| `public_key` | Required | String | The public key is the identifier of the created merchant. For example: `i000000001` |
| `id`         | Required | Number | Invoice ID                                                                          |
| `phone`      | Required | String | Phone                                                                               |

### /invoices/send-email

| Parameter    | Required | Type   | Description                                                                         |
| :----------- | :------- | :----- | :---------------------------------------------------------------------------------- |
| `public_key` | Required | String | The public key is the identifier of the created merchant. For example: `i000000001` |
| `id`         | Required | Number | Invoice ID                                                                          |
| `email`      | Required | String | Email                                                                               |

## Heartbeat API { #heartbeat }

To check the service availability, send a GET request to `https://epoint.az/api/heartbeat`.

This endpoint is designed to verify if the service is operational. A successful response with
`status: "ok"` indicates that the service is running properly.

## Bank Response Codes { #bank-response-codes }

| Code  | Description                                                              |
| :---- | :----------------------------------------------------------------------- |
| `000` | Confirmed                                                                |
| `100` | Rejected (general, no comment)                                           |
| `101` | Declined, your card has expired                                          |
| `102` | Rejected, suspected fraud                                                |
| `103` | Rejected, cardholder will contact acquirer                               |
| `104` | Rejected, restricted card                                                |
| `105` | Rejected, card receiver will contact acquirer security                   |
| `106` | Rejected, PIN attempts exceeded                                          |
| `107` | Declined, please contact your card issuer                                |
| `108` | Declined, please refer to card issuer's special terms                    |
| `109` | Rejected, invalid merchant                                               |
| `110` | Rejected, incorrect amount                                               |
| `111` | Rejected, incorrect card number                                          |
| `112` | Rejected, PIN required                                                   |
| `113` | Denied, inappropriate payment                                            |
| `114` | Rejected, no account of the requested type                               |
| `115` | Denied, requested function is not supported                              |
| `116` | Declined, insufficient funds                                             |
| `117` | Rejected, incorrect PIN                                                  |
| `118` | Rejected, no card data                                                   |
| `119` | Rejected, transaction not allowed by cardholder                          |
| `120` | Rejected, transaction not allowed to terminal                            |
| `121` | Declined, withdrawal limit exceeded                                      |
| `122` | Rejected, safety violation                                               |
| `123` | Declined, withdrawal limit exceeded                                      |
| `124` | Rejected, violation of the law                                           |
| `125` | Rejected, card not valid                                                 |
| `126` | Rejected, invalid PIN block                                              |
| `127` | Rejected, PIN length error                                               |
| `128` | Rejected, PIN key synchronization failed                                 |
| `129` | Rejected, suspected fake card                                            |
| `180` | Rejected, at the request of cardholders                                  |
| `200` | Pick-up (general, no comment)                                            |
| `201` | Pick-up, expired card                                                    |
| `202` | Pick-up, suspected fraud                                                 |
| `203` | Pick-up, the card receiver will contact the acquirer                     |
| `204` | Pick-up, restricted card                                                 |
| `205` | Pick-up, the cardholder will contact the acquirer's security department  |
| `206` | Pick-up, PIN limit exceeded                                              |
| `207` | Pick-up, special conditions                                              |
| `208` | Pick-up, lost card                                                       |
| `209` | Pick-up, stolen card                                                     |
| `210` | Pick-up, suspected fake card                                             |
| `300` | Status message: file action successful                                   |
| `301` | Status message: file action not supported by recipient                   |
| `302` | Status message: could not find an entry in the file                      |
| `303` | Status message: duplicate record, old record replaced                    |
| `304` | Status message: file write field edit error                              |
| `305` | Status message: file locked                                              |
| `306` | Status message: file action failed                                       |
| `307` | Status message: file data format error                                   |
| `308` | Status message: duplicate record, new record rejected                    |
| `309` | Status message: unknown file                                             |
| `400` | Accepted (for cancellation)                                              |
| `499` | Confirmed, no original message data                                      |
| `500` | Status message: agreed, in the balance sheet                             |
| `501` | Status message: agreed, out of balance                                   |
| `502` | Status message: amount not agreed, amount provided                       |
| `503` | Status message: amount not available for negotiation                     |
| `504` | Status message: not agreed, amount provided                              |
| `600` | Accepted (for administrative information)                                |
| `601` | Status message: original transaction cannot be tracked                   |
| `602` | Status message: invalid transaction reference number                     |
| `603` | Status message: link number/PANs are incompatible                        |
| `604` | Status message: POS photo not available                                  |
| `605` | Status message: requested item provided                                  |
| `606` | Status message: request failed — required documentation unavailable      |
| `680` | The list is ready                                                        |
| `681` | The list is not ready                                                    |
| `700` | Accepted (for payment collection)                                        |
| `800` | Accepted (for network management)                                        |
| `900` | The recommendation has been taken into account, no financial obligations have been accepted |
| `901` | Recommendations taken into account, financial liability accepted         |
| `902` | Rejection reason message: invalid transaction                            |
| `903` | Status message: re-enter transaction                                     |
| `904` | Rejection reason message: format error                                   |
| `905` | Deviation cause message: acquirer not supported by switch                |
| `906` | Reason for deviation report: process reduction                           |
| `907` | Reason for rejection message: card issuer or switch not in effect        |
| `908` | Rejection reason message: unable to find the destination of the routing transaction |
| `909` | Cause of deviation report: system failure                                |
| `910` | Reason for rejection message: card issuer disabled                       |
| `911` | Reason for rejection message: card issuer expired                        |
| `912` | Reason for rejection message: issuer unavailable                         |
| `913` | Deviation cause message: duplicate transmission                          |
| `914` | Rejection reason message: failed to track original transaction           |
| `915` | Deviation cause message: failure to disable negotiation or checkpoint    |
| `916` | Deviation cause message: MAC incorrect                                   |
| `917` | Reject cause message: MAC key synchronization error                      |
| `918` | Rejection reason message: no binding keys available for use              |
| `919` | Reject cause message: encryption key synchronization error               |
| `920` | Cause of deviation message: software/hardware security error — try again |
| `921` | Deviation cause message: software/hardware security error — no action    |
| `922` | Rejection reason message: incorrect message number sequence              |
| `923` | Status message: in-process query                                         |
| `950` | Reason for rejection message: business agreement violation               |
| `XXX` | Code to be replaced by card status code or stop list reason code         |
| `0Y1` | Confirmed, offline ICC                                                   |
| `0Y3` | Confirmed, offline ICC                                                   |
| `1Q1` | Rejected due to ICC offline mode                                         |
| `1Z1` | Rejected due to ICC offline mode                                         |
| `1Z3` | Rejected due to ICC offline mode                                         |
