from django.conf import settings


def main_host(request):
    return {'MAIN_HOST': settings.MAIN_HOST}
