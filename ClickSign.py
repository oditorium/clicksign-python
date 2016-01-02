"""thin wrapper around the ClickSign API

docs - <https://clicksign.readme.io/>
account url - <https://desk.clicksign-demo.com/> <https://desk.clicksign.com/>


DEPENDENCIES
------------

## requests 
- documentation:  <http://docs.python-requests.org/>
- installation:   `pip install requests`

COPYRIGHT
------------
(c) Copyright Stefan Loesch 2016, All Rights Reserved
Licensed under an MIT Licences (see LICENSE file)
"""
__version__ = "1.0"
__version_dt__ = "2016-01-02"

import requests
import zipfile as zf
from io import BytesIO
import json


######################################################################################
## CLASS CLICKSIGN DEMO

class ClickSignDemo():
    """API wrapper for the ClickSign Demo API"""

    def __init__(s, token=None):
        s._token = token

    # constant for the different signature actions
    SIGN  = 'sign'
    APPR  = 'approve'
    ACK   = 'acknowledge'
    PARTY = 'party'
    WITN  = 'witness'
    INTV  = 'intervenient'
    RCPT  = 'receipt'

    # the API URL
    _API   = 'https://api.clicksign-demo.com/v1'


    ############################################################################
    ## PRIVATE METHODS
     
    def _url(s, url):
        """assembles the endpoint url"""
        url = s._API+url+"?access_token="+s._token
        return url
    
    def _get(s, url):
        """standard GET request"""
        headers = {'Accept': 'application/json'}
        r = requests.get(s._url(url), headers=headers)
        return r
    
    def _post(s, url, data=None, files=None):
        """standard POST request"""
        headers = {'Accept': 'application/json'}
        if data != None:
            if files != None: raise RunTimeError("cant have both files and data")
            headers['Content-Type'] = 'application/json'
        r = requests.post(s._url(url), headers=headers, files=files, data=data)
        return r


    ############################################################################
    ## API METHODS

    def documents(s):
        """get info on all the user's documents"""
        rq = s._get('/documents')
        if rq.status_code == 200: return rq.json()
        return None

    def document(s, key):
        """get info on one of the user's documents"""
        rq = s._get('/documents/{}'.format(key))
        if rq.status_code == 200: return rq.json()
        return None

    def download(s, key):
        """download a document"""
        rq = s._get('/documents/{}/download'.format(key))
        r = {}
        if rq.status_code == 202: 
            r['success']  = True
            r['complete'] = False
            return r
        if rq.status_code == 200:
            r['success']   = True
            r['complete']  = True
            r['file']      = zf.ZipFile(BytesIO(rq.content))
            r['filename']  = rq.headers['Content-Disposition'].rpartition('=')[2].strip('"')
            return r
        return {'success': False}

    def upload (s, fname):
        """upload a document into the system"""
        files = {'document[archive][original]': (fname, open(fname, 'rb'), 'application/pdf')}
        rq = s._post('/documents', files=files)
        return rq

    def siglist(s, key, sigl, message='', skip_email=False):
        """uploads a signature list for a document

        sigl is like {'a@b.net': ClickSign.SIGN, 'c@d.net': ClickSign.APPR}
        """
        signers = [{'email': k, 'act': sigl[k]} for k in sigl]
        data = {
            'signers'   : signers,
            'message'   : message,
            'skip_email': skip_email,
        }
        rq = s._post('/documents/{}/list'.format(key), data=json.dumps(data))
        return rq

    def webhook(s, key, hook):
        """sets webhook for document (deprecated; there will be one webhook only)"""
        data = {
            'url' : hook,
        }
        rq = s.post('/documents/{}/hooks'.format(key), data=json.dumps(data))
        return rq



######################################################################################
## CLASS CLICKSIGN 

class ClickSign(ClickSignDemo):
    """API wrapper for the ClickSign API"""

    def __init__(s, token=None):
        s._token = token
    
    _API   = 'https://api.clicksign.com/v1'
    
