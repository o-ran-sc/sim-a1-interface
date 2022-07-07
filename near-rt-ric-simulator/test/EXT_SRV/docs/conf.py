from docs_conf.conf import *

language = 'en'

extensions = [
   # ...
   #'sphinxcontrib.redoc',
   'sphinxcontrib.openapi',
]

## sphinxcontrib works fine as well
#redoc = [
    #{
        #'name': 'External Server API',
        #'page': 'EXT_SRV_api',
        #'spec': '../api/EXT_SRV_api.yaml',
        #'embed': True,
    #}
#]

linkcheck_ignore = [
    'http://localhost.*',
    'http://127.0.0.1.*',
    'https://gerrit.o-ran-sc.org.*'
]
