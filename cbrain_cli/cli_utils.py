import json
import urllib.error
import functools


def handle_errors(func):
    """
    Decorator to handle common errors for all CLI commands.

    Returns
    -------
    None
        A command is ran via inputs from the user.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except urllib.error.HTTPError as e:
            print(f"Request failed: HTTP {e.code} - {e.reason}")
            if e.code == 401:
                print("Invalid username or password")
            return 1
        except urllib.error.URLError as e:
            print(f"Connection failed: {e.reason}")
            return 1
        except json.JSONDecodeError:
            print("Failed: Invalid response from server")
            return 1
        except KeyboardInterrupt:
            print("\nOperation cancelled")
            return 1
        except Exception as e:
            print(f"Operation failed: {str(e)}")
            return 1
    return wrapper