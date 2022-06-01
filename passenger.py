import sys, os
INTERP = "/home/james_main/hnjplusenv/bin/python3" # absolute path to your virtual env
#INTERP is present twice so that the new python interpreter 
#knows the actual executable path 
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)
cwd = os.getcwd()
sys.path.append(cwd)
sys.path.append(cwd + '/main')  # name of your Django project
sys.path.insert(0,cwd+'../hnjplusenv/bin') # virtual env # relative path to your virtual env
sys.path.insert(0,cwd+'../hnjplusenv/lib/python3.9/site-packages') # relative path to your virtual env
os.environ['DJANGO_SETTINGS_MODULE'] = "main.settings" # name of your Django project
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
