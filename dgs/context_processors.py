from django.conf import settings


def site(request):
    return {
        'SITE_NAME': getattr(settings, 'SITE_NAME', ''),
        'SITE_API_NAME': getattr(settings, 'SITE_API_NAME', ''),
        'SITE_API_URL': getattr(settings, 'SITE_API_URL', ''),
    }
