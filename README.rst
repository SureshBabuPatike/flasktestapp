===============================
flasktestapp
===============================

A Flask app for learning Flask


Quickstart
----------

First, set your app's secret key as an environment variable. For example, example add the following to ``.bashrc`` or ``.bash_profile``.

.. code-block:: bash

    export FLASKTESTAPP_SECRET='something-really-secret'

Before running shell commands, set the ``FLASK_APP`` environment variable ::

    export FLASK_APP=/path/to/autoapp.py

Then run the following commands to bootstrap your environment ::

    git clone https://github.com/westurner/flasktestapp
    cd flasktestapp
    pip install -r requirements/dev.txt
    bower install
    flask run

You will see a pretty welcome screen.

Once you have installed your DBMS, run the following to create your app's database tables and perform the initial migration ::

    flask db init
    flask db migrate
    flask db upgrade
    flask run


Deployment
----------

In your production environment, make sure the ``FLASKTESTAPP_ENV`` environment variable is set to ``"prod"``.


Shell
-----

To open the interactive shell, run ::

    flask shell

By default, you will have access to the flask ``app``.


Running Tests
-------------

To run all tests, run ::

    flask test


Migrations
----------

Whenever a database migration needs to be made. Run the following commands ::

    flask db migrate

This will generate a new migration script. Then run ::

    flask db upgrade

To apply the migration.

For a full migration command reference, run ``flask db --help``.
