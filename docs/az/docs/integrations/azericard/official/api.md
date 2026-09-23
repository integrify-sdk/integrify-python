# Azericard E-Commerce API

???+ info
    Bu səhifə Azericard-ın rəsmi developer sənədinin ([developer.azericard.com/en](https://developer.azericard.com/en), ingiliscə) Markdown versiyasıdır. Uyğunsuzluq olarsa, orijinal mənbə əsas götürülür.

## 1 Overview

This manual is intended for use by developers responsible for the merchant payment gateway interface. It describes the interface that merchant systems use to process credit card based e-commerce transactions using the standard CGI/WWW forms posting method. This interface transparently supports various cardholder authentication protocols such as 3D-Secure and Secure Code as well as legacy unauthenticated SSL commerce transactions.

### 1.1 Transaction flow scenario

Below diagram describes payment process between client (card holder), merchant and processing center (Azericard)

![](https://developer.azericard.com/paymentFlow.svg)

Gateway validates the incoming message and requests a reversal of the pending or completed transaction from the Way4 card system.

## 2 E-Commerce integration { #integration }

To make payment merchant first of all should fill the below listed parameters and send data to:  
TRTYPE=1 should be sent in the POST request for authorization TRTYPE=0 should be sent in the first POST request for preauthorization, and TRTYPE=21 should be sent to confirm the order after successful return information.

https://testmpi.3dsecure.az/cgi-bin/cgi\_link

| Fields | Size | Description |
| --- | --- | --- |
| AMOUNT | 1-12 | Order total amount in float format with decimal point separator |
| CURRENCY | 03 | Order currency: Consist of 3 symbols |
| ORDER | 6-32 | Merchant order ID, numeric. Last 6 digits used as a system trace audit number, which must be unique within a day for the terminal id |
| DESC | 1-50 | Order description |
| MERCH\_NAME | 1-50 | Merchant name (recognizable by cardholder) |
| MERCH\_URL | 1-250 | Merchant primary web site URL |
| TERMINAL | 8 | Merchant Terminal ID assigned by bank |
| EMAIL | 80 | E-mail address for notification. If this field is present Gateway may send transaction results notification to specified e-mail address. |
| TRTYPE | 1 | Transaction type = 0 (Pre-Authorization),Transaction type = 1 (Authorization) |
| COUNTRY | 02 | Merchant shop 2-character country code. Must be provided if merchant system is located in a country other than the gateway server\`s country. |
| MERCH\_GMT | 1-5 | Merchant UTC/GMT time zone offset (e.g. –3). Must be provided if merchant system is located in a time zone other than the gateway server\`s time zone. |
| BACKREF | 1-250 | Merchant URL for posting authorization result. |
| TIMESTAMP | 14 | Merchant transaction timestamp in GMT: YYYYMMDDHHMMSS. Timestamp difference between merchant server and e-Gateway server must not exceed 1 hour, otherwise e-Gateway will reject this transaction. |
| NONCE | 1-64 | Merchant nonce. Must be filled with 8-32 unpredictable random bytes in hexadecimal format. Must be present if MAC is used. |
| LANG | 2 | Language type |
| P\_SIGN | 1-256 | Merchant MAC in hexadecimal form. |
| NAME | 2-45 | Customer's name (as indicated on the card) |
| M\_INFO | 35000 | Must be a Base64-encoded string of JSON-formatted "parameter": "value data". |

Below is an example of data prepared for the M\_INFO field:

"M\_INFO"="ewoiYnJvd3NlclNjcmVlbkhlaWdodCI6IjE5MjAiLAoiYnJvd3NlclNjcmVlbldpZHRoIjoiMTA4MCIsCiJicm93c2VyVFoiOiIwIiwKIm1vYmlsZVBob25lIiA6eyAiY2MiOiI5OTQiLCAic3Vic2NyaWJlciI6IjU1Nzc3Nzc3Nzc3IiB9Cn0=",

Decoded format: {"browserScreenHeight":"1920","browserScreenWidth":"1080","browserTZ":"0","mobilePhone":{"cc":"994","subscriber":"5077777777"}}

M\_INFO Parameters description:

browserScreenHeight - Total height of the Cardholder’s screen in pixels.

browserScreenWidth - Total width of the Cardholder’s screen in pixels.in pixels.

browserTZ - Time difference between UTC time and the Cardholder browser local time, in minutes.

mobilePhone - The mobile phone number provided by the Cardholder.

Request body should be like below:

"AMOUNT"="xx", "CURRENCY"="AZN", "ORDER"="xxxxxxxxxxxx", "DESC"="xxxxxxxxxxx xxxx", "MERCH\_NAME"="xxxxx.xxx", "MERCH\_URL"="https://xxxxxxxxxx.xx/xxxx", "MERCH\_GMT"="+4", "TERMINAL"="xxxxxxxxx", "EMAIL"="xxxxx@xxxxx.xx", "TRTYPE"="x", "COUNTRY"="AZ", "TIMESTAMP"="xxxxxxxxxxxxxx", "NONCE"="xxxxxxxxxxxxxxx", "BACKREF"="https://xxxxxxxxxxx/xxxxxxxxxxx/xxxxxx", "LANG=xx", "NAME"="xxxxxx", "M\_INFO"="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", "P\_SIGN"="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

### Response format

| Fields | Size | Description |
| --- | --- | --- |
| TERMINAL | 8 | Echo from the request |
| TRTYPE | 2 | Echo from the request |
| ORDER | 6-32 | Echo from the request |
| AMOUNT | 12 | Amount authorized. Usually, will be equal to original amount plus acquirer’s fee. |
| CURRENCY | 3 | Echo from the request |
| ACTION | 1 | EGateway action code |
|  |  | §0 – Transaction successfully completed |
|  |  | §1 – Duplicate transaction detected |
|  |  | §2 – Transaction declined  |
|  |  | §3 – Transaction processing error |
|  |  | §6 – Repeat of a declined transaction |
|  |  | §7 - Repeat of a transaction with an authentication error |
|  |  | §8 - Repeat of a transaction that terminated without a response |
| RC | 02 | Transaction response code (ISO-8583 Field 39) |
| APPROVAL | 06 | Client bank’s approval code (ISO-8583 Field 38). Can be empty if not provided by card management system. |
| RRN | 12 | Merchant bank’s retrieval reference number (ISO-8583 Field 37) |
| INT\_REF | 1-128 | E-Commerce gateway internal reference number |
| TIMESTAMP | 14 | E-Commerce gateway timestamp in GMT: YYYYMMDDHHMMSS |
| NONCE | 1-64 | E-Commerce gateway nonce value. Will be filled with 8-32 unpredictable random bytes in hexadecimal format. Will be present if MAC is used. |
| P\_SIGN | 1-256 | E-Commerce gateway MAC (Message Authentication Code) in hexadecimal form. Will be present if MAC is used. |

### 2.1 Payment confirmation and refund

Following the rules of P\_Sign generation should check callback P\_Sign with MPI public key. İf the payment is successful, to complete and refund the payment should send below fields depending on trtype (trtype = 21 – checkout, trtype = 22 – online reversal, trtype = 24 – offline reversal). [Link](#callbackCalc)

https://testmpi.3dsecure.az/cgi-bin/cgi\_link

#### 2.1.1 TRTYPE = 21

**Note:**The following data must be posted to confirm the payment. The sequence of calculating the P\_SIGN value of the request is indicated in the link.[Link](#trtype21)

| Fields | Size | Order description |
| --- | --- | --- |
| AMOUNT | 1-12 | Order total amount in float format with decimal point separator |
| CURRENCY | 03 | Order currency: Consist of 3 symbols |
| ORDER | 6-32 | Merchant order ID, numeric. Last 6 digits used as a system trace audit number, which must be unique within a day for the terminal id |
| RRN | 1 | Retrieval reference number from authorization response. |
| INT\_REF | 1-32 | Internal reference number from authorization response. |
| TERMINAL | 8 | Merchant Terminal ID assigned by bank |
| TRTYPE | 2 | Transaction type = 21 (Sales completion) |
| TIMESTAMP | 14 | Merchant transaction timestamp in GMT: YYYYMMDDHHMMSS. Timestamp difference between merchant server and e-Gateway server must not exceed 1 hour, otherwise e-Gateway will reject this transaction. |
| NONCE | 16 | Merchant nonce. Must be filled with 8-32 unpredictable random bytes in hexadecimal format. Must be present if MAC is used. |
| P\_SIGN | 1-256 | Merchant MAC in hexadecimal form. |

Request body should be like below:

"AMOUNT"="xx", "CURRENCY"="AZN", "ORDER"="xxxxxxxxxxxx", "RRN"="xxxxxxxxx", "INT\_REF"="xxxxxxxxx", "TERMINAL"="xxxxxxxxx", "TRTYPE"="x", "TIMESTAMP"="xxxxxxxxxxxxxx", "NONCE"="xxxxxxxxxxxxxxx", "LANG=xx", "P\_SIGN"="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

#### 2.1.2 TRTYPE = 22

**Note:**The following data must be posted for a refund. The sequence of calculation of the P\_SIGN value of the request is mentioned in the link.[Link](#trtype22)

| Fields | Size | Order description |
| --- | --- | --- |
| AMOUNT | 1-12 | Order total amount in float format with decimal point separator |
| CURRENCY | 03 | Order currency: Consist of 3 symbols |
| ORDER | 6-32 | Merchant order ID, numeric. Last 6 digits used as a system trace audit number, which must be unique within a day for the terminal id |
| RRN | 1 | Retrieval reference number from authorization response. |
| INT\_REF | 1-32 | Internal reference number from authorization response. |
| TERMINAL | 8 | Merchant Terminal ID assigned by bank |
| TRTYPE | 2 | Transaction type = 22 (Online reversal) |
| TIMESTAMP | 14 | Merchant transaction timestamp in GMT: YYYYMMDDHHMMSS. Timestamp difference between merchant server and e-Gateway server must not exceed 1 hour, otherwise e-Gateway will reject this transaction. |
| NONCE | 16 | Merchant nonce. Must be filled with 8-32 unpredictable random bytes in hexadecimal format. Must be present if MAC is used. |
| P\_SIGN | 1-256 | Merchant MAC in hexadecimal form. |

Request body should be like below:

"AMOUNT"="xx", "CURRENCY"="AZN", "ORDER"="xxxxxxxxxxxx", "RRN"="xxxxxxxxx", "INT\_REF"="xxxxxxxxx", "TERMINAL"="xxxxxxxxx", "TRTYPE"="x", "TIMESTAMP"="xxxxxxxxxxxxxx", "NONCE"="xxxxxxxxxxxxxxx", "LANG=xx", "P\_SIGN"="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

#### 2.1.3 TRTYPE = 24

**Note:**The following data must be posted for a refund. The sequence of calculation of the P\_SIGN value of the request is mentioned in the link.[Link](#trtype24)

| Fields | Size | Order description |
| --- | --- | --- |
| AMOUNT | 1-12 | Order total amount in float format with decimal point separator |
| CURRENCY | 03 | Order currency: Consist of 3 symbols |
| ORDER | 6-32 | Merchant order ID, numeric. Last 6 digits used as a system trace audit number, which must be unique within a day for the terminal id |
| RRN | 1 | Retrieval reference number from authorization response. |
| INT\_REF | 1-32 | Internal reference number from authorization response. |
| TERMINAL | 8 | Merchant Terminal ID assigned by bank |
| TRTYPE | 2 | Transaction type = 24 (Offline reversal) |
| TIMESTAMP | 14 | Merchant transaction timestamp in GMT: YYYYMMDDHHMMSS. Timestamp difference between merchant server and e-Gateway server must not exceed 1 hour, otherwise e-Gateway will reject this transaction. |
| NONCE | 16 | Merchant nonce. Must be filled with 8-32 unpredictable random bytes in hexadecimal format. Must be present if MAC is used. |
| P\_SIGN | 1-256 | Merchant MAC in hexadecimal form. |

Request body should be like below:

"AMOUNT"="xx", "CURRENCY"="AZN", "ORDER"="xxxxxxxxxxxx", "RRN"="xxxxxxxxx", "INT\_REF"="xxxxxxxxx", "TERMINAL"="xxxxxxxxx", "TRTYPE"="x", "TIMESTAMP"="xxxxxxxxxxxxxx", "NONCE"="xxxxxxxxxxxxxxx", "LANG=xx", "P\_SIGN"="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

### 2.2 P-Sign generation

MAC is calculated over all fields generated by the merchant system as defined in corresponding format tables (visible and hidden fields generated by the merchant system) except the MAC field (“P\_SIGN”) itself.

In order to generate or verify the message authentication field, the merchant system must assemble a MAC source string; all field values from the format tables are prefixed with the decimal field length in ASCII and concatenated in a specified order.

The MAC source string for example is:

81720078010511.48142003010515302116IT Books. Qty: 2

After the MAC source string is assembled, the merchant system must apply a cryptographic algorithm to generate the message authentication code.

The merchant system must implement SHA256 sign, add MAC source to sign and crypts with private key in hexadecimal format.

Merchant system implemented by special algorithm fully responsible for the secure storage and usage of corresponding cryptographic keys. An effective key length must be at least 2048 bits for RSA algorithm.

The order of fields in test terminal (terminal id: The terminal will be presented during the test) is as follows:

#### 2.2.1 TRTYPE = 0, TRTYPE = 1

| Fields | Size | Description |
| --- | --- | --- |
| AMOUNT | 1-12 | Order total amount in float format with decimal point separator |
| CURRENCY | 03 | Order currency: Consist of 3 symbols |
| TERMINAL | 8 | Merchant Terminal ID assigned by bank |
| TRTYPE | 1 | Transaction type = 1 (Finance document) |
| TIMESTAMP | 14 | Merchant transaction timestamp in GMT: YYYYMMDDHHMMSS. Timestamp difference between merchant server and e-Gateway server must not exceed 1 hour, otherwise e-Gateway will reject this transaction. |
| NONCE | 1-64 | Merchant nonce. Must be filled with 8-32 unpredictable random bytes in hexadecimal format. Must be present if MAC is used. |
| MERCH\_URL | 1-250 | Merchant primary web site URL |

#### 2.2.2 TRTYPE = 21 { #trtype21 }

| Fields | Size | Description |
| --- | --- | --- |
| AMOUNT | 1-12 | Order total amount in float format with decimal point separator |
| CURRENCY | 03 | Order currency: Consist of 3 symbols |
| TERMINAL | 8 | Merchant Terminal ID assigned by bank |
| TRTYPE | 2 | Transaction type = 21 (Sales completion) |
| ORDER | 6-32 | Merchant order ID, numeric. Last 6 digits used as a system trace audit number, which must be unique within a day for the terminal id |
| RRN | 1 | Retrieval reference number from authorization response. |
| INT\_REF | 1-32 | Internal reference number from authorization response. |

#### 2.2.3 TRTYPE = 22 { #trtype22 }

| Fields | Size | Description |
| --- | --- | --- |
| AMOUNT | 1-12 | Order total amount in float format with decimal point separator |
| CURRENCY | 03 | Order currency: Consist of 3 symbols |
| TERMINAL | 8 | Merchant Terminal ID assigned by bank |
| TRTYPE | 2 | Transaction type = 22 (Online reversal) |
| ORDER | 6-32 | Merchant order ID, numeric. Last 6 digits used as a system trace audit number, which must be unique within a day for the terminal id |
| RRN | 1 | Retrieval reference number from authorization response. |
| INT\_REF | 1-32 | Internal reference number from authorization response. |

#### 2.2.4 TRTYPE = 24 { #trtype24 }

| Fields | Size | Description |
| --- | --- | --- |
| AMOUNT | 1-12 | Order total amount in float format with decimal point separator |
| CURRENCY | 03 | Order currency: Consist of 3 symbols |
| TERMINAL | 8 | Merchant Terminal ID assigned by bank |
| TRTYPE | 2 | Transaction type = 24 (Offline reversal) |
| ORDER | 6-32 | Merchant order ID, numeric. Last 6 digits used as a system trace audit number, which must be unique within a day for the terminal id |
| RRN | 1 | Retrieval reference number from authorization response. |
| INT\_REF | 1-32 | Internal reference number from authorization response. |

### 2.3 S2S integration

**Note:** The indicated type of integration is valid only for merchants with a valid PCI DSS certificate.  
TRTYPE=1 should be sent in the POST request for authorization TRTYPE=0 should be sent in the first POST request for preauthorization, and TRTYPE=21 should be sent to confirm the order after successful return information.

HTTP POST request should be sent to Azericard e-commerce gateway at URL:

https://testmpi.3dsecure.az/cgi-bin/cgi\_link

#### Request format

| Fields | Size | Description |
| --- | --- | --- |
| AMOUNT | 1-12 | Order total amount in float format with decimal point separator |
| CURRENCY | 03 | Order currency: Consist of 3 symbols |
| ORDER | 6-32 | Merchant order ID, numeric. Last 6 digits used as a system trace audit number, which must be unique within a day for the terminal id |
| DESC | 1-50 | Order description |
| MERCH\_NAME | 1-50 | Merchant name (recognizable by cardholder) |
| MERCH\_URL | 1-250 | Merchant primary web site URL |
| TERMINAL | 8 | Merchant Terminal ID assigned by bank |
| EMAIL | 80 | E-mail address for notification. If this field is present Gateway may send transaction results notification to specified e-mail address. |
| TRTYPE | 1 | Transaction type = 0 (Pre-Authorization),Transaction type = 1 (Authorization) |
| COUNTRY | 02 | Merchant shop 2-character country code. Must be provided if merchant system is located in a country other than the gateway server\`s country. |
| MERCH\_GMT | 1-5 | Merchant UTC/GMT time zone offset (e.g. –3). Must be provided if merchant system is located in a time zone other than the gateway server\`s time zone. |
| BACKREF | 1-250 | Merchant URL for posting authorization result. |
| TIMESTAMP | 14 | Merchant transaction timestamp in GMT: YYYYMMDDHHMMSS. Timestamp difference between merchant server and e-Gateway server must not exceed 1 hour, otherwise e-Gateway will reject this transaction. |
| NONCE | 1-64 | Merchant nonce. Must be filled with 8-32 unpredictable random bytes in hexadecimal format. Must be present if MAC is used. |
| LANG | 2 | Language type |
| P\_SIGN | 1-256 | Merchant MAC in hexadecimal form. |
| NAME | 2-45 | Customer's name (as indicated on the card) |
| M\_INFO | 35000 | Must be a Base64-encoded string of JSON-formatted "parameter": "value data". |
| MERCH\_3D\_TERM\_URL |  | MerchantURL where will return Cres response from client ACS. |
| CARD | 9-19 | Card number (Primary account number). |
| EXP | 02 | Card expiration month (Numeric 2 digit value). |
| EXP\_YEAR | 02 | Card expiration year (Numeric 2 digit value: 20XX) |
| CVC2 | 03 | Card verification code(last three digits on the signature panel). |
| CVC2\_RC | 01 | CVC2 reason code. values:  
value="1" -CVC2 is present  
value="0" -CVC2 is not provided  
value="2"-CVC2 is illegible |

Below is an example of data prepared for the M\_INFO field:

"M\_INFO"="ewoiYnJvd3NlclNjcmVlbkhlaWdodCI6IjE5MjAiLAoiYnJvd3NlclNjcmVlbldpZHRoIjoiMTA4MCIsCiJicm93c2VyVFoiOiIwIiwKIm1vYmlsZVBob25lIiA6eyAiY2MiOiI5OTQiLCAic3Vic2NyaWJlciI6IjU1Nzc3Nzc3Nzc3IiB9Cn0=",

Decoded format:  
{"browserIP":"0.0.0.0","browserScreenHeight":"1920","browserScreenWidth":"1080","browserTZ":"0","mobilePhone":{"cc":"994","subscriber":"5077777777"}}

M\_INFO Parameters description:

browserScreenHeight - Total height of the Cardholder’s screen in pixels.

browserScreenWidth - Total width of the Cardholder’s screen in pixels.in pixels.

browserTZ - Time difference between UTC time and the Cardholder browser local time, in minutes.

mobilePhone - The mobile phone number provided by the Cardholder.

Request body should be like below:

"AMOUNT"="xx", "CURRENCY"="AZN", "ORDER"="xxxxxxxxxxxx", "DESC"="xxxxxxxxxxx xxxx", "MERCH\_NAME"="xxxxx.xxx", "MERCH\_URL"="https://xxxxxxxxxx.xx/xxxx", "MERCH\_GMT"="+4", "TERMINAL"="xxxxxxxxx", "EMAIL"="xxxxx@xxxxx.xx", "TRTYPE"="x", "COUNTRY"="AZ", "TIMESTAMP"="xxxxxxxxxxxxxx", "NONCE"="xxxxxxxxxxxxxxx", "BACKREF"="https://xxxxxxxxxxx/xxxxxxxxxxx/xxxxxx", "M\_INFO"="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", "P\_SIGN"="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", "MERCH\_3D\_TERM\_URL"="xxxxxxxxxxxxxxxxxxxxxxxx", "CARD"="xxxxxxxxxxxxxxxxxxx", "EXP"="xx", "EXP\_YEAR"="xx", "CVC2"="xxx", "CVC2\_RC"="x",

#### Response format

| Fields | Size | Description |
| --- | --- | --- |
| TERMINAL | 8 | Echo from the request |
| TRTYPE | 2 | Echo from the request |
| ORDER | 6-20 | Echo from the request |
| AMOUNT | 1-12 | Amount authorized. Usually, will be equal to original amount plus acquirer’s fee. |
| CURRENCY | 3 | Echo from the request |
| ACTION | 1 | EGateway action code |
|  |  | §0 – Transaction successfully completed |
|  |  | §1 – Duplicate transaction detected |
|  |  | §2 – Transaction declined  |
|  |  | §3 – Transaction processing error |
| RC | 02 | Transaction response code (ISO-8583 Field 39) |
| APPROVAL | 06 | Client bank’s approval code (ISO-8583 Field 38). Can be empty if not provided by card management system. |
| RRN | 12 | Merchant bank’s retrieval reference number (ISO-8583 Field 37) |
| INT\_REF | 1-32 | E-Commerce gateway internal reference number |
| TIMESTAMP | 14 | E-Commerce gateway timestamp in GMT: YYYYMMDDHHMMSS |
| NONCE | 1-64 | E-Commerce gateway nonce value. Will be filled with 8-32 unpredictable random bytes in hexadecimal format. Will be present if MAC is used. |
| P\_SIGN | 1-256 | E-Commerce gateway MAC (Message Authentication Code) in hexadecimal form. Will be present if MAC is used. |

1\. If the card was enrolled on 3DSecure and card supports 3DS method, additional card authentication will take place before Authorization Response, as follows.

1.1 If client card supports ThreeDSMethod; as an answer to the post request to below URL testmpi will return an XML response.

https://testmpi.3dsecure.az/cgi-bin/cgi\_link

Example:

`<?xml version="1.0" encoding="utf-8" ?> <response> <action> https://testacs.3dsecure.az/way4acs/threeDSMethodURL</action>; <threeDSMethodData> eyJ0aHJlZURTTWV0aG9kTm90aWZpY2F0aW9uVVJMIjoiaHR0cHM6Ly90ZXN0bXBpLjNkc2VjdXJlLmF6L2NnaS1iaW4vY2dpX2xpbmsiLC J0aHJlZURTU2VydmVyVHJhbnNJRCI6IjZkYTllMDk4LWFmZGEtNGY5NC1iMTMxLTAxZGNhZDA4NDgzOCJ9 </threeDSMethodData> <threeDSMethodState>C</threeDSMethodState> <url>https://testmpi.3dsecure.az/cgi-in/cgi_link</url>; </response>`

2\. At the next step `threeDSMethodData` value should be posted to url specified in `<action>` field above as in the following example.

Note: in header must send `"content-type"="application/x-www-form-urlencoded”` parameter.

https://testacs.3dsecure.az/way4acs/threeDSMethodURL

`threeDSMethodData:eyJ0aHJlZURTTWV0aG9kTm90aWZpY2F0aW9uVVJMIjoiaHR0cHM6Ly90ZXN0bXBpLjNkc2VjdXJlLmF6L2NnaS1iaW4vY2dpX2xpbmsiLC J0aHJlZURTU2VydmVyVHJhbnNJRCI6IjZkYTllMDk4LWFmZGEtNGY5NC1iMTMxLTAxZGNhZDA4NDgzOCJ9`

Answer to this request should be ignored, if http=200 (ok)

Example of postman request.

![threeDSMethodData](https://developer.azericard.com/i/image1.png)

3\. At the next step threeDSMethodData value and `threeDSMethodState=C` should be Posted to below URL as in the following example

https://testmpi.3dsecure.az/cgi-bin/cgi\_link

in header must send `"content-type"="application/x-www-form-urlencoded”` parameter.

`threeDSMethodData:eyJ0aHJlZURTTWV0aG9kTm90aWZpY2F0aW9uVVJMIjoiaHR0cHM6Ly90ZXN 0bXBpLjNkc2VjdXJlLmF6L2NnaS1iaW4vY2dpX2xpbmsiLCJ0aHJlZURTU2VydmVyVHJhbnNJRCI6Ijc5Yz Y3ZWY4LTZhN2ItNDBlOS04ZDdjLWE5N2I5MzcyM2RmMiJ9   threeDSMethodState:C`

Example screen from postman below

![threeDSMethodState](https://developer.azericard.com/i/image2.png)

If answer “WAITING” received, previous message should be resend until “CONTINUE” answer received or 10 seconds of such cycle exceeded. After receiving “CONTINUE” message or 10 sec time exceeded, whichever is the first, the same as above message with threeDSMethodState=N should be sent to URL:https://testmpi.3dsecure.az/cgi-bin/cgi\_link as in the following example to proceed, example is below:

https://testmpi.3dsecure.az/cgi-bin/cgi\_link

in header must send `"content-type"="application/x-www-form-urlencoded”` parameter.

`threeDSMethodData:eyJ0aHJlZURTTWV0aG9kTm90aWZpY2F0aW9uVVJMIjoiaHR0cHM6Ly90ZXN 0bXBpLjNkc 2VjdXJlLmF6L2NnaS1iaW4vY2dpX2xpbmsiLCJ0aHJlZURTU2VydmVyVHJhbnNJRCI6Ijc5YzY3ZWY4LTZ hN2ItNDBlOS04ZDdjLWE5N2I5MzcyM2RmMiJ9   threeDSMethodState:N`

4\. Response to this message will be an issuer ACS html page which should be answered to original customer session. Merchant must open mentioned HTML ACS page to customer and customer will be redirected to his issuer ACS system.

5\. Client authenticates itself on this page. After client is authenticated, issuer ACS will post url specified in **Authorization Request** at MERCH\_3D\_TERM\_URL field (the merchant url). This post will contain CRES authentication response. Example of such post below.

Example:

`"cres":"eyJtZXNzYWdlVHlwZSI6IkNSZXMiLCJtZXNzYWdlVmVyc2lvbiI6IjIuMS4wIiwidGhyZWVEU1Nlc nZlclRyYW5zSUQiOiI3YTQ1NzhlNC1kNjk5LTQwN2EtODg2MS0zNDIwNTk0ZTk0MjkiLCJhY3NUcmFuc 0lEIjoiMGVhNzU3ODUtOTQ5OC00MjQ3LWEzYzctYzViY2FlMDk2NzU5IiwiY2hhbGxlbmdlQ29tcGxld GlvbkluZCI6IlkiLCJ0cmFuc1N0YXR1cyI6IlkifQ",   "threeDSSessionData":"MDdhYTNiNDQtYzY0OC00YThiLThiOTktOTBiNDM3ZDc2MTI5"`

1.5. This received Cres data response “as is” should be send (post) to MPI

URL:

https://testmpi.3dsecure.az/cgi-bin/cgi\_link

Example:in POST cres request in header must be `content-type=x-www-form-urlencoded` parameter

`cres:eyJtZXNzYWdlVHlwZSI6IkNSZXMiLCJtZXNzYWdlVmVyc2lvbiI6IjIuMS4wIiwidGhyZWVEU1Nlc nZlclRyYW5zSUQiOiI3YTQ1NzhlNC1kNjk5LTQwN2EtODg2MS0zNDIwNTk0ZTk0MjkiLCJhY3NUcmFuc 0lEIjoiMGVhNzU3ODUtOTQ5OC00MjQ3LWEzYzctYzViY2FlMDk2NzU5IiwiY2hhbGxlbmdlQ29tcGxld GlvbkluZCI6IlkiLCJ0cmFuc1N0YXR1cyI6IlkifQ   threeDSSessionData:MDdhYTNiNDQtYzY0OC00YThiLThiOTktOTBiNDM3ZDc2MTI5`

Example screen from postman below

![threeDSSessionData](https://developer.azericard.com/i/image3.png)

6\. As an answer to this MPI will send Authorization Response.  
Example of response will contain below data’s

`<?xml version="1.0" encoding="utf-8" ?> <response> <desc>Approved</desc> <terminal>1111111</terminal> <trtype>1</trtype> (can be 0) <order>20230621052514</order> <amount>1.00</amount> <currency>944</currency> <action>0</action> <rc>00</rc> <approval>111111</approval> <rrn>317276406077</rrn> <intref>0A7E21C778330DF2</intref> <timestamp>20230621052514</timestamp> <nonce>7fdc0caafb113590</nonce> <p_sign>5dc32febbca757927aa353b526515b30a3ef4bf87a5ce24e4e01ad6292954560e97b3a30283fd034d3e5b6d21 ec72ce2a37db27a476ff970f7e5ae694b39b637101643f220f701f7918295d06c287c46ec8e6aa7e48e2d560c49 f76a09ccd0aa4404dd889e98c474f162f7154c95e5bd9c16333c4f0088f8a732c48fc902de9d9b782a7a07cd0aa 1a1d07852b1306b8185160cdc36d665e65ac9b63ca44700933a1e0bfba9624f08d86a4259fecf3a020d7ff254a0 7468881e05e3fe08f11624f5d235341965cc272e4360a27a0bbe8ad868952a0b4072b4a4239704712fa033989 35ab2527517672948c4ef2d4cb5a8e4e2381f7e3ef9d8c6ccb85d154b08fd </p_sign> </response>`

2\. If the card was enrolled on 3DSecure and card does not support 3DS method, additional card authentication will take place before Authorization Response, as follows.

1\. Response to Authorization Request message will be an issuer ACS html page should be answered to original customer session, customer will be redirected to his issuer ACS system.

Example response of issuer ACS html form below. Merchant should open mentioned page to client.

`<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN"> <HTML> <HEAD> </HEAD> <BODY ONLOAD="javascript:OnLoadEvent();"> <FORM ACTION="https://testacs1.3dsecure.az/way4acs/brw/challenge?id=67a0c292-2e65-461d-901b-04d72717d294" METHOD="post" NAME="ThreeDform" target="_self"> <input name="creq" type="hidden" value="eyJtZXNzYWdlVHlwZSI6IkNSZXEiLCJtZXNzYWdlVmVyc2lvbiI6IjIuMS4wIiwidGhyZWVEU1NlcnZlclRyYW5zSUQiOiI2N2EwYzI5Mi0yZTY1LTQ2MWQtOTAxYi0wNGQ3MjcxN2QyOTQiLCJhY3NUcmFuc0lEIjoiNTZmNjE4NzEtMTUwZC00NjIyLTk4MjgtZjZlYmY0MWRhNjhhIiwiY2hhbGxlbmdlV2luZG93U2l6ZSI6IjA1In0"> <input name="threeDSSessionData" type="hidden" value="NjdhMGMyOTItMmU2NS00NjFkLTkwMWItMDRkNzI3MTdkMjk0"> </FORM> <SCRIPT> function OnLoadEvent () { document.forms[0].submit(); } </SCRIPT> </BODY> </HTML>`

2\. Client authenticates itself on this page.

3\. After client authenticated, issuer ACS will post url specified in **Authorization Request** at MERCH\_3D\_TERM\_URL field. This post will contain CRES authentication response. Example of such post below.

Example:

`"cres":"eyJtZXNzYWdlVHlwZSI6IkNSZXMiLCJtZXNzYWdlVmVyc2lvbiI6IjIuMS4wIiwidGhyZWVEU1Nlc nZlclRyYW5zSUQiOiI3YTQ1NzhlNC1kNjk5LTQwN2EtODg2MS0zNDIwNTk0ZTk0MjkiLCJhY3NUcmFuc 0lEIjoiMGVhNzU3ODUtOTQ5OC00MjQ3LWEzYzctYzViY2FlMDk2NzU5IiwiY2hhbGxlbmdlQ29tcGxld GlvbkluZCI6IlkiLCJ0cmFuc1N0YXR1cyI6IlkifQ",   "threeDSSessionData":"MDdhYTNiNDQtYzY0OC00YThiLThiOTktOTBiNDM3ZDc2MTI5"`

This received Cres data response “as is” should be send (post) to MPI:

https://testmpi.3dsecure.az/cgi-bin/cgi\_link

Example:in POST cres request in header must be `content-type=x-www-form-urlencoded` parameter

`cres:eyJtZXNzYWdlVHlwZSI6IkNSZXMiLCJtZXNzYWdlVmVyc2lvbiI6IjIuMS4wIiwidGhyZWVEU1Nlc nZlclRyYW5zSUQiOiI3YTQ1NzhlNC1kNjk5LTQwN2EtODg2MS0zNDIwNTk0ZTk0MjkiLCJhY3NUcmFuc 0lEIjoiMGVhNzU3ODUtOTQ5OC00MjQ3LWEzYzctYzViY2FlMDk2NzU5IiwiY2hhbGxlbmdlQ29tcGxld GlvbkluZCI6IlkiLCJ0cmFuc1N0YXR1cyI6IlkifQ   threeDSSessionData:MDdhYTNiNDQtYzY0OC00YThiLThiOTktOTBiNDM3ZDc2MTI5`

![threeDSSessionData](https://developer.azericard.com/i/image3.png)

4.As an answer to this MPI will send Authorization Response.Example of response will contain below data’s

`<?xml version="1.0" encoding="utf-8" ?> <response> <desc>Approved</desc> <terminal>1111111</terminal> <trtype>1</trtype> (can be 0) <order>20230621052514</order> <amount>1.00</amount> <currency>944</currency> <action>0</action> <rc>00</rc> <approval>111111</approval> <rrn>317276406077</rrn> <intref>0A7E21C778330DF2</intref> <timestamp>20230621052514</timestamp> <nonce>7fdc0caafb113590</nonce> <p_sign>5dc32febbca757927aa353b526515b30a3ef4bf87a5ce24e4e01ad6292954560e97b3a30283fd034d3e5b6d21 ec72ce2a37db27a476ff970f7e5ae694b39b637101643f220f701f7918295d06c287c46ec8e6aa7e48e2d560c49 f76a09ccd0aa4404dd889e98c474f162f7154c95e5bd9c16333c4f0088f8a732c48fc902de9d9b782a7a07cd0aa 1a1d07852b1306b8185160cdc36d665e65ac9b63ca44700933a1e0bfba9624f08d86a4259fecf3a020d7ff254a0 7468881e05e3fe08f11624f5d235341965cc272e4360a27a0bbe8ad868952a0b4072b4a4239704712fa033989 35ab2527517672948c4ef2d4cb5a8e4e2381f7e3ef9d8c6ccb85d154b08fd </p_sign> </response>`

3\. If the card supports frictionless authentication. During the authorization the Frictionless Flow does not require further Cardholder interaction to achieve a successful authentication and complete the 3-D Secure authentication process.

3.1. As an answer to this MPI will send Authorization Response.Example of response will contain below data’s

`<?xml version="1.0" encoding="utf-8" ?> <response> <desc>Approved</desc> <terminal>1111111</terminal> <trtype>1</trtype> (can be 0) <order>20230621052514</order> <amount>1.00</amount> <currency>944</currency> <action>0</action> <rc>00</rc> <approval>111111</approval> <rrn>317276406077</rrn> <intref>0A7E21C778330DF2</intref> <timestamp>20230621052514</timestamp> <nonce>7fdc0caafb113590</nonce> <p_sign>5dc32febbca757927aa353b526515b30a3ef4bf87a5ce24e4e01ad6292954560e97b3a30283fd034d3e5b6d21 ec72ce2a37db27a476ff970f7e5ae694b39b637101643f220f701f7918295d06c287c46ec8e6aa7e48e2d560c49 f76a09ccd0aa4404dd889e98c474f162f7154c95e5bd9c16333c4f0088f8a732c48fc902de9d9b782a7a07cd0aa 1a1d07852b1306b8185160cdc36d665e65ac9b63ca44700933a1e0bfba9624f08d86a4259fecf3a020d7ff254a0 7468881e05e3fe08f11624f5d235341965cc272e4360a27a0bbe8ad868952a0b4072b4a4239704712fa033989 35ab2527517672948c4ef2d4cb5a8e4e2381f7e3ef9d8c6ccb85d154b08fd </p_sign> </response>`

4\. If card supports 3DS method and not enrolled on 3D service need to do 1.1, 1.2, 1.3 actions and As an answer to this MPI for Authorization will response with Authentication failed message like below.  
Example of response will contain below data’s

`<?xml version="1.0" encoding="utf-8" ?> <response> <desc>Authentication failed</desc> <terminal>1111111</terminal> <trtype>1</trtype> (can be 0) <order>20230621052514</order> <amount>1.00</amount> <currency>944</currency> <action>3</action> <rc>-19</rc> <approval></approval> <rrn></rrn> <intref></intref> <timestamp>20230621052514</timestamp> <nonce>7fdc0caafb113590</nonce> <p_sign>5dc32febbca757927aa353b526515b30a3ef4bf87a5ce24e4e01ad6292954560e97b3a30283fd034d3e5b6d21 ec72ce2a37db27a476ff970f7e5ae694b39b637101643f220f701f7918295d06c287c46ec8e6aa7e48e2d560c49 f76a09ccd0aa4404dd889e98c474f162f7154c95e5bd9c16333c4f0088f8a732c48fc902de9d9b782a7a07cd0aa 1a1d07852b1306b8185160cdc36d665e65ac9b63ca44700933a1e0bfba9624f08d86a4259fecf3a020d7ff254a0 7468881e05e3fe08f11624f5d235341965cc272e4360a27a0bbe8ad868952a0b4072b4a4239704712fa033989 35ab2527517672948c4ef2d4cb5a8e4e2381f7e3ef9d8c6ccb85d154b08fd </p_sign> </response>`

5\. If card doesn’t supports 3DS method and not enrolled on 3D. During the Authorization MPI will send Authorization Response like Authentication failed message like below.  
Example of response will contain below data’s

`<?xml version="1.0" encoding="utf-8" ?> <response> <desc>Authentication failed</desc> <terminal>1111111</terminal> <trtype>1</trtype> (can be 0) <order>20230621052514</order> <amount>1.00</amount> <currency>944</currency> <action>3</action> <rc>-19</rc> <approval></approval> <rrn></rrn> <intref></intref> <timestamp>20230621052514</timestamp> <nonce>7fdc0caafb113590</nonce> <p_sign>5dc32febbca757927aa353b526515b30a3ef4bf87a5ce24e4e01ad6292954560e97b3a30283fd034d3e5b6d21 ec72ce2a37db27a476ff970f7e5ae694b39b637101643f220f701f7918295d06c287c46ec8e6aa7e48e2d560c49 f76a09ccd0aa4404dd889e98c474f162f7154c95e5bd9c16333c4f0088f8a732c48fc902de9d9b782a7a07cd0aa 1a1d07852b1306b8185160cdc36d665e65ac9b63ca44700933a1e0bfba9624f08d86a4259fecf3a020d7ff254a0 7468881e05e3fe08f11624f5d235341965cc272e4360a27a0bbe8ad868952a0b4072b4a4239704712fa033989 35ab2527517672948c4ef2d4cb5a8e4e2381f7e3ef9d8c6ccb85d154b08fd </p_sign> </response>`

**Note:**Payment confirmation, refund and calculation of P\_SIGN value are same as in E-commerce integration method.

## 3 Installment

During the installation service, in addition to the parameters shown above [(Switch link)](#integration) , the following parameter is posted to the appropriate url address. To perform installment operations, the ACQ\_INST\_PAYIN parameter is posted in the query and the INST\_ALL\* (\*=3,6,9,12,18,24,27,30) installment numbers are sent according to the number of installments.

### For installment

| Fields | Size | Description |
| --- | --- | --- |
| ACQ\_INST\_PAYIN | 9 - 10 | INST\_ALL\* (\*=3,6,9,12,18,24,27,30) |

### Non installment

| Fields | Size | Description |
| --- | --- | --- |
| ACQ\_INST\_PAYIN | 9-10 | INST\_ALL\* (\*= X) |

### Response format

Success response: `<install>INST_ALL*</install>`

| Kod | Xəta | Description |
| --- | --- | --- |
| U1 | Empty instalment configuration | No entries (no rows at all) in the BinRangeFile |
| U2 | Invalid instalment configuration | Number of fields in the BinRangeFile is not equal to 3 |
| U3 | Card BIN range not found | No BIN range matched the provided PAN |
| U4 | No instalments configured for the BIN range | BIN range matched, but no instalments configured for the range |
| U5 | No instalments configured for the terminal | Terminal configuration AcqInstTypeList is empty |
| U6 | Selected instalment not configured for the terminal |  |
| U7 | Selected instalment not configured for the BIN range |  |

## 4 Test data

This is the test environment, where you can do test transactions and simulate results (approved, declined). It’s usage is recommended while you are developing and testing your integration. In test environment you will use test keys generated by AZC and test data placed on website.

### 4.1 Test card

For transaction with test card number you should use the following card data.

<table class="Content_table__1qEsQ"><tbody><tr class="Content_trResponse__2Lqwt"><td class="Content_tdResponse__2IPey">PAN</td><td class="Content_tdResponse__2IPey">4127208104942601</td></tr><tr class="Content_trResponse__2Lqwt"><td class="Content_tdResponse__2IPey">EXP_MONTH</td><td class="Content_tdResponse__2IPey">05</td></tr><tr class="Content_trResponse__2Lqwt"><td class="Content_tdResponse__2IPey">EXP_YEAR</td><td class="Content_tdResponse__2IPey">31</td></tr><tr class="Content_trResponse__2Lqwt"><td class="Content_tdResponse__2IPey">CVV</td><td class="Content_tdResponse__2IPey">796</td></tr><tr class="Content_trResponse__2Lqwt"><td class="Content_tdResponse__2IPey">SMS One Time Password</td><td class="Content_tdResponse__2IPey">1111</td></tr></tbody></table>

<table class="Content_table__1qEsQ"><tbody><tr class="Content_trResponse__2Lqwt"><td class="Content_tdResponse__2IPey">PAN</td><td class="Content_tdResponse__2IPey">5167513332880780</td></tr><tr class="Content_trResponse__2Lqwt"><td class="Content_tdResponse__2IPey">EXP_MONTH</td><td class="Content_tdResponse__2IPey">05</td></tr><tr class="Content_trResponse__2Lqwt"><td class="Content_tdResponse__2IPey">EXP_YEAR</td><td class="Content_tdResponse__2IPey">31</td></tr><tr class="Content_trResponse__2Lqwt"><td class="Content_tdResponse__2IPey">CVV</td><td class="Content_tdResponse__2IPey">609</td></tr><tr class="Content_trResponse__2Lqwt"><td class="Content_tdResponse__2IPey">SMS One Time Password</td><td class="Content_tdResponse__2IPey">1111</td></tr></tbody></table>

<table class="Content_table__1qEsQ"><tbody><tr class="Content_trResponse__2Lqwt"><td class="Content_tdResponse__2IPey">PAN</td><td class="Content_tdResponse__2IPey">4127214121630724</td></tr><tr class="Content_trResponse__2Lqwt"><td class="Content_tdResponse__2IPey">EXP_MONTH</td><td class="Content_tdResponse__2IPey">04</td></tr><tr class="Content_trResponse__2Lqwt"><td class="Content_tdResponse__2IPey">EXP_YEAR</td><td class="Content_tdResponse__2IPey">31</td></tr><tr class="Content_trResponse__2Lqwt"><td class="Content_tdResponse__2IPey">CVV</td><td class="Content_tdResponse__2IPey">536</td></tr><tr class="Content_trResponse__2Lqwt"><td class="Content_tdResponse__2IPey">SMS One Time Password</td><td class="Content_tdResponse__2IPey">1111</td></tr><tr class="Content_trResponse__2Lqwt"><td class="Content_tdResponse__2IPey">Card Name</td><td class="Content_tdResponse__2IPey">Tam Card Visa (ABB müştərilərinə)</td></tr></tbody></table>

### 4.2 Test terminal

For transaction with test terminal you should use the following terminal id.

<table class="Content_table__1qEsQ"><tbody><tr class="Content_trResponse__2Lqwt"><td class="Content_tdResponse__2IPey">Terminal ID</td><td class="Content_tdResponse__2IPey">It will be presented during integration</td></tr></tbody></table>

### 4.3 Test keys

In the test environment, you will be presented with 1 Azericard public key (Public RSA). Generation of keys is mentioned in paragraph 4. [Link](#generateKeys)

<table class="Content_table__1qEsQ"><tbody><tr class="Content_trResponse__2Lqwt"><td class="Content_tdResponse__2IPey">MPI Public Key</td><td class="Content_tdResponse__2IPey">It will be presented during integration</td></tr></tbody></table>

#### Calculation of callback P_SIGN { #callbackCalc }

The following variables are used to calculate callback P\_SIGN. Additionally, if the value of any of the specified variables is sent empty, then a - (hyphen) sign is added instead of that value, and its length is ignored in the P\_SIGN part.

| Fields | Size | Description |
| --- | --- | --- |
| AMOUNT | 1-12 | Order total amount in float format with decimal point separator |
| TERMINAL | 8 | Merchant Terminal ID assigned by bank |
| APPROVAL | 6 | Client bank’s approval code (ISO-8583 Field 38). Can be empty if not provided by card management system. |
| RRN | 12 | Merchant bank’s retrieval reference number (ISO-8583 Field 37) |
| INT\_REF | 1-32 | Internal reference number from authorization response. |

## 5 Key generation process { #generateKeys }

In production system merchant should generate and give his public key to Azericard and Azericard will give his public key to merchant. Private keys must be private for each side (merchant/Azericard). Generating Public and Private RSA Keys from Merchant side:

To perform the following actions for Windows or Linux, you must have OpenSSL installed on your system.

### 5.1 Generating the private key(Windows)

1\. Open the Command Prompt:

Start > Programs > Accessories > Command Prompt.

2\. Navigate to the following folder:

C:\\Program Files\\ListManager\\tclweb\\bin\\certs

3\. Type the following:

openssl genrsa -out merchant\_name\_private\_key.pem 2048

4\. Press ENTER.

The private key is generated and saved in a file named 'merchant\_name\_private\_key .pem' located in the same folder.

### 5.2 Generating the public key(Windows)

1\. At the command prompt, type the following:

openssl rsa -in merchant\_name\_private\_key.pem -pubout -out merchant\_name\_public\_key.pem

2\. Press ENTER.

The public key saved in a file named merchant\_name\_public\_key .pem located in the same folder.

### 5.3 Generating the private key(Linux)

1\. Open the Terminal.

2\. Type the following:

openssl genrsa -out merchant\_name\_private\_key.pem 2048

4\. Press ENTER.

The private key is generated and saved in a file named 'merchant\_name\_private\_key .pem' located in the same folder.

### 5.4 Generating the public key(Linux)

1\. Open the Terminal.

2\. Type the following:

openssl rsa -in merchant\_name\_private\_key.pem -pubout -out merchant\_name\_public\_key.pem

3\. Press ENTER.

The public key is saved in a file named merchant\_name\_public\_keypem located in the same folder.

## 6 Card storage

Above during card storage service ([Link](#integration)) in addition to the specified parameters, the parameter mentioned below is posted to the corresponding url address

[https://testmpi.3dsecure.az/token/cgi\_link](https://testmpi.3dsecure.az/token/cgi_link)

### 6.1 Card save integration

| Fields | Size | Description |
| --- | --- | --- |
| TOKEN\_ACTION | 8 | REGISTER  
  
The parameter must be posted when storing the token |
| MERCH\_TRAN\_STATE | 1 | Authorization initiation indicator  
value = 'S' |

When storing the card, the merchant must post the TOKEN\_ACTION=REGISTER parameter in the request. To save the card, the merchant must make a successful payment, even if it is a minimal amount. After the payment is completed, the following parameters will be sent to the callback address provided by the merchant.

"AMOUNT"="xx", "CURRENCY"="AZN", "ORDER"="xxxxxxxxxxxx", "ACTION"="xxxxx", "RC"="xxx", "APPROVAL"="xxx", "RRN"="xxx", "INT\_REF"="xxxxxxxx", "EMAIL"="xxxxxxxx", "CARD"="xxxxxxxx", "TOKEN"="xxxxxxxx", "TERMINAL"="xxxxxxxxx", "TRTYPE"="x", "TIMESTAMP"="xxxxxxxxxxxxxx", "NONCE"="xxxxxxxxxxxxxxx", "P\_SIGN"="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

### 6.2 Payment by stored card

| Fields | Size | Description |
| --- | --- | --- |
| TOKEN | 28 | TOKEN parameter of saved card |

When paying with a stored card, the merchant must post the TOKEN parameter received in the request callback. After the payment is completed, the following parameters will be sent to the callback address provided by the merchant.  
NOTE: The TOKEN\_ACTION=REGISTER parameter should not be posted for saved card payments.

"AMOUNT"="xx", "CURRENCY"="AZN", "ORDER"="xxxxxxxxxxxx", "ACTION"="xxxxx", "RC"="xxx", "APPROVAL"="xxx", "RRN"="xxx", "INT\_REF"="xxxxxxxx", "EMAIL"="xxxxxxxx", "CARD"="xxxxxxxx", "TOKEN"="xxxxxxxx", "TERMINAL"="xxxxxxxxx", "TRTYPE"="x", "TIMESTAMP"="xxxxxxxxxxxxxx", "NONCE"="xxxxxxxxxxxxxxx", "P\_SIGN"="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

### 6.3 CIT Payment

| Fields | Size | Description |
| --- | --- | --- |
| MERCH\_TRAN\_STATE | 1 | Authorization initiation indicator  
value = 'C' |
| TOKEN | 28 | Value returned to the merchant during card storage |

When storing the card, the merchant must post the TOKEN\_ACTION=REGISTER parameter in the request. To save the card, the merchant must make a successful payment, even if it is a minimal amount. After the payment is completed, the following parameters will be sent to the callback address provided by the merchant.

"AMOUNT"="xx", "CURRENCY"="AZN", "ORDER"="xxxxxxxxxxxx", "ACTION"="xxxxx", "RC"="xxx", "APPROVAL"="xxx", "RRN"="xxx", "INT\_REF"="xxxxxxxx", "EMAIL"="xxxxxxxx", "CARD"="xxxxxxxx", "TOKEN"="xxxxxxxx", "TERMINAL"="xxxxxxxxx", "TRTYPE"="x", "TIMESTAMP"="xxxxxxxxxxxxxx", "NONCE"="xxxxxxxxxxxxxxx", "P\_SIGN"="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

## 7 Recurring

Above during card storage service ([Link](#integration)) in addition to the specified parameters, the parameter mentioned below is posted to the corresponding url address

[https://testmpi.3dsecure.az/token/cgi\_link](https://testmpi.3dsecure.az/token/cgi_link)

### 7.1 MIT Unscheduled – Cardsave

| Fields | Size | Description |
| --- | --- | --- |
| MERCH\_TRAN\_STATE | 1 | Authorization initiation indicator  
value = 'S' |
| TOKEN\_ACTION | 8 | REGISTER |
| MERCH\_RN\_ID | 16 | Merchant nonce. Must be generated using 8–32 random bytes and represented in hexadecimal format. Must be considered when MAC is used. |
| MIT\_AGREEMENT | 1 | Indicates whether a payment agreement exists with the cardholder for Merchant-Initiated Transactions.  
value = 'N' |
| TRTYPE | 1 | Transaction type = 1 (Finance document) |

After sending the request, the following response is returned. Save the EXT\_NET\_REF parameters. For this, you must specify EXT\_NET\_REF. If the EXT\_NET\_REF value is not returned in the response to the card storage request, then there is no need to send the parameter during payment

"AMOUNT"="xx", "CURRENCY"="AZN", "ORDER"="xxxxxxxxxxxx", "ACTION"="xxxxx", "RC"="xxx", "APPROVAL"="xxx", "RRN"="xxx", "INT\_REF"="xxxxxxxx", "EMAIL"="xxxxxxxx", "CARD"="xxxxxxxx", "TOKEN"="xxxxxxxx", "TERMINAL"="xxxxxxxxx", "TRTYPE"="x", "TIMESTAMP"="xxxxxxxxxxxxxx", "NONCE"="xxxxxxxxxxxxxxx", "P\_SIGN"="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", "EXT\_NET\_REF"="xxxxxxxxxxxxxxxxxxxxx"

### 7.2 MIT Unscheduled – Payment

| Fields | Size | Description |
| --- | --- | --- |
| MERCH\_TRAN\_STATE | 1 | Authorization initiation indicator  
value = 'M' |
| EXT\_NET\_REF | 6-32 | Value returned to the merchant during card storage |
| MERCH\_RN\_ID | 16 | Merchant nonce. Must be generated using 8–32 random bytes and represented in hexadecimal format. Must be considered when MAC is used. |
| TOKEN | 28 | Value returned to the merchant during card storage |
| TRTYPE | 1 | Transaction type = 1 (Finance document) |

### 7.3 MIT Scheduled – Cardsave

| Fields | Size | Description |
| --- | --- | --- |
| MERCH\_TRAN\_STATE | 1 | Authorization initiation indicator  
value = 'S' |
| TOKEN\_ACTION | 8 | REGISTER |
| MERCH\_RN\_ID | 16 | Merchant nonce. Must be generated using 8–32 random bytes and represented in hexadecimal format. Must be considered when MAC is used. |
| MIT\_AGREEMENT | 1 | Indicates whether a payment agreement exists with the cardholder for Merchant-Initiated Transactions.  
value = 'Y' |
| TRTYPE | 1 | Transaction type = 1 (Finance document) |
| RECUR\_FREQ | 2 | Minimum time interval between authorizations (charges). Numeric format. (Example: 11) |
| RECUR\_EXP | 8 | Expiration date of the subscription in YYYYMMDD format. The subscription may last up to 1 year from the card registration date. |

After sending the request, the following response is returned. Save the EXT\_NET\_REF parameters. For this, you must specify EXT\_NET\_REF. If the EXT\_NET\_REF value is not returned in the response to the card storage request, then there is no need to send the parameter during payment

"AMOUNT"="xx", "CURRENCY"="AZN", "ORDER"="xxxxxxxxxxxx", "ACTION"="xxxxx", "RC"="xxx", "APPROVAL"="xxx", "RRN"="xxx", "INT\_REF"="xxxxxxxx", "EMAIL"="xxxxxxxx", "CARD"="xxxxxxxx", "TOKEN"="xxxxxxxx", "TERMINAL"="xxxxxxxxx", "TRTYPE"="x", "TIMESTAMP"="xxxxxxxxxxxxxx", "NONCE"="xxxxxxxxxxxxxxx", "P\_SIGN"="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", "EXT\_NET\_REF"="xxxxxxxxxxxxxxxxxxxxx"

### 7.4 MIT Scheduled – Payment

| Fields | Size | Description |
| --- | --- | --- |
| EXT\_NET\_REF | 6-32 | Value returned to the merchant during card storage |
| TOKEN | 28 | Value returned to the merchant during card storage |
| TRTYPE | 3 | 185 |

## 8 Transaction Status

### 8.1 Check transaction status

Merchant can send transaction status request to E-commerce gateway during 24h from transaction request time.

To our E-commerce gateway need send HTTP POST request to URL:

https://testmpi.3dsecure.az/cgi-bin/cgi\_link

#### Request format

| Fields | Size | Description |
| --- | --- | --- |
| TRAN\_TRTYPE | 1-2 | Original transaction type for state request (For example: TRTYPE 0, 1, 22, 24 and etc.) |
| ORDER | 6-20 | Original transaction order id for state request |
| TERMINAL | 8 | Merchant Terminal ID assigned by bank |
| TRTYPE | 2 | Must be equal to "90" (Transaction request type). |
| TIMESTAMP | 14 | Merchant transaction timestamp in GMT: YYYYMMDDHHMMSS. Timestamp difference between merchant server and e-Gateway server must not exceed 1 hour, otherwise e-Gateway will reject this transaction. |
| NONCE | 1-64 | Merchant nonce. Must be filled with 8-32 unpredictable random bytes in hexadecimal format. Must be present if MAC is used. |
| P\_SIGN | 1-256 | Merchant MAC in hexadecimal form. |

### 8.2 Response can be in HTML, XML and JSON format according to Merchant request.

| Fields | Description |
| --- | --- |
| ACTION | Original transaction action for state request |
| Response code | Original transaction RC for state request |
| Transaction Status message | Original transaction status message |
| TERMINAL | Original transaction Terminal ID |
| Card number | Original transaction masked card number |
| Transaction amount | Original transaction amount |
| Transaction currency | Original transaction currency |
| Transaction date | Original transaction date |
| Transaction state | Original transaction state |
| Merchant order id | Original transaction ORDER ID |
| Banks approval code | Original transaction approval code |
| Transaction RRN | Original transaction RRN |
| INT\_REF | Original transaction INT\_REF |
| Original transaction TRTYPE | Original transaction TRTYPE |
| Timestamp | Request Timestamp |
| Nonce | Original transaction Nonce |
| P\_SIGN | E-Commerce gateway MAC (Message Authentication Code) in Hexadecimal form. Will be present if MAC is used. |

### 8.3 Merchant MAC – Message Authentication Code

To authenticate transaction messages on gateway to/from the merchant link, the merchant system should be able to calculate and verify message authentication codes for at least the transactions passed through cardholder browser redirects. Messages that are sent directly to e-Commerce Gateway (“Sales completion” and “Reversal”) may be mutually authenticated with SSL client/server certificates and does not require MAC; if they are not mutually authenticated, MAC for these messages is mandatory.

MAC is calculated over all fields generated by the merchant system as defined in corresponding format Tables (visible and hidden fields generated by the merchant system) except the MAC field (“P\_SIGN”) itself.

In order to generate or verify the message authentication field, the merchant system must assemble a MAC source string; all field values from the format tables are prefixed with the decimal field length in ASCII and concatenated in a specified order. If the field is not present, the '-' character is added to the message in its place.

Authorization message example: MAC source string will contain the following field values - ORDER, TERMINAL, TRTYPE, TIMESTAMP and NONCE. Suppose that we have a transaction with following fields:

| Fields | Size | Value |
| --- | --- | --- |
| ORDER | 14 | 20211112075614 |
| TERMINAL | 8 | 17202191 |
| TRTYPE | 2 | 90 |
| TIMESTAMP | 14 | 20211112075714 |
| NONCE | 16 | 7cfb4c2512eeec72 |

`14`20211112075614`8`17202191`2`90`14`20211112075714`16`7cfb4c2512eeec72

Line breaks are inserted for visibility only. This string is 190 bytes long

After the MAC source string is assembled, the merchant system must apply a cryptographic algorithm to generate the message authentication code. Gateway supports various cryptographic algorithms and the system administrator may specify which algorithm will be used for a particular merchant terminal.

The merchant system must implement a chosen algorithm either in hardware or software form and be fully responsible for the secure storage and usage of corresponding cryptographic keys. An effective key length must be at least 112 bits for asymmetric cryptographic algorithms and 2048 bits for RSA with SHA256 algorithm.

The default MAC algorithm is RSAwithSHA256. Additional options may be available on demand. For our MAC source string example and HMAC RSA with SHA256 algorithm with Private RSA key the result MAC (“P\_SIGN”) field must be equal to:

`“5dc32febbca757927aa353b526515b30a3ef4bf87a5ce24e4e01ad6292954560e97b3a30283fd034d3e5b6d21 ec72ce2a37db27a476ff970f7e5ae694b39b637101643f220f701f7918295d06c287c46ec8e6aa7e48e2d560c49 f76a09ccd0aa4404dd889e98c474f162f7154c95e5bd9c16333c4f0088f8a732c48fc902de9d9b782a7a07cd0aa 1a1d07852b1306b8185160cdc36d665e65ac9b63ca44700933a1e0bfba9624f08d86a4259fecf3a020d7ff254a0 7468881e05e3fe08f11624f5d235341965cc272e4360a27a0bbe8ad868952a0b4072b4a4239704712fa033989 35ab2527517672948c4ef2d4cb5a8e4e2381f7e3ef9d8c6ccb85d154b08fd”`

MAC field value can be either an upper case or lower case hexadecimal string.

## 9 GooglePay Acquiring Service Integration

"Azericard" LLC is the first processing centre in the Republic of Azerbaijan, completely certified by International Payment Systems: MasterCard, Visa, American Express, Diners Club, UnionPay and JCB. AzeriCard performs processing for15 bank in Azerbaijan and abroad, all of them are the members of International Payment Systems. Azericard actively implements state-of-the-art technological projects such as payments for telecom services and public utilities, customs and tax payments, Internet and Mobile Banking, Card-to-Card transfers (Kart Transfer, VISA Direct, MasterCard Money Send), VTS, insurance and deposit payments via ATMs, different loyalty programs, multicurrency card and so on.

This document provides merchants and their affiliates with the tools to integrate Azericard Google Pay Interface so that Azericard may process their transaction requests.

#### GOOGLEPAY™APIWEB INTEGRATION

#### Accept payments without entering card details.

Google Pay™ is a digital wallet, which enables simple and fast card payments, without the need to enter the card data for each payment. The card data is safely stored by Google. This payment method is available for all devices (mobile phones and computers), irrespective of the operating system and web browser.In case of Google Pay usage, Acceptor is obligated to comply with the provisions of the following [regulations](https://payments.developers.google.com/terms/sellertos)

#### Authorization methods

-   PAN\_ONLY: This authentication method is associated with payment cards stored on file with the user's Google Account.Returned payment data includes personal account number(PAN) with the expiration month and the expiration year.
-   CRYPTOGRAM\_3DS: This authentication method is associated with cards stored as Android device tokens.Returned payment data includes a 3-D Secure(3DS) cryptogram generated on the device.

The authorization methods allowed with GooglePay ™ are by card and by 3D Secure cryptogram. For more information about the authorized authorization methods consult the [official Google™ documentation](https://developers.google.com/pay/api/web/reference/request-objects#CardParameters)

#### Accepted cards

The cards that are allowed for these payment methods are:

-   VISA
-   MASTERCARD
-   AMEX
-   JCB
-   DCI

#### Documentation links for integration:

Android: [https://developers.google.com/pay/api/android/overview?hl=en](https://developers.google.com/pay/api/android/overview?hl=en)

Web: [https://developers.google.com/pay/api/web/overview?hl=en](https://developers.google.com/pay/api/web/overview?hl=en)

Design Guideline: [https://developers.google.com/pay/api/web/guides/brand-guidelines?hl=en](https://developers.google.com/pay/api/web/guides/brand-guidelines?hl=en)

Google Pay and Wallet APIs Acceptable Use Policy: [https://payments.developers.google.com/terms/aup?hl=en](https://payments.developers.google.com/terms/aup?hl=en)

Google Pay API Terms of Service: [https://payments.developers.google.com/terms/sellertos](https://payments.developers.google.com/terms/sellertos)

The gateway parameter in the script should have the constant value of **Azericard**, according to the example below:

1.  Add Google Pay Button for get payment data.
2.  Merchant receives the payment data from Google.
3.  Merchant generate payment request to Azericard gateway.
4.  Merchant receive payment data from Azericard gateway.
5.  Merchant displays payment status to consumer.

#### Example code for displaying Google Pay button

```
<script async src="https://pay.google.com/gp/p/js/pay.js" onload="onGooglePayLoaded()"></script>;
<script>
    /**
     * Define the version of the Google Pay API referenced when creating your configuration
     *
     * @see {@link https://developers.google.com/pay/api/web/reference/request-objects#PaymentDataRequest|apiVersion in PaymentDataRequest}
     */
    const baseRequest = {
        apiVersion: 2,
        apiVersionMinor: 0
    };

    /**
     * Card networks supported by your site and your gateway
     * @see {@link https://developers.google.com/pay/api/web/reference/request-objects#CardParameters|CardParameters}
     * @todo confirm card networks supported by your site and gateway
     */
    const allowedCardNetworks = ["AMEX", "DISCOVER", "INTERAC", "JCB", "MASTERCARD", "VISA"];

    /**
     * Card authentication methods supported by your site and your gateway
     * @see {@link https://developers.google.com/pay/api/web/reference/request-objects#CardParameters|CardParameters}
     * @todo confirm your processor supports Android device tokens for your supported card networks
     */
    const allowedCardAuthMethods = ["PAN_ONLY", "CRYPTOGRAM_3DS"];

    /**
     * Identify your gateway and your site's gateway merchant identifier
     * @todo check with your gateway on the parameters to pass
     * @see {@link https://developers.google.com/pay/api/web/reference/request-objects#gateway|PaymentMethodTokenizationSpecification}
     */
    const tokenizationSpecification = {
        type: 'PAYMENT_GATEWAY',
        parameters: {
            gateway: 'azericardgpay',
            gatewayMerchantId: '123456789' // Provided by Azericard
        }
    };

    /**
     * Describe your site's support for the CARD payment method and its required fields
     * @see {@link https://developers.google.com/pay/api/web/reference/request-objects#CardParameters|CardParameters}
     */
    const baseCardPaymentMethod = {
        type: 'CARD',
        parameters: {
            allowedAuthMethods: allowedCardAuthMethods,
            allowedCardNetworks: allowedCardNetworks
        }
    };

    /**
     * Describe your site's support for the CARD payment method including optional fields
     * @see {@link https://developers.google.com/pay/api/web/reference/request-objects#CardParameters|CardParameters}
     */
    const cardPaymentMethod = Object.assign({}, baseCardPaymentMethod, {
        tokenizationSpecification: tokenizationSpecification
    });

    /**
     * An initialized google.payments.api.PaymentsClient object or null if not yet set
     * @see {@link getGooglePaymentsClient}
     */
    let paymentsClient = null;

    /**
     * Configure your site's support for payment methods supported by the Google Pay API.
     * @returns {object} Google Pay API version, payment methods supported by the site
     */
    function getGoogleIsReadyToPayRequest() {
        return Object.assign({}, baseRequest, {
            allowedPaymentMethods: [baseCardPaymentMethod]
        });
    }

    /**
     * Configure support for the Google Pay API
     * @returns {object} PaymentDataRequest fields
     */
    function getGooglePaymentDataRequest() {
        const paymentDataRequest = Object.assign({}, baseRequest);
        paymentDataRequest.allowedPaymentMethods = [cardPaymentMethod];
        paymentDataRequest.transactionInfo = getGoogleTransactionInfo();
        paymentDataRequest.merchantInfo = {
            // @todo a merchant ID is available for a production environment after approval by Google
            // See https://developers.google.com/pay/api/web/guides/test-and-deploy/integration-checklist
            merchantId: 'Merchant ID', // Provided by Azericard
            merchantName: 'Merchant Name',
            merchantOrigin: 'Merchant URL'
        };
        return paymentDataRequest;
    }

    /**
     * Return an active PaymentsClient or initialize
     * @returns {google.payments.api.PaymentsClient} Google Pay API client
     */
    function getGooglePaymentsClient() {
        if (paymentsClient === null) {
            paymentsClient = new google.payments.api.PaymentsClient({
                environment: 'TEST' // For production use 'PRODUCTION'
            });
        }
        return paymentsClient;
    }

    /**
     * Initialize Google PaymentsClient after Google-hosted JavaScript has loaded
     */
    function onGooglePayLoaded() {
        const paymentsClient = getGooglePaymentsClient();
        paymentsClient.isReadyToPay(getGoogleIsReadyToPayRequest())
            .then(function (response) {
                if (response.result) {
                    addGooglePayButton();
                    // Optionally prefetch payment data
                    // prefetchGooglePaymentData();
                }
            })
            .catch(function (err) {
                console.error(err);
            });
    }

    /**
     * Add a Google Pay purchase button alongside an existing checkout button
     */
    function addGooglePayButton() {
        const paymentsClient = getGooglePaymentsClient();
        const button = paymentsClient.createButton({
            onClick: onGooglePaymentButtonClicked,
            allowedPaymentMethods: [baseCardPaymentMethod]
        });
        document.getElementById('gpay_container').appendChild(button);
    }

    // Payment amount and currency elements
    const amount = document.getElementsByName("AMOUNT");
    const currency = document.getElementsByName("CURRENCY");

    /**
     * Provide Google Pay API with a payment amount, currency, and amount status
     * @returns {object} transaction info
     */
    function getGoogleTransactionInfo() {
        return {
            currencyCode: currency[0].value,
            totalPriceStatus: 'FINAL',
            totalPrice: amount[0].value
        };
    }

    /**
     * Prefetch payment data to improve performance
     */
    function prefetchGooglePaymentData() {
        const amount = document.getElementsByName("AMOUNT");
        const currency = document.getElementsByName("CURRENCY");
        const paymentDataRequest = getGooglePaymentDataRequest();
        paymentDataRequest.transactionInfo = {
            totalPriceStatus: 'NOT_CURRENTLY_KNOWN',
            currencyCode: currency[0].value
        };
        const paymentsClient = getGooglePaymentsClient();
        paymentsClient.prefetchPaymentData(paymentDataRequest);
    }

    /**
     * Show Google Pay payment sheet when Google Pay payment button is clicked
     */
    function onGooglePaymentButtonClicked() {
        const paymentDataRequest = getGooglePaymentDataRequest();
        paymentDataRequest.transactionInfo = getGoogleTransactionInfo();
        const paymentsClient = getGooglePaymentsClient();
        paymentsClient.loadPaymentData(paymentDataRequest)
            .then(function (paymentData) {
                processPayment(paymentData);
            })
            .catch(function (err) {
                console.error(err);
            });
    }

    /**
     * Process payment data returned by the Google Pay API
     * @param {object} paymentData - response from Google Pay API after user approves payment
     */
    function processPayment(paymentData) {
        const paymentToken = paymentData.paymentMethodData.tokenizationData.token;
        // Function to add token and submit form
        if (paymentToken) {
            addValue("tform", "GPAYTOKEN", paymentToken);
            document.getElementById("tform").submit();
        }
    }
</script>
```

**allowedAuthMethods** - Azericard can process both PAN\_ONLY and CRYPTOGRAM\_3DS authentication methods.

**allowedCardNetworks** - specify the card networks that you wish to allow. If the customer has cards in their wallet that are not in the 'allowed' list then those cards will be greyed-out/disabled in their wallet.

**merchantId** - found in the Google Pay Business Console under your account's Public merchant profile setting. Please note that this is only required in Google Pay's production environment; while testing, this field can be set to a dummy value or omitted.

**gateway** - a unique property that identifies Azericard as the processor; all encryption keys are associated with this ID. This field value provided by Azericard.

**gatewayMerchantId** - a property that uniquely identifies the merchant. This field value provided by Azericard.

#### Request Example to Azericard Payment Gateway.

**Request URL**: [https://testmpi.3dsecure.az/cgi-bin/cgi\_link](https://testmpi.3dsecure.az/cgi-bin/cgi_link)

**CONTENT-TYPE**: x-www-form-urlencoded

Request Parameters:

| Fields | Size | Description |
| --- | --- | --- |
| AMOUNT | 1-12 | Order total amount Required Float with decimal point separator |
| CURRENCY | 3 | Order currency Required Alphabetic, \[A-Z\] |
| ORDER | 6-20 | Merchant order ID Required Integer Last 6 digits used as system trace audit number and must be unique within a day for the terminal ID |
| DESC | 2 | This document describes the ApplePay & GPay Acquiring service details and the integration procedure between the Azericard Apple/GPay service and the merchants or banks’ mobile applications. |
| MERCH\_URL | 1-250 | Merchant primary website URL Required |
| TERMINAL | 8 | Merchant terminal ID assigned by bank Required |
| TRTYPE | 1 | Transaction type Required Integer Possible values: 1 – purchase |
| TIMESTAMP | 14 | Merchant transaction timestamp in GMT (GMT time zone offset 0) Required Integer, YYYYMMDDHHMMSS Discrepancy between merchant and gateway servers should not exceed 1 hour, otherwise, the transaction will be declined. |
| NONCE | 1-64 | Merchant nonce Conditional Hexadecimal, 8-32 unpredictable random bytes Required if MAC is used |
| P\_SIGN | 1-256 | Merchant MAC Required Hexadecimal |
| ADDENDUM | 2 | Optional Possible values: AD |
| AD.ECOM\_PAY\_DTLS |  | Optional |
| GPAYTOKEN | 8-9 | Received paymentToken |

#### HTTP POST Data:

"AMOUNT"="1.00",

"CURRENCY"="AZN",

"ORDER"="123456",

"DESC"="Some Record",

"TERMINAL"="77777777",

"TRTYPE"="1",

"ADDENDUM"="AD",

"AD.ECOM\_PAY\_DTLS"=" Some Record",

"MERCH\_URL"="https://merchantURL.com",

"NONCE"="3403fcef17df3c1c",

"TIMESTAMP"="20250123044608",

"P\_SIGN"="3641aa45289d8801d47de2f2dc5a88830b1dd72136082309cbef4adad75b17cf91da23a1948c 12e71cd866b8cd6213217e8f68c24f54dfee5826fbd9da4ec18d2b343587db5683f134ac1c5638271c2039 720701152fa0f28bc72eecda23973d8cb96e0779ad1fab488f1d13a08ebc413991c1913b8e17d8dda11f7c 699e23f0db90bf2ba832f805bc91ce7886b4e1d6b45181d0d4aca7b10c1a312a4b300c613f80f7fc7b2495c 2c20f4e8d3e83574abc4e94079575f57a6293d0b438398b7f7c0a63ccd23a180bfda18c99765528c4a55ace 8fcaa18babed0fb56dbbad0346309f8ff11948285f8ad64f24fd17b8a08fc4f116bae531ba45e346fe5dacec4 a"

"GPAYTOKEN"="{"signature":"MEYCIQDHIUKOq6QqJPx9dFYaLHBKA9aTUdDXujcg3GKmeSZKXAIhAI50BC eNNxKBGu/71RteOqqc+R+iBfRlZMYKftJnXKB+","intermediateSigningKey":{"signedKey":"{\\"keyValue\\":\\ "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAELCtHG9bjtMWCu4Iv4Td6npa/DiKc3Fou5R0bX2dk7tzEp+m byu3RJu+6epmmVwkHC5SbTztme9qk/kT65tpGiA\\=\\=\\",\\"keyExpiration\\":\\"1738277361000\\"}","signat ures":\["MEUCIEE+ADhhucm6jrwyn1UxqFLAGI3zHDp/XgpLGSuqPcemAiEAtuLPNLlPfl2uJzvlAYmouI6wT7y /akSlL5SEPVW+iXE="\]},"protocolVersion":"ECv2","signedMessage":"{\\"encryptedMessage\\":\\"AnnDsgE3 CaFKzQ2OEBJgg3f/2NnVF4gL6V1EbwLpJW4CCj2gvH7IKJFbHcYtofIT9JiiweTmalniMPpsfQiMgOcLT/Al4a7/ YNLkZrPYLO5g6G/qfsPfhWmlVHp6s3kistOvWmB8x2tCWaRa5XDQT4xs+PVzdd5Sv6aE0MN99zLw2fRcnYxi jqbD7DsVx3cW55LnGc2Hu/s2U/ExQp+/5Nqn2LNJQhMP03DS1kFv0r0dxlKkmYMv5VPVyKkrvPtCdc63W0 3tdCdJID6bDS6sb60C9n1Md/h92t6WX6T/XlyKmbsGcWb9Yqxx0h0AMBa4KY/jBMeSZc1Hsz/hIWZSLp+jFb pgiU4seBTA9cNeHswzb8T/gjffOM2rE/32v6UMKk+3Z8GTLoaYUYEIvv1MfY6fqkrOngqIw0iABi3NDrXBi5om v1p/IuRrOHNM/R9rybtAKNJcgSi0u9W90XeQxzWSISl49fUa8DEKjLXZNKFxg9w2J12mUNShfyfYu17+0h8ilik JZJPvB4r3CvjxueX6INpiMLixiSW8qSRARWbgh0inzRBpwolbi+pFD6nIAOHgzUDXGdlsGvW15KF/Td93fVsCB P9RUtD3dnbWVZWIyvzKGs6A3igtO7PgCxEPGvF02ubZq2awW8APXN2i\\",\\"ephemeralPublicKey\\":\\"BINi T+HhksaGzpP1Z2uCCWYNTW6dIG2cyDpcdhGh5FMN1da/kD2977KEIbXnJb0L2B5XGq0KpCEEgUPX4FGNY GQ\\=\\",\\"tag\\":\\"5lUVCC+Y+nvT/nsVNi8ZVnm8OCIQib8+z5EvN9z2gjM\\=\\"}"}",

#### Example of Authorization Response:

| Fields | Size | Description |
| --- | --- | --- |
| TERMINAL | 8 | Echo from the request |
| TRTYPE | 2 | Echo from the request |
| ORDER | 6-20 | Echo from the request |
| AMOUNT | 1-12 | Amount authorized. Usually, will be equal to original amount plus aquirer’s fee. |
| CURRENCY | 3 | Echo from the request |
| ACTION | 1 | Е-Gateway action code:  
0 – Transaction successfully completed;  
1 – Duplicate transaction detected;  
2 – Transaction declined;  
3 – Transaction processing fault. |
| RC | 2 | Transaction response code (ISO-8583 Field 39) |
| APPROVAL | 6 | Client bank’s approval code (ISO-8583 Field 38). Can be empty if not provided by card management system. |
| RRN | 12 | Merchant bank’s retrieval reference number (ISO-8583 Field 37). |
| INT\_REF | 1-32 | E-Commerce gateway internal reference number |
| TIMESTAMP | 14 | E-Commerce gateway timestamp in GMT: YYYYMMDDHHMMSS |
| NONCE | 1-64 | E-Commerce gateway nonce value. Will be filled with 8-32 unpredictable random bytes in hexadecimal format. Will be present if MAC is used. |
| P\_SIGN | 1-256 | E-Commerce gateway MAC (Message Authentication Code) in hexadecimal form. Will be present if MAC is used. |

#### Merchant MAC – Message Authentication Code

To authenticate transaction messages on gateway to/from the merchant link, the merchant system should be able to calculate and verify message authentication codes for at least the transactions passed through cardholder browser redirects. Messages that are sent directly to e-Commerce Gateway (“Sales completion” and “Reversal”) may be mutually authenticated with SSL client/server certificates and does not require MAC; if they are not mutually authenticated, MAC for these messages is mandatory.

MAC is calculated over all fields generated by the merchant system as defined in corresponding format tables (visible and hidden fields generated by the merchant system) except the MAC field (“P\_SIGN”) itself.

In order to generate or verify the message authentication field, the merchant system must assemble a MAC source string; all field values from the format tables are prefixed with the decimal field length in ASCII and concatenated in a specified order. If the field is not present, the '-' character is added to the message in its place.

**Authorization Request message example:** MAC source string will contain the following field values - AMOUNT, CURRENCY, TERMINAL, TRTYPE, TIMESTAMP, NONCE, MERCH\_URL.

Suppose that we have a transaction with following fields::

| Fields | Size | Description |
| --- | --- | --- |
| AMOUNT | 5 | 11.48 |
| CURRENCY | 3 | USD |
| TERMINAL | 8 | 99999999 |
| TRTYPE | 1 | 1 |
| TIMESTAMP | 14 | 20030105153021 |
| NONCE | 16 | F2B2DD7E603A7ADA |
| MERCH\_URL | 22 | www.sample.com |

Calculated fields for generate P\_SIGN beow. First of all need to use hex2bin(P\_SIGN) function then verify data using AZERICARDpublic.pem. File will be provided during the test. During the P\_SIGN verification if some parameter will be empty need to add -(dash) parameter instead of value and length of parameter should not count.

`5`11.48`3`USD`8`99999999`1`1`14`20030105153021`16`F2B2DD7E603A7ADA`14`www.sample.com

**Verify Callback P\_SIGN parameter:**MAC source string will contain the following field values - AMOUNT, TERMINAL, APPROVAL, RRN, INT\_REF.

| Fields | Size | Description |
| --- | --- | --- |
| AMOUNT | 5 | 11.48 |
| TERMINAL | 8 | 99999999 |
| APROVAL | 6 | 168975 |
| RRN | 12 | 306276834930 |
| INT\_REF | 16 | 4A29E93C607E33DC |

Calculated fields for generate P\_SIGN

`5`11.48`8`99999999`6`168975`12`306276834930`16`4A29E93C607E33DC

After the MAC source string is assembled, the merchant system must apply a cryptographic algorithm to generate the message authentication code. Gateway supports various cryptographic algorithms and the system administrator may specify which algorithm will be used for a particular merchant terminal. The merchantsystem mustimplement SHA256 sign, add MAC source to sign and crypts with private key in hexadecimal. Merchantsystem implemented by special algorithm fully responsible for the secure storage and usage of corresponding cryptographic keys. An effective key length must be at least 2048 bits for RSA algorithm. MAC field value can be either an upper case or lowercase hexadecimal string. Additional options may be available on demand.

## 10 Applepay/Googlepay direct integration

Google və Apple ilə merchantın birbaşa inteqrasiyası üçün linklər aşağıda qeyd edilib.

-   Google Pay: [https://developers.google.com/pay/api/](https://developers.google.com/pay/api/)
-   Apple Pay: [https://developer.apple.com/documentation/passkit/apple-pay](https://developer.apple.com/documentation/passkit/apple-pay) or light version  
    [https://docs.payengine.co/developer-docs/processing-payments/apple-pay/apple-pay-in-your-native-app](https://docs.payengine.co/developer-docs/processing-payments/apple-pay/apple-pay-in-your-native-app)

#### Applepay/Googlepay Authorization Request Format

HTTP POST request should be sent to Azericard e-commerce gateway URL: [https://testmpi.3dsecure.az/cgi-bin/cgi\_link](https://testmpi.3dsecure.az/cgi-bin/cgi_link)

#### Authorization Request Example:

| Fields | Size | Description |
| --- | --- | --- |
| AMOUNT | 1-12 | Order total amount Required Float with decimal point separator |
| CURRENCY | 3 | Order currency Required Alphabetic, \[A-Z\] |
| ORDER | 6-20 | Merchant order ID Required Integer Last 6 digits used as system trace audit number and must be unique within a day for the terminal ID |
| DESC | 1-50 | This document describes the ApplePay & GPay Acquiring service details and the integration procedure between the Azericard Apple/GPay service and the merchants or banks’ mobile applications. |
| MERCH\_NAME | 1-50 | Merchant name (recognizable by cardholder) |
| MERCH\_URL | 1-250 | Merchant primary website URL Required |
| TERMINAL | 8 | Merchant terminal ID assigned by bank Required |
| TRTYPE | 1 | Must be equal to "1" (Authorization).Transaction type = 0 (Pre-Authorization),Transaction type = 1 (Authorization) |
| COUNTRY | 02 | Merchant country code Conditional Required if merchant server is located in a different time zone rather than the gateway’s server. |
| MERCHANT\_GMT | 1-5 | Merchant’s UTC/GMT time zone offset Conditional Example: -4 Required if merchant is located in different time zone rather than the gateway server. |
| TIMESTAMP | 14 | Merchant transaction timestamp in GMT (GMT time zone offset 0) Required Integer, YYYYMMDDHHMMSS Discrepancy between merchant and gateway servers should not exceed 1 hour, otherwise, the transaction will be declined. |
| NONCE | 1-64 | Merchant nonce Conditional Hexadecimal, 8-32 unpredictable random bytes Required if MAC is used |
| BACKREF | 1-250 | Merchant URL for posting authorization result. |
| P\_SIGN | 1-256 | Merchant MAC Required Hexadecimal |
| CARD | 9-19 | Card number (Primary account number). |
| EXP | 02 | Card expiration month (Numeric 2 digit value). |
| EXP\_YEAR | 02 | Card expiration year (Numeric 2 digit value: 20XX) |
| CVC2\_RC | 1 | CVC2 reason code. values:  
value="1" -CVC2 is present  
value="0" -CVC2 is not provided  
value="2"-CVC2 is illegible |
| EXT\_MPI\_ECI | 02 | Response ECI variable from GooglePay \\ApplePay server1 |
| TAVV |  | Response CAVV variable from GooglePay \\ApplePay server |

**Note1:**For Mastercard card static value ‘02’.

#### Authorization Response from our system in XML format

| Fields | Size | Description |
| --- | --- | --- |
| TERMINAL | 8 | Echo from the request |
| TRTYPE | 2 | Echo from the request |
| ORDER | 6-20 | Echo from the request |
| AMOUNT | 1-12 | Amount authorized. Usually, will be equal to original amount plus aquirer’s fee. |
| CURRENCY | 3 | Echo from the request |
| ACTION | 1 | Е-Gateway action code:  
0 – Transaction successfully completed;  
1 – Duplicate transaction detected;  
2 – Transaction declined;  
3 – Transaction processing fault. |
| RC | 2 | Transaction response code (ISO-8583 Field 39) |
| APPROVAL | 6 | Client bank’s approval code (ISO-8583 Field 38). Can be empty if not provided by card management system. |
| RRN | 12 | Merchant bank’s retrieval reference number (ISO-8583 Field 37). |
| INT\_REF | 1-32 | E-Commerce gateway internal reference number |
| TIMESTAMP | 14 | E-Commerce gateway timestamp in GMT: YYYYMMDDHHMMSS |
| NONCE | 1-64 | E-Commerce gateway nonce value. Will be filled with 8-32 unpredictable random bytes in hexadecimal format. Will be present if MAC is used. |
| P\_SIGN | 1-256 | E-Commerce gateway MAC (Message Authentication Code) in hexadecimal form. Will be present if MAC is used. |

#### Merchant MAC – Message Authentication Code

To authenticate transaction messages on gateway to/from the merchant link, the merchant system should be able to calculate and verify message authentication codes for at least the transactions passed through cardholder browser redirects. Messages that are sent directly to e-Commerce Gateway (“Sales completion” and “Reversal”) may be mutually authenticated with SSL client/server certificates and does not require MAC; if they are not mutually authenticated, MAC for these messages is mandatory.

MAC is calculated over all fields generated by the merchant system as defined in corresponding format tables (visible and hidden fields generated by the merchant system) except the MAC field (“P\_SIGN”) itself.

In order to generate or verify the message authentication field, the merchant system must assemble a MAC source string; all field values from the format tables are prefixed with the decimal field length in ASCII and concatenated in a specified order. If the field is not present, the '-' character is added to the message in its place.

**Authorization Request message example (for TRTYPE=1 and TRTYPE=0):** MAC source string will contain the following field values - AMOUNT, CURRENCY, TERMINAL, TRTYPE, TIMESTAMP, NONCE, MERCH\_URL.

Suppose that we have a transaction with following fields::

| Fields | Size | Description |
| --- | --- | --- |
| AMOUNT | 5 | 11.48 |
| CURRENCY | 3 | USD |
| TERMINAL | 8 | 99999999 |
| TRTYPE | 1 | 1 |
| TIMESTAMP | 14 | 20030105153021 |
| NONCE | 16 | F2B2DD7E603A7ADA |
| MERCH\_URL | 22 | www.sample.com |

Calculated fields for generate P\_SIGN

`5`11.48`3`USD`8`99999999`1`1`14`20030105153021`16`F2B2DD7E603A7ADA`14`www.sample.com

**Verify Callback P\_SIGN parameter:**MAC source string will contain the following field values - AMOUNT, TERMINAL, APPROVAL, RRN, INT\_REF.

| Fields | Size | Description |
| --- | --- | --- |
| AMOUNT | 5 | 11.48 |
| TERMINAL | 8 | 99999999 |
| APROVAL | 6 | 168975 |
| RRN | 12 | 306276834930 |
| INT\_REF | 16 | 4A29E93C607E33DC |

Calculated fields for generate P\_SIGN beow. First of all need to use hex2bin(P\_SIGN) function then verify data using AZERICARDpublic.pem. File will be provided during the test. During the P\_SIGN verification if some parameter will be empty need to add -(dash) parameter instead of value and length of parameter should not count.

`5`11.48`8`99999999`6`168975`12`306276834930`16`4A29E93C607E33DC

After the MAC source string is assembled, the merchant system must apply a cryptographic algorithm to generate the message authentication code. Gateway supports various cryptographic algorithms and the system administrator may specify which algorithm will be used for a particular merchant terminal. The merchantsystem mustimplement SHA256 sign, add MAC source to sign and crypts with private key in hexadecimal. Merchantsystem implemented by special algorithm fully responsible for the secure storage and usage of corresponding cryptographic keys. An effective key length must be at least 2048 bits for RSA algorithm. MAC field value can be either an upper case or lowercase hexadecimal string. Additional options may be available on demand.

## 11 Money transfer integration

This document describes the rules for generating requests sent from merchant payment center to the banks payment center

The interaction between payment center and bank is carried out according to the HTTP protocol using the Redirect form and JSON format, encoding UTF-8

### 11.1 Redirect with parameters

Redirect with parameters to “Azericard” page URL:

https://testmt.azericard.com/payment/view

#### 11.1.1 Description

You redirect the user to our page with the fields listed below. Then the user enters his card number and other optional parameters on the Azericard page. After this if you get a success response from Azericard so now transaction status is “pending”.

#### 11.1.2 Request Structure

| Fields | Size | Description |
| --- | --- | --- |
| Merchant | 1-16 | Company name |
| SRN | 10 | Unique transaction number on your side |
| Amount | 1-2 | Payment amount |
| Cur | 3 | Payment currency |
| ReceiverCredentials | 151 | User full name |
| RedirectLink | 12 | The link to which you want to redirect the client at the end of **the operation** |
| Signature | 32 | Calculated value  
MD5(All fields concatenated + Key\*) |

\* Key will be given to you during the integration

#### 11.1.3 Card Data Entry

User enters the card number on the Azericard web page and receives all the required data.

\- The user will be redirected by clicking "back" button or after 60 seconds

#### 11.1.4 Redirect Response Structure

The user will be redirected to the merchant link with the parameters listed below.

| Fields | Size | Description |
| --- | --- | --- |
| OperationID | 16-20 | Unique operation number on our side |
| SRN | 10 | Unique transaction number on your side |
| Amount | 1-2 | Amount from request |
| Cur | 3 | Currency from request, must be 944 only |
| CardStatus |  | User card status on Azericard side |
| ReceiverPAN | 16 | Masked card number |
| Status |  | Current transaction status (f.e. “pending”) |
| Timestamp |  | Response timestamp |
| Response Code |  | Processing response code |
| Message |  | Response message |
| Signature | 32 | Calculated value MD5(All fields concatenated + Key) |

#### 11.1.5 Card status List

1\. “our\_active” - the card is in our PC and has an active status

2\. “our\_inactive” - the card is in our PC and has an inactive status (blocked/ expired and etc.)

3\. “foreign” - the card is not in our PC

### 11.2 Direct Money Withdrawal Request *

**Note:** for direct request need PCI DSS certificate

### 11.1 Description

The method registers the withdrawal request directly without involving the UI part of the application.

### 11.2 Request Structure

POST

https://testmt.azericard.com/api/direct

Body

`{ "ReceiverPAN":"4444444444444444", "SRN":"4142398967", "Amount":"10.00", "Merchant":"TEST", "Cur":"944", "ReceiverCredentials":"Elvin Goderman", "RedirectLink":"http://localhost:8080/payment/callback", "Signature":"4E34786EB5788E4AE2BEF724E2D33E12" }`

To calculate signatures, concatenate all request fields' values, add the key at the end of the string and calculate MD5 hash of the final string. The example for the Direct Money Withdrawal Request string to be hashed is “44444444444444441414239896710.00TEST944Elvin Godermanhttp://localhost:8080/payment/callback+yourkey” Note that the field order should be the same as the order of fields in the request json body.

### 11.3 Responses Structure

#### 11.3.1 Success

Body:

`{ "OperationID": "20230414155833291728", "SRN": "4142398967", "Amount": 10.00, "Cur": 944, "CardStatus": "Our_Active", "ReceiverPAN": "476019******7181", "Status": "Pending", "Timestamp": "20230414155835106", "ResponseCode": "0", "Message": "Success", "Signature": "4E34786EB5788E4AE2BEF724E2D33E12" }`

#### 11.3.2 Error

Body (Card error):

`{ "OperationID": "0", "SRN": "4705316214", "Amount": 10.00, "Cur": 944, "CardStatus": "Unknown", "Status": "PAN Value is not valid", "Timestamp": "20230414161509967", "ResponseCode": "137", "Message": "Error", "Signature": "B674CD6EC279C3AA2B4E421AB158F1CB" }`

#### 11.3.3 Card status List

1\. “our\_active” - the card is in our PC and has an active status

2\. “our\_inactive” - the card is in our PC and has an inactive status (blocked/ expired and etc.)

3\. “foreign” - the card is not in our PC

4\. “Unknown” - authentication of the card did not start

#### 11.3.4 Possible Error List

Codes and messages

| Response Code | Message | Description |
| --- | --- | --- |
| 0 | Successfully completed | Successfully completed |
| 106 | Signature Error | Input data does not match signature |
| 112 | Payment not found | The payment not found on back end side |
| 116 | Transaction already started | The transaction already started waiting for completion or check by proceeding to the Status check call. |
| 105 | Duplicate transaction | Transaction is not in Pending status cannot be declined or confirmed. Contact Azericard for more info |
| Different errors code | The transaction was declined due to different reasons on the UFX side. | Different causes |

### 11.4 Confirmation of Transaction request

#### 11.4.1 Description

This method confirms pending transaction

#### 11.4.2 Request Structure

POST

https://testmt.azericard.com/api/confirm

Body:

`{ "Merchant":"TEST", "SRN": "1234567890", "Amount":10.00, "Cur": 944, "Timestamp" : "20200703224154887", "Signature" : "098f6bcd4621d373cade4e832627b4f6" }`

### 11.5 Responses Structure

#### 11.5.1 Success

Body:

`{ "OperationID": "c84cbf53-0dd6-441d-95cb-7be8d22dd690", "SRN": "1234567890", "RRN": "PP3031665341", "Amount": 10.00, "Cur": 944, "ReceiverPAN": "4760********7181", "Status": "Confirmed", "Timestamp": "20230131163601372", "ResponseCode": 0, "Message": "Successfully Completed", "Signature": "A75B75FD1ACCB8C5BD3EAB5C892A2A93" }`

#### 11.5.2 Error

Body (Card error):

`{ "OperationID": "c84cbf53-0dd6-441d-95cb-7be8d22dd690", "SRN": "1234567890", "RRN": "PP3031665341", "Amount": 10.00, "Cur": 944, "ReceiverPAN": "4760********7181", "Status": "Confirmed", "Timestamp": "20230131163601372", "ResponseCode": 0, "Message": "Successfully Completed", "Signature": "A75B75FD1ACCB8C5BD3EAB5C892A2A93" }`

#### 11.5.3 Possible Error List

Codes and messages

| Response Code | Message | Description |
| --- | --- | --- |
| 0 | Successfully completed | Successfully completed |
| 106 | Signature Error | Input data does not match signature |
| 112 | Payment not found | The payment not found on back end side |
| 116 | Transaction already started | The transaction already started waiting for completion or check by proceeding to the Status check call. |
| 105 | Duplicate transaction | Transaction is not in Pending status cannot be declined or confirmed. Contact Azericard for more info |
| Different errors code | The transaction was declined due to different reasons on the UFX side. | Different causes |

### 11.6 Decline reques

#### 11.6.1 Description

The method is used to decline pending transactions.

#### 11.6.2 Request Structure

POST

https://testmt.azericard.com/api/decline

Header: `Content Type: application/json`

Body:

`{ "Merchant": "TEST", "SRN": "1234567890", "Amount": 10.00, "Cur": 944, "Timestamp" : "20200703224154887", "Signature" : "183488e0609297b31e1ef18afb2d3673" }`

#### 11.6.3 Response Structure

##### Success

Body:

`{ "OperationID": "20230124105429272794", "SRN": "1234567890", "Amount": 10.00, "Cur": 944, "Status": "Declined", "Timestamp": "20230124152435358", "ResponseCode": 0, "Message": "Successfully Completed", "Signature": "83B14022FFF060D44A0DD4357E7F3A73" }`

##### Error

Body:

`{ "OperationID": "20230124105429272794", "SRN": "1234567890", "Timestamp": "20230124154656216", "ResponseCode": 105, "Message": "Duplicate transaction", "Signature": "2C13385948D54A0BC73951AD452869E4" }`

##### Possible Error List

| Response Code | Message | Description |
| --- | --- | --- |
| 0 | Successfully completed | Successfully completed |
| 106 | Signature Error | Input data does not match signature |
| 112 | Payment not found | The payment not found on back end side |
| 105 | Duplicate transaction | Transaction is not in Pending status cannot be declined or confirmed. Contact Azericard for more info |

### 11.7 Status of Transaction Request

#### 11.7.1 Description

This method is for checking transaction status on PC Azericard side.

#### 11.7.2 Request Structure

POST

https://testmt.azericard.com/api/status

Body:

`{ "Merchant":"TEST", "SRN": "1234567890", "Signature" : "098f6bcd4621d373cade4e832627b4f6" }`

#### 11.7.3 Response Structure

##### Success

Body:

`{ "Merchant": "TEST", "OperationID": "20230125140012670902", "SRN": "1234567890", "RRN": "PU2334078354", "Amount": 10.00, "Cur": 944, "CardStatus": "Our_Active", "ReceiverPAN": "4127********8698", "Status": "Successfully processed", "Timestamp": "20230126122109741", "TransactionStatus": "0", "Signature": "B1CB778B65B3C6039BCB173A5BCCDFDB" }`

##### Error

As an example “Not found Payment” response used

Body:

`{ "OperationID": "20230126093557306490", "SRN": "1234567890", "Timestamp": "20230126132719593", "ResponseCode": 104, "Message": "Payment not found", "Signature": "582F507C77F9051C4F15E7B8A844E2AF" }`

##### Possible Error List

| Response Code | Message | Description |
| --- | --- | --- |
| 0 | Successfully completed | Successfully completed |
| 106 | Signature Error | Input data does not match signature |
| 104 | Payment not found | The payment not found on back end side |
| 113 | The status is pending, the payment needs to be confirmed to complete transaction | The status is pending, the payment needs to be confirmed to complete transaction |
| 115 | The payment was declined previously | The payment was declined previously |
| 110 | Internal error, report to Azericard | Different Azericard related errors are possible, contact Azericard for additional information. |
| 114 | Report service returned no success for the transaction | Report service returned no success for the transaction |

### 11.8 Alive structure request

#### 11.8.1 Request Structure

GET

https://testmt.azericard.com/api/alive

#### 11.8.2 Response Structure

Body:

`{ "Version": x.x.x, "ResponseCode": 0, "Message": "Successfully" }`

### 11.9 Fields description

Field format designation:

number - numbers of characters 0–9

ans - alphanumeric, numeric and special characters, including space

| Title | Appointment | Format | Length | Presence |
| --- | --- | --- | --- | --- |
| Amount | Transfer amount in currency which is indicated in the field of Cur. The amount is indicated minimal units | number | Less than 12 | Required |
| Cur | Three-digit currency code of the field. Transfer amount. For AZN 944 | number | 3 | Required |
| ReceiverPAN | Transfer recipient card number | number | Less than 20 | Required |
| ReceiverCredentials | Surname Name Father name of recipient | string | Less than 151 | Required |
| Merchant | Merchant id agreed with the bank | string | Less than 16 | Required |
| OperationID | Unique ID operation, formed by merchant if needed for future use | number | Less than 13 | Optional |
| SRN | Transaction reference number, formed by merchant if needed for future use | number | 12 | Required |
| RRN | Transaction reference number, formed by PC Azericard | number | 12 | Required |
| SenderCountry | Sender country code | number | 3 | Optional |
| SenderCity | Sender city code | string | 13 | Optional |
| SenderAddress | Address of sender | string | 25 | Optional |
| SenderCredentials | Name Surname Father name of sender | string | Less than 151 | Optional |
| Attribute | Contains a chain of optional request fields object | any |  | Optional |
| SenderPAN | Card number of Sender | number | Less than 20 | Optional |
| TransactionNumber | Transaction ID, formed by PC Bank. Returned in response to the request | string | 15 | Required |
| ApprovalCode | Returned to the response at the request in case of a successful transfer of amount. (at Code=00) | ans | 6 | Required |
| ResponseCode | Response Code | number | 3 | Required |
| CardStatus | Receiver card status in PC Azericard system | string | Less than 20 | Optional |
| Timestamp | Request/Response timestamp | timestamp | 17 | Required |
| Status | Transaction status in local service databasedatabase | string | Less than 20 | Optional |
| TransactionStatus | Transaction on PC Azericard OWS database | number | 3 | Optional |
| Signature | Calculated value MD5(all fields concatenated + Key) | string | 32 | Required |

### 11.10 Response Code

| Code | Message |
| --- | --- |
| 0 | Successfully completed, Successfully processed \*(response message depends of local issuing banks) |
| 1 | Refer to card issue |
| 3 | Invalid merchant |
| 5 | Do not honor |
| 12 | Invalid transaction |
| 57 | Transaction not permitted to card holder |
| 61 | Exceeds withdrawal amount limit |
| 65 | Exceeded withdrawal frequency limit |
| 91 | Network error limit |
| 96 | System malfunction |
| 103 | Validation error |
| 104 | Payment not found |
| 105 | Duplicate transaction |
| 106 | Signature Error |
| 108 | Internal error |
| 110 | Internal error, contact Azericard |
| 113 | The status is pending, the payment needs to be confirmed to complete transaction |
| 114 | Report service returned no success for the transaction |
| 116 | Transaction already started |
| 118 | Error while call to ufx |
| 119 | The timestamp not in range |
| 120 | The timestamp has invalid format |
| 123 | The direct withdrawal request is not allowed for this merchant |
| 131 | Merchant doesn't exist |
| 132 | The SRN value is not 10 characters long |
| 133 | Amount value is not valid |
| 134 | Currency code is not valid |
| 135 | Credentials value is not valid |
| 136 | Call back URI is not valid |
| 137 | PAN Value is not valid |
| 138 | Common validation error, contact Azericard |
| 139 | The SRN value is not unique for the given merchant |
| 201 | The payment was declined previously |
| 202 | The transaction is in progress state |

## 12 Click to Pay

### 12.1 Overview

Click to Pay is an online payment solution based on the EMV® Secure Remote Commerce (SRC) standard.Click to Pay allows customers to use their saved payment credentials during online checkout without manually entering full card details for every purchase.For merchants, Click to Pay can be integrated into an existing checkout flow as an additional payment method.

### 12.2 Benefits

-   Simplified checkout experience.
-   Reduced manual entry of card details.
-   Improved customer experience.
-   Potential increase in payment conversion.
-   Support for tokenized payment credentials.
-   Modern payment security mechanisms.

### 12.3 Prerequisites

-   Click to Pay must be enabled for the Merchant Account.
-   A valid MERCHANT\_ID must be available.
-   Merchant Backend must be configured.
-   Merchant Frontend origin must be available.
-   Click to Pay integration must be enabled for the required card network.
-   Backend endpoints for Capture Context and payment completion must be implemented.

Note: Merchant activation and technical configuration may depend on the payment provider, acquirer, and Click to Pay implementation used by the merchant.

### 12.4 Frontend Integration

The frontend integration is responsible for:

-   Requesting a Capture Context from Merchant Backend.
-   Loading the Click to Pay SDK.
-   Initializing the Accept instance.
-   Initializing Unified Payments.
-   Rendering the Click to Pay Button.
-   Receiving the transientToken.
-   Sending the transientToken to Merchant Backend.

#### 12.4.1 HTML Example

```

<!doctype html>
<html lang="en">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Click to Pay</title>
</head>

<body>
    <h2>Payment</h2>
    <p id="status">Loading...</p>
    <div id="payment-buttons"></div>
    <p id="error-box"></p>

    <script>
        const CLIENT_URL = window.location.origin;
        const SERVER_URL = 'BACKEND_API_URL';
        const MERCHANT_ID = 'YOUR_MERCHANT_ID';
        
        const initialCaptureContext = {
            allowedCardNetworks: ["VISA"],
            allowedPaymentTypes: ["CLICKTOPAY"],
            captureMandate: {
                billingType: "NONE",
                requestEmail: true,
                requestPhone: true,
                requestShipping: false,
                showAcceptedNetworkIcons: true
            },
            clientVersion: "0.33",
            country: "AZ",
            locale: "en_US",
            orderInformation: {
                amountDetails: {
                    currency: "AZN",
                    totalAmount: "0.15"
                },
                billTo: {
                    email: "CUSTOMER_EMAIL",
                    firstName: "CUSTOMER_FIRSTNAME",
                    lastName: "CUSTOMER_LASTNAME",
                    phoneNumber: "CUSTOMER_PHONENUMBER",
                    phoneType: "mobile"
                }
            },
            targetOrigins: [CLIENT_URL]
        };

        let acceptInstance = null;

        function setStatus(text) {
            document.getElementById('status').textContent = text;
        }

        function cleanup() {
            if (acceptInstance) {
                try {
                    acceptInstance.dispose();
                } catch (_) { }
                acceptInstance = null;
            }
        }

        function loadScript(src) {
            return new Promise((resolve, reject) => {
                if (window.Accept) {
                    resolve();
                    return;
                }

                const script = document.createElement('script');
                script.src = src;
                script.onload = () => {
                    window.Accept ? resolve() : reject(new Error('Script loaded but Accept was not found'));
                };
                script.onerror = () => {
                    reject(new Error('Failed to load Click to Pay SDK'));
                };
                document.head.appendChild(script);
            });
        }

        async function captureContext(body) {
            const response = await fetch(`${SERVER_URL}/click-to-pay/capture-context`, {
                method: "POST",
                body: JSON.stringify(body),
                headers: {
                    "Content-Type": "application/json",
                    ...(MERCHANT_ID ? {
                        "x-merchant-id": MERCHANT_ID
                    } : {}),
                },
            });
            
            if (!response.ok) {
                throw new Error(`Capture Context error: ${response.status}`);
            }
            
            return await response.json();
        }

        async function processPayment(sessionId, transientToken) {
            const response = await fetch(`${SERVER_URL}/click-to-pay/complete-flow`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    ...(MERCHANT_ID ? {
                        "x-merchant-id": MERCHANT_ID
                    } : {}),
                },
                body: JSON.stringify({
                    sessionId,
                    transientToken
                }),
            });
            
            if (!response.ok) {
                throw new Error(`Payment error: ${response.status}`);
            }
            
            const result = await response.json();
            console.log('Payment result:', result);
            setStatus('Payment successfully completed');
            cleanup();
        }

        async function init() {
            try {
                setStatus('Getting Capture Context...');
                const data = await captureContext(initialCaptureContext);
                const captureContextJwt = data.captureContextJwt;
                const clientLibraryUrl = data.clientLibraryUrl;
                const sessionId = data.sessionId;
                setStatus('Loading SDK...');
                await loadScript(clientLibraryUrl);
                setStatus('Initializing Click to Pay...');
                acceptInstance = await window.Accept(captureContextJwt);
                const up = await acceptInstance.unifiedPayments();
                setStatus('');
                const transientToken = await up.show({
                    containers: {
                        paymentSelection: '#payment-buttons'
                    },
                });
                await processPayment(sessionId, transientToken);
            } catch (error) {
                console.error(error);
                setStatus(`Payment error: ${error.message}`);
            }
        }
        init();
    </script>
</body>

</html>
                
```

### 12.5 Capture Context

To initialize the Click to Pay SDK, the frontend must first obtain a Capture Context from the Merchant Backend.

The Capture Context request may contain:

-   Supported card networks.
-   Payment type.
-   Customer information.
-   Order amount.
-   Currency.
-   Merchant origin.
-   Checkout configuration.

#### 12.5.1 Configuration Example

```

                {
                  "allowedCardNetworks": [
                    "VISA"
                  ],
                  "allowedPaymentTypes": [
                    "CLICKTOPAY"
                  ],
                  "captureMandate": {
                    "billingType": "NONE",
                    "requestEmail": true,
                    "requestPhone": true,
                    "requestShipping": false,
                    "showAcceptedNetworkIcons": true
                  },
                  "country": "AZ",
                  "locale": "en_US",
                  "orderInformation": {
                    "amountDetails": {
                      "currency": "AZN",
                      "totalAmount": "0.15"
                    }
                  },
                  "targetOrigins": [
                    "https://merchant.example.com"
                  ]
                }
            
```

#### 12.5.2 Main Parameters

| Parameter | Description |
| --- | --- |
| allowedCardNetworks | Supported card networks |
| allowedPaymentTypes | Supported payment types |
| captureMandate | Customer information request configuration |
| country | Country code |
| locale | User interface locale |
| orderInformation | Order information |
| amountDetails | Payment amount and currency |
| billTo | Customer information |
| targetOrigins | Allowed frontend origins |

### 12.6 Merchant Backend API

The Merchant Backend must provide the following endpoints.

#### 12.6.1 Create Capture Context

##### Endpoint:

```
POST /click-to-pay/capture-context
```

##### Headers:

```
Content-Type: application/json
x-merchant-id: YOUR_MERCHANT_ID
```

##### Request:

```

{
 "allowedCardNetworks": [
   "VISA"
 ],
 "allowedPaymentTypes": [
   "CLICKTOPAY"
 ],
 "captureMandate": {
   "billingType": "NONE",
   "requestEmail": true,
   "requestPhone": true,
   "requestShipping": false,
   "showAcceptedNetworkIcons": true
 },
 "country": "AZ",
 "locale": "en_US",
 "orderInformation": {
   "amountDetails": {
     "currency": "AZN",
     "totalAmount": "0.15"
   }
 },
 "targetOrigins": [
   "https://merchant.example.com"
 ]
}              
              
```

##### Response:

```

{
  "captureContextJwt": "CAPTURE_CONTEXT_JWT",
  "clientLibraryUrl": "CLIENT_LIBRARY_URL",
  "sessionId": "SESSION_ID"
}              
              
```

##### Response Parameters

| Parameter | Description |
| --- | --- |
| captureContextJwt | JWT used to initialize the Click to Pay SDK |
| clientLibraryUrl | URL of the Click to Pay client SDK |
| sessionId | Unique payment session identifier |

### 12.7 Click to Pay Button

After receiving the Capture Context, the frontend loads the SDK and initializes the Accept instance.

```

await loadScript(clientLibraryUrl);
acceptInstance = await window.Accept(captureContextJwt);
              
```

Unified Payments is then initialized:

```

const up = await acceptInstance.unifiedPayments();
              
```

The Click to Pay Button is rendered using:

```

const transientToken = await up.show({ containers: { paymentSelection: '#payment-buttons' }, });
              
```

The following container must be present on the HTML page:

```

<div id="payment-buttons"></div>
              
```

After the customer completes the payment selection process, the SDK returns a transientToken. The transientToken must be sent to the Merchant Backend to complete the payment.

### 12.8 Complete Payment

Endpoint:

```

POST /click-to-pay/complete-flow
              
```

Headers:

```

Content-Type: application/json
x-merchant-id: YOUR_MERCHANT_ID
              
```

Request:

```

{
  "sessionId": "SESSION_ID",
  "transientToken": "TRANSIENT_TOKEN"
}
              
```

Example:

```

await fetch(`${SERVER_URL}/click-to-pay/complete-flow`,
    {
       method: 'POST',
       headers: {
         'Content-Type': 'application/json',
         'x-merchant-id': MERCHANT_ID
       },
       body: JSON.stringify({ sessionId, transientToken }),
    });
              
```

The Merchant Backend uses sessionId and transientToken to complete the payment operation and return the payment result.:

### 12.9 Payment Statuses

| Status | Description |
| --- | --- |
| APPROVED | Payment successfully completed |
| DECLINED | Payment was declined |
| PENDING | Final payment result is not yet available |

Recommended order status mapping:

APPROVED => PAID

DECLINED => PAYMENT\_FAILED

PENDING => PAYMENT\_PENDING

The merchant should not consider a payment successful based only on the frontend result. The final payment status must be confirmed by the Merchant Backend or the payment provider.

### 12.10 Integration Checklist

-   Click to Pay is enabled for the Merchant Account.
-   MERCHANT\_ID is configured.
-   Merchant Backend is available.
-   POST /click-to-pay/capture-context is implemented.
-   POST /click-to-pay/complete-flow is implemented.
-   Merchant frontend origin is configured in targetOrigins.
-   Correct clientLibraryUrl is returned.
-   Click to Pay Button is displayed correctly.
-   transientToken is received successfully.
-   transientToken is sent to the backend.
-   Successful payments return APPROVED.
-   Declined payments are handled correctly.
-   PENDING payments are handled separately.
-   Payment status is verified on the backend.
-   Secret keys are not exposed in frontend code.
-   Sensitive payment data is not stored in application logs.

### 12.11 References

-   EMVCo Secure Remote Commerce (SRC)
-   Click to Pay
-   Applicable payment network
-   Merchant's PSP / Payment Gateway
-   Merchant's Acquirer

Note: Technical parameters, SDK versions, supported payment networks, API endpoints, and authentication requirements may vary depending on the payment provider and integration model.

#### Sandbox

To support merchants who wish to test their integrations we have made a sandbox environment. By using following link you can reach many purposes such as developing, new features, testing patches, identifying and squashing bugs.

P\_SIGN Check:

[https://testsite.3dsecure.az/sandbox/p-sign.php](https://testsite.3dsecure.az/sandbox/p-sign.php)

Link to check payment in the test system

[https://testsite.3dsecure.az/sandbox/auth.php](https://testsite.3dsecure.az/sandbox/auth.php)

The link below (checkout-reversal-psign.php) will show how and what values are calculated in the mac section of the request's P\_SIGN data before performing a reversal and checkout.

[https://testsite.3dsecure.az/sandbox/checkout-reversal-psign.php](https://testsite.3dsecure.az/sandbox/checkout-reversal-psign.php)

The script (checkout-reversal.php) shown below will allow the client to checkout and reverse transactions through the sandbox. TRTYPE=21 should be used for Checkout, and TRTYPE=22 and TRTYPE=24 should be used for Reversal.

[https://testsite.3dsecure.az/sandbox/checkout-reversal.php](https://testsite.3dsecure.az/sandbox/checkout-reversal.php)

The links shown below will be used to calculate P\_SIGN transaction status requests and check the status of the payment.

[https://testsite.3dsecure.az/sandbox/transaction\_status.php](https://testsite.3dsecure.az/sandbox/transaction_status.php)

[https://testsite.3dsecure.az/sandbox/transaction\_status\_psign.php](https://testsite.3dsecure.az/sandbox/transaction_status_psign.php)

#### Sample curl requests

TRTYPE=0,1

```
curl --location --request POST 'https://testmpi.3dsecure.az/cgi-bin/cgi_link' \--header 'Content-Type: application/x-www-form-urlencoded' \--data-urlencode 'AMOUNT=10' \--data-urlencode 'CURRENCY=AZN' \--data-urlencode 'ORDER=20220628084800' \--data-urlencode 'DESC=test Odenish' \--data-urlencode 'TRTYPE=0' \--data-urlencode 'TIMESTAMP=20220825105200' \--data-urlencode 'NONCE=7fdc0caafb113590' \--data-urlencode 'BACKREF=https//test.com/test/callback' \--data-urlencode 'P_SIGN=2f3ac6adba8af5b38dcab617c59284bb69e5618197c60189f38d3f3727cfa2b533147bde577fb8b45e7b7ecaa80d500f069386013ec52367f93bcb127b31c1fa9843ca776cdca571986a925c1ce9f9ad50c29689ca74890369bbb5bcf86af6dea4 e9dca805b360f47752fe9dfc6b5848dc43f2cd9552fad4309545c6169f625de46963ca0401407f9319294db6e8d27f35f9d1bc48a61811502a391cef230d6f219b01cd1e32ad58c21af6f051c56485b4ae3759a3080f6fc2d6d8dcd5f0bb1b2acd7b2b4dc43b1c9fcdc7794e7272281216edd0742b9d3 fd879004fa9b45662d9b7e7f7c7b278f1808461b31a9572c43ae36df78a6eea54e60f4d1a681edc62' \--data-urlencode 'MERCH_NAME=test' \--data-urlencode 'MERCH_URL=http://test.com' \--data-urlencode 'TERMINAL=77777777' \--data-urlencode 'EMAIL=tsupport@test.com' \--data-urlencode 'COUNTRY=AZ' \--data-urlencode 'MERCH_GMT=+4' \--data-urlencode 'M_INFO=ewoiYnJvd3NlclNjcmVlbkhlaWdodCI6IjE5MjAiLAoiYnJvd3NlclNjcmVlbldpZHRoIjoiMTA4MCIsCiJicm93c2VyVFoiOiIwIiwKIm1vYmlsZVBob25lIiA6eyAiY2MiOiI5OTQiLCAic3Vic2NyaWJlciI6IjU1Nzc3Nzc3Nzc3IiB9Cn0' \--data-urlencode 'NAME=Test Testov'
```

HTTP POST

```
POST /cgi-bin/cgi_link HTTP/1.1Host: testmpi.3dsecure.azContent-Type: application/x-www-form-urlencodedAMOUNT=10&CURRENCY=AZN&ORDER=20220628084800&DESC=test Odenish&TRTYPE=0&TIMESTAMP=20220825105200&NONCE=7fdc0caafb113590&BACKREF=https//test.com/test/callback&P_SIGN=2f3ac6adba8af5b38dcab617c59284bb69e5618197c60189f38d3f3727cfa2b533147bde577fb8b45e7b7ecaa80d500f069386013ec52367f93bcb127b31c1fa9843ca776cdca571986a925c1ce9f9ad50c29689ca74890369bbb5bcf86af6dea4 e9dca805b360f47752fe9dfc6b5848dc43f2cd9552fad4309545c6169f625de46963ca0401407f9319294db6e8d27f35f9d1bc48a61811502a391cef230d6f219b01cd1e32ad58c21af6f051c56485b4ae3759a3080f6fc2d6d8dcd5f0bb1b2acd7b2b4dc43b1c9fcdc7794e7272281216edd0742b9d3 fd879004fa9b45662d9b7e7f7c7b278f1808461b31a9572c43ae36df78a6eea54e60f4d1a681edc62&MERCH_NAME=test&MERCH_URL=http://test.com&TERMINAL=77777777&EMAIL=tsupport@test.com&COUNTRY=AZ&MERCH_GMT=+4&M_INFO=ewoiYnJvd3NlclNjcmVlbkhlaWdodCI6IjE5MjAiLAoiYnJvd3NlclNjcmVlbldpZHRoIjoiMTA4MCIsCiJicm93c2VyVFoiOiIwIiwKIm1vYmlsZVBob25lIiA6eyAiY2MiOiI5OTQiLCAic3Vic2NyaWJlciI6IjU1Nzc3Nzc3Nzc3IiB9Cn0&NAME=Test Testov
```

TRTYPE = 21, 22, 24 (Refund / Reversal / Completion)

```
curl --location --request POST 'https://testmpi.3dsecure.az/cgi-bin/cgi_link' \--header 'Content-Type: application/x-www-form-urlencoded' \--data-urlencode 'AMOUNT=5' \--data-urlencode 'CURRENCY=AZN' \--data-urlencode 'ORDER=20210506070034' \--data-urlencode 'RRN=112676199769' \--data-urlencode 'INT_REF=5E3601D7C71745A9' \--data-urlencode 'TERMINAL=77777777' \--data-urlencode 'TRTYPE=21' \--data-urlencode 'TIMESTAMP=20210506070051' \--data-urlencode 'NONCE=2c9434b2aa5bb4af' \--data-urlencode 'P_SIGN=2f3ac6adba8af5b38dcab617c59284bb69e5618197c60189f38d3f3727cfa2b533147bde577fb8b45e7b7ecaa80d500f069386013ec52367f93bcb127b31c1fa9843ca776cdca571986a925c1ce9f9ad50c29689ca74890369bbb5bcf86af6dea4 e9dca805b360f47752fe9dfc6b5848dc43f2cd9552fad4309545c6169f625de46963ca0401407f9319294db6e8d27f35f9d1bc48a61811502a391cef230d6f219b01cd1e32ad58c21af6f051c56485b4ae3759a3080f6fc2d6d8dcd5f0bb1b2acd7b2b4dc43b1c9fcdc7794e7272281216edd0742b9d3 fd879004fa9b45662d9b7e7f7c7b278f1808461b31a9572c43ae36df78a6eea54e60f4d1a681edc62'
```

HTTP POST

```
HTTP POSTPOST /cgi-bin/cgi_link HTTP/1.1Host: testmpi.3dsecure.azContent-Type: application/x-www-form-urlencodedAMOUNT=5&CURRENCY=AZN&ORDER=20210506070034&RRN=112676199769&INT_REF=5E3601D7C71745A9&TERMINAL=77777777&TRTYPE=21&TIMESTAMP=20210506070051&NONCE=2c9434b2aa5bb4af&P_SIGN=2f3ac6adba8af5b38dcab617c59284bb69e5618197c60189f38d3f3727cfa2b533147bde577fb8b45e7b7ecaa80d500f069386013ec52367f93bcb127b31c1fa9843ca776cdca571986a925c1ce9f9ad50c29689ca74890369bbb5bcf86af6dea4 e9dca805b360f47752fe9dfc6b5848dc43f2cd9552fad4309545c6169f625de46963ca0401407f9319294db6e8d27f35f9d1bc48a61811502a391cef230d6f219b01cd1e32ad58c21af6f051c56485b4ae3759a3080f6fc2d6d8dcd5f0bb1b2acd7b2b4dc43b1c9fcdc7794e7272281216edd0742b9d3 fd879004fa9b45662d9b7e7f7c7b278f1808461b31a9572c43ae36df78a6eea54e60f4d1a681edc62
```

TRTYPE = 90 (Transaction Status Inquiry)

```
curl --location --request POST 'https://testmpi.3dsecure.az/cgi-bin/cgi_link' \--header 'Content-Type: application/x-www-form-urlencoded' \--data-urlencode 'TRAN_TRTYPE=1' \--data-urlencode 'ORDER=20210506070034' \--data-urlencode 'TERMINAL=77777777' \--data-urlencode 'TRTYPE=90' \--data-urlencode 'TIMESTAMP=20210506070051' \--data-urlencode 'NONCE=2c9434b2aa5bb4af' \--data-urlencode 'P_SIGN=2f3ac6adba8af5b38dcab617c59284bb69e5618197c60189f38d3f3727cfa2b533147bde577fb8b45e7b7ecaa80d500f069386013ec52367f93bcb127b31c1fa9843ca776cdca571986a925c1ce9f9ad50c29689ca74890369bbb5bcf86af6dea4 e9dca805b360f47752fe9dfc6b5848dc43f2cd9552fad4309545c6169f625de46963ca0401407f9319294db6e8d27f35f9d1bc48a61811502a391cef230d6f219b01cd1e32ad58c21af6f051c56485b4ae3759a3080f6fc2d6d8dcd5f0bb1b2acd7b2b4dc43b1c9fcdc7794e7272281216edd0742b9d3 fd879004fa9b45662d9b7e7f7c7b278f1808461b31a9572c43ae36df78a6eea54e60f4d1a681edc62'
```

HTTP POST

```
POST /cgi-bin/cgi_link HTTP/1.1Host: testmpi.3dsecure.azContent-Type: application/x-www-form-urlencodedTRAN_TRTYPE=1&ORDER=20210506070034&TERMINAL=77777777&TRTYPE=90&TIMESTAMP=20210506070051&NONCE=2c9434b2aa5bb4af&P_SIGN=2f3ac6adba8af5b38dcab617c59284bb69e5618197c60189f38d3f3727cfa2b533147bde577fb8b45e7b7ecaa80d500f069386013ec52367f93bcb127b31c1fa9843ca776cdca571986a925c1ce9f9ad50c29689ca74890369bbb5bcf86af6dea4 e9dca805b360f47752fe9dfc6b5848dc43f2cd9552fad4309545c6169f625de46963ca0401407f9319294db6e8d27f35f9d1bc48a61811502a391cef230d6f219b01cd1e32ad58c21af6f051c56485b4ae3759a3080f6fc2d6d8dcd5f0bb1b2acd7b2b4dc43b1c9fcdc7794e7272281216edd0742b9d3 fd879004fa9b45662d9b7e7f7c7b278f1808461b31a9572c43ae36df78a6eea54e60f4d1a681edc62
```
