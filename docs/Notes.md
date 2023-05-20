# Project Setup

Only after when you install python first time in your PC
    
    pip install pipenv

# To Create a new project with pipenv 

Create a project folder (Project Name) inside that folder Run
    
    pipenv install django

+   This will create the pip-file and pip-lock file. 

Sub Commands to help you to  
    
    pipenv shell //(Activate pipenv)      
    pipenv --venv //(path to pipenv) 

To Create/Start a Project 
    
    django-admin startproject --projectName-- .

+ This will add manage.py and project folder

$$
---
$$
## To Create new pipenv in Existing Project
Simply Run this command in the Project Folder

    pipenv install

+ This will create a new env for you project and Auto install pages
+ you can now config the path to you IDE

# To Create a App In You Project
    python manage.py startapp --appName--
+ Will add a new app folder.
+ Don't forgot to register the app in the project 'setting.py > INSTALLED_APPS'


//Token 
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg0NDIyOTM4LCJpYXQiOjE2ODQzMzY1MzgsImp0aSI6IjE0ZDkwZmRlZDg4ZjQyYjRiNWRjNWRiZjcxZTBhOWU5IiwidXNlcl9pZCI6MX0.WmPut8rql_nKmHAu8umy8NnQkcbrQlv3QnRmJv0_XyY