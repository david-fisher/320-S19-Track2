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
1. Branch off of the `develop` branch and name your new branch after the feature you are creating.
2. Commit your code to your new branch with commit messages in proper English with capitalization
and punctuation.
3. Once you are content with your branch create a pull request to merge back into the `develop`
branch.
4. Share that pull request with your peers and incorporate any feedback they may have, or defend
your code professionally. 

Backend Local Setup
-------------------
1. Install Python for your system, ensuring that Python is available in the PATH variable (this is default 
for Mac and Linux.)
2. Install virtualenv with `pip install virtualenv`. Run this in the command line (`sudo` may be required for
Linux and Mac)
3. Create the virtual environment with `virtualenv venv` **in the project directory!!**
4. Activate virtual environment on Windows with `venv\Scripts\activate`. Activate virtual environment on
Mac or Linux with `source venv/bin/activate`.
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
