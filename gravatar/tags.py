import hashlib
import urllib
from django import template

register = template.Library()

@register.filter
def gravatar_url(email, size=100):
    """
    This is a tag to be used in templates so that email can be used to request a profile picture
    TEMPLATE USE:  {{ email|gravatar_url:150 }}
    :param email: email to query
    :param size: size of the image we want to query, by default it is 100px
    :return: only the URL of the gravatar (string)
    """
    default = "identicon"
    return "https://www.gravatar.com/avatar/%s?%s" % (
    hashlib.md5(str(email.lower()).encode('utf-8')).hexdigest(), urllib.parse.urlencode({'d': default, 's': str(size)}))
