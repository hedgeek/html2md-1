#!/usr/bin/env python
import argparse
from urlparse import urlparse

try:
    from urllib.request import urlopen # Py3k
except:
    from urllib2 import urlopen

from html2md import Html2Md, __version__


def main():
    parser = argparse.ArgumentParser(description='HTML to Markdown converter')
    parser.add_argument('source', help='url or filename')
    parser.add_argument('-c', '--coding', dest='coding', default='UTF-8',
                        help='override document encoding')
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)

    args = parser.parse_args()

    parsed_url = urlparse(args.source)
    if parsed_url.scheme in (None, '', 'file'):
        document = open(args.source, 'rb').read()
    else:
        document = urlopen(args.source).read()

    # TODO: coding
    return Html2Md(document).parse()


if __name__ == "__main__":
    print main()
