# -*- coding: utf-8 -*-

import os, sys

sys.path.insert(0, '/home/a/andrewfekl/andrewfekl.beget.tech/extrasense_testing')
sys.path.insert(1, '/home/a/andrewfekl/andrewfekl.beget.tech/ djangoenv/lib/python3.9/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'coolsite.settings'
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()