#!/usr/bin/env python
import optparse

from html2md import Html2Md, __version__

def main():
    parser = optparse.OptionParser('%prog (filename|url)', version='%prog ' + __version__)
    (opts, args) = parser.parse_args()

if __name__ == "__main__":
    main()
