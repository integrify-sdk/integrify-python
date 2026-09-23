# Kapital Bank E-commerce API Sənədləşməsi

???+ info
    Bu səhifə Kapital Bank-ın rəsmi API sənədinin ([pg.kapitalbank.az/docs](https://pg.kapitalbank.az/docs)) Markdown versiyasıdır. Uyğunsuzluq olarsa, orijinal mənbə əsas götürülür.

## Təsvir

Bu sənədləşmə Kapital Bank müştəriləri üçün e-ticarət sisteminə inteqrasiya məqsədi ilə nəzərdə tutulmuşdur.

## Əsas URL

- Test Mühiti: https://txpgtst.kapitalbank.az/api
- Prod Mühiti: https://e-commerce.kapitalbank.az/api

## Autentifikasiya

Bütün əməliyyatlar üçün autentifikasiya məqsədilə BasicAuth formatında başlıq tələb olunur. Bu başlıq tacirin istifadəçi adı və parolunu ehtiva edir və onlar base64 formatında kodlaşdırılır. Bu, tacirin istifadəçi adı və parolunun açıq mətn kimi göndərilməsinin qarşısını alaraq daha təhlükəsiz autentifikasiya üsuludur.

- BasicAuth haqqında daha çox məlumat: https://www.twilio.com/docs/glossary/what-is-basic-authentication
- PostMan-da BasicAuth https://learning.postman.com/docs/sending-requests/authorization/authorization-types/
- Java : https://www.baeldung.com/java-httpclient-basic-auth
- ASP.NET : https://code-maze.com/aspnetcore-basic-authentication-with-httpclient/
- Java : https://www.baeldung.com/java-httpclient-basic-auth
- Php : https://www.gavsblog.com/blog/how-to-use-basic-authentication-with-php-curl
- NodeJS : https://www.geeksforgeeks.org/basic-authentication-in-node-js-using-http-header/

## Basic Auth test etimadnamələri

- İstifadəçi adı: TerminalSys/kapital
- Şifrə: kapital123

## Əməliyyat Axını

## Əməliyyat axını (Adi ödəniş)

1. Sifariş yaratma sorğusu göndərin (Order_SMS). Əgər cavab müsbətdirsə, 2-ci addıma keçin.
2. Sifariş yaratma cavabından alınan məlumatlarla URL-ə yönləndirin (1-ci bənd): URL nümunəsi{{order.hppUrl}}/flex?id={{order.id}}&password={{order.password}}
3. PC-də (Emal Mərkəzi tərəfində) əməliyyat tamamlandıqdan sonra müştərini bir neçə (aşağıda göstərilən) əməliyyat sahəsi ilə birlikdə yönləndirin (callback) URL-ə yönləndirin. Əməliyyat axını tamamlandı. Callback URL nümunəsi: {{callback.url}}?ID=1234&STATUS=FullyPaidSTATUS parametri dəyəri müvəqqəti ola bilər. Buna görə də əməliyyatın statusunu əməliyyat detalları sorğusu ilə təsdiqləməlisiniz.

## Preauthorization əməliyyat axını (Preauthorization + Clearing)

1. Sifariş yaratma sorğusu göndərin (Order_DMS). Əgər cavab müsbətdirsə, 2-ci addıma keçin.
2. Sifariş yaratma cavabından alınan məlumatlarla URL-ə yönləndirin (1-ci bənd): URL nümunəsi{{order.hppUrl}}/flex?id={{order.id}}&password={{order.password}}
3. PC-də (Emal Mərkəzi tərəfində) əməliyyat tamamlandıqdan sonra müştərini bir neçə (aşağıda göstərilən) əməliyyat sahəsi ilə birlikdə yönləndirin (callback) URL-ə yönləndirin. Preauthorization birinci mərhələ tamamlandı və məbləğ blokda olacaq.
4. Xidmət və ya məhsul təmin edildikdən sonra İcra Əməliyyatı Clearing sorğusu göndərməlisiniz (preauthorization əməliyyatının ikinci addımı). Əməliyyat axını tamamlandı.

## Təkrar ödəniş axını (cvv2 və 3d yoxlamaları olmadan)

1. Təkrar ödəniş sifarişini yaratma sorğusu göndərin (Recurring). Əgər cavab müsbətdirsə, 2-ci addıma keçin.
2. Mənbə Token təyin etmə sorğusu göndərin. Əgər cavab müsbətdirsə, 3-cü addıma keçin.
3. Əməliyyatı icra edin (Saxlanılan kart ilə alış). Əgər cavab müsbətdirsə, əməliyyat tamamlandı.

## Sifariş Kredit Əməliyyatı axını (Karta vəsait göndərmək)

1. Təkrar ödəniş sifarişini yaratma sorğusu göndərin (Sifariş Kredit Əməliyyatı). Əgər cavab müsbətdirsə, 2-ci addıma keçin.
2. Mənbə Token təyin etmə sorğusu göndərin. Əgər cavab müsbətdirsə, 3-cü addıma keçin.
3. Əməliyyatı icra etmə sorğusu göndərin (Kredit Əməliyyatını İcra Et). Əgər cavab müsbətdirsə, əməliyyat tamamlandı.

## Test kart məlumatları

- PAN: 4169741330151778
- ExpDate: 06/25
- CVV: 119

- PAN: 5239151747183468
- ExpDate: 11/24
- CVV2: 292

## Sifariş Yarat

Bu endpoint yeni sifariş yaratmağa imkan verir.

### URI

POST /order

### Sorğu

- typeRid: Sifarişin növü. Sifariş növlərinin siyahısı:
    - Order_SMS: Alış əməliyyatları üçün
    - Order_DMS: Preauthorization əməliyyatları üçün
    - Order_REC: Təkrar Alış əməliyyatları üçün (saxlanılan kart ilə əməliyyatlar)
    - DMSN3D: Təkrar Preauthorization əməliyyatları üçün (saxlanılan kart ilə əməliyyatlar)
    - OCT: Kartdan Karta əməliyyatlar üçün (Sifariş Kredit Əməliyyatı)
- amount: Sifarişə aid məbləğ.
- currency: Sifarişin valyutası.
- language: Sifariş üçün dil üstünlüyü.
- description: Sifariş haqqında qısa təsvir və ya şərh.
    - Taksit əməliyyatları üçün təsvir sahəsinə ayları bu formatda göndərməlisiniz: TAKSIT=6
- hppRedirectUrl: Əməliyyatı tamamladıqdan sonra yönləndiriləcək URL.
- hppCofCapturePurposes: Sifariş üçün Ödəniş səhifəsində Kart-on-File (COF) saxlama məqsədini əhatə edən massiv. Saxlayarkən bütün 3 məlumatı istifadə edin.
- aut: hppCofCapturePurpose ilə birlikdə istifadə olunur. Bu parametr təyin edildikdə, ödəniş səhifəsində kart saxlama üçün seçmə qutusu həmişə aktiv olacaq.
- srcToken.storedId: Bu parametr ödəniş tokenini (Saxlanılan Kart) yaratmaq üçün istifadə olunur.

### Cavab

- id: Sifariş üçün unikal identifikator.
- hppUrl: Sifariş ilə əlaqəli Hosted Payment Page (HPP) URL-i.
- password: Sifariş ilə əlaqəli parol və ya autentifikasiya tokeni.
- status: Sifarişin cari statusu, "Preparing" və ya başqa status ola bilər.
- cvv2AuthStatus: Sifariş üçün CVV2 autentifikasiya tələbi.
- secret: Sifariş ilə əlaqəli gizli və ya əlavə təhlükəsizlik məlumatı.

### Nümunə

Sorğu

```
{
	"order": {
	  "typeRid":"Order_SMS",
    "amount":"1",
    "currency":"AZN",
    "language": "az",
    "title": "Othub",
    "description": "Testdesc",
    "initiationEnvKind":"Browser",
    "hppRedirectUrl":"http://txpgtst.kapitalbank.az",
	  "hppCofCapturePurposes": [
			"UnspecifiedMit",
      "Cit",
      "Recurring"
		],
		"aut":{
			"purpose": "AddCard"
		},
		"srcToken": {
		  "storedId": 1234
		}
	}
}
```

Sadə ödəniş sorğusu:

```
{
	"order": {
	  "typeRid":"Order_SMS",
		"amount":"1",
    "currency":"AZN",
    "language": "az",
    "title": "Othub",
    "description": "Testdesc",
    "hppRedirectUrl":"http://txpgtst.kapitalbank.az"
  }
}
```

Sadə preauthorization sorğusu:

```
{
	"order": {
	  "typeRid":"Order_DMS",
		"amount":"1",
    "currency":"AZN",
    "language": "az",
    "title": "Othub",
    "description": "Testdesc",
    "hppRedirectUrl":"http://txpgtst.kapitalbank.az"
  }
}
```

Account-to-Card (OCT - Sifariş Kredit Əməliyyatı):

```

  {
	"order": {
	  "typeRid":"OCT",
		"amount":"1",
    "currency":"AZN",
    "language": "az",
    "title": "Othub",
    "description": "Testdesc"
  }
}
```

Installment (Taksit) sorğusu:

```
{
    "order": {
        "typeRid":"Order_SMS",
        "amount":"1.0",
        "currency":"AZN",
        "language": "az",
        "description": "TAKSIT=3",
        "hppRedirectUrl":"http://txpgtst.kapitalbank.az"
    }
}
```

Cavab

```
{
  "order": {
    "id": 4595,
    "hppUrl": "https://txpgtst.kapitalbank.az/flex",
    "password": "8xjpd1ejxdma",
    "status": "Preparing",
    "cvv2AuthStatus": "Required",
    "secret": "312866"
  }
}
```

## Mənbə Tokeni Təyin Et

Bu sorğu ödəniş tokeni yaratmaq üçün istifadə olunur.

### URI

POST /order/{ID}/set-src-token?password={{orderPassword}}

### Saxlanılan ID ilə

### Sorğu

- order.initiationEnvKind Sifarişin başlanğıc mühit növünü göstərir, "Server" olaraq göstərilir (MIT/Təkrar əməliyyatlar üçün) və "Browser" (CIT əməliyyatları üçün).
- token.storedId: Saxlanılan kartın identifikatoru.

### Nümunə

Sorğu

```
{
   "order":{
        "initiationEnvKind":"Server"
    },
   "token": {
        "storedId": 5125
   }
}
```

Cavab

```
{
    "order": {
        "status": "Preparing",
        "cvv2AuthStatus": "IneligibleOrder",
        "tdsV1AuthStatus": "IneligibleOrder",
        "tdsV2AuthStatus": "IneligibleOrder",
        "otpAutStatus": "IneligibleOrder",
        "srcToken": {
            "id": 6298,
            "paymentMethod": "Card",
            "role": "Src",
            "status": "Active",
            "regTime": "2024-08-09 15:03:26",
            "displayName": "416974******1778",
            "card": {
                "expiration": "1125",
                "brand": "Visa"
            }
        }
    }
}
```

## Təyinat Tokeni Təyin Et

Bu sorğu Kart Köçürmə axınında təyinat kartını təyin etmək üçün istifadə olunur.

### URI

POST /order/{ID}/set-dst-token?password={{orderPassword}}

### Sorğu

- token.card.panBlock.data: Kart Pan.

### Nümunə

Sorğu

```
{
    "token": {
        "card": {
            "panBlock": {
                "data": "4169741330151778"
            },
            "entryMode": "ECommerce"
        }
    }
}
```

Cavab

```
{
    "order": {
        "status": "Preparing",
        "cvv2AuthStatus": "IneligibleOrder",
        "tdsV1AuthStatus": "IneligibleOrder",
        "tdsV2AuthStatus": "IneligibleOrder",
        "otpAutStatus": "IneligibleOrder",
        "srcToken": {
            "id": 6298,
            "paymentMethod": "Card",
            "role": "Src",
            "status": "Active",
            "regTime": "2024-08-09 15:03:26",
            "displayName": "416974******1778",
            "card": {
                "expiration": "1125",
                "brand": "Visa"
            }
        }
    }
}
```

## Əməliyyatın İcrası

Bu sorğu əməliyyatı yekunlaşdırmaq üçün istifadə olunur.

### URI

POST /order/{ID}/exec-tran

### Sorğu

- phase Əməliyyat mərhələsinin göstəricisi. Mərhələ nümunələri:
    - Single. Bir addımlı əməliyyatlar üçün (Standart Alış)
    - Auth. Preauthorization əməliyyatının ilk mərhələsi üçün. authorizationKind ilə birlikdə istifadə olunmalıdır.
    - Clearing. Preauthorization əməliyyatının ikinci mərhələsi üçün.
- type Əməliyyatın növü. Növ nümunələri:
    - Credit. Kartdan Karta əməliyyat üçün.
    - Refund. Əməliyyatdan pulu geri qaytarmaq üçün.
- amount Əməliyyat üçün təsdiqlənəcək məbləğ. Əgər göstərilməyibsə, məbləğ Sifariş Yaratma Sorğusundakı məbləğdən istifadə ediləcək.
- authorizationKind Preauthorization əməliyyatında Auth mərhələsi ilə birlikdə istifadə olunmalıdır.

conditions.cofUsage Təkrar əməliyyat göstəricisi.

```
{
    "tran":{
        "phase":"Auth",
        "type":"Credit",
        "amount":"1.00",
        "authorizationKind": "Preliminary",
        "conditions":{
            "cofUsage":"Recurring"
        }
    }
}
```

### Nümunə

#### Sorğu

Clearing (Preauthorization əməliyyatının ikinci mərhələsi):

```
{
    "tran":{
        "phase":"Clearing",
        "amount":"1.00"
    }
}
```

Saxlanılan kart ilə əməliyyat:

```

      {
    "tran":{
        "phase":"Single",
        "conditions":{
            "cofUsage":"Recurring"
        }
    }
}
```

Saxlanılan kart ilə Preauthorization əməliyyat:

```
{
    "tran":{
        "phase":"Auth",
        "authorizationKind": "Preliminary",
        "conditions":{
            "cofUsage":"Recurring"
        }
    }
}
```

Account-to-Card (OCT)

```
{
    "tran":{
        "phase":"Single",
        "type":"Credit"
    }
}
```

### Cavab

Uğurlu cavab

```
{
  "tran": {
    "approvalCode": "053703",
    "match": {
      "tranActionId": "240422-13060545-000oed=",
      "ridByPmo": "17302955"
    },
    "pmoResultCode": "1"
  }
}
```

Səhv ilə olan Cavab

```
{
    "errorCode": "PmoDecline",
    "errorDescription": "Transaction declined by PMO: Auth Response: 52 - Card not found for MBR calculation. PAN=416974******1778, ExpDate from Track2 (YYMM)=2511",
    "errorDetails": {
        "declineReason": "SrcCardInvalid",
        "match": {
            "ridByPmo": "17947770"
        },
        "pmoResultCode": "52",
        "pmoDeclineDesc": "Card not found for MBR calculation. PAN=416974******1778, ExpDate from Track2 (YYMM)=2511"
    }
}
```

## Geri Ödəniş (Refund)

Bu əməliyyat pulu əməliyyat üçün geri qaytarmaq məqsədilə istifadə olunur. Sorğu nümunəsi, İcra Əməliyyatı (Execute Transaction) sorğusu ilə eyni və eyni URI-dır.

```
{
    "tran":{
        "phase":"Single",
        "amount":"2.00",
        "type": "Refund"
    }
}
```

## Ləğv Etmə (Reversal)

Bu sorğu gün ərzində əməliyyatı ləğv etmək üçün istifadə olunur.

### URI

POST /order/{ID}/exec-tran

### Sorğu

Sorğu, İcra Əməliyyatı (Execute Transaction) sorğusu ilə eynidir, lakin fərqli parametrlərlə.

- phase Əməliyyat mərhələsinin göstəricisi. Mərhələ nümunələri:
    - Single. Bir addımlı əməliyyatlar üçün (Standart Alış)
    - Auth. Preauthorization əməliyyatının ilk mərhələsi üçün. authorizationKind ilə birlikdə istifadə olunmalıdır.
    - Clearing. Preauthorization əməliyyatının ikinci mərhələsi üçün.
- voidKind Ləğv Etmə əməliyyatının göstəricisi. Ləğv növləri:
    - Full. Əməliyyatın tam məbləğini geri qaytarmaq üçün istifadə olunur.
    - Partial. Əvvəlki məbləğdən az olan vəsaitləri geri qaytarmaq üçün istifadə olunur. Bir dəfə istifadə oluna bilər.

amount Əməliyyat üçün geri qaytarılacaq məbləğ. Yalnız qismən geri qaytarma istifadə edildikdə göstərilməlidir.

```
{
    "tran":{
        "phase":"Single",
        "amount":"1.00",
        "voidKind": "Partial"
    }
}
```

### Nümunə

#### Sorğu

Alışdan sonra tam ləğv etmə

```
{
    "tran":{
        "phase":"Single",
        "voidKind": "Full"
    }
}
```

Alışdan sonra hissəli ləğv etmə

```

    {
    "tran":{
        "phase":"Single",
        "amount":"1.00",
        "voidKind": "Partial"
    }
}
```

Preauthorization sorğusunnan sonra tam ləğv etmə (Birinci mərhələdən sonra)

```
{
    "tran":{
        "phase":"Auth",
        "voidKind": "Full"
    }
}
```

Preauthorization sorğusunnan sonra tam ləğv etmə (İkinci mərhələdən sonra)

```
{
    "tran":{
        "phase":"Clearing",
        "voidKind": "Full"
    }
}
```

## Sifariş Təfərrüatlarını Al (Get Order Details)

Bu sorğu əməliyyat haqqında məlumat almaq üçün istifadə olunur.

### URI

GET /order/{ID}

### Sorğu

Əlavə məlumat almaq üçün URI-ə parametrlər əlavə edə bilərsiniz.

### PARAMETRLƏR

- tranDetailLevel=2 : Bu parametr əməliyyat haqqında bütün məlumatları əlavə edir.
- tokenDetailLevel=2 : Bu parametr ödəniş tokeni və ya kart haqqında bütün məlumatları əlavə edir.
- orderDetailLevel=2 : Bu parametr sifariş haqqında bütün məlumatları əlavə edir.

### Nümunə

Sorğu

https://txpgtst.kapitalbank.az/api/order/1111/?&tranDetailLevel=2&tokenDetailLevel=2&orderDetailLevel=2

Cavab

Parametrsiz sadə cavab

```
{
    "order": {
      "id": 5531,
      "typeRid": "Order_SMS",
      "status": "Refunded",
      "prevStatus": "FullyPaid",
      "lastStatusLogin": "E1010",
      "amount": 1,
      "currency": "AZN",
      "createTime": "2024-06-12 15:38:23",
      "finishTime": "2024-06-12 15:39:17",
      "title": "Othub",
      "type": {
        "title": "Single message"
      }
    }
  }
```

Detallı cavab bütün parametrlərlə

```
{
    "order": {
      "id": 5531,
      "hppUrl": "https://txpgtst.kapitalbank.az/flex",
      "hppRedirectUrl": "http://txpgtst.kapitalbank.az",
      "password": "1a06f5aj3yhqr",
      "status": "Refunded",
      "prevStatus": "FullyPaid",
      "lastStatusLogin": "E1010",
      "amount": 1,
      "currency": "AZN",
      "terminal": {
        "id": 41,
        "rid": "E1000010",
        "title": "E1000010",
        "mcc": 3011,
        "status": "Active"
      },
      "srcAmount": 1,
      "srcAmountFull": 1,
      "srcCurrency": "AZN",
      "dstAmount": 1,
      "dstCurrency": "AZN",
      "createTime": "2024-06-12 15:38:23",
      "finishTime": "2024-06-12 15:39:17",
      "trans": [
        {
          "approvalCode": "047347",
          "actionId": "240612-11385786-000tn5=",
          "orderId": 5531,
          "terminalId": 41,
          "merchantId": 101,
          "billingStatus": "Normal",
          "isReversal": false,
          "ridByAcquirer": "17579346",
          "ridByPmo": "17579346",
          "regTime": "2024-06-12 15:38:57",
          "clearAmount": 1,
          "clearCcy": "AZN",
          "amount": 1,
          "currency": "AZN",
          "description": "Purchase",
          "phase": "Single",
          "type": "Purchase",
          "pmoResultCode": "1"
        },
        {
          "approvalCode": "963348",
          "actionId": "240612-11391689-000tn7=",
          "orderId": 5531,
          "terminalId": 41,
          "merchantId": 101,
          "billingStatus": "Normal",
          "isReversal": false,
          "ridByAcquirer": "17579348",
          "ridByPmo": "17579348",
          "regTime": "2024-06-12 15:39:16",
          "clearAmount": -1,
          "clearCcy": "AZN",
          "amount": 1,
          "currency": "AZN",
          "description": "Refund",
          "phase": "Single",
          "type": "Refund",
          "pmoResultCode": "1"
        }
      ],
      "cvv2AuthStatus": "Provided",
      "tdsV1AuthStatus": "IneligibleOrder",
      "tdsV2AuthStatus": "Verified",
      "tdsServerUrl": "http://172.21.14.67:1341",
      "authorizedChargeAmount": 1,
      "clearedChargeAmount": 1,
      "clearedRefundAmount": 1,
      "title": "Othub",
      "description": "Testdesc",
      "language": "az",
      "srcToken": {
        "id": 4833,
        "paymentMethod": "Card",
        "role": "Src",
        "status": "Active",
        "regTime": "2024-06-12 15:38:28",
        "entryMode": "ECommerce",
        "displayName": "416974******1778",
        "owner": {},
        "card": {
          "authentication": {
            "needCvv2": false,
            "needTds": false,
            "tranId": "a3b35fe8-e245-4a3e-ba01-e250a4ac20ad",
            "tdsDsTranId": "c087b446-192b-48fb-b78f-2c4bb53ac26c",
            "timestamp": "2024-06-12 11:38:23",
            "tdsProtocolVer": "2.2.0",
            "cryptType": "Tds",
            "cryptVal": "AJkBA0KTRAAAAABklEFkdQAAAAA=",
            "eci": "05",
            "tdsARes": "{"threeDSServerTransID":"a3b35fe8-e245-4a3e-ba01-e250a4ac20ad","acsTransID":"6663aebe-7f7a-4f34-be7f-bdb9731c1adf","dsTransID":"c087b446-192b-48fb-b78f-2c4bb53ac26c","messageType":"ARes","messageVersion":"2.2.0","messageExtension":[{"name":"MesExt2","id":"ID2","criticalityIndicator":false,"data":{"valueOne":"value"}}],"dsReferenceNumber":"DSRefNumVISA","acsReferenceNumber":"3DS_LOA_ACS_COPL_020100_00081","acsOperatorID":"ACS-V210-KAPITAL-BANK-78858","authenticationValue":"AJ************************A=","eci":"05","transStatus":"Y","transStatusReason":"17"}"
          },
          "expiration": "1126",
          "brand": "Visa",
          "issuerRid": "4"
        }
      },
      "merchant": {
        "id": 101,
        "rid": "E1000010",
        "title": "E1000010",
        "businessAddress": {
          "country": "AZE",
          "countryA2": "AZ",
          "countryN3": 31
        },
        "trustConsumerPhone": false
      },
      "initiationEnvKind": "Server",
      "type": {
        "allowVoid": true,
        "hppTranPhase": "Single",
        "secretLength": 6,
        "title": "Single message",
        "rid": "Order_SMS",
        "paymentMethods": [
          "Card"
        ],
        "cardBrands": [
          "Visa",
          "Mastercard"
        ],
        "allowTdsAttempt": false,
        "allowTdsCant": false,
        "allowTdsChallenged": false,
        "allowSurcharge": false,
        "allowTranTypes": [
          "Purchase",
          "Refund",
          "CheckToken"
        ],
        "allowTranPhases": [
          "Single",
          "Prepare"
        ],
        "allowAuthKinds": [
          "Final",
          "Undefined"
        ],
        "allowCofStoreUsages": [
          "Cit",
          "PartialShipment",
          "Instalment",
          "Recurring",
          "UnspecifiedMit",
          "DelayedCharge"
        ],
        "orderClass": "Sale",
        "allowCVV2": true
      },
      "hppCofCapturePurposes": [
        "UnspecifiedMit"
      ],
      "custAttrs": [],
      "reportPubs": {}
    }
  }
```

Detallı cavab saxlanılan kart məlumati ilə bir yerdə (storedTokens.id)

```
{
    "order": {
      "id": 10947,
      "hppUrl": "https://txpgtst.kapitalbank.az/flex",
      "hppRedirectUrl": "http://txpgtst.kapitalbank.az",
      "password": "mzvjai9qsj8x",
      "status": "FullyPaid",
      "prevStatus": "Preparing",
      "lastStatusLogin": "E1010",
      "amount": 5,
      "currency": "AZN",
      "terminal": {
        "id": 41,
        "rid": "E1000010",
        "title": "E1000010",
        "mcc": 3011,
        "status": "Active"
      },
      "srcAmount": 5,
      "srcAmountFull": 5,
      "srcCurrency": "AZN",
      "dstAmount": 5,
      "dstCurrency": "AZN",
      "createTime": "2024-07-30 16:57:36",
      "storedTokens": [
        {
          "id": 5654
        }
      ],
      "trans": [
        {
          "approvalCode": "511369",
          "actionId": "240730-12583839-001drl=",
          "orderId": 10947,
          "terminalId": 41,
          "merchantId": 101,
          "billingStatus": "Normal",
          "isReversal": false,
          "ridByAcquirer": "17850012",
          "ridByPmo": "17850012",
          "regTime": "2024-07-30 16:58:38",
          "clearAmount": 5,
          "clearCcy": "AZN",
          "amount": 5,
          "currency": "AZN",
          "description": "Purchase",
          "phase": "Single",
          "type": "Purchase",
          "pmoResultCode": "1"
        }
      ],
      "cvv2AuthStatus": "Provided",
      "tdsV1AuthStatus": "IneligibleOrder",
      "tdsV2AuthStatus": "Verified",
      "tdsServerUrl": "http://172.21.14.67:1340",
      "authorizedChargeAmount": 5,
      "clearedChargeAmount": 5,
      "clearedRefundAmount": 0,
      "title": "Othub",
      "description": "Testdesc",
      "language": "az",
      "srcToken": {
        "id": 5652,
        "paymentMethod": "Card",
        "role": "Src",
        "status": "Active",
        "regTime": "2024-07-30 16:57:43",
        "entryMode": "ECommerce",
        "displayName": "510307******3118",
        "owner": {},
        "card": {
          "authentication": {
            "needCvv2": false,
            "needTds": false,
            "tranId": "0682c816-a368-4f66-9c27-ea2298b8b2a8",
            "tdsDsTranId": "fd1a1d37-1ec8-4d47-a8cd-6f1d640d8425",
            "timestamp": "2024-07-30 12:57:36",
            "tdsProtocolVer": "2.2.0",
            "cryptType": "Tds",
            "cryptVal": "xgR6+aR8AAAAAAAAAAAAAAAAAAAA",
            "eci": "02",
            "tdsARes": "{"threeDSServerTransID":"0682c816-a368-4f66-9c27-ea2298b8b2a8","acsTransID":"ace44ca4-df3d-478d-9553-dd20174169d8","dsTransID":"fd1a1d37-1ec8-4d47-a8cd-6f1d640d8425","messageType":"ARes","messageVersion":"2.2.0","messageExtension":[{"name":"MesExt2","id":"ID2","criticalityIndicator":false,"data":{"valueOne":"value"}}],"dsReferenceNumber":"DSRefNum","acsReferenceNumber":"3DS_LOA_ACS_COPL_020100_00081","acsChallengeMandated":"N","acsOperatorID":"ACS-V210-KAPITAL-BANK-78858","acsURL":"https://acs1test.kapitalbank.az","authenticationType":"02","transStatus":"C"}",
            "tdsRReq": "{"threeDSServerTransID":"0682c816-a368-4f66-9c27-ea2298b8b2a8","acsTransID":"ace44ca4-df3d-478d-9553-dd20174169d8","dsTransID":"fd1a1d37-1ec8-4d47-a8cd-6f1d640d8425","messageType":"RReq","messageVersion":"2.2.0","authenticationMethod":"02","authenticationType":"02","authenticationValue":"xg************************AA","eci":"02","interactionCounter":"01","messageCategory":"01","transStatus":"Y"}"
          },
          "expiration": "0125",
          "brand": "Mastercard",
          "issuerRid": "5"
        }
      },
      "merchant": {
        "id": 101,
        "rid": "E1000010",
        "title": "E1000010",
        "businessAddress": {
          "country": "AZE",
          "countryA2": "AZ",
          "countryN3": 31
        },
        "trustConsumerPhone": false
      },
      "initiationEnvKind": "Browser",
      "type": {
        "allowVoid": true,
        "hppTranPhase": "Single",
        "secretLength": 6,
        "title": "Single message",
        "rid": "Order_SMS",
        "paymentMethods": [
          "Card"
        ],
        "cardBrands": [
          "Visa",
          "Mastercard"
        ],
        "allowTdsAttempt": false,
        "allowTdsCant": false,
        "allowTdsChallenged": false,
        "allowSurcharge": false,
        "allowTranTypes": [
          "Purchase",
          "Refund",
          "CheckToken"
        ],
        "allowTranPhases": [
          "Single",
          "Prepare"
        ],
        "allowAuthKinds": [
          "Final",
          "Undefined"
        ],
        "allowCofStoreUsages": [
          "Cit",
          "PartialShipment",
          "Instalment",
          "Recurring",
          "UnspecifiedMit",
          "DelayedCharge"
        ],
        "orderClass": "Sale",
        "allowCVV2": true
      },
      "hppCofCapturePurposes": [
        "UnspecifiedMit",
        "Cit",
        "Recurring"
      ],
      "custAttrs": [],
      "reportPubs": {}
    }
  }
```

## Google Pay™ İnteqrasiyası

Əgər siz Google Pay™ vasitəsilə ödənişlərin işlənməsini aktivləşdirmək istəyirsinizsə, zəhmət olmasa, kuratorunuzla əlaqə saxlayın və o, bu funksiyanı sizin əsas girişinizə əlavə edəcək.

## Google Pay™ üçün məlumatlar

- gatewayid: ecommercekapitalbank
- gatewayMerchantId: testmerch

Qeyd: Bu gatewayMerchantId yalnız test mühitində əməliyyatlar aparmaq üçün istifadə olunur. Testlər uğurla keçildikdən sonra sizə istehsalat mühitində istifadə üçün öz gatewayMerchantId təqdim olunacaq.

#### İnteqrasiya üçün sənəd bağlantıları:

- Android: [https://developers.google.com/pay/api/android/overview?hl=ru](https://developers.google.com/pay/api/android/overview?hl=ru)
- Web: https://developers.google.com/pay/api/web/overview?hl=ru
- Design Guidline: [https://developers.google.com/pay/api/web/guides/brand-guidelines?hl=ru](https://developers.google.com/pay/api/web/guides/brand-guidelines?hl=ru)
- Google Pay and Wallet APIs Acceptable Use Policy: [https://payments.developers.google.com/terms/aup?hl=ru](https://payments.developers.google.com/terms/aup?hl=ru)
- Google Pay API Terms of Service [https://payments.developers.google.com/terms/sellertos](https://payments.developers.google.com/terms/sellertos)

## Əməliyyat axını

- Müştəri internet mağazanın veb-saytında məhsul seçir.
- Satıcı Kapital Bank-a Create Order əməliyyatını yerinə yetirmək üçün sorğu göndərərək sifariş yaradır.

Sorğu

POST /order

```
{
    "order": {
        "typeRid":"GN3D",
        "amount":"1.0",
        "currency":"AZN",
        "description": "Testdesc"
    }
}
```

Cavab

```
{
    "order": {
        "id": 29575,
        "hppUrl": "https://txpgtst.kapitalbank.az/flex",
        "password": "113bl56jgrz5l",
        "status": "Preparing",
        "cvv2AuthStatus": "Required",
        "secret": "513391"
    }
}
```

Qeyd: İki əməliyyat növü (Cryptogram3DS və PAN_ONLY) üçün müxtəlif typeRid dəyərlərindən istifadə edilməlidir. Varsayılan olaraq Cryptogram3DS üçün GN3D, PAN_ONLY üçün isə GSMS istifadə olunur. Bu dəyərlər terminal parametrlərinizdən asılı olaraq fərqlənə bilər və kuratorunuz tərəfindən ayrıca təqdim ediləcək.

- Kapital Bank sifarişi yaradır və sifariş ID-si və digər məlumatlarla birlikdə cavab göndərir.
- Müştəri Google Pay™ ilə ödəniş seçir.
- Müştəriyə Google Pay™ xidmətinin dialoq pəncərəsi göstərilir, Google hesabına giriş etmək, kart və çatdırılma ünvanını seçmək təklif olunur.
- Satıcı Google Pay™ ödəniş məlumatlarını googlePayBlock parametrində Kapital Bank-a göndərir. Kapital Bank, şifrələmə açarından istifadə edərək məlumatları deşifrə edir və sifariş məlumatlarını təhlil edir. Bunun nəticəsində 3DS v1.x / 3DS v2.x protokolu ilə doğrulama tələb oluna bilər. Bu sorğuda satıcı ödəniş tokenindən alınan JSON-u HEX formatında göndərməlidir.

Sorğu

/order/{{OrderId}}/set-src-token

```
{
    "token": {
        "googlePayBlock": "7B227369676E6174757265223A224D4559434951432B354F6C3748565A657A585174574C6A3667735074324A2F3671554D4E302B4A4134314E49466C657357514968414C3249685545646376305363646A626246377436553078305655334B666D444830574D306B515933617766222C22696E7465726D6564696174655369676E696E674B6579223A7B227369676E65644B6579223A227B5C226B657956616C75655C223A5C224D466B77457759484B6F5A497A6A3043415159494B6F5A497A6A3044415163445167414544713939545136702B6F76342F624E7136706C4E2B79547943324975646B4476697A6B6E456B466B734936476B4C742F65734C4E4A385A78644B44476D6A79305472646447423074725275483452535A6A66443778515C5C75303033645C5C75303033645C222C5C226B657945787069726174696F6E5C223A5C22313733323236303937333038395C227D222C227369676E617475726573223A5B224D4555434951446B383746656C4F52507062556C513637545039484E3838533048423658756635745551573276787A7050674967576C382F4A347276626A6971707630364544475A49736773425357367038626B4A486D69334852667446555C7530303364225D7D2C2270726F746F636F6C56657273696F6E223A2245437632222C227369676E65644D657373616765223A227B5C22656E637279707465644D6573736167655C223A5C224F2B3534746E2B7051426B763543376746694230776E7A6D39594A7853686C643953796C776D6F61474D6C446F7A3541735433564A4E3464416A7977454537517844686F58337A4C47687734693152706F34767147517642424F4F70796A38634758363370474E38483845364965724D47684846355836333066702B4D464B784F476A784D734667566C76445241497335573074762B36634D4B5A6F7662376D56504D75677664736F48535A2F713441545A42375549334A736E7144496A4C79515633674E47614C694D30424B57446D4841426B416F76785A736E65306C4273334A6C756257724B6E642F4D6962524556744954717A424B57376A76556C4A70377042394F754339676C50675842784735473575346E336E59322B51313344494B6B48774E5A6E59764F626D754D684579442F6274624C655A454E777233614B55477035677566794A6774555148616B4E46336569484452566E68726E6C49337275467835762B682B5238484257366E5864646278423658637638433049323571583552365A4E6C51685237617A6F2F6E59755938367632776C6E734B4D5835782B756A6A356C75344A624237476A5A49697364744177414F6570666C4854643133694872664667794E426E787277483453425A4149316F48613137674E5769694C644B517365364C39524D35314E52454B696875564D4D724E3641724A59422F5472766B6A517A3672746162796A374D54497677574E74513550745630414D4477536447446353783453756E515C5C75303033645C5C75303033645C222C5C22657068656D6572616C5075626C69634B65795C223A5C224250684A563543627A6735556A5A2F31725761665576634E496C4747663672486C43326E386731474868592B6135344D702B6156356F4B752F782B66706B4C63566D36447170332F70555A6473384648714678464E79345C5C75303033645C222C5C227461675C223A5C224A4565536161524957512F6843706565494F737062734A51365078533359336E744A6C4B546275475A706B5C5C75303033645C227D227D"
    }
}
```

Sorğu

```

    {
    "order": {
        "status": "Preparing",
        "cvv2AuthStatus": "IneligibleOrder",
        "tdsV1AuthStatus": "IneligibleOrder",
        "tdsV2AuthStatus": "IneligibleOrder",
        "otpAutStatus": "IneligibleOrder",
        "srcToken": {
            "id": 23516,
            "paymentMethod": "GooglePay",
            "role": "Src",
            "status": "Active",
            "regTime": "2024-11-15 10:58:36",
            "displayName": "411111******1111",
            "card": {
                "expiration": "1226",
                "brand": "Visa"
            }
        }
    }
}
```

- Kapital Bank-dan cavab alındıqdan sonra satıcı, ödənişi maliyyələşdirmək üçün Execute Order Transaction əməliyyatını Kapital Bank-a göndərir.

Sorğu

/order/{{OrderId}}/exec-tran

```
{
    "tran":{
        "phase":"Single",
    }
}
```

- Maliyyə əməliyyatının nəticəsindən asılı olaraq, Kapital Bank sifarişə müvafiq status verir: Tam ödənilib / Əməliyyat rədd edildi.
- Satıcı, müştəriyə sifariş haqqında məlumatı internet mağazanın veb-saytında göstərir.

## Ödəniş Statusları

|  |
|

## Errorlar

|  |
|

## PmoDecline Kodları (Processing Error codes)

|  |
|
