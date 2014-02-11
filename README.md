mediaserver
===========

Our media server.


# Developer Setup

* Create a settings file for your machine

Set these environment variables:

* mysql_user
* mysql_password
* DJANGO_SETTINGS_MODULE to something like mediaserver.settings_nickc

If you're on OSX you'll probably need to set `DYLD_LIBRARY_PATH` to `/usr/local/mysql/lib`

You'll want to set these in your IDE and in your virtualenv.

To do this, edit `~/.virtualenvs/mediaserver/bin/activate` and add lines like this:

    export DJANGO_SETTINGS_MODULE=mediaserver.settings_nickc
    export mysql_user=root
    export mysql_password=blah

Create a database.

Set up the database

    manage.py syncdb
    manage.py migrate

Add some disks to monitor

Go to /admin to access the Django admin and add a new disk model.
Set the name to '/' or whatever mount point you want. Set the numeric values to 1.
hit /disk/update to update the models and get a json representation of how full your disks are.