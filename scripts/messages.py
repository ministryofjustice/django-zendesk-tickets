#!/usr/bin/env python
import argparse
import logging
import os
import pathlib
import sys

from django.core.management import call_command


def main():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    parser = argparse.ArgumentParser(description='Manage gettext localisation messages')
    sub_parsers = parser.add_subparsers()
    description = 'Update localisation message files from source code'
    sub_parser = sub_parsers.add_parser('update', help=description, description=description)
    sub_parser.set_defaults(command='update')
    description = 'Compile gettext binary localisation message files'
    sub_parser = sub_parsers.add_parser('compile', help=description, description=description)
    sub_parser.set_defaults(command='compile')

    args = parser.parse_args()
    if not hasattr(args, 'command'):
        parser.print_help()
        sys.exit(1)

    root_path = pathlib.Path(__file__).parent.parent
    os.chdir(root_path / 'zendesk_tickets')

    if args.command == 'update':
        logging.info('Updating localisation message files')
        call_command('makemessages', all=True, no_wrap=True, keep_pot=True)

    if args.command == 'compile':
        logging.info('Compiling localisation message files')
        call_command('compilemessages', fuzzy=False)


if __name__ == '__main__':
    main()
