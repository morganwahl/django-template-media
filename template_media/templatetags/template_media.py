import re

from django import template
from django.forms import Media


register = template.Library()

class MediaNode(template.Node):
    def __init__(self, media, var_name):
        self.media = media
        self.var_name = var_name

    def render(self, context):
        if self.var_name in context:
            context[self.var_name] += self.media
        else:
            context[self.var_name] = self.media
        return ''

class MediaJsNode(MediaNode):
    def __init__(self, filename, var_name):
        super(MediaJsNode, self).__init__(Media(js=(filename,)), var_name)

@register.tag
def media_js(parser, token):
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires 2 arguments" % token.contents.split()[0]
        )
    m = re.search(r'(.*?)\s+in\s+(\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError(
            "%r tag had invalid arguments" % tag_name
        )
    filename, var_name = m.groups()
    if not (filename[0] == filename[-1] and filename[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            "%r tag's argument should be in quotes" % tag_name
        )
    return MediaJsNode(filename[1:-1], var_name)

class MediaCssNode(MediaNode):
    def __init__(self, css_media, filename, var_name):
        super(MediaCssNode, self).__init__(
            Media(css={css_media: (filename,)}),
            var_name,
        )

@register.tag
def media_css(parser, token):
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires 3 arguments" % token.contents.split()[0]
        )
    m = re.search(r'(.*?)\s+(.*?)\s+in\s+(\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError(
            "%r tag had invalid arguments" % tag_name
        )
    css_media, filename, var_name = m.groups()
    if not (css_media[0] == css_media[-1] and css_media[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            "%r tag's argument should be in quotes" % tag_name
        )
    if not (filename[0] == filename[-1] and filename[0] in ('"', "'")):
        raise template.TemplateSyntaxError(
            "%r tag's argument should be in quotes" % tag_name
        )
    return MediaCssNode(css_media[1:-1], filename[1:-1], var_name)
