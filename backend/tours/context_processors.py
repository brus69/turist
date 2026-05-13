from .content_home import HEADER_NAV


def site_context(request):
    return {"HEADER_NAV": HEADER_NAV}
