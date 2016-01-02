# clicksign-python
Python API for ClickSign [reference](https://clicksign.readme.io/)

## Installation

Place the file `ClickSign.py` somewhere in your python path

## Usage

First you need to create a ClickSign object for either the demo or the live environment

	import ClickSign as cs
	token = '--your-clicksign-api-token--'
	c = cs.ClickSignDemo(token)  # to use the demo API
	c = cs.ClickSign(token)      # to use the production API

This object can then be used to make the API calls, for example to **get a list of all your documents** [ref](https://clicksign.readme.io/docs/documentos)

	docs = c.documents()
  
or to **get the information for a single document** [ref](https://clicksign.readme.io/docs/visualizacao)

	key = '--the-document-key--'
	doc = c.document(key)

or to **download a document** [ref](https://clicksign.readme.io/docs/download)

	doc_dl = c.download(key)
  
Apart from the above informational API calls you can also make calls that **create a new document** [ref](https://clicksign.readme.io/docs/upload)

	filename = '/path/to/document.pdf'
	result = c.upload(filename)
	new_key = result.json()['document']['key']

or that **add a signature list to a document** [ref](https://clicksign.readme.io/docs/lista-de-assinatura)

	siglist = {'signer@example.com': ClickSign.SIGN, 'approver@example.come': ClickSign.APPR}
	message = 'PLease find the attached document'
	skip_email = False
	result = c.siglist(new_key, siglist, message, skip_email)
  
or that **add a webhook to a document** (note that in future versions per-document webhooks are no longer supported) [ref](https://clicksign.readme.io/docs/webhooks)

	hook_url = 'https://webhooks.example.com/'
	result = c.webhook(new_key, hook_url)


## Notes

A number of API elements have not yet been implemented, but their implementation is straight forward
- resend email [ref](https://clicksign.readme.io/docs/reenvio-de-email)
- cancel a document [ref](https://clicksign.readme.io/docs/cancelamento)
- batch processing [ref](https://clicksign.readme.io/docs/lotes)
- combined upload & signature list [ref](https://clicksign.readme.io/docs/upload-e-lista-de-assinatura)

## Version History

- Version 1.0 (2 Jan 2016): major API components implemented

