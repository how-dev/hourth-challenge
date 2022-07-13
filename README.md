# Hourth

> First, let's agree that since it's a technical test, I'm going to leave the .env credentials exposed in example.env. So let's move on =)

## Stories

> **ME** as admin user
>
> **I WANT** to be able to manage **ALL** users
>
> **ALL** the products

> **ME** as a staff user
>
> **I NEED** an admin user to register
>
> **SO THAT** I can have access to the administration
>
> of **ALL** products

## First Steps

### Run localy

> Make sure you have created the .env file based on the example.env file

### With the `make` command (recommended)

Just run the following command:

```commandline
make setup
```

This command will make all the necessary configurations to manually upload and test the application. In addition, it creates a super user to access the /admin/ endpoint and the other endpoints with the following credentials:

```json
{
  "email": "base@tester.com",
  "password": "base"
}
```

To access the routes, take the token received when logging in and use it in the request header with the following pattern:

| Key           | Value           |
|---------------|-----------------|
| Authorization | Token < token > |

### Without the `make` command (not recommended)

1.

```commandline
docker volume create --name=db_persist
```

2.

```commandline
docker-compose build --no-cache
```

3.

```commandline
docker-compose run web bash -c "python manage.py makemigrations && python manage.py migrate && python manage.py create_superuser && python manage.py create_products && python manage.py create_randomusers"
```

## Tests

To run the tests, just use the `make test` command (with make command)

You can specify a test path like: `make test path=path/to/file.py`

And...

Specify a class and a test, like: `make test path=path/to/file.py::TestClass::test_name`

or:

```commandline
docker-compose run web bash -c "pytest <optional-file-path> -s -v --disable-warnings --cov-report term-missing"
```

without `make` command.

> All `make` commands are in the `Makefile`. I strongly recommend using it to your advantage in development.

## Run

To launch the application with the `make` command, just run the following command:

```commandline
make run
```

Without the `make` command:

```commandline
docker-compose up
```

## API

`base_url` = <http://localhost:8000/api/v1/>

### Product

**Endpoint: `product/`**

Method: `GET`

Header: `Authorization: Token <token>[is_superuser=true || is_superuser=false]`

Accepted filtering parameters: `name`, `consult_page`

Status: `200 OK`

Body: `No Body`

Response Example:

```json
{
  "count": 1234,
  "next": "http://localhost:8000/api/v1/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "product_url__image": null,
      "product_url": "http://www.green.com/",
      "product_url__created_at": "2022-07-13 04:34:07.340620+00:00",
      "sales": [
        {
          "2022-07-13": 57,
          "2022-01-13": 13,
          "2022-02-13": 190
        }
      ]
    },
    {
      "id": 2,
      "product_url__image": null,
      "product_url": "https://www.vazquez-hernandez.info/",
      "product_url__created_at": "2022-07-13 04:34:07.347890+00:00",
      "sales": [
        {
          "2022-07-13": 57,
          "2022-01-13": 13,
          "2022-02-13": 190
        }
      ]
    ... // Default: 15 per page
  ]
}
```

----

**Endpoint: `product/?consult_page=YYYY-mm-dd`**

Method: `GET`

Header: `Authorization: Token <token>[is_superuser=true || is_superuser=false]`

Status: `200 OK`

Body: `No Body`

This filter returns another object format:

```json
{
  "id": 1,
  "product_url__image": null,
  "product_url": "http://www.green.com/",
  "product_url__created_at": "2022-07-13 04:34:07.340620+00:00",
  "consult_date": "2022-07-13",
  "sales_on_the_day": 5
}
```

----

**Endpoint: `product/<product_id>/`**

Method: `GET`

Header: `Authorization: Token <token>[is_superuser=true || is_superuser=false]`

Status: `200 OK`

Body: `No Body`

Response Example:

```json
{
  "id": 1,
  "product_url__image": null,
  "product_url": "http://www.green.com/",
  "product_url__created_at": "2022-07-13 04:34:07.340620+00:00",
  "sales": [
    {
      "2022-07-13": 51,
      "2022-05-12": 76
    }
  ]
}
```

### Login

----

**Endpoint: `login/`**

Method: `POST`

Header: `No Header`

Status: `200 OK`

Body:

```json
{
  "email": "doc@readme.md",
  "password": "readme"
}
```

Response Example:

```json
{
  "id": 203,
  "last_login": "2022-04-16T01:48:51.289333-03:00",
  "is_superuser": false,
  "is_staff": false,
  "email": "doc@readme.md",
  "name": "Doc",
  "document": "00011122233",
  "token": "8bba19c9fe4dc2c9d1c562303e4906d647a44ba1"
}
```

> Note: This token expires every 1 hour. But don't worry, it only expires after an hour if you log in. We don't want your session to fall in the middle of an important task =)

----

### User

----

**Endpoint: `user/`**

Method: `GET`

Accepted filtering parameters: `page`, `id`, `last_login`, `is_active`, `date_joined`, `email`, `name`, `document`

Header: `Authorization: Token <token>[is_superuser=true]`

Status: `200 OK`

Body: `No Body`

Response Example:

```json
{
  "count": 101,
  "next": "http://localhost:8000/api/v1/user/?page=2",
  "previous": null,
  "results": [
    {
      "id": 6,
      "last_login": null,
      "is_superuser": false,
      "is_staff": false,
      "email": "louisconway@example.com",
      "name": "Ariel",
      "document": "65625248737"
    },
    {
      "id": 16,
      "last_login": null,
      "is_superuser": false,
      "is_staff": false,
      "email": "bhoffman@example.net",
      "name": "Mark",
      "document": "24550560665"
    },
    {
      "id": 58,
      "last_login": null,
      "is_superuser": false,
      "is_staff": false,
      "email": "wkelly@example.org",
      "name": "Charles",
      "document": "27762125779"
    },
    ...
    // Default: 15 per page
  ]
}
```

----

**Endpoint: `user/<int:user_id>/`**

Method: `GET`

Header: `Authorization: Token <token>[is_superuser=true || is_superuser=false]`

Status: `200 OK`

Body: `No Body`

Response Example:

```json
{
  "id": 16,
  "last_login": null,
  "is_superuser": false,
  "is_staff": false,
  "email": "bhoffman@example.net",
  "name": "Mark",
  "document": "24550560665"
}
```

> Note: If you are not a superuser, you can only **get retrieve**, and only on yourself.

----

**Endpoint: `user/`**

Method: `POST`

Header: `Authorization: Token <token>[is_superuser=true]`

Status: `201 CREATED`

Body:

```json
{
  "name": "Doc",
  "document": "00011122233",
  "email": "doc@readme.md",
  "password": "readme"
}
```

Response example:

```json
{
  "id": 203,
  "last_login": null,
  "is_superuser": false,
  "is_staff": false,
  "email": "doc@readme.md",
  "name": "Doc",
  "document": "00011122233",
  "token": "1db5d82e55ef0685ac674464d8939cc05c45ab8d"
}
```

----

**Endpoint: `user/<int:user_id>/`**

Method: `PATCH`

Header: `Authorization: Token <token>[is_superuser=true || is_superuser=false]`

Status: `200 OK`

Body:

```json
{
  "name": "Docker"
}
```

```json
{
  "id": 203,
  "last_login": "2022-04-16T00:39:08.344401-03:00",
  "is_superuser": false,
  "is_staff": false,
  "email": "doc@readme.md",
  "name": "Docker",
  "document": "00011122233"
}
```

> Note: If you are not a superuser, you can only **patch yourself**.

----

**Endpoint: `user/<int:user_id>/`**

Method: `DELETE`

Header: `Authorization: Token <token>[is_superuser=true || is_superuser=false]`

Status: `204 NO CONTENT`

Body: `No Body`

Response Example: `No Content`

> Note: If you are not a superuser, you can only **delete yourself**.

----
