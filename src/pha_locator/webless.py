import imp

from django.core.management import setup_environ

try:
    imp.find_module('settings') # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
    sys.exit(1)


import settings
setup_environ(settings)
from src.pha_locator.apps.phas.models import Pha

has = Pha.objects.filter(web_page_address='')
for ha in has:
    print ha.name, ha.email_address, ha.web_page_address

print len(has)
