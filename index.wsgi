import sae

from wechooser import wsgi

application = sae.create_wsgi_app(wsgi.application)
