from django.http import HttpResponse, HttpResponseRedirect
import datetime

def directory(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html) 