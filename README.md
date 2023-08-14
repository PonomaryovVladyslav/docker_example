# Canonical test app from Vladyslav Ponomarov

## Used frameworks

- Django [docs](https://docs.djangoproject.com/en/4.1/)
- Django rest framework [docs](https://www.django-rest-framework.org/)

## Instructions for environment setup and running your code and tests

### Docker and docker compose

If you have docker and docker compose installed and running you can run project by simple command:

All command have to be run from main directory (the same level as file `manage.py`)

Run server

```
docker compose up api
```

Run tests

```
docker compose up test
```

Run only unit tests

```
docker compose up test-unit
```

Run only integration tests

```
docker compose up test-integration
```

### Virtual environment

If you want to use virtual environment

#### Prepare project:

1) You have to create virtual environment, to do it in console run command

   ```
   python3 -m venv /path/to/your/venv
   ```

   where `/path/to/your/venv` any available path on your PC

2) Activate virtual environment

   For linux/mac:
    ```
   sourse /path/to/your/venv/bin/activate
    ```

   For windows:
    ```
    /path/to/your/venv/Scripts/activate
    ```

   After this step you have to see name of your venv in brackets before any command in command line, `(canonical)` for
   example

3) Install dependencies

   Change current for working directory (which contains file `manage.py`) in command line.

   Run command:

   ```
   pip install -r requeirements.txt
   ```

4) Migrate database structure

   Into the same folder from previous step run
   ```
   python manage.py migrate
   ```

#### Running commands

**Please check virtual environment has to be activated and folder could be correct for next commands**

To run project run command:

```
python manage.py runserver 127.0.0.1:5000
```

`:5000` is a port, you can change it if needed

To run tests:

```
python manage.py test
```

To run only unit tests:

```
python manage.py test --tag=unit
```

To run only integration tests:

```
python manage.py test --tag=integration
```

## Any additional context on your solution and approach, including any assumptions made

### /transactions

Allowed only `POST` requests, any other will return HTTP status code 405 `Method not allowed`

Expected field `data` which should contain file with list of strings

Try to send empty file or not file (string or number f.e.) will return HTTP 400 `Bad request` with message what is the
problem

Strings which contain 4 elements separated by `,` and contain values:

1) Date in format `YYYY-MM-DD`
2) `Expense` or `Income`
3) Decimal value separated by `.`, if value has more than 2 symbols after `.` try to round it by math rules 1-4 round
   down, 5-9 round up, f.e `11.111` will be converted to `11.11`, `66.666` will be converted to `66.67`
4) String with additional info which will be store do database as `job_address` if 2nd part of the string is `Income`
   and as `expense_category` if 2nd part of the string is `Expense`. Will be stored as string.

If string couldn't be parsed by this rules string will be skipped. F.e. contains 3 or 5 elements, contains incorrect
date, incorrect type etc.

Each new request with at least 1 valid string in the file will remove all record in database and put new.

Return HTTP response with status code 200 and JSON in format ```{"count": 5}``` where value is a count how many
transactions were stored

### /report

Allow only `GET` HTTP requests, any other will return 405 `Method not allowed`

Return HTTP with 200 status code and JSON content

```JSON
{
  "gross-revenue": 225.0,
  "expenses": 72.93,
  "net-revenue": 152.07
}
``` 

Where `gross-revenue` - sum of values for all transactions with type `Income`

`expenses` - sum of values for all transactions with type `Expenses`

`net-revenue` - result of subtraction between `gross-revenue` and `expenses`

If transactions weren't stored all values in JSON will be `0`

## What are the shortcomings of your solution?

The main shortcoming is using Django as framework for small project. Using this framework is redundant, but I chose it
because I have the most experience in it (If needed I can use any other framework)

The second is using SQLite. SQLite cannot be used as production database.

The third is small functional, my view about how to improve it I'll describe in next paragraph

## If you had additional time to work on this problem, what would you add or refine?

1) Provide at least delete and update actions for transaction object. Need it if file with data contains wrong records which could be changed or removed.
2) Add cache. To prevent unneeded database query at least if data wasn't changed.
3) Expand stored data. Add model to keep each request in additional table (f.e. 3 requests -> 3 record to provide data
   from each of them separately)
4) Add authentication system. To separate requests (and stored data) by users and to protect getting data from other
   users.
5) Try to avoid duplicates. Skip duplicates or union records from the same user, day, and address depends on
   conditions (maybe you got the same jobs 2 times the same day, the same place, have to be discussed)
6) Add taxes calculator.
7) Provide ability to set tax schema or formula, tax size, additional options (f.e. count of your children which can have effort to taxes, etc.)
8) Update tables to provide way to mark some transaction "tax free" it can be usefully in the future.
