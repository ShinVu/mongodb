#!/bin/bash

set -e

# Use the environment variables to run the MongoDB Exporter
exec mongodb_exporter \
  --mongodb.uri="${MONGODB_URI}" \
  --collect-all \
  --log.level="${LOG_LEVEL}"