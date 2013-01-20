#!/usr/bin/env python
import argparse

from html2md import Html2Md, __version__

def main():
    parser = argparse.ArgumentParser(description='HTML to Markdown converter')
    parser.add_argument('source', help='url or filename')
    parser.add_argument('-c', '--coding', dest='coding', default='UTF-8',
                        help='override document encoding')
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)

    args = parser.parse_args()

if __name__ == "__main__":
    main()
