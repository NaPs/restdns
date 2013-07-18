RestDNS README
==============

RestDNS is a REST API used to store and manage your DNS zones. Also look at
`restdns-cli <https://github.com/NaPs/restdns-cli>`_ and
`restdns-bind <https://github.com/NaPs/restdns-bind>`_

Setup
-----

RestDNS is packaged for the Debian Wheezy distro, but since its a standard
Django application, it should be easy to install it on any other distro.

Install the RestDNS package
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add these lines in your ``/etc/apt/source.list`` file::

    deb http://debian.tecknet.org/debian wheezy tecknet
    deb-src http://debian.tecknet.org/debian wheezy tecknet

Add the Tecknet repositories key in your keyring:

    # wget http://debian.tecknet.org/debian/public.key -O - | apt-key add -

Update and install the *restdns* package::

    # aptitude update
    # aptitude install restdns

The installation procedure will configure the database (SQLite by default)
in the ``/var/lib/restdns/`` directory.

Configure Gunicorn
~~~~~~~~~~~~~~~~~~

The next step is to configure gunicorn to serve the restdns application, in
the ``/etc/gunicorn.d/`` directory, copy the ``restdns.example`` file
to ``restdns``::

    # cd /etc/gunicorn.d
    # cp restdns.example restdns

You can customize the file to add or change Gunicorn options such as the http
listening port (by default 9001) or the number of workers to start.

Restart the Gunicorn daemon to start RestDNS::

    # service gunicorn restart

Configure the web server
~~~~~~~~~~~~~~~~~~~~~~~~

The last thing to do is to configure a web server to reverse proxify the
RestDNS application. Here is an example for nginx::

    # cat /etc/nginx/site-enabled/restdns
    server {
        location / {
            proxy_pass_header Server;
            proxy_set_header Host $http_host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_pass http://127.0.0.1:9001/;
            proxy_redirect default;
        }
    }

Contribute
----------

You can send your pull-request for RestDNS through Github:

    https://github.com/NaPs/RestDNS

I also accept well formatted git patches sent by email.

Feel free to contact me for any question/suggestion/patch: <antoine@inaps.org>.