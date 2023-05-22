# Deploying to a Ubuntu Server

## Preparing the Server

* [X] Install needed software packages on server
  * [X] python3-pip
  * [X] python-dev
  * [X] libpq-dev
  * [X] postgresql-contrib
  * [X] nginx

## Creating the Database

* [X] Create postgresql database
  * [X] sudo -u postgres psql (login to console)
  * [X] CREATE DATABASE djangoblog;
  * [X] CREATE USER djangobloguser WITH PASSWORD 'djangoblogpassword';
  * [X] ALTER ROLE djangobloguser SET client_encoding TO 'utf8';
  * [X] ALTER ROLE djangobloguser SET default_transaction_isolation TO 'read committed';
  * [X] ALTER ROLE djangobloguser SET timezone TO 'UTC';
  * [X] GRANT ALL PRIVILEGES ON DATABASE djangoblog TO djangobloguser;
  * [X] \q to exit

## Creating the virtual environment

* [X] Install virtualenv (or venv)
  * [X] sudo -H pip3 install --upgrade pip
  * [X] sudo -H pip3 install virtualenv (or venv)
* [X] Create folder
  * [X] mkdir -p /webapps/django-demo-blog
* [X] Create Linux group and user
  * [X] sudo groupadd --system webapps
  * [X] sudo useradd --system --gid webapps --shell /bin/bash --home /webapps/django-demo-blog django
* [X] Create environment
  * [X] cd /webapps/django-demo-blog
  * [X] virtualenv env_3.10.6
  * [X] source env_3.10.6/bin/activate
  * [X] cd env_3.10.6/

## Cloning project from Github

* [X] Clone project from Github
  * [X] git clone https://github.com/drobb2020/django-demo-blog.git
* [X] Install packages and postgresql driver
  * [X] pip install -r requirements.txt
  * [X] pip install psycopg2-binary

## Configure settings.py for new database

* [X] Configure settings.py to use postgresql database
  * [X] Copy settings.py to settingsprod.py
  * [X] Edit settings.py and do the following:
    * [X] Go to DATABASES and make the following modifications
      * add dns name for the server to ALLOWED_HOSTS
      * change 'django.db.backends.sqlite3' to 'django.db.backends.postgresql_psycopg2'
      * set NAME to djangoblog
      * set USER to djangobloguser
      * set PASSWORD to djangoblogpassword
      * set HOST to localhost
      * set PORT to 5432 or ''
    * [X] run python manage.py makemigrations --settings djangoblog.settingsprod
    * [X] run python manage.py migrate --settings djangoblog.settingsprod
    * [X] run python manage.py createsuperuser --settings djangoblog.settingsprod

## Install and configure gunicorn

* [ ] Install and setup gunicorn
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

    * [X] sudo chmod +x bin/gunicorn_start
    * [X] ./bin/gunicorn_start (to test) (troubleshoot if it does not start, stop it if it does start)

## Install and Configure Supervisor

* [X] Install and setup supervisor
  * [X] sudo apt install supervisor
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
    * [X] Do a sudo chown -R djangoblog:webapps .
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
