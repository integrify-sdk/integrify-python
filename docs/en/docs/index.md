# Integrify

**Integrify** is a Python library that simplifies third-party API integrations.
Every integration ships as its own package — install only what you need:

```bash
pip install integrify                 # shared core only
pip install integrify[clopos]         # core + Clopos
pip install integrify[all]            # every integration
```

Every request comes in both **sync** and **async** flavours, with full type-hint support.

## Integrations

| Integration | Type                | Docs                                                                         |
| :---------- | :------------------ | :--------------------------------------------------------------------------- |
| Clopos      | POS                 | [Open](integrations/clopos/index.md)                                         |
| E-Customs   | Logistics (private) | [Open :material-lock:](/private/ecustoms/){ title="Password required" } (AZ) |

> The Azerbaijani payment & SMS integrations (EPoint, Kapital Bank, Azericard, LSIM, Posta Güvərçini)
> are currently documented in **[Azerbaijani](https://integrify.mmzeynalli.dev/az/)**.

## Contributing

The project is open source on [GitHub](https://github.com/integrify-sdk/integrify-python). Contributions welcome!
