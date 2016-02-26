#!/bin/bash

NAME="hello_app"                                  # Name of the application
DJANGODIR=/webapps/infodiscovery/infodiscovery             # Django project directory
SOCKFILE=/webapps/infodiscovery/run/gunicorn.sock  # we will communicte using this unix socket
USER=daljeet     #the user to run as
GROUP=webapps
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=infodiscovery.settings             # which settings file should Django use
DJANGO_WSGI_MODULE=infodiscovery.wsgi                     # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source ../bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
    --name $NAME \
    --workers $NUM_WORKERS \
    --user=$USER --group=$GROUP \
    --bind=unix:$SOCKFILE \
    --log-level=debug \
    --log-file=-
