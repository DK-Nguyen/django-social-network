import hashlib
import urllib
from django import template

register = template.Library()

# return only the URL of the gravatar
# TEMPLATE USE:  {{ email|gravatar_url:150 }}
@register.filter
def gravatar_url(email, size=100):
    default = "identicon"
    return "https://www.gravatar.com/avatar/%s?%s" % (
    hashlib.md5(str(email.lower()).encode('utf-8')).hexdigest(), urllib.parse.urlencode({'d': default, 's': str(size)}))
