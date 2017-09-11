=================================================
DGs: Development Goals data management platform
=================================================

DGs is an open-source data management platform for development goals.

This can be used for managing data for things like
`Sustainable Development Goals (SDGs) <http://www.un.org/sustainabledevelopment/sustainable-development-goals/>`_
, National Development Plans, Sectorial Plans, Local Government Plans and more.


Features
=========
- A faily simple and featureful web based data management interface.
- Convenient handling of multiple development plans within a single deployment.
- Support for more than one logframe structure.
- Multilingual support.
- Users authentication and access level management.
- Full-text search capabilities.
- A poweful RESTful Application Programming Interface (API).


Technology
============
The platform is developed using mostly
`Python <https://www.python.org/>`_ -
`Django framework <https://www.djangoproject.com/>`_.
`Postgresql <https://www.postgresql.org/>`_ with
`HStore <https://www.postgresql.org/docs/current/static/hstore.html>`_ extension is used as a primary database while
`Elasticsearch <https://www.elastic.co/products/elasticsearch>`_ 5 is a default search engine.

The API is built using `Django Rest Framework <http://www.django-rest-framework.org/>`_.

Additionally by default `Redis <https://redis.io/>`_ is used for caching,
`Celery <http://www.celeryproject.org/>`_ for asyncronous tasks processing and
`RabbitMQ <https://www.rabbitmq.com/>`_ is used as a message broker for Celery.

Elasticsearch, Redis, Celery and RabbitMQ are optional components therefore they can be replaced or
disabled through some project level settings.


Installation
=============
The source code works a most of other typical Django projects and
Therefore you can always find more information on internet on how to develop and deploy projects by using Django.

Install and setup postgresql
-----------------------------

Install postgresql

::

    sudo apt-get install postgresql postgresql-contrib libpq-dev

Make sure the Postgresql server is running

::

    sudo service postgresql start

Login as `postgres` (Postgresql admin user)

::

    sudo su - postgres

While logged in as `postgres` create the project database 

::

    createdb dgs

Connect to the database shell

::

    psql dgs

While you are in the database shell create the database user, grant appropriate privillages to the user and enable Hstore.

::

    CREATE USER dgs WITH PASSWORD '<your_dbuser_password>';
    GRANT ALL PRIVILEGES ON DATABASE dgs TO dgs;
    CREATE EXTENSION hstore;
    exit;

Logout as `postgres` user

::

    exit

Make sure you remember your database credentials because they are goint to be used later
in your project configuration.


Install Elasticsearch 5, Redis and RabbitMQ
--------------------------------------------

Install system wide Python dependancies
----------------------------------------

::

    sudo apt-get install python-dev python-pip libz-dev libjpeg-dev libfreetype6-dev


Setup a Python virtual environment
----------------------------------

You may need to upgrade pip

::

    sudo pip install -U pip

Using pip install python-virtualenv and python-virtualenvwrapper

::

    sudo pip install virtualenv virtualenvwrapper


Virtualenvwrapper is an optional but very convenient when working
with python virtual enviroments especially during development.
To use virtualenvwrapper you may need to make some few configurations to
your system according to its documentation
http://virtualenvwrapper.readthedocs.io/en/latest/install.html#shell-startup-file/ .

For example on ubuntu you may need to create or edit ``~/.bashrc`` or ``~/.profile`` and add the following lines

::

    export WORKON_HOME=$HOME/.virtualenvs
    export PROJECT_HOME=$HOME/Devel
    source /usr/local/bin/virtualenvwrapper.sh


You may need to start a new terminal session for the above changes to take effect.

For more information on python virtualenv and virtualenvwrapper please consult the available online resources

Create a virtualenvironment for the project

::

    mkvirtualenv dgs


Download the source code
-------------------------

Download the source code archive directly and extract its content to your working directory

**OR**

Move to the directory where you want to your source code to live
then clone the github repository

::

    git clone https://github.com/tehamalab/dgs.git

Go to project root

::

    cd dgs

make sure your python virtual environment is active then use pip to install the project requirements.

::

    pip install -r requirements.txt


Configuring the project
------------------------
Project level conigurations can be modified by using system environment variable,
using environment variables written in a file named ``.env`` in a project root or
by modifying the ``dgs/settings.py`` file directly.

For more information on django settings you can also check out https://docs.djangoproject.com/en/1.11/topics/settings/

Checking if things are ok

::

    python manage.py check

Create database tables

::

    python manage.py migrate

Create a superuser for the project

::

    python manage.py createsuperuser

**NOTE:** When you are executing ``python manage.py ...`` commands make sure the vertualenv is active.

Starting the development server
--------------------------------

Django comes with an inbuilt server which can be used during development.
You shouldn't be using this server on production sites.

To start the development server within your project root directory run something like

::

    python manage.py runserver 8000

Now you will be able to access a site locally via http://127.0.0.1:8000


Deployment
-----------

Since this is a typical Django project any standard Django deployment stack can be used.
For more information on Django deployment please look for available resources on the
Internet including https://docs.djangoproject.com/en/1.11/howto/deployment/


Most of modern Django deployments usually include a frontend web/proxy server like Nginx,
an application server  like Gunicorn or uWSGI and a process manager like supervisor (especially when using Gunicorn)


Data visualization
--------------------

The project offers an API which allows building unlimited custom visualizations and data driven application.

One of the aaplications for providing a public portal based on DGs API can be found at https://github.com/tehamalab/dgs-dash
