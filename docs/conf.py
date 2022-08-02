from docs_conf.conf import *

branch = 'latest'

language = 'en'

linkcheck_ignore = [
    'http://localhost.*',
    'http://127.0.0.1.*',
    'https://gerrit.o-ran-sc.org.*',
    './EXT_SRV_api.html', #Generated file that doesn't exist at link check.
]

extensions = ['sphinxcontrib.redoc']

redoc = [
            {
                'name': 'CALLOUT SERVER',
                'page': 'EXT_SRV_api',
                'spec': '../near-rt-ric-simulator/test/EXT_SRV/api/EXT_SRV_api.yaml',
                'embed': True,
            }
        ]

redoc_uri = 'https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js'
