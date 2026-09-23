# LSIM SMS API

???+ info
    Bu səhifə LSIM-in rəsmi API sənədlərinin (tək SMS və toplu SMS) Markdown versiyasıdır.
    Kitabxananın bu sorğulara uyğun metodları üçün [LSIM](../index.md) səhifəsinə baxın.

## Single SMS sending API

### Send SMS — HTTP GET

**URL**

```text
http(s)://apps.lsim.az/quicksms/v1/send?login=LOGIN&msisdn=MSISDN&text=MSG_BODY&sender=SENDER&key=KEY[&unicode=UNICODE]
```

**Method:** `GET`

| Parameter | Description |
|---|---|
| `LOGIN` | Your login. |
| `MSISDN` | Subscriber number: country code + operator code + number. Example: `99450XXXXXXX`. |
| `MSG_BODY` | Message text. |
| `SENDER` | Sender title to use when sending the message. |
| `KEY` | `md5((md5(password)) + LOGIN + MSG_BODY + MSISDN + SENDER)` |
| `UNICODE` | Optional. `false` by default; use `true` when `MSG_BODY` contains Unicode characters. |

**Response**

```json
{"successMessage":null,"errorMessage":null,"obj":long,"errorCode":integer}
```

| Field | Description |
|---|---|
| `successMessage` | Success message of the operation. |
| `errorMessage` | Error message if an error occurred. |
| `obj` | Integer representing the transaction ID. |
| `errorCode` | Error code if an error occurred. |

Parameters in square brackets are optional. Use optional parameters without the brackets. Before using Unicode, consult the provider's Unicode documentation.

### Send SMS — HTTP POST

**URL:** `https://apps.lsim.az/quicksms/v1/smssender`

**Method:** `POST`

**Request body**

```json
{
  "login": "LOGIN",
  "key": "md5((md5(password)) + LOGIN + MSG_BODY + MSISDN + SENDER)",
  "msisdn": "99450XXXXXXX",
  "text": "message body",
  "sender": "sender title",
  "scheduled": "NOW",
  "unicode": false
}
```

| Field | Description |
|---|---|
| `login` | Your login. |
| `key` | `md5((md5(password)) + LOGIN + MSG_BODY + MSISDN + SENDER)` |
| `msisdn` | Subscriber number in country-code format. Example: `99450XXXXXXX`. |
| `text` | Message body. |
| `sender` | Sender title to use when sending the message. |
| `scheduled` | `NOW` or a date-time such as `2023-05-19 15:40:05`. Defaults to `NOW`. |
| `unicode` | `false` or `true`. Defaults to `false`. |

**Response**

```json
{"successMessage":null,"errorMessage":null,"obj":long,"errorCode":integer}
```

### Check balance

**URL**

```text
http(s)://apps.lsim.az/quicksms/v1/balance?login=LOGIN&key=KEY
```

**Method:** `GET`

| Parameter | Description |
|---|---|
| `LOGIN` | Your login. |
| `KEY` | `md5((md5(password)) + LOGIN)` |

**Response**

```json
{"successMessage":null,"errorMessage":null,"obj":integer,"errorCode":integer}
```

`obj` contains the current balance.

### Get report — HTTP POST

**URL:** `https://apps.lsim.az/quicksms/v1/smsreporter`

**Method:** `POST`

**Request body**

```json
{
  "login": "LOGIN",
  "transid": "TRANSACTION_ID"
}
```

`transid` is the transaction ID returned after a successful SMS submission.

### Get report — HTTP GET

**URL**

```text
http(s)://apps.lsim.az/quicksms/v1/report?login=LOGIN&trans_id=TRANS_ID
```

**Method:** `GET`

| Parameter | Description |
|---|---|
| `LOGIN` | Your login. |
| `TRANS_ID` | Transaction ID returned after a successful SMS submission. |

### Delivery statuses

| Code | Meaning |
|---:|---|
| `100` | In queue |
| `101` | Delivered |
| `102` | Undelivered |
| `103` | Expired |
| `104` | Rejected |
| `105` | Cancelled |
| `106` | Error |
| `107` | Unknown — contact support |
| `108` | Sent |
| `109` | Black list |

### Error responses

| Code | Meaning |
|---:|---|
| `-100` | Invalid key |
| `-101` | Text exceeds the allowed length |
| `-102` | Wrong number format |
| `-103` | Invalid sender name |
| `-104` | Insufficient balance |
| `-105` | Number is on the blacklist |
| `-106` | Invalid transaction ID |
| `-107` | IP address not allowed |
| `-108` | Invalid hash |
| `-109` | No host |
| `-110` | Reporting limit exceeded |
| `-500` | Internal error |

**Reporting limit:** Since 2019-02-01, reporting is limited per minute. The default TPM limit is 150 transactions. The counter resets at the beginning of each minute.

### Push delivery reports

Delivery reports can be pushed to a URL over HTTP GET if a callback URL is provided in this form:

```text
http[s]://hostname/?trans_id={trans_id}&status={status}
```

`{trans_id}` is replaced with the transaction ID, and `{status}` is replaced with one of the delivery status codes above.

---

## Bulk SMS REST API

**Endpoint:** [https://www.sendsms.az/smxml/api](https://www.sendsms.az/smxml/api)

**Content type:** `application/json`

### 1. Submit a bulk message

Use `isbulk: true` to send the same message to multiple phone numbers.

**Request**

```json
{
  "request": {
    "head": {
      "operation": "submit",
      "login": "your login",
      "password": "your password",
      "controlid": "generated control ID",
      "title": "your sender name",
      "scheduled": "NOW",
      "isbulk": true,
      "bulkmessage": "your message text"
    },
    "body": [
      {"msisdn": "994XXXXXXXXX"},
      {"msisdn": "994XXXXXXXXX"}
    ]
  }
}
```

`controlid` should be generated to prevent multiple submissions of the same task. `scheduled` may be `NOW` or a time in `YYYY-MM-DD HH:mm:ss` format. Phone numbers use the `994XXXXXXXXX` format.

**Response**

```json
{
  "response": {
    "head": {"responsecode": "000"},
    "body": {"taskid": "XXXXXXXX"}
  }
}
```

### 2. Submit individual messages

Use `isbulk: false` when each recipient needs a different message.

**Request**

```json
{
  "request": {
    "head": {
      "operation": "submit",
      "login": "your login",
      "password": "your password",
      "controlid": "generated control ID",
      "title": "your sender name",
      "scheduled": "NOW",
      "isbulk": false
    },
    "body": [
      {
        "msisdn": "994XXXXXXXXX",
        "message": "message text for phone number 1"
      },
      {
        "msisdn": "994XXXXXXXXX",
        "message": "message text for phone number 2"
      }
    ]
  }
}
```

**Response**

```json
{
  "response": {
    "head": {"responsecode": "000"},
    "body": {"taskid": "XXXXXXXX"}
  }
}
```

### 3. Get a message-status report

**Request**

```json
{
  "request": {
    "head": {
      "operation": "report",
      "login": "your login",
      "password": "your password",
      "taskid": "XXXXXXXX"
    }
  }
}
```

**Response**

```json
{
  "response": {
    "head": {"responsecode": "000"},
    "body": {
      "expired": 0,
      "removed": 0,
      "blackList": 0,
      "undelivered": 0,
      "delivered": 1,
      "duplicate": 0,
      "error": 0,
      "send": 0,
      "queue": 0
    }
  }
}
```

### 4. Get a detailed status report

**Request**

```json
{
  "request": {
    "head": {
      "operation": "detailedreport",
      "login": "your login",
      "password": "your password",
      "taskid": "XXXXXXXX"
    }
  }
}
```

**Response**

```json
{
  "response": {
    "head": {"responsecode": "000"},
    "body": [
      {
        "msisdn": "994XXXXXXXXX",
        "message": "message text",
        "status": 2
      }
    ]
  }
}
```

### 5. Get a detailed report with dates

**Request**

```json
{
  "request": {
    "head": {
      "operation": "detailedreportwithdate",
      "login": "your login",
      "password": "your password",
      "taskid": "XXXXXXXX"
    }
  }
}
```

**Response**

```json
{
  "response": {
    "head": {"responsecode": "000"},
    "body": [
      {
        "date": "YYYY-MM-DD HH:mm:ss",
        "msisdn": "994XXXXXXXXX",
        "message": "message text",
        "status": 2
      }
    ]
  }
}
```

### Bulk API status codes

| Code | Meaning |
|---:|---|
| `1` | Message expired |
| `2` | Message successfully delivered |
| `3` | Message undelivered |
| `4` | Message sent |
| `5` | System error |
| `6` | Blacklist |
| `7` | Message is in the queue |
| `8` | Duplicate message |

### 6. Get current SMS balance

**Request**

```json
{
  "request": {
    "head": {
      "operation": "units",
      "login": "your login",
      "password": "your password"
    }
  }
}
```

**Response**

```json
{
  "response": {
    "head": {"responsecode": "000"},
    "body": {"units": 13}
  }
}
```
