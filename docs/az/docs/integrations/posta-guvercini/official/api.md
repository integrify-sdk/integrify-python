# Posta Guvercini SMS Service (v1)

???+ info
    Bu səhifə Posta Güvərçini-nin rəsmi Swagger spesifikasiyasının ([Swagger UI](https://www.poctgoyercini.com/api_json/swagger/ui/index#/)) Markdown versiyasıdır. Sorğu/cavab nümunələri spesifikasiyadakı modellərdən yaradılıb. Uyğunsuzluq olarsa, orijinal mənbə əsas götürülür.

Base URL: `https://www.poctgoyercini.com/api_json`

## Endpoints

### POST `/v1/Sms/Send_1_N`

It is the method that can be used in cases where there is 1 sms text and N recipients.

- If the StatusCode value is other than 200, it means there is an error or validation problem. Request parameters and StatusDescription should be checked.
- Requests should be made in packages containing 800 recipients each.

Content-Type: `application/json`, `text/json`, `application/xml`, `text/xml`, `application/x-www-form-urlencoded`

**Request body** (`RequestSmsSend_1_N`):

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `Message` | string | Yes | Indicates the text of the SMS. It cannot be empty. |
| `Receivers` | string[] | Yes | Indicates the recipients of the SMS. It cannot be empty. Example: `905320000000` |
| `SendDate` | string | No | Indicates the time to send the SMS. When it is blank, sms will be sent immediately. When a valid date is passed, an sms will be sent when the time has passed. Format: yyyyMMdd HH:mm Example: `20200630 15:00` |
| `ExpireDate` | string | No | Indicates the last time the SMS will be attempted to be sent. When it is blank, the time determined by the system will be valid. Format: yyyyMMdd HH:mm Example: `20200701 14:00` |
| `Channel` | string | No | Indicates on which platform (OTP or BULK) the sms will be sent with the originator. Example: `OTP` |
| `Originator` | string | No | It is a field to be used when it is desired to send sms under different originators with a single account. The information to be sent will be given by the customer service representative and is an 11-character value. |
| `Username` | string | Yes | Refers to the username of the account in the Posta Guvercini SMS System. It cannot be empty. |
| `Password` | string | Yes | Refers to the password of the account in the Posta Guvercini SMS System. It cannot be empty. |

```json
{
    "Message": "string",
    "Receivers": [
        "string"
    ],
    "SendDate": "string",
    "ExpireDate": "string",
    "Channel": "string",
    "Originator": "string",
    "Username": "string",
    "Password": "string"
}
```

**Response 200** — OK (`ApiResponse[List[ResponseSmsSendObject]]`):

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `StatusCode` | integer (int32) — 200, 400, 500, 1020, 1030, 1040, 1050, 1060, 1061, 1062, 1063, 1064, 1065, 1066, 1070, 1090, 2060 | No | Indicates the status of the response to the request. |
| `StatusDescription` | string | No | Indicates a detailed explanation of the response to the request made. |
| `Result` | ResponseSmsSendObject[] | No | Indicates the data to be returned in response to the request. |

```json
{
    "StatusCode": 0,
    "StatusDescription": "string",
    "Result": [
        {
            "MessageId": "string",
            "Receiver": "string",
            "Charge": 0
        }
    ]
}
```

### POST `/v1/Sms/Send_N_N`

It is the method that can be used in cases where there is N sms text and N recipients.

- If the StatusCode value is other than 200, it means there is an error or validation problem. Request parameters and StatusDescription should be checked.
- Requests should be made in packages containing 800 recipients each.

Content-Type: `application/json`, `text/json`, `application/xml`, `text/xml`, `application/x-www-form-urlencoded`

**Request body** (`RequestSmsSend_N_N`):

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `Messages` | RequestSmsObject_N_N[] | Yes | It refers to the text of the SMS and its recipients. It cannot be empty. |
| `SendDate` | string | No | Indicates the time to send the SMS. When it is blank, sms will be sent immediately. When a valid date is passed, an sms will be sent when the time has passed. Format: yyyyMMdd HH:mm Example: `20200630 15:00` |
| `ExpireDate` | string | No | Indicates the last time the SMS will be attempted to be sent. When it is blank, the time determined by the system will be valid. Format: yyyyMMdd HH:mm Example: `20200701 14:00` |
| `Channel` | string | No | Indicates on which platform (OTP or BULK) the sms will be sent with the originator. Example: `OTP` |
| `Originator` | string | No | It is a field to be used when it is desired to send sms under different originators with a single account. The information to be sent will be given by the customer service representative and is an 11-character value. |
| `Username` | string | Yes | Refers to the username of the account in the Posta Guvercini SMS System. It cannot be empty. |
| `Password` | string | Yes | Refers to the password of the account in the Posta Guvercini SMS System. It cannot be empty. |

```json
{
    "Messages": [
        {
            "Receiver": "string",
            "Message": "string"
        }
    ],
    "SendDate": "string",
    "ExpireDate": "string",
    "Channel": "string",
    "Originator": "string",
    "Username": "string",
    "Password": "string"
}
```

**Response 200** — OK (`ApiResponse[List[ResponseSmsSendObject]]`):

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `StatusCode` | integer (int32) — 200, 400, 500, 1020, 1030, 1040, 1050, 1060, 1061, 1062, 1063, 1064, 1065, 1066, 1070, 1090, 2060 | No | Indicates the status of the response to the request. |
| `StatusDescription` | string | No | Indicates a detailed explanation of the response to the request made. |
| `Result` | ResponseSmsSendObject[] | No | Indicates the data to be returned in response to the request. |

```json
{
    "StatusCode": 0,
    "StatusDescription": "string",
    "Result": [
        {
            "MessageId": "string",
            "Receiver": "string",
            "Charge": 0
        }
    ]
}
```

### POST `/v1/Sms/Status`

It is the method to checking the status of sent SMSs.

- If the StatusCode value is other than 200, it means there is an error or validation problem. Request parameters and StatusDescription should be checked.
- Requests should be made in packages containing 800 recipients each.

Content-Type: `application/json`, `text/json`, `application/xml`, `text/xml`, `application/x-www-form-urlencoded`

**Request body** (`RequestSmsStatus`):

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `MessageIds` | string[] | Yes | It refers to the message Id in the Posta Guvercini SMS System of Sms. Example: `EZ_43D2B5QC-FD3A-406G-8C5B-D079F24FD400` |
| `Username` | string | Yes | Refers to the username of the account in the Posta Guvercini SMS System. It cannot be empty. |
| `Password` | string | Yes | Refers to the password of the account in the Posta Guvercini SMS System. It cannot be empty. |

```json
{
    "MessageIds": [
        "string"
    ],
    "Username": "string",
    "Password": "string"
}
```

**Response 200** — OK (`ApiResponse[List[ResponseSmsStatusObject]]`):

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `StatusCode` | integer (int32) — 200, 400, 500, 1020, 1030, 1040, 1050, 1060, 1061, 1062, 1063, 1064, 1065, 1066, 1070, 1090, 2060 | No | Indicates the status of the response to the request. |
| `StatusDescription` | string | No | Indicates a detailed explanation of the response to the request made. |
| `Result` | ResponseSmsStatusObject[] | No | Indicates the data to be returned in response to the request. |

```json
{
    "StatusCode": 0,
    "StatusDescription": "string",
    "Result": [
        {
            "MessageId": "string",
            "Receiver": "string",
            "SmsStatus": "string",
            "SmsStatusDescription": "string",
            "IsFinalStatus": "string",
            "StatusTime": "string",
            "SmsCharge": "string"
        }
    ]
}
```

### POST `/v1/Sms/CreditBalance`

It is the method to checking the account balance.

- If the StatusCode value is other than 200, it means there is an error or validation problem. Request parameters and StatusDescription should be checked.

Content-Type: `application/json`, `text/json`, `application/xml`, `text/xml`, `application/x-www-form-urlencoded`

**Request body** (`RequestCreditBalance`):

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `Username` | string | Yes | Refers to the username of the account in the Posta Guvercini SMS System. It cannot be empty. |
| `Password` | string | Yes | Refers to the password of the account in the Posta Guvercini SMS System. It cannot be empty. |

```json
{
    "Username": "string",
    "Password": "string"
}
```

**Response 200** — OK (`ApiResponse[ResponseCreditBalanceObject]`):

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `StatusCode` | integer (int32) — 200, 400, 500, 1020, 1030, 1040, 1050, 1060, 1061, 1062, 1063, 1064, 1065, 1066, 1070, 1090, 2060 | No | Indicates the status of the response to the request. |
| `StatusDescription` | string | No | Indicates a detailed explanation of the response to the request made. |
| `Result` | ResponseCreditBalanceObject | No | Indicates the data to be returned in response to the request. |

```json
{
    "StatusCode": 0,
    "StatusDescription": "string",
    "Result": {
        "Balance": 0
    }
}
```

## Models

### `RequestSmsSend_1_N`

It is a 1_N type SMS sending model.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `Message` | string | Yes | Indicates the text of the SMS. It cannot be empty. |
| `Receivers` | string[] | Yes | Indicates the recipients of the SMS. It cannot be empty. Example: `905320000000` |
| `SendDate` | string | No | Indicates the time to send the SMS. When it is blank, sms will be sent immediately. When a valid date is passed, an sms will be sent when the time has passed. Format: yyyyMMdd HH:mm Example: `20200630 15:00` |
| `ExpireDate` | string | No | Indicates the last time the SMS will be attempted to be sent. When it is blank, the time determined by the system will be valid. Format: yyyyMMdd HH:mm Example: `20200701 14:00` |
| `Channel` | string | No | Indicates on which platform (OTP or BULK) the sms will be sent with the originator. Example: `OTP` |
| `Originator` | string | No | It is a field to be used when it is desired to send sms under different originators with a single account. The information to be sent will be given by the customer service representative and is an 11-character value. |
| `Username` | string | Yes | Refers to the username of the account in the Posta Guvercini SMS System. It cannot be empty. |
| `Password` | string | Yes | Refers to the password of the account in the Posta Guvercini SMS System. It cannot be empty. |

### `ApiResponse[List[ResponseSmsSendObject]]`

Indicates the model to return in response to API requests.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `StatusCode` | integer (int32) — 200, 400, 500, 1020, 1030, 1040, 1050, 1060, 1061, 1062, 1063, 1064, 1065, 1066, 1070, 1090, 2060 | No | Indicates the status of the response to the request. |
| `StatusDescription` | string | No | Indicates a detailed explanation of the response to the request made. |
| `Result` | ResponseSmsSendObject[] | No | Indicates the data to be returned in response to the request. |

### `ResponseSmsSendObject`

It is the model that sms sending methods will return as a reply.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `MessageId` | string | No | It is the unique id information in the Posta Guvercini SMS system of Sms. This id information should be kept if Sms status checking is to be made. |
| `Receiver` | string | No | It is the recipient address sent to the API during the sms sending request. |
| `Charge` | integer (int32) | No | Indicates the estimated number of sms the message will be charged with. |

### `RequestSmsSend_N_N`

It is N_N type SMS sending model.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `Messages` | RequestSmsObject_N_N[] | Yes | It refers to the text of the SMS and its recipients. It cannot be empty. |
| `SendDate` | string | No | Indicates the time to send the SMS. When it is blank, sms will be sent immediately. When a valid date is passed, an sms will be sent when the time has passed. Format: yyyyMMdd HH:mm Example: `20200630 15:00` |
| `ExpireDate` | string | No | Indicates the last time the SMS will be attempted to be sent. When it is blank, the time determined by the system will be valid. Format: yyyyMMdd HH:mm Example: `20200701 14:00` |
| `Channel` | string | No | Indicates on which platform (OTP or BULK) the sms will be sent with the originator. Example: `OTP` |
| `Originator` | string | No | It is a field to be used when it is desired to send sms under different originators with a single account. The information to be sent will be given by the customer service representative and is an 11-character value. |
| `Username` | string | Yes | Refers to the username of the account in the Posta Guvercini SMS System. It cannot be empty. |
| `Password` | string | Yes | Refers to the password of the account in the Posta Guvercini SMS System. It cannot be empty. |

### `RequestSmsObject_N_N`

It is a N_N type SMS sending model.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `Receiver` | string | Yes | Indicates the recipients of the SMS. It cannot be empty. Example: `905320000000` |
| `Message` | string | Yes | Indicates the text of the SMS. It cannot be empty. |

### `RequestSmsStatus`

It is sms status checking model.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `MessageIds` | string[] | Yes | It refers to the message Id in the Posta Guvercini SMS System of Sms. Example: `EZ_43D2B5QC-FD3A-406G-8C5B-D079F24FD400` |
| `Username` | string | Yes | Refers to the username of the account in the Posta Guvercini SMS System. It cannot be empty. |
| `Password` | string | Yes | Refers to the password of the account in the Posta Guvercini SMS System. It cannot be empty. |

### `ApiResponse[List[ResponseSmsStatusObject]]`

Indicates the model to return in response to API requests.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `StatusCode` | integer (int32) — 200, 400, 500, 1020, 1030, 1040, 1050, 1060, 1061, 1062, 1063, 1064, 1065, 1066, 1070, 1090, 2060 | No | Indicates the status of the response to the request. |
| `StatusDescription` | string | No | Indicates a detailed explanation of the response to the request made. |
| `Result` | ResponseSmsStatusObject[] | No | Indicates the data to be returned in response to the request. |

### `ResponseSmsStatusObject`

It is the model that sms status methods will return as a response.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `MessageId` | string | No | It is the unique id information in the Posta Guvercini SMS system of Sms. |
| `Receiver` | string | No | It refers to the recipient of the sms. |
| `SmsStatus` | string | No | Indicates the status of the sms. |
| `SmsStatusDescription` | string | No | It refers to the description of the status of the sms. |
| `IsFinalStatus` | string | No | Indicates whether the SMS has reached its final state or not. If the Sms has reached its final status, its status will no longer be updated. Inquiries should no longer be made for this sms. 0: Final state not yet reached 1: Final state reached. No more inquiries should be made. |
| `StatusTime` | string | No | If the sms has reached the recipient (Status=400), it means the time of arrival. In other cases, it refers to the time when the last status change of the sms was made. Format: yyyyMMdd HH:mm Example: `20200630 16:08` |
| `SmsCharge` | string | No | Indicates the number of sms charged. If IsFinalStatus = 1, valid data is returned. |

### `RequestCreditBalance`

It is sms status checking model.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `Username` | string | Yes | Refers to the username of the account in the Posta Guvercini SMS System. It cannot be empty. |
| `Password` | string | Yes | Refers to the password of the account in the Posta Guvercini SMS System. It cannot be empty. |

### `ApiResponse[ResponseCreditBalanceObject]`

Indicates the model to return in response to API requests.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `StatusCode` | integer (int32) — 200, 400, 500, 1020, 1030, 1040, 1050, 1060, 1061, 1062, 1063, 1064, 1065, 1066, 1070, 1090, 2060 | No | Indicates the status of the response to the request. |
| `StatusDescription` | string | No | Indicates a detailed explanation of the response to the request made. |
| `Result` | ResponseCreditBalanceObject | No | Indicates the data to be returned in response to the request. |

### `ResponseCreditBalanceObject`

It is the model that sms status methods will return as a response.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `Balance` | integer (int32) | No | Indicates the number of sms charged. If IsFinalStatus = 1, valid data is returned. |
