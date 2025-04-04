import click
import requests
import json
from .sessions import CBRAINSession
from .users import UserManager
from tabulate import tabulate

# Create instances
session = CBRAINSession()
user_manager = UserManager(session)

@click.group()
def main():
    pass

@main.command()
@click.option('--username', prompt=True, help='Your CBRAIN username')
@click.option('--password', prompt=True, hide_input=True, help='Your CBRAIN password')
def login(username, password):
    """Login to CBRAIN."""
    try:
        if session.login(username, password):
            click.echo('Successfully logged in to CBRAIN')
        else:
            click.echo('Login failed - no session token received', err=True)
    except requests.exceptions.RequestException as e:
        click.echo(f'Error logging in: {str(e)}', err=True)

@main.command()
def logout():
    session.logout()
    click.echo('Successfully logged out from CBRAIN')

@main.command()
def status():
   
    if session.is_authenticated():
        click.echo(f'Logged in to CBRAIN (User ID: {session.user_id})')
    else:
        click.echo('Not logged in')

@main.group()
def users():
  
    pass

@users.command(name='create')
def create_user():
    if not session.is_authenticated():
        click.echo('Please login first', err=True)
        return

    click.echo(f"Logged in as admin (User ID: {session.user_id})")
    click.echo("\nCreating new CBRAIN user. Please provide the following information:")
    
    # Only prompt for user details if we're authenticated
    try:
        user_data = {
            'login': click.prompt('Username (must be unique)'),
            'password': click.prompt('Password (min 8 characters)', hide_input=True),
            'password_confirmation': click.prompt('Confirm password', hide_input=True),
            'full_name': click.prompt('Full name'),
            'email': click.prompt('Email address'),
            'city': click.prompt('City'),
            'country': click.prompt('Country'),
            'time_zone': click.prompt('Time zone'),
            'type': click.prompt('User type', default='NormalUser',
                               type=click.Choice(['NormalUser', 'AdminUser'])),
            'site_id': click.prompt('Site ID', default=1, type=int)
        }

        # Validate password match
        if user_data['password'] != user_data['password_confirmation']:
            click.echo('Passwords do not match', err=True)
            return

        # Validate password length
        if len(user_data['password']) < 8:
            click.echo('Password must be at least 8 characters long', err=True)
            return

        result = user_manager.create_user(user_data)
        if result:
            click.echo(f"\nUser created successfully with ID: {result['id']}")
            click.echo("\nUser details:")
            click.echo(json.dumps(result, indent=2))
        else:
            click.echo('Failed to create user', err=True)

    except click.Abort:
        click.echo('\nUser creation cancelled')
        return

@users.command(name='list')
@click.option('--detailed', '-d', is_flag=True, help='Show detailed user information')
def list_users(detailed):
    """List all users."""
    if not session.is_authenticated():
        click.echo('Please login first', err=True)
        return

    users = user_manager.list_users()
    if users:
 
        if detailed:
            headers = [
                'ID', 'Login', 'Full Name', 'Email', 
                'Type', 'Site ID', 'Time Zone', 
                'City', 'Last Connected', 'Account Status'
            ]
            table_data = [
                [
                    user['id'], 
                    user['login'], 
                    user['full_name'], 
                    user['email'], 
                    user['type'], 
                    user['site_id'], 
                    user['time_zone'], 
                    user['city'], 
                    user['last_connected_at'] or 'Never', 
                    'Locked' if user['account_locked'] else 'Active'
                ] for user in users
            ]
        else:
            headers = ['ID', 'Login', 'Full Name', 'Email', 'Type']
            table_data = [
                [
                    user['id'], 
                    user['login'], 
                    user['full_name'], 
                    user['email'], 
                    user['type']
                ] for user in users
            ] 
        click.echo(tabulate(
            table_data, 
            headers=headers, 
            tablefmt='fancy_grid',
            numalign='center',
            stralign='left'
        )) 
        click.echo(f"\nTotal Users: {len(users)}")
    else:
        click.echo('Failed to fetch users', err=True)

@users.command(name='show')
@click.argument('user_id', type=int)
def show_user(user_id):
    
    if not session.is_authenticated():
        click.echo('Please login first', err=True)
        return

    user = user_manager.get_user(user_id)
    if user:
        click.echo(json.dumps(user, indent=2))
    else:
        click.echo(f'Failed to fetch user with ID {user_id}', err=True)

if __name__ == '__main__':
    main() 