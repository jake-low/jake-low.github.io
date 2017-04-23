FROM nginx:latest
MAINTAINER Jake Low <hello@jakelow.com>

COPY nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /etc/letsencrypt/live/jakelow.com

RUN openssl req -x509 -nodes -days 365 -newkey rsa:4096 \
  #-newkey ec -pkeyopt ec_paramgen_curve:prime256v1 \
  -subj "/C=US/ST=Washington/L=Seattle/O=jakelow.com/CN=jakelow.com" \
  -keyout /etc/letsencrypt/live/jakelow.com/privkey.pem \
  -out /etc/letsencrypt/live/jakelow.com/fullchain.pem

COPY ./output /srv
