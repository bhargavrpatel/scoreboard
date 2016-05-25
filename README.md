# Scoreboard

### Prerequisites
- Assumes your username is `ubuntu` and you have sudo
- Assumes you have cloned this repo to `~`
- Assumes you already have a working hardware implementation
- Assumes nginx is already installed

### Service Creation
We will have the falcon application running as a service. To do so,
add the following to `/etc/init/scoreboard.conf`.

```
description "uWSGI server instance configured to serve myproject"

start on runlevel [2345]
stop on runlevel [!2345]

setuid ubuntu
setgid www-data

env PATH=/home/ubuntu/scoreboard/scorenv/bin
chdir /home/ubuntu/scoreboard
exec uwsgi --ini scoreboard.ini
```

### NGINX setup
Create a sites-available file at `/etc/nginx/sites-available/scoreboard`
and point it to the `scoreboard.sock` file. Ensure you replace
`<YOUR-DOMAIN>` in the snippet below.

```
server {
    listen 443;
    server_name <YOUR-DOMAIN>;

    ssl on;
    ssl_certificate /etc/nginx/ssl/nginx.crt;
    ssl_certificate_key /etc/nginx/ssl/nginx.key;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/home/ubuntu/scoreboard/scoreboard.sock;
    }
}
```

You then have to create a symlink of this file such that
`/etc/nginx/sites-enabled/scoreboard` points to
`/etc/nginx/sites-available/scoreboard`.

Essentially, you are adding scoreboard as an available "website" then
also adding it in enabled "websites" to actually enable it.


### All it takes is a little push...
* Start the scoreboard service
```sh
sudo start myproject
```
* Restart nginx
```sh
sudo service nginx restart
```


### Credits
Along with man pages, and documentations of the libraries used, a lot
of the ops stuff has been done by combining the learnings from the
following two pages; kudos to them.
* [Giant Flying Saucer](http://www.giantflyingsaucer.com/blog/?p=4342)
* [Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-14-04)
