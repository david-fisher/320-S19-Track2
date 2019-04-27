# How to add postgreSQL into Django

## 1. Create Database
Run postgresql server
```
psql postgres
```

First, create a database for your project
```
CREATE DATABASE membersonly;
CREATE USER admin WITH PASSWORD 'password';
ALTER ROLE admin SET client_encoding TO 'utf8';
ALTER ROLE admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE admin SET timezone TO 'UTC';
ALTER USER admin CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE membersonly TO admin;
```
Quit postgresql server
```
\q
```
open up your database
```
psql membersonly
```

## 2. Edit setting.py in Django
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'membersonly',
        'USER' : 'admin',
        'PASSWORD' : 'password',
        'HOST':'localhost',
        'PORT':'5432'
    }
}
```

## 3. migrate
```
python manage.py makemigrations
python manage.py migrate
```
## Open up the database
```
psql membersonly
```
