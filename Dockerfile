# Builder

FROM ruby:2.4-alpine as builder

# Sass needs libffi, which needs libffi and ruby C headers
RUN apk --update add build-base ruby-dev libffi-dev exiftool imagemagick

RUN mkdir /jakelow.com
WORKDIR /jakelow.com
COPY Gemfile /jakelow.com
COPY Gemfile.lock /jakelow.com
RUN bundle install

COPY . /jakelow.com
RUN bundle exec nanoc compile

# Runner

FROM abiosoft/caddy:latest
COPY --from=builder /jakelow.com/output /srv/www
COPY --from=builder /jakelow.com/Caddyfile /srv
WORKDIR /srv
ENTRYPOINT ["caddy"]
