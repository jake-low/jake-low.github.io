FROM abiosoft/caddy:latest
MAINTAINER Jake Low <hello@jakelow.com>

COPY Caddyfile /etc/Caddyfile

COPY ./output /srv/www
