from django.conf import settings


def site(request):
    return {
        'SITE_NAME': getattr(settings, 'SITE_NAME', ''),
        'PUBLIC_SITE_URL': getattr(settings, 'PUBLIC_SITE_URL', '/'),
        'SITE_API_NAME': getattr(settings, 'SITE_API_NAME', ''),
        'SITE_API_URL': getattr(settings, 'SITE_API_URL', ''),
    }
