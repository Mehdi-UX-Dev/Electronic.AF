# Api for the Electronic.AF website

### This API is built with [<img src="https://static.djangoproject.com/img/logos/django-logo-negative.svg" width="50" height="20" />](https://www.djangoproject.com/) and [Django Rest Framework](https://www.django-rest-framework.org/)

## Running the server localy

To run the project after cloning the project(or just pulling new changes from the repo) open `API/ElectronicAF_Api/` folder in vscode then open vscode integrated terminal and run the following command:

```

python -m venv venv

```

That will create a new folder `venv` in your project directory. and you will see the bellow prompt in vscode:

<img src="https://i.stack.imgur.com/HzSHk.png" width="600"/>

Select Yes, then close the current instance of vscode terminal and open a new vscode terminal instance and install the project dependencies with following command:

```

pip install -r requirements.txt

```

After installation completed run the following two commands to create database tables

```

python manage.py migrate
python manage.py migrate core

```

Now you can run the project with this command

```

python manage.py runserver

```

This will start the server at [127.0.0.1:8000/](http://127.0.0.1:8000/) address

<span style="color:orange">
Above commands was firsttime setup on future updates just pull new changes from repo and run following commands.
</span>

```

pip install -r requirements.txt

python manage.py migrate
python manage.py migrate core

python manage.py runserver

```

==================================

### Current ready to use endpoints

==================================

+++++++++++++++++++

#### Authentication

+++++++++++++++++++

1:- `127.0.0.1:8000/api/token/`

- `Method`: Post
- `IsProtected` : NO
- `Expecting inputs`:

- ```json
  {
    "email": "useremail@example.com",
    "password": "atleast 6 charachter long password"
  }
  ```
- `Success Status`: `HTTP 200 OK`
- `Success Response`:
- ```json
  {
    "access": "a very very very long access token used to access protected endpoints",
    "refresh": "a very very very long token used to renew both tokens"
  }
  ```
- `Failiure Status`: `HTTP 401 Unauthorized`
- `Failiure Response`:
- ```json
  {
    "detail": "no active account found with the given credentials"
  }
  ```

2:- `127.0.0.1:8000/api/token/refresh/`

- `Method`: Post
- `IsProtected` : NO
- `Expecting inputs`:

- ```json
  {
    "refresh": "current refresh token"
  }
  ```
- `Success Status`: `HTTP 200 OK`
- `Success Response`:
- ```json
  {
    "access": "a very very very long access token with renewed expiratino date",
    "refresh": "a very very very long token used to renew both tokens"
  }
  ```
- `Failiure Status`: `HTTP 401 Unauthorized`
- `Failiure Response`:
- ```json
  {
    "detail": "Token is invalid or expired",
    "code": "token_not_valid"
  }
  ```

3:- `127.0.0.1:8000/api/register/`

- `Method`: Post
- `IsProtected` : NO
- `Expecting inputs`:

- ```json
  {
    "email": "new user email",
    "password": "at least 6 char long password",
    "phone": "9 digits long phone number eg:777888888",
    "firstname": "firstname of user",
    "lastname": "lastname of user"
  }
  ```
- `Success Status`: `HTTP 201 CREATED`
- `Success Response`:
- ```json
  {
    "email": "user saved email",
    "phone": "saved phone number",
    "firstname": "saved firstname",
    "lastname": "saved lastname"
  }
  ```
- `Failiure Status`: `HTTP 400 BadRequest`
- `Failiure Response`:
- ```json
  {
    "errors": {
      "email": "email error",
      "password": "password error",
      "phone": "phone error",
      "firstname": "firstname error",
      "lastname": "lastname error"
    }
  }
  ```