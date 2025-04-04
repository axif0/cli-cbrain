# CBRAIN Command Line Interface (CLI)

## Overview

CBRAIN CLI is a command-line interface for interacting with the CBRAIN platform, providing easy access to user management and authentication functions.

## Features

- User authentication (login/logout)
- User management (create, list, show users)
- Session status checking

## Prerequisites

- Python 3.10+
- pip package manager

## Installation
 

1. Clone the repository:
```bash
git clone https://github.com/aces/cbrain-cli.git
cd cbrain-cli
```

2. Create a virtual environment :
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the package:
```bash
pip install -r requirements.txt
pip install .
```

## Usage

### Authentication

#### Login
```bash
cbrain login
```
- Prompts for username and password
- Stores session token for subsequent commands

#### Logout
```bash
cbrain logout
```
- Clears the current session

#### Check Status
```bash
cbrain status
```
- Shows current login status and user ID

### User Management

#### List Users
```bash
cbrain users list
```
- Lists all users
- Use `-d` or `--detailed` flag for more information
```bash
cbrain users list -d
```

#### Create User
```bash
cbrain users create
```
- Interactively creates a new user
- Requires admin authentication
- Prompts for user details like username, password, email, etc.

#### Show User Details
```bash
cbrain users show USER_ID
```
- Displays detailed information for a specific user
  
### Demo use :
![cbrain](https://github.com/user-attachments/assets/d40c92e0-a8e8-4880-8d1c-8ebfbca64890)



## Configuration

- Session token is stored in `~/.cbrain/session.json`
- Base URL defaults to `http://localhost:3000` (configurable in future versions)

 
