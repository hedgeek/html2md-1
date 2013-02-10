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
        self.tags = defaultdict (lambda: self.undefined, {
            '!doctype': self.drop,
            'a': self.a,
            'abbr': self.not_implemented,
            'acronym': self.not_implemented,
            'address': self.not_implemented,
            'applet': self.drop,
            'area': self.drop,
            'article': self.not_implemented,
            'aside': self.not_implemented,
            'audio': self.drop,
            'b': self.not_implemented,
            'base': self.drop, # base url for relative links
            'basefont': self.drop,
            'bdi': self.not_implemented,
            'bdo': self.not_implemented,
            'big': self.not_implemented,
            'blockquote': self.not_implemented,
            'body': self.ignore,
            'br': self.not_implemented,
            'button': self.drop,
            'canvas': self.drop,
            'caption': self.not_implemented,
            'center': self.ignore,
            'cite': self.not_implemented,
            'code': self.not_implemented,
            'col': self.not_implemented,
            'colgroup': self.ignore,
            'command': self.drop,
            'data': self.not_implemented,
            'datagrid': self.drop,
            'datalist': self.drop,
            'dd': self.not_implemented,
            'del': self.not_implemented,
            'details': self.not_implemented,
            'dfn': self.not_implemented,
            'dir': self.ignore,
            'div': self.not_implemented,
            'dl': self.not_implemented,
            'dt': self.not_implemented,
            'em': self.not_implemented,
            'embed': self.drop,
            'eventsource': self.drop,
            'fieldset': self.drop,
            'figcaption': self.not_implemented,
            'figure': self.ignore,
            'font': self.ignore,
            'footer': self.not_implemented,
            'form': self.drop,
            'frame': self.drop,
            'frameset': self.ignore,
            'h1': self.h1,
            'h2': self.h2,
            'h3': self.h3,
            'h4': self.h4,
            'h5': self.h5,
            'h6': self.h6,
            'head': self.drop,
            'header': self.not_implemented,
            'hgroup': self.ignore,
            'hr': self.not_implemented,
            'html': self.ignore,
            'i': self.not_implemented,
            'iframe': self.drop,
            'img': self.not_implemented,
            'input': self.drop,
            'ins': self.not_implemented,
            'isindex': self.drop,
            'kbd': self.not_implemented,
            'keygen': self.drop,
            'label': self.drop,
            'legend': self.drop,
            'li': self.not_implemented,
            'link': self.drop,
            'map': self.drop,
            'mark': self.not_implemented,
            'menu': self.drop,
            'meta': self.drop,
            'meter': self.drop,
            'nav': self.ignore,
            'noframes': self.drop,
            'noscript': self.ignore,
            'object': self.drop,
            'ol': self.not_implemented,
            'optgroup': self.drop,
            'option': self.drop,
            'output': self.drop,
            'p': self.p,
            'param': self.drop,
            'pre': self.not_implemented,
            'progress': self.drop,
            'q': self.not_implemented,
            'rp': self.not_implemented,
            'rt': self.not_implemented,
            'ruby': self.not_implemented,
            's': self.not_implemented,
            'samp': self.not_implemented,
            'script': self.drop,
            'section': self.not_implemented,
            'select': self.drop,
            'small': self.not_implemented,
            'source': self.drop,
            'span': self.not_implemented,
            'strike': self.not_implemented,
            'strong': self.not_implemented,
            'style': self.drop,
            'sub': self.not_implemented,
            'summary': self.not_implemented,
            'sup': self.not_implemented,
            'table': self.not_implemented,
            'tbody': self.not_implemented,
            'td': self.not_implemented,
            'textarea': self.drop,
            'tfoot': self.not_implemented,
            'th': self.not_implemented,
            'thead': self.not_implemented,
            'time': self.not_implemented,
            'title': self.not_implemented,
            'tr': self.not_implemented,
            'track': self.not_implemented,
            'tt': self.not_implemented,
            'u': self.not_implemented,
            'ul': self.not_implemented,
            'var': self.not_implemented,
            'video': self.drop,
            'wbr': self.not_implemented,
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
        return self.postprocess()

    def deduplicate_newlines(self):
        length = len(self.out)
        if length:
            last = self.out[-1]
            for i in xrange(length-2, -1, -1):
                if last == self.out[i] == '\n':
                    del self.out[i]
                else:
                    last = self.out[i]

    def postprocess(self):
        self.deduplicate_newlines()
        return ''.join(self.out)

    def handle(self, element):
        self.tags[element.tag](element)

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
