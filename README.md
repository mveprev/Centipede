# Team *Centipede* Small Group project

## Team members
The members of the team are:
- *Ricky Brown*
- *Abdul Khan*
- *Yusheng Lu*
- *Guy Van Dijken*
- *Maksim Veprev*

## Project structure
The project is called `msms` (Music School Management System).  It currently consists of a single app `lessons` where all functionality resides.

## Deployed version of the application
The deployed version of the application can be found at *https://guyvandijken.pythonanywhere.com/*.

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Migrate the database:

```
$ python3 manage.py migrate
```

Seed the development database with:

```
$ python3 manage.py seed
```

Run all tests with:
```
$ python3 manage.py test
```

*The above instructions should work in your version of the application.  If there are deviations, declare those here in bold.  Otherwise, remove this line.*

## Sources
The packages used by this application are specified in `requirements.txt`

utils.py from Line0 to Line36 and views.py from Line489 to Line532 implement the Calendar function for Teacher Timetable. Reference link:
- *https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html*
