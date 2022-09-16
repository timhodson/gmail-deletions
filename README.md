# Delete Gmail Emails

These scripts based on the quickstart code at <https://developers.google.com/gmail/api/quickstart/python#step_1_install_the_google_client_library>

1. Have `python` and `pipenv` installed
2. In the repo root run `pipenv install` which will install the dependancies for the APIs.
3. __DON'T just run the scripts. You need to modify them first__
4. Get a `credentials.js` file. create your own https://developers.google.com/workspace/guides/create-credentials
   1. Gmail API.
   2. Select the `https://mail.google.com/` scope when needed.
   3. When you have downloaded the credentials file update the path to point to it in both scripts.
5. run `pipenv shell` to put you in the virtual environment which contains all the right packages.
6. Identify the Label ID for your particular label.
   1. Run the Script `python quickstart.py`
   2. It will open a browser window and ask you to allow the application to access your account
   3. It will then print out the labels and IDs for your emails.
   4. Authorization will only happen the first time, or after token expiry.
7. Modify the `delete-emails.py` script to use your label id
8. Run the script `python delete-emails.py`
   1. __Line 91 is commented out this is the line that ACTUALLY does the deletion__ uncomment when you are ready.

