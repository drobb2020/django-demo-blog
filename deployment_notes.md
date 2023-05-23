# Deploying to a Ubuntu Server

IMPORTANT: When running these commands and configurations on the server make sure you are doing this as root. By default Ubuntu does not allow a direct login as root since the account does not have a password. To set a password on the root user do the following:

- sudo passwd root
- enter your password
- enter the password you want to set for root
- repeat the password

Now log off the server and re-authenticate as root.

## Preparing the Server

Install the following software packages on the server

* [X] python3-pip
* [X] python-dev
* [X] libpq-dev
* [X] postgresql-contrib
* [X] nginx

## Creating the Database

Run the following commands to create the postgresql database:

* [X] sudo -u postgres psql (login to console)
* [X] CREATE DATABASE djangoblog;
* [X] CREATE USER djangobloguser WITH PASSWORD 'djangoblogpassword';
* [X] ALTER ROLE djangobloguser SET client_encoding TO 'utf8';
* [X] ALTER ROLE djangobloguser SET default_transaction_isolation TO 'read committed';
* [X] ALTER ROLE djangobloguser SET timezone TO 'UTC';
* [X] GRANT ALL PRIVILEGES ON DATABASE djangoblog TO djangobloguser;
* [X] \q to exit

## Creating the virtual environment

Create a virtual environment for Python

* [X] Install virtualenv (or venv)
  * [X] sudo -H pip3 install --upgrade pip
  * [X] sudo -H pip3 install virtualenv (or venv)
* [X] Create folder to host the project
  * [X] mkdir -p /webapps/django-demo-blog
* [X] Create a Linux group and user
  * [X] sudo groupadd --system webapps
  * [X] sudo useradd --system --gid webapps --shell /bin/bash --home /webapps/django-demo-blog django
* [X] Create environment
  * [X] cd /webapps/django-demo-blog
  * [X] virtualenv env_3.10.6
  * [X] source env_3.10.6/bin/activate
  * [X] cd env_3.10.6/

## Cloning project from Github

* [X] git clone https://github.com/drobb2020/django-demo-blog.git
* [X] Install packages and postgresql driver
  * [X] pip install -r requirements.txt
  * [X] pip install psycopg2-binary

## Configure settings.py for new database

* [X] Configure settings.py to use postgresql database
  * [X] Copy the current settings.py to settingsDev.py
  * [X] Edit settings.py and do the following:
    * [X] Go to ALLOWED_HOSTS and add the dns name of the server
    * [X] Go to DATABASES and make the following modifications
      * change 'django.db.backends.sqlite3' to 'django.db.backends.postgresql_psycopg2'
      * set NAME to djangoblog
      * set USER to djangobloguser
      * set PASSWORD to djangoblogpassword
      * set HOST to localhost
      * set PORT to 5432 or ''
    * [X] run python manage.py makemigrations
    * [X] run python manage.py migrate
    * [X] run python manage.py createsuperuser
    * [X] run python manage.py collectstatic

## Install and configure gunicorn

* [X] pip install gunicorn
* [X] in the bin folder of the virtual environment create a script named gunicorn_start and add the following lines:

    ``` sh
    #!/bin/bash

    NAME='djangoblog'
    DJANGODIR=/webapps/djangoblog/env_3.10.6/djangoblog
    SOCKFILE=/webapps/djangoblog/env_3.10.6/run/gunicorn.sock
    USER=djangoblog
    GROUP=webapps
    NUM_WORKERS=5
    DJANGO_SETTINGS_MODULE=django-demo-blog.settingsprod
    DJANGO_WSGI_MODULE=django-demo-blog.wsgi
    TIMEOUT=120

    cd $DJANGODIR
    source ../env_3.10.6/bin/activate
    export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
    export PYTHONPATH=$DJANGODIR:$PYTHONPATH

    RUNDIR=$(dirname $SOCKFILE)
    test -d $RUNDIR || mkdir -p $RUNDIR

    exec ../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
    --name $NAME \
    --workers $NUM_WORKERS \
    --timeout $TIMEOUT \
    --user=$USER --group=$GROUP \
    --bind=unix:$SOCKFILE \
    --log-level=debug \
    --log-file=-
    ```

* [X] chmod +x bin/gunicorn_start
* [X] ./bin/gunicorn_start (to test) (troubleshoot if it does not start, stop it if it does start)
* [X] at this point all the files and folders under env_3.10.6 are owned by root:root. This needs to be modified so that all files and folder are owned by django:webapps. To do this run the following command:
  * [X] make sure you are in the env_3.10.6 folder
  * [X] chown -R django:webapps .

## Install and Configure Supervisor

* [X] Install and setup supervisor
  * [X] apt install supervisor
  * [X] cd /etc/supervisor/conf.d/
  * [X] Create the following configuration file djangoblog.conf

    ```sh
    [program:djangoblog]
    command = /webapps/djangoblog/env_3.10.6/bin/gunicorn_start
    user = djangoblog
    stdout_logfile = /webapps/djangoblog/env_3.10.6/logs/supervisor.log
    redirect_stderr = true
    environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8
    ```

    * [X] create the logs folder under env_3.10.6/
    * [X] Run supervisorctl reread - this should read in the djangoblog.conf file.
    * [X] Run supervisorctl update
    * [X] Run supervisorctl status to see the running status of djangoblog

## Install and Configure nginx

* [X] Setup nginx
  * [X] cd /etc/nginx/sites-available/
  * [X] create a djangoblog.conf file with the following contents:

    ```sh
    upstream djangoblog_app_server {
        server unix:/webapps/djangoblog/env_3.10.6/run/gunicorn.sock fail_timeout=0;
    }

    server {
        listen 80;
        server_name blog.excession.org;

        access_log /webapps/djangoblog/env_3.10.6/logs/nginx-django-access.log;
        error_log /webapps/djangoblog/env_3.10.6/logs/nginx-django-error.log;

        location /static/ {
            alias /webapps/djangoblog/env_3.10.6/djangoblog/static/;
        }

        location /media/ {
            alias /webapps/djangoblog/env_3.10.6/djangoblog/media/;
        }

        location / {
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

            proxy_set_header Host $http_host;

            proxy_redirect off;

            if (!-f $request_filename) {
                proxy_pass http://djangoblog_app_server
            }
        }
    }
    ```

  * [X] cd ../sites-enabled/
  * [X] ln -sf ../sites-available/djangoblog.conf .
  * [X] service nginx restart
  * [X] If everything is running as expected, go back into settingsprod.py and change DEBUG = True to False
  * [X] Restart supervisor with the command: supervisorctl restart djangoblog
  - Whenever you make a change to any files in the django project you must restart the supervisor for the changes to take effect.
