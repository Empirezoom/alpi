from .models import *

def alpicom(request):
    alp = CompanyProfile.objects.get(pk=1)

    context = {
    'alp': alp,
    }
    return context