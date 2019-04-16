# How to add postgreSQL into Django

## Initial Configuration
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

## Edit setting.py in Django
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

## Open up the database
```
psql membersonly
```


## Useful command 
Show all databse
```
\l
```
Drop a database
```
DROP DATABASE [databas-name]
```