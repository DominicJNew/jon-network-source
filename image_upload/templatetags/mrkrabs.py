from django import template
register = template.Library()

@register.filter
def urlify(title):
    for c in '!@#$%^&*()_+{}|:"<>?,./;\'[]\\`~-':
        title = title.replace(c, '')
    
    title = title.replace('  ', '')
    
    title = title.replace(' ', '-')
    
    return title

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