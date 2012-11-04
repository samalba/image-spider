#!/bin/sh

source $(dirname $0)/credentials.sh

$(dirname $0)/../tests/api.py
