# Integrify

**Integrify** — üçüncü tərəf API inteqrasiyalarını rahatlaşdıran Python kitabxanasıdır.
Hər inteqrasiya ayrıca paket kimi dərc olunur; yalnız lazım olanı quraşdırırsınız:

```bash
pip install integrify                 # yalnız daxili nüvə (core)
pip install integrify[epoint]         # core + EPoint
pip install integrify[epoint,lsim]    # core + EPoint + LSIM
pip install integrify[all]            # bütün inteqrasiyalar
```

Bütün sorğuların həm **sinxron**, həm də **asinxron** versiyası var və tam tip dəstəyi (type hints) ilə gəlir.

## İnteqrasiyalar

| İnteqrasiya     | Növ                        | Sənəd                                                                  |
| :-------------- | :------------------------- | :--------------------------------------------------------------------- |
| EPoint          | Ödəniş                     | [Keçid](integrations/epoint/index.md)                                  |
| Kapital Bank    | Ödəniş                     | [Keçid](integrations/kapitalbank/index.md)                             |
| Azericard       | Ödəniş                     | [Keçid](integrations/azericard/index.md)                               |
| LSIM            | SMS                        | [Keçid](integrations/lsim/index.md)                                    |
| Posta Güvərçini | SMS                        | [Keçid](integrations/posta-guvercini/index.md)                         |
| Clopos          | Restoran idarəetməsi (POS) | [Keçid (EN)](https://integrify.mmzeynalli.dev/en/integrations/clopos/) |
| ECustoms        | Logistika (məxfi)          | [Keçid](integrations/ecustoms/index.md)                                |

> Clopos (POS) inteqrasiyasının sənədi hələlik yalnız **[İngiliscə](https://integrify.mmzeynalli.dev/en/)** mövcuddur.

## Töhfə

Layihə [GitHub](https://github.com/integrify-sdk/integrify-python)-da açıq mənbədir. Töhfələr gözlənilir!
