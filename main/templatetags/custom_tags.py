from django import template

register = template.Library()


@register.filter
def split(text):
    if len(text) > 100:
        text = text[:100]
    return text


@register.simple_tag
def previews_mediapath(path):
    result = f"/media/{path}"
    return result
