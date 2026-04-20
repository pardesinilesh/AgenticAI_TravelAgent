#!/bin/bash
# Run all travel planning tests in the testing folder
set -e

echo "Running travel planning tests..."
pytest testing/ --maxfail=2 --disable-warnings -v
