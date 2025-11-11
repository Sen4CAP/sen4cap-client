# Python API Reference

The `sen4cap_client.Client` class provides a synchronous API for interacting with 
the Sen4CAP processing service.
If you want an asynchronous version, use the `AsyncClient` class instead.
It provides the same interface, but using asynchronous server calls.

Both clients return their configuration as a `sen4cap_client.ClientConfig` object.

Methods of the `sen4cap_client.Client` and `sen4cap_client.AsyncClient` 
may raise a `sen4cap_client.ClientError` if a server call fails. 

The `sen4cap_client` Python API is a thin wrapper around the 
[Eozilla](https://eo-tools.github.io/eozilla/) Client API 
called [Cuiman](https://eo-tools.github.io/eozilla/client-api/).
 