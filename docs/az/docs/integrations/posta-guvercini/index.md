# Posta Güvərçini

???+ warning
    Bu sorğulardan istifadə edə bilmək üçün, düzgün "environment variable"-ları quraşdırmalısınız. Daha ətraflı [burdan](./env.md) oxuya bilərsiniz.

## Rəsmi Dokumentasiya (v1) { #official-documentation }

[İngliscə](https://www.poctgoyercini.com/api_json/swagger/ui/index#/)

Markdown versiyası (bu saytda): [Posta Güvərçini API](./official/api.md)

## Sürətli başlanğıc { #quickstart }

SMS göndərmək və statusunu yoxlamaq:

```python
from integrify.postaguvercini import PostaGuverciniClient

resp = PostaGuverciniClient.send_single_sms(message='Salam!', receivers=['994501234567'])

if resp.ok:
    message_id = resp.body.result[0].message_id

    status = PostaGuverciniClient.get_status(message_ids=[message_id])
    print(status.body.result[0].sms_status_description)
else:
    print(resp.body.status_description)
```

Asinxron istifadə üçün `PostaGuverciniAsyncClient` import edib, eyni metodları `await` ilə çağırın.

## Sorğular listi { #list-of-requests }

| Sorğu metodu                                                                                       | Məqsəd                            |        PostaGuvercini API        |
| :------------------------------------------------------------------------------------------------- | :-------------------------------- | :------------------------------: |
| [`send_single_sms`][integrify.postaguvercini.client.PostaGuverciniClientClass.send_single_sms]     | Tək nömrəyə sms göndərilməsi      |   `/api_json/v1/Sms/Send_1_N`    |
| [`send_multiple_sms`][integrify.postaguvercini.client.PostaGuverciniClientClass.send_multiple_sms] | Bir neçə nömrəyə sms göndərilməsi |   `/api_json/v1/Sms/Send_N_N`    |
| [`get_status`][integrify.postaguvercini.client.PostaGuverciniClientClass.get_status]               | SMS-in statusunu yoxlamaq         |    `/api_json/v1/Sms/Status`     |
| [`credit_balance`][integrify.postaguvercini.client.PostaGuverciniClientClass.credit_balance]       | Balansın yoxlanılması             | `/api_json/v1/Sms/CreditBalance` |
