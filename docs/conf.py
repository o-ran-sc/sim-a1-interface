from docs_conf.conf import *

branch = 'latest'

language = 'en'

linkcheck_ignore = [
    'http://localhost.*',
    'http://127.0.0.1.*',
    'https://gerrit.o-ran-sc.org.*',
]

extensions = ['sphinxcontrib.openapi']

# sphinxcontrib-openapi synthesises HTTP request/response examples
# whose bodies (e.g. enum literal values, free-form 'string'
# placeholders) Pygments' http lexer rejects. The extension already
# falls back to relaxed-mode lexing, but the warnings are promoted to
# errors under sphinx-build -W. Suppress them since the rendered
# output is correct.
suppress_warnings = ['misc.highlighting_failure']

# The Kafka Message Dispatcher API spec uses non-standard HTTP status
# code 419 ("KafkaMessagePublishFailed"). sphinxcontrib-httpdomain's
# strict mode treats unknown status codes as docutils errors; disable
# it so the spec renders without aborting sphinx-build -W.
http_strict_mode = False
