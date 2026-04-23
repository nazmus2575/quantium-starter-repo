#!/bin/bash

# Activate the virtual environment
source "$(dirname "$0")/.venv/bin/activate"

# Run the test suite
pytest test_app.py -v

# Capture exit code from pytest
EXIT_CODE=$?

# Return 0 if all tests passed, 1 if anything failed
if [ $EXIT_CODE -eq 0 ]; then
    echo "All tests passed."
    exit 0
else
    echo "Tests failed."
    exit 1
fi
