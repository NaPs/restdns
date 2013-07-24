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

REST API
--------

Zones
~~~~~

Properties:

- name (string, read): name of the zone (without the final dot)
- refresh (integer, read/write): refresh delay value
- retry (integer, read/write): retry delay value
- expire (integer, read/write): expire delay value
- minimum (integer, read/write): minimum delay value
- rname (string, read/write): administrator email adress
- primary_ns (string, read/write): primary name-server address
- serial (integer, read): serial number
- url (string, read): url to the zone
- records_url (string, read): url to zone records

List all zones
^^^^^^^^^^^^^^

Request::

    GET /zones

Reponse::

    < 200
    < Content-Type: application/json

    {
        "zones": [
            {"name": "example.com",
             "refresh": 300,
             "retry": 300,
             "expire": 604800,
             "minimum": 86400,
             "rname": "admin.example.com.",
             "primary_ns": "ns.example.net."
             "serial": 42,
             "url": "/zones/example.com",
             "records_url": "zones/example.com/records"},
            {"name": "my.lan",
             "refresh": 300,
             "retry": 300,
             "expire": 604800,
             "minimum": 86400,
             "rname": "admin.my.lan.",
             "primary_ns": "ns.my.lan."
             "serial": 21,
             "url": "/zones/my.lan",
             "records_url": "zones/my.lan/records"},
        ]
    }

Create a new zone
^^^^^^^^^^^^^^^^^

Request::

    POST /zones
    > Content-Type: application/json

    {"name": "exemple.fr",
     "refresh": 300,
     "retry": 300,
     "expire": 604800,
     "minimum": 86400,
     "rname": "admin.example.fr.",
     "primary_ns": "ns.example.org."}

Response::

    < 201
    < Location: /zones/example.fr
    < Content-Type: application/json

    {"name": "exemple.fr",
     "refresh": 300,
     "retry": 300,
     "expire": 604800,
     "minimum": 86400,
     "rname": "admin.example.fr.",
     "primary_ns": "ns.example.org.",
     "serial": 1,
     "url": "/zones/example.fr",
     "records_url": "/zones/example.fr/records"}

Get zone details
^^^^^^^^^^^^^^^^

Request::

    GET /zones/example.com

Response::

    < 200
    < Content-Type: application/json

    {"name": "example.com",
     "refresh": 300,
     "retry": 300,
     "expire": 604800,
     "minimum": 86400,
     "rname": "admin.example.com.",
     "primary_ns": "ns.example.net."
     "serial": 42,
     "url": "/zones/example.com",
     "records_url": "zones/example.com/records"},

Modify a zone
^^^^^^^^^^^^^

Request::

    PUT /zones/example.com
    > Content-Type: application/json

    {"refresh": 300,
     "retry": 300,
     "expire": 604800,
     "minimum": 86400}

Response::

    < 200
    < Content-Type: application/json

    {"name": "exemple.fr",
     "refresh": 300,
     "retry": 300,
     "expire": 604800,
     "minimum": 86400,
     "rname": "admin.example.fr.",
     "primary_ns": "ns.example.org.",
     "serial": 2,
     "url": "/zones/example.fr",
     "records_url": "/zones/example.fr/records"}

Delete a zone
^^^^^^^^^^^^^

Request::

    DELETE /zones/example.com

Response::

    < 204

Records
~~~~~~~

Properties:

- uuid (string, read): uuid of the record
- name (string, read/write): name of the record
- type (string, read/write): type of the record
- parameters (object, read/write): object of parameters of the record according to the type
- url (string, read/write): url of the record

List all records for a zone
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Request::

    GET /zones/example.com/records

Response::

    < 200
    < Content-Type: application/json

    {"records": [{"uuid": "fee3670a-fe68-4bb4-a926-009f0e01c41c",
                  "name": "www",
                  "type": "a",
                  "parameters": {"ip": "127.0.0.1"},
                  "url": "/zones/example.com/records/fee3670a-fe68-4bb4-a926-009f0e01c41c"},
                 {"uuid": "671969b0-c88e-4a65-ac98-7d736e135bf3",
                  "name": "www",
                  "type": "aaaa",
                  "parameters": {"ipv6": "::1"},
                  "url": "/zones/example.com/records/671969b0-c88e-4a65-ac98-7d736e135bf3"}]}

Create a new record
^^^^^^^^^^^^^^^^^^^

Request::

    POST /zones/example.com/records
    > Content-Type: application/json

    {"name": "",
     "type": "mx",
     "parameters": {"pref": 5, "name": "mx.example.net"}}

Response::

    < 201
    < Location: /zones/example.com/records/4901adf8-f26d-400a-8ac1-b978c116cff
    < Content-Type: application/json

    {"uuid": "4901adf8-f26d-400a-8ac1-b978c116cff5",
     "name": "",
     "type": "mx",
     "parameters": {"pref": 5, "name": "mx.example.net"},
     "url": "/zones/example.com/records/4901adf8-f26d-400a-8ac1-b978c116cff5"}

Modify a record
^^^^^^^^^^^^^^^

Request::

    PUT /zones/example.com/records/fee3670a-fe68-4bb4-a926-009f0e01c41c
    > Content-Type: application/json

    {"name": "www",
     "type": "a",
     "parameters": {"127.0.0.2"}}

Response::

    < 200
    < Content-Type: application/json

    {"uuid": "fee3670a-fe68-4bb4-a926-009f0e01c41c",
     "name": "www",
     "type": "a",
     "parameters": {"ip": "127.0.0.2"},
     "url": "/zones/example.com/records/fee3670a-fe68-4bb4-a926-009f0e01c41c"}}

Delete a record
^^^^^^^^^^^^^^^

Request::

    DELETE /zones/example.com/records/fee3670a-fe68-4bb4-a926-009f0e01c41c

Response::

    < 204

List record types
^^^^^^^^^^^^^^^^^

Request::

    GET /record/types

Response::

    < 200
    < Content-Type: application/json

    {"a": {"parameters": ["ip"]},
     "aaaa": {"parameters": ["ipv6"]},
     "mx": {"parameters": ["pref", "name"]}}

Contribute
----------

You can send your pull-request for RestDNS through Github:

    https://github.com/NaPs/RestDNS

I also accept well formatted git patches sent by email.

Feel free to contact me for any question/suggestion/patch: <antoine@inaps.org>.