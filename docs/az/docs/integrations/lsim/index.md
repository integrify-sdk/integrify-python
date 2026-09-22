# LSIM

???+ warning
    Bu sorğulardan istifadə edə bilmək üçün, düzgün "environment variable"-ları quraşdırmalısınız. Daha ətraflı [burdan](./env.md) oxuya bilərsiniz.

## Rəsmi Dokumentasiya (v2024.11.22) { #official-documentation }

[İngliscə](./official/api.md)

## Sürətli başlanğıc { #quickstart }

Tək və toplu SMS göndərmək, balansı yoxlamaq:

```python
from integrify.lsim import LSIMBulkSMSClient, LSIMSingleSMSClient

# Tək SMS (LSIM_LOGIN, LSIM_PASSWORD, LSIM_SENDER_NAME mühit dəyişənlərindən götürülür)
resp = LSIMSingleSMSClient.send_sms_post(msisdn='994501234567', text='Salam!')

if resp.ok:
    print(resp.body.obj)  # tranzaksiya ID-si (hesabat üçün lazımdır)

# Toplu SMS: hamıya eyni mətn
bulk = LSIMBulkSMSClient.bulk_send_one_message(
    controlid=1,  # hər göndəriş üçün unikal olmalıdır
    msisdns=['994501234567', '994551234567'],
    bulkmessage='Salam!',
)
print(bulk.body.task_id)

# Balans
balance = LSIMSingleSMSClient.check_balance()
print(balance.body.obj)
```

Asinxron istifadə üçün `LSIMSingleSMSAsyncClient`/`LSIMBulkSMSAsyncClient` import edib, eyni metodları `await` ilə çağırın.

## Sorğular listi { #list-of-requests }

### Tək SMS sorğuları { #single-sms-requests }

| Sorğu metodu                                                                               | Məqsəd                                            |          LSIM API          |
| :----------------------------------------------------------------------------------------- | :------------------------------------------------ | :------------------------: |
| [`send_sms_get`][integrify.lsim.single.client.LSIMSingleSMSClientClass.send_sms_get]       | GET sorğusu ilə SMS göndərilmə                    |    `/quicksms/v1/send`     |
| [`send_sms_post`][integrify.lsim.single.client.LSIMSingleSMSClientClass.send_sms_post]     | POST sorğusu ilə SMS göndərilmə                   |  `/quicksms/v1/smssender`  |
| [`check_balance`][integrify.lsim.single.client.LSIMSingleSMSClientClass.check_balance]     | Balansı yoxlamaq                                  |   `/quicksms/v1/balance`   |
| [`get_report_get`][integrify.lsim.single.client.LSIMSingleSMSClientClass.get_report_get]   | GET sorğusu ilə göndərilmiş SMS haqqında məlumat  |   `/quicksms/v1/report`    |
| [`get_report_post`][integrify.lsim.single.client.LSIMSingleSMSClientClass.get_report_post] | POST sorğusu ilə göndərilmiş SMS haqqında məlumat | `/quicksms/v1/smsreporter` |

### Toplu SMS sorğuları { #bulk-sms-requests }

| Sorğu metodu                                                                                                         | Məqsəd                                              |   LSIM API   |
| :------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------- | :----------: |
| [`bulk_send_one_message`][integrify.lsim.bulk.client.LSIMBulkSMSClientClass.bulk_send_one_message]                   | Toplu şəkildə hamıya eyni SMS göndərilmə            | `/smxml/api` |
| [`bulk_send_different_messages`][integrify.lsim.bulk.client.LSIMBulkSMSClientClass.bulk_send_different_messages]     | Toplu şəkildə hərəyə fərqli SMS göndərilmə          | `/smxml/api` |
| [`get_report`][integrify.lsim.bulk.client.LSIMBulkSMSClientClass.get_report]                                         | Toplu göndərilmiş SMS-in reportu                    | `/smxml/api` |
| [`get_detailed_report`][integrify.lsim.bulk.client.LSIMBulkSMSClientClass.get_detailed_report]                       | Toplu göndərilmiş SMS-in detallı reportu            | `/smxml/api` |
| [`get_detailed_report_with_dates`][integrify.lsim.bulk.client.LSIMBulkSMSClientClass.get_detailed_report_with_dates] | Toplu göndərilmiş SMS-in detallı və tarixli reportu | `/smxml/api` |
| [`check_balance`][integrify.lsim.bulk.client.LSIMBulkSMSClientClass.check_balance]                                   | Balansı yoxlamaq                                    | `/smxml/api` |
