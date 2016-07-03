# Django-lotto

## Install & setup 

To install run the following: 

```
virtualenv lotto_env
cd lotto_env
source ./bin/activate
cd django_lotto
pip install -r requirements/base.txt
python manage.py migrate
```

To create some initial data:

```
python manage.py create_test_data
```

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