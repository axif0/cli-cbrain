"""
Setup and commands for the CBRAIN CLI command line interface. 
"""

import argparse
import sys

from cbrain_cli.cli_utils import handle_errors, is_authenticated
from cbrain_cli.sessions import (
    create_session,
    logout_session
)

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

    # MARK: Sessions
    # Create new session.
    login_parser = subparsers.add_parser('login', help='Login to CBRAIN')
    login_parser.set_defaults(func=handle_errors(create_session))

    # Logout session.
    logout_parser = subparsers.add_parser('logout', help='Logout from CBRAIN')
    logout_parser.set_defaults(func=handle_errors(logout_session))

    # Show current session.
    subparsers.add_parser('whoami', help='Show current session')

    # MARK: Setup CLI
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 

    if args.command == 'login':
        return handle_errors(create_session)(args)
    elif args.command == 'logout':
        return handle_errors(logout_session)(args) 
    elif args.command == 'whoami':
        credentials = is_authenticated()
        if credentials:
            print(f"Currently logged in as {credentials.get('user_id')} on server {credentials.get('cbrain_url')}")
        else:
            print("Not logged in. Please login with 'cbrain login'.")
            return 1

    if hasattr(args, 'func'):
        return args.func(args)
 

if __name__ == '__main__':
    sys.exit(main()) 