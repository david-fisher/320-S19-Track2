Members Only
============
Introduction
------------
Members Only: A Revolution in Exclusive Social Arenas!

This is for the Members Only repo. It contains code for both the backend and frontend, as well as the github
wiki and reports for other information. Frontend and Backend teams will have to have both set up
to test the site.

You can find a working Heroku instance of Members Only at https://members-only-torch-jugglers.herokuapp.com/.

Requirements
------------
1. You should have the most current version of Python installed (3.7.2 at the time of writing). If you don't have it, you can get it [here](https://www.python.org/downloads/).

2. You should have the latest Node JS LTS release, available [here](https://nodejs.org/en/).

3. PostgreSQL is required on MacOS, but is also required on Windows and Linux if you don't want to use SQLite. 
You can get it [here](https://www.postgresql.org/download/), or run `brew install postgres` on MacOS (requires [brew](https://brew.sh/)). If on Windows, make sure Postgres is in the PATH variable.

4. For Windows users, I suggest not using PowerShell, as it has issues running scripts, so I suggest using 
cmd or [conemu](https://conemu.github.io/).

If you want to contribute:

3. You should have git installed.

4. You should have the `develop` branch checked out and opened in your python IDE of choice.

Backend Local Setup
-------------------
1. Ensure this folder is unzipped, and navigate to it in the command line.

2. Install virtualenv with `pip install virtualenv`. Run this in the command line (`sudo` may be required for
Linux and Mac)

3. Create the virtual environment with `virtualenv venv` **in the project directory!!**

4. Activate the virtual environment on Windows with `venv\Scripts\activate`. Activate the virtual environment on
Mac or Linux with `source venv/bin/activate`. When using the fish shell, run  `. venv/bin/activate.fish`

5. With venv activated, install the project requirements with `pip install -r requirements.txt`. 

If you experience issues installing the requirements on MacOS, try running `brew install openssl` and `export LDFLAGS="-L/usr/local/opt/openssl/lib"
  export CPPFLAGS="-I/usr/local/opt/openssl/include"`, then try running it again (requires [brew](https://brew.sh/)).

Running the Dev Server
----------------------
1. Ensure that your virtual environment (`venv`) is running. You only need to run step 4 of the Backend Local
Setup to run your virtual environment after you've set it up. 

2.  Run `python manage.py runserver 8000` in the project directory.

3. You can now access the site at http://127.0.0.1:8000

Provisioning the Database
-------------------------
1. Ensure that your virtual environment (`venv`) is running. You only need to run step 4 of the Backend Local
Setup to run your virtual environment after you've set it up. 

2. Run `python manage.py migrate` in the project directory.

When making changes to the models, you need to run `python manage.py makemigrations` before running
`python manage.py migrate`.

Setting up and Compiling the Frontend
----------------------
1. Run `npm install --dev`. You only need to do this once.

2. In the project directory, run `npm run dev`. If you're compiling for production use `npm run build`

Making a Backend User
---------------------
1. Run the manage.py command 
```
python manage.py createsuperuser --email yourEmail@email.com 
--username YourUserName
```

Adding PostgreSQL into Django (replacing SQLite):
-------------------------------------------------

#### 1. Create The Database
Launch PostgreSQL Server:
```
psql postgres
```
On Windows, try `psql -Upostgres`.

Create a database for your project:
```
CREATE DATABASE membersonly;
CREATE USER admin WITH PASSWORD 'password';
ALTER ROLE admin SET client_encoding TO 'utf8';
ALTER ROLE admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE admin SET timezone TO 'UTC';
ALTER USER admin CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE membersonly TO admin;
```
Enter your database from within postgres:
```
\q
psql membersonly
```
On Windows, try:
```
\c membersonly
```

#### 2. Edit setting.py in Django:
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

#### 3. Migrate:
```
python manage.py makemigrations
python manage.py migrate
```
You can open the database at any time with `psql membersonly`.


Backend REST API
----------------
The REST documentation is available at /api/. If you're looking to add to the API refer to 
https://www.django-rest-framework.org/tutorial/quickstart/

Stripe Setup
------------
This setup is only required if you want to connect members only to your own Stripe account. The current private and public keys are test keys for an account created by Model 2.

**Security Note:** The private key should normally never be posted publicly on a repo. The keys currently posted will be deactivited once the project is complete.

Stripe Registration: https://dashboard.stripe.com/register

1. Set the variable STRIPE_KEY in members_only/settings.py to your Stripe accounts private key

2. Set the value of the stripeKey parameter of the Stripe Payment Form in members_only/js/components/Setup.js to your Stripe accounts public key

Stripe Testing
------------
If the the public and private keys are set to test keys, Stripe has a set of credit card numbers that can be used for testing payments without using a real card.

Example:
CC Number (Visa): 4242424242424242
CVC: any numbers
EXP: any date that is not expired

More information at https://stripe.com/docs/testing

GitHub Contribution Guide
------------------
1. Navigate to the project directory.

2. `git checkout develop` Puts you on the develop branch.

3. `git pull origin develop` Pulls the latest from the develop branch.

4. `git checkout -b [NAME OF YOUR NEW BRANCH]` Makes a new branch. Name your branches a one to three
word description of what you did, replacing spaces with dashes, for example: `fun-new-feature`.

5. Perform your changes. Then add the files you want to commit with, `git add members_only/my_cool_modified_script.py`.

6. Commit your changes. The message should be in present tense, capitalized, and grammatically correct US
English, for example: `git commit -m "Changed how script does the logic for color derivation."`.

7. Push your changes to your new branch. `git push -u origin [NAME OF YOUR BRANCH]`.

8. You should now see a link to make a pull request in the terminal. You may follow it, but you can
also go to the GitHub repository and you will see a suggestion to create one. Click that. Name and
describe your pull request and share among your peers. Implement their changes, or wait for your
changes to be approved.

