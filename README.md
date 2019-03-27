Members Only
============
Introduction
------------
This is for the Members Only repo. It contains code for both the backend and frontend, as well as the github
wiki and reports for other information. Frontend and Backend teams will have to have both set up
to test the site.

Requirements
------------
1. You should have the most current version of python installed (3.7.2 at the time of writing).

2. You should have the `develop` branch checked out and opened in your python IDE of choice.

3. You should have git installed.

4. For Windows users, I suggest not using Powershell, as it has issues running scripts, so I suggest using 
cmd or conemu.


Contribution Guide
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

Backend Local Setup
-------------------
1. Install Python for your system, ensuring that Python is available in the PATH variable (this is default 
for Mac and Linux.)

2. Install virtualenv with `pip install virtualenv`. Run this in the command line (`sudo` may be required for
Linux and Mac)

3. Create the virtual environment with `virtualenv venv` **in the project directory!!**

4. Activate virtual environment on Windows with `venv\Scripts\activate`. Activate virtual environment on
Mac or Linux with `source venv/bin/activate`. When using the fish shell `. venv/bin/activate.fish`

5. Install project requirements with `pip install -r requirements.txt` with venv activated.

Running the Dev Server
----------------------
1. Ensure that your virtual environment is running. You only need to run step 4 of the Backend Local
Setup to run your virtual environment after you've set it up. 

2.  Run `python manage.py runserver 8000` in the project directory.

3. You can now access the site at http://127.0.0.1:8000

Provisioning the Database
-------------------------
1. Ensure that your virtual environment is running. You only need to run step 4 of the Backend Local
Setup to run your virtual environment after you've set it up. 

2. Run `python manage.py migrate` in the project directory.

When making changes to the models, you need to run `python manage.py makemigrations` and then run
`python manage.py migrate`.

Making a Backend User
---------------------
1. Run the manage.py command `python manage.py createsuperuser --email yourEmail@email.com 
--username YourUserName`

Backend REST API
----------------
The REST documentation is available at /api/. If you're looking to add to the API refer to 
https://www.django-rest-framework.org/tutorial/quickstart/

Frontend Local Setup
--------------------
1. Install the current node JS LTS release https://nodejs.org/en/

2. In the project directory run `npm install --dev`

Compiling the Frontend
----------------------
In the project directory run `npm run dev`. If you're compiling for production use `npm run build`
