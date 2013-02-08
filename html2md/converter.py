from collections import defaultdict
from cStringIO import StringIO

try:
    import htmlentitydefs as entities
except ImportError:
    from html import entities # Py3k

from lxml import html

from .options import DEFAULT_OPTIONS

class Html2Md(object):
    def __init__(self, source, options=None):
        # override options
        self.options = dict(DEFAULT_OPTIONS)
        if options: self.options.update(options)

        self.tree = self.parse_source(source)

        # set output buffer
        self.out = []

        # assign tag handlers
        self.tags = defaultdict (lambda: {'cb': self.undefined}, {
            '!doctype': {'cb': self.drop},
            'a': {'cb': self.a},
            'abbr': {'cb': self.not_implemented},
            'acronym': {'cb': self.not_implemented},
            'address': {'cb': self.not_implemented},
            'applet': {'cb': self.drop},
            'area': {'cb': self.drop},
            'article': {'cb': self.not_implemented},
            'aside': {'cb': self.not_implemented},
            'audio': {'cb': self.drop},
            'b': {'cb': self.not_implemented},
            'base': {'cb': self.drop}, # base url for relative links
            'basefont': {'cb': self.drop},
            'bdi': {'cb': self.not_implemented},
            'bdo': {'cb': self.not_implemented},
            'big': {'cb': self.not_implemented},
            'blockquote': {'cb': self.not_implemented},
            'body': {'cb': self.ignore},
            'br': {'cb': self.not_implemented},
            'button': {'cb': self.drop},
            'canvas': {'cb': self.drop},
            'caption': {'cb': self.not_implemented},
            'center': {'cb': self.ignore},
            'cite': {'cb': self.not_implemented},
            'code': {'cb': self.not_implemented},
            'col': {'cb': self.not_implemented},
            'colgroup': {'cb': self.ignore},
            'command': {'cb': self.drop},
            'data': {'cb': self.not_implemented},
            'datagrid': {'cb': self.drop},
            'datalist': {'cb': self.drop},
            'dd': {'cb': self.not_implemented},
            'del': {'cb': self.not_implemented},
            'details': {'cb': self.not_implemented},
            'dfn': {'cb': self.not_implemented},
            'dir': {'cb': self.ignore},
            'div': {'cb': self.not_implemented},
            'dl': {'cb': self.not_implemented},
            'dt': {'cb': self.not_implemented},
            'em': {'cb': self.not_implemented},
            'embed': {'cb': self.drop},
            'eventsource': {'cb': self.drop},
            'fieldset': {'cb': self.drop},
            'figcaption': {'cb': self.not_implemented},
            'figure': {'cb': self.ignore},
            'font': {'cb': self.ignore},
            'footer': {'cb': self.not_implemented},
            'form': {'cb': self.drop},
            'frame': {'cb': self.drop},
            'frameset': {'cb': self.ignore},
            'h1': {'cb': self.h1},
            'h2': {'cb': self.h2},
            'h3': {'cb': self.h3},
            'h4': {'cb': self.h4},
            'h5': {'cb': self.h5},
            'h6': {'cb': self.h6},
            'head': {'cb': self.drop},
            'header': {'cb': self.not_implemented},
            'hgroup': {'cb': self.ignore},
            'hr': {'cb': self.not_implemented},
            'html': {'cb': self.ignore},
            'i': {'cb': self.not_implemented},
            'iframe': {'cb': self.drop},
            'img': {'cb': self.not_implemented},
            'input': {'cb': self.drop},
            'ins': {'cb': self.not_implemented},
            'isindex': {'cb': self.drop},
            'kbd': {'cb': self.not_implemented},
            'keygen': {'cb': self.drop},
            'label': {'cb': self.drop},
            'legend': {'cb': self.drop},
            'li': {'cb': self.not_implemented},
            'link': {'cb': self.drop},
            'map': {'cb': self.drop},
            'mark': {'cb': self.not_implemented},
            'menu': {'cb': self.drop},
            'meta': {'cb': self.drop},
            'meter': {'cb': self.drop},
            'nav': {'cb': self.ignore},
            'noframes': {'cb': self.drop},
            'noscript': {'cb': self.ignore},
            'object': {'cb': self.drop},
            'ol': {'cb': self.not_implemented},
            'optgroup': {'cb': self.drop},
            'option': {'cb': self.drop},
            'output': {'cb': self.drop},
            'p': {'cb': self.p},
            'param': {'cb': self.drop},
            'pre': {'cb': self.not_implemented},
            'progress': {'cb': self.drop},
            'q': {'cb': self.not_implemented},
            'rp': {'cb': self.not_implemented},
            'rt': {'cb': self.not_implemented},
            'ruby': {'cb': self.not_implemented},
            's': {'cb': self.not_implemented},
            'samp': {'cb': self.not_implemented},
            'script': {'cb': self.drop},
            'section': {'cb': self.not_implemented},
            'select': {'cb': self.drop},
            'small': {'cb': self.not_implemented},
            'source': {'cb': self.drop},
            'span': {'cb': self.not_implemented},
            'strike': {'cb': self.not_implemented},
            'strong': {'cb': self.not_implemented},
            'style': {'cb': self.drop},
            'sub': {'cb': self.not_implemented},
            'summary': {'cb': self.not_implemented},
            'sup': {'cb': self.not_implemented},
            'table': {'cb': self.not_implemented},
            'tbody': {'cb': self.not_implemented},
            'td': {'cb': self.not_implemented},
            'textarea': {'cb': self.drop},
            'tfoot': {'cb': self.not_implemented},
            'th': {'cb': self.not_implemented},
            'thead': {'cb': self.not_implemented},
            'time': {'cb': self.not_implemented},
            'title': {'cb': self.not_implemented},
            'tr': {'cb': self.not_implemented},
            'track': {'cb': self.not_implemented},
            'tt': {'cb': self.not_implemented},
            'u': {'cb': self.not_implemented},
            'ul': {'cb': self.not_implemented},
            'var': {'cb': self.not_implemented},
            'video': {'cb': self.drop},
            'wbr': {'cb': self.not_implemented},
        })

    def parse_source(self, source):
        return html.parse(StringIO(source))

    def iterate(self):
        for event, element in html.etree.iterwalk(self.tree):
            if isinstance(element.tag, (str, unicode)):
                yield element

    def parse(self):
        for element in self.iterate():
            self.handle(element)
        return ''.join(self.out)

    def handle(self, element):
        self.tags[element.tag]['cb'](element)

    def as_text(self, element):
        return ''.join(element.itertext())

    ###### tag handlers

    def hn(self, element, n):
        self.out.append(u'%s %s\n' % ('#' * n, self.as_text(element)))

    def h1(self, element):
        self.hn(element, 1)

    def h2(self, element):
        self.hn(element, 2)

    def h3(self, element):
        self.hn(element, 3)

    def h4(self, element):
        self.hn(element, 4)

    def h5(self, element):
        self.hn(element, 5)

    def h6(self, element):
        self.hn(element, 6)

    def p(self, element):
        self.out.append('\n')

    def a(self, element):
        self.out.append('[%s](%s)' % (self.as_text(element), element.attrib.get('href')))

    ###### other handlers

    def not_implemented(self, element):
        print 'NOT IMPLEMENTED', element

    def undefined(self, element):
        print 'WARNING, undefined tag', element

    def ignore(self, element):
        pass

    def drop(self, element):
        element.drop_tree()
