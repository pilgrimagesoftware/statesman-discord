#!/bin/bash

set -e

scriptdir="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

cd ${scriptdir}/..

colima start || true

docker-compose -f ${scriptdir}/docker/docker-compose.yml up

colima stop
