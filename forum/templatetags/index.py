from django import template
import re
import commonmark

from users.models import CustomUser as CU

# import html_sanitizer as san
# from html_sanitizer.sanitizer import sanitize_href, bold_span_to_strong, italic_span_to_em, tag_replacer, target_blank_noopener

register = template.Library()

@register.filter
def index(List, i):
    return List[int(i)]
    
def xss(chat):
    chat = chat.replace('{', '&#123;')
    chat = chat.replace('}', '&#125;')
    chat = chat.replace('&', '&amp;')
    chat = chat.replace('\'', '&apos;')
    chat = chat.replace('\"', '&quot;')
    chat = chat.replace('<', '&lt;')
    chat = chat.replace('>', '&gt;')
    return chat


def linkify(chat):
    s = ''
    for word in chat.split(' '):
        try:
            if ('http://' in word[:7] or 'https://' in word[:8]) and '.' in word and len(word) > 11: 
                s += '<a href="{}" rel="ugc">{}</a> '.format(word, word)
                continue
            elif word[0] == '@' and len(word) > 2:
                s += '<b style="color:yellow">{}</b> '.format(word)
                continue 
        except IndexError:
            pass
        
        s += word + ' '
    return s

@register.filter
def formatchat(chat, is_safe=True):
    return linkify(xss(chat))
    
@register.filter
def urlify(title):
    for c in '!@#$%^&*()_+{}|:"<>?,./;\'[]\\`~-':
        title = title.replace(c, '')
    
    title = title.replace('  ', ' ')
    
    title = title.replace(' ', '-')
    
    return title
    
@register.filter
def split(s):
    return s.split(';')

# san_settings = {
#     "tags": {
#         "a", "h1", "h2", "h3", "h4", "h5", "h6", "strong", "em", "p", "ul", "ol",
#         "li", "br", "sub", "sup", "hr", "code", "pre", "div", "tr", "td", "table",
#         "thead", "tbody"
#     },
#     "attributes": {"a": ("href", "name", "target", "title", "id", "rel")},
#     "empty": {"hr", "a", "br"},
#     "separate": {"a", "p", "li"},
#     "whitespace": {"br"},
#     "keep_typographic_whitespace": True,
#     "add_nofollow": True,
#     "autolink": True,
#     "sanitize_href": sanitize_href,
#     "element_preprocessors": [
#         # convert span elements into em/strong if a matching style rule
#         # has been found. strong has precedence, strong & em at the same
#         # time is not supported
#         bold_span_to_strong,
#         italic_span_to_em,
#         tag_replacer("b", "strong"),
#         tag_replacer("i", "em"),
#         tag_replacer("form", "p"),
#         target_blank_noopener,
#     ],
#     "element_postprocessors": [],
#     "is_mergeable": lambda e1, e2: True,
# }


@register.filter
def markdown(s):
    s = commonmark.commonmark(s)
    # s = san.Sanitizer(san_settings).sanitize(s)
    s = s.replace('<pre><code', '<div class="code"><pre><code')
    s = s.replace('</code></pre>', '</code></pre></div>')
    return s

@register.filter
def trunc(s, max_len):
    if len(s) <= max_len:
        return s
    else:
        return s[:max_len-3] + '...'
        
@register.filter
def rep(username):
    user = CU.objects.get(username=username)
    return user.rep
    
@register.filter
def gravatar(username):
    user = CU.objects.get(username=username)
    return user.gravatar

