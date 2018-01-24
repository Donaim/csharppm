import argparse

def entrypoint():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='subparsersXXX', dest='subparser_ZZZ')
    pa = subparsers.add_parser('parser_A', help='parser A help')
    parser.add_argument('llul')
    parser.add_argument('kek')
    parser.add_argument('sex')
