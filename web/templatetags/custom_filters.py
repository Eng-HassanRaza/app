import random
import logging

from django.template.defaultfilters import register

logger = logging.getLogger("main")


@register.filter
def random_int(items):
    return random.randint(0, len(items) - 1)


@register.filter
def auth_page(request):
    logger.info("auth_page={}".format('auth_page' in request.session))
    if "auth_page" in request.session:
        return request.session["auth_page"]
    else:
        return ""


@register.filter
def current_url(request):
    return "{0}://{1}{2}".format(request.scheme, request.get_host(), request.path)
