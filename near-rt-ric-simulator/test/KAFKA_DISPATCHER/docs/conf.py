from docs_conf.conf import *

branch = 'latest'

language = 'en'

linkcheck_ignore = [
    'http://localhost.*',
    'http://127.0.0.1.*',
    'https://gerrit.o-ran-sc.org.*',
    './KAFKA_DISPATCHER_api.html'
]

extensions = ['sphinxcontrib.redoc']

redoc = [
            {
                'name': 'Kafka Message Dispatcher',
                'page': 'KAFKA_DISPATCHER_api',
                'spec': '../api/KAFKA_DISPATCHER_api.yaml',
                'embed': True,
            },
        ]

redoc_uri = 'https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js'
