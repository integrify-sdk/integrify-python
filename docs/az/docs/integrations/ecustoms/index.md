# E-Customs

Azərbaycan Respublikası Dövlət Gömrük Komitəsinin (DGK) daşıyıcı şirkətlər üçün
nəzərdə tutulmuş `Carriers V4` API-si üçün Integrify inteqrasiyası.

???+ warning "Bu inteqrasiya məxfidir"
    `integrify-ecustoms` paketi **ictimai deyil** və PyPI-a dərc olunmur. DGK-nın
    `Carriers V4` API-si daşıyıcı şirkətlərlə bağlanan müqavilə əsasında verildiyi
    üçün, paketin kodu və sənədi yalnız girişi olan komandalar üçün açıqdır.

## Nə edir? { #what-it-does }

Daşıyıcı şirkətin anbarına daxil olan bağlamaların DGK-da qeydiyyatını, vətəndaş
bəyannamələrinin alınmasını və gömrük əməliyyatlarının izlənməsini avtomatlaşdırır:
bağlamanın bildirilməsi → bəyannamənin alınması və təsdiqlənməsi → qutuya yığılma →
depeş → gömrük əməliyyatlarının izlənməsi.

Digər inteqrasiyalar kimi eyni `integrify` namespace-ini paylaşır:

```python
from integrify.ecustoms import ECustomsClient      # məxfi paket
```

## Giriş { #access }

Paketə giriş üçün DGK ilə daşıyıcı müqaviləniz olmalıdır. Müraciət üçün:
[integrify-sdk](https://github.com/integrify-sdk) komandası ilə əlaqə saxlayın.

Giriş verildikdən sonra paket birbaşa məxfi repodan quraşdırılır:

```toml
[tool.uv.sources]
integrify-ecustoms = { git = "ssh://git@github.com/integrify-sdk/integrify-ecustoms-python.git", subdirectory = "packages/ecustoms", tag = "v1.0.0" }
```

## Sənəd { #docs }

Sorğuların tam siyahısı, mühit dəyişənləri və API referansı şifrə ilə qorunan
[məxfi sənəd bölməsindədir](/private/ecustoms/). Giriş məlumatları paketə giriş
verilən komandalara ayrıca təqdim olunur.
