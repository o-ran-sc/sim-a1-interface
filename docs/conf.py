from docs_conf.conf import *

language = 'en'

linkcheck_ignore = [
    'http://localhost.*',
    'http://127.0.0.1.*',
    'https://gerrit.o-ran-sc.org.*'
]

extensions = [
   'sphinxcontrib.openapi',
]
