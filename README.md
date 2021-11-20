## Setup Virtual Environment

Install and update python library, make sure `venv` was installed on the system

```bash
  $ sudo apt update && sudo apt install python
  $ sudo apt install python3.9-venv
```

Run `python3 -m venv .` to init virtual development environment

Run `source bin/activate` to activate the virtual environment

Run `python -m pip install --upgrade pip` to update latest pip

To **deactivate** virtual environment, run `deactivate` to deactivate environment.

## Dependencies

Run `pip list` to list all installed packages

Run `pip install -r requirements.txt -y` to install all dependencies

## Running application

Create `.env` file and store your environment setting

```bash
    DATABASE_URL=[your-mongo-database-connection-string]
    SECRET_KEY=[your-secret-key]
```

Run `python3 app.py` to start application.

## Testing application

Create new user

```bash
    $ curl -X POST -H "Content-Type: application/json" \
        -d '{
        "id": "1"
        "username": "username",
        "password": "password",
        "first_name": "first_name",
        "last_name": "last_name",
        "is_owner": true,
        "members": ["members","member1", "member22"]
    }' \
        http://localhost:5000/user/signup
```

Login

```bash
    $ curl -X POST -H "Content-Type: application/json" \
        -d '{
        "username": "username",
        "password": "password"
    }' \
        http://localhost:5000/user/login

```
