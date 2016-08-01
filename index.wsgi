import sae
sae.add_vendor_dir('packages')

from wechooser import wsgi

application = sae.create_wsgi_app(wsgi.application)
