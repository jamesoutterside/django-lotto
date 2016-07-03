# Django-lotto

[Full list of requirements](requirements/base.txt)

**Tested with - Django 1.9.7, pyton 2.7**

## Install & setup 

To install run the following: 

```
virtualenv lotto_env
cd lotto_env
source ./bin/activate
git clone https://github.com/jamesoutterside/django-lotto
cd django-lotto
pip install -r requirements/base.txt
python manage.py migrate
```

To create some initial data:

```
python manage.py create_test_data
```
This will create a set of users, entries and lotteries. Two key users are **super** and **admin**. All users are created with the password - password.  

And then run with runserver:

```
python manage.py runserver
```


## Development 

Reset SQLite DB 

```
rm django-lotto_test.db; python manage.py migrate; python manage.py create_test_data
```



> Note this is not a real app, just part of a code demo...