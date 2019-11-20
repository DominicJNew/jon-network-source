from django import template
register = template.Library()

def xss(chat):
    chat = chat.replace('{', '&#123;')
    chat = chat.replace('}', '&#125;')
    chat = chat.replace('&', '&amp;')
    chat = chat.replace('\'', '&apos;')
    chat = chat.replace('<', '&lt;')
    chat = chat.replace('>', '&gt;')
    return chat


def linkify(chat):
    s = ''
    for word in chat.split(' '):
        try:
            if 'http://' or 'https://' in word[:7]:
                s += '<a href="{}">{}</a> '.format(word, word)
                continue
        except IndexError:
            pass
        
        s += word + ' '

@register.filter
def formatchat(chat, is_safe=True):
    return linkify(xss(chat))