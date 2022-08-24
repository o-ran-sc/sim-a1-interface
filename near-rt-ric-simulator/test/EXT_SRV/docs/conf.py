from docs_conf.conf import *

language = 'en'

extensions = [
   'sphinxcontrib.openapi',
]

linkcheck_ignore = [
    'http://localhost.*',
    'http://127.0.0.1.*',
    'https://gerrit.o-ran-sc.org.*'
]
