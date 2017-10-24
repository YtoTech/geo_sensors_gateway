# Inspired by https://github.com/erlang/docker-erlang

# It misses things to fetch package by rebar.
# Maybe wget? curl?
# FROM erlang:20.0.2-alpine
FROM erlang:latest

# Install Rebar3.
# RUN mkdir -p /usr/bin
ADD https://s3.amazonaws.com/rebar3/rebar3 /usr/bin/rebar3
RUN chmod a+x /usr/bin/rebar3

# Setup Environment.
# ENV PATH=:/usr/bin/rebar3:$PATH

# Working directory.
RUN mkdir -p /home/geo-sensors-gateway
WORKDIR /home/geo-sensors-gateway

# TODO Do not copy configuration.json. Use another way to provide it?
# Mount directory? We can put it in a config sub-direct so we can mount it only.
# Implement a provider fetching from web?
# Local file still should be a way to get started.
COPY rebar.config rebar.lock Makefile /home/geo-sensors-gateway/
COPY src/* /home/geo-sensors-gateway/src/

RUN make release
COPY configuration.docker.json /home/geo-sensors-gateway/_build/prod/rel/GeoSensorsGateway/configuration.json
RUN mkdir -p /home/geo-sensors-gateway/dumps

# Expose relevant ports.
EXPOSE 25

CMD ["make", "start"]
