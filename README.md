# datadog-otlp

test project sending OpenTelemetry traces in OTLP to datadog-agent


## Pre-requisite

 - `docker`
 - `docker-compose`
 - a valid datadog api key


## Usage

### Start

`DD_API_KEY=<valid_api_key> make run`


### Http request

`make curl`: issues an Http request to the running service.

Default path is `/redis/${KEY}`.

To override the key for redis: `KEY=<my_key> make curl`.

To change to a different route: `ROUTE=/foo make curl`.

Supported routes:
 - `/`
 - `/ot`
 - `/redis/<key>`


### Stop

`make stop`


## Diagnose

1. [terminal 0] start the service on.
2. [terminal 1] run `make ssh` and you're inside `datadog-agent` container as root.
3. [terminal 1] run `apt update && apt install -y net-tools tcpdump`
4. [terminal 1] verify connections: `netstat -apln`
5. [terminal 1] start tcpdump for trace related ports: `tcpdump -nnA -s 0 -i any "port 4317 or 5003"`
6. [terminal 2] run `make curl`
7. [terminal 0] observe `stdout`: a otlp console exporter is active in the pipeline.
8. [terminal 1] observe `tcpdump` output: `4317` port receives the trace telemetry but not `5003`
