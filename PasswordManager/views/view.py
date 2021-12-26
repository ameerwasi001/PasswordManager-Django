from django.http import HttpResponse, HttpResponseRedirect
import datetime

def directory(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")
    print("=>>", request.user.email)
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html) 