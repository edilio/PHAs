import os, re 
import ho.pisa as pisa
from django.conf import settings
import tempfile


def tmpfile(max_size=131072, dir=None, pre="tmp_", suf=".pdf"):
    if dir is None:
        dir = tempfile.gettempdir()
    try:
        file = tempfile.SpooledTemporaryFile(max_size=max_size, dir=dir, prefix=pre, suffix=suf)
    except:
        print "Error: can't created temporary file"

    return file


def fetch_resources(uri, rel):
    """
    Callback to allow pisa/reportlab to retrieve Images,Stylesheets, etc.
    `uri` is the href attribute from the html link element.
    `rel` gives a relative path, but it's not used here.

    """
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path

import sys, StringIO

class DownloadToPDF():
    """
    download requested apge to DPF
    """
       
    def process_response(self, request, response):
        if ("pdf" in request.GET 
            and "text" in response['Content-Type'] 
            and response.status_code == 200):
            
            fd  = StringIO.StringIO()
            pdf = pisa.CreatePDF(response.content, fd, None, fetch_resources, 0, None, None)

#           pisa.showLogging()
#           pdf = pisa.pisaDocument(
#               response.content,   # src
#               fd,                 # dest
#               debug=0,
#               path=None,
#               errout=sys.stdout
#               tempdir=None,
#               format = 'pdf',
#               link_callback = fetch_resources,
#               encoding = 'iso-8859-1',
#               default_css=None,
#               xhtml=True,
#               xml_output=fd,
#           )
            
            if not pdf.err:
                response['Content-Type'] = u'%s; %s' % (settings.REPORT_CONF['content_type'], settings.REPORT_CONF['encoding'], )
                response.content = fd.getvalue()
            fd.close()

        return response

