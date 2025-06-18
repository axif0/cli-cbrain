"""
Setup and commands for the CBRAIN CLI command line interface. 
"""

import argparse
import sys

from cbrain_cli.sessions import (
    create_session 
)
from cbrain_cli.cli_utils import handle_errors

def main():
    """
    The function that controls the CBRAIN CLI.

    Returns
    -------
    None
        A command is ran via inputs from the user.
    """
    parser = argparse.ArgumentParser(description='CBRAIN CLI')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Create new session.
    login_parser = subparsers.add_parser('login', help='Login to CBRAIN')
    login_parser.set_defaults(func=handle_errors(create_session))

    # MARK: Setup CLI
    args = parser.parse_args()

    if args.command == 'login':
        return handle_errors(create_session)(args) 

    if hasattr(args, 'func'):
        return args.func(args)
    else:
        parser.print_help()
        return 1

if __name__ == '__main__':
    sys.exit(main()) 