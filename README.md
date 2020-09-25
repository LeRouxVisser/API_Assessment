# API_Assessment
## Installing prerequisites and running program

Before running the code first run the following to make sure all dependencies are installed.

```
pip install -r requirements.txt
```
After the dependencies have been installed successfully, run the following three line:

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
#############################################################################################

## How scalability was implemented

The program will request a unique request once every day and then store it in the database. 
If the same request comes in again on that day, the API will not send a request to the https://www.coingecko.com/en/api given endpoint.
The API will rather take the already stored data, previous stored for that exact request earlier that day and respond with the given data stored.
All data will be truncated in the sqlite3 databases, for 2 tables used, everyday once the first request for the new day is made.
This will ensure the data is always up to date in the database and the DB does not run out of storage space.
