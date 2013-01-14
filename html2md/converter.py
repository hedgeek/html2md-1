try:
    import htmlentitydefs as entities
except ImportError:
    from html import entities # Py3k

from .options import DEFAULT_OPTIONS

class Html2Md(object):
    def __init__(self, options=None):
        self.options = dict(DEFAULT_OPTIONS)
        if options: self.options.update(options)
