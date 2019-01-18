#!/usr/bin/env python3

"""
Script used to validate the swapper spec that lives in this repo. Nothing more, nothing less.
"""


import json
import yaml

from swagger_spec_validator.validator20 import validate_spec

SWAGGER_FILE = 'specification/swagger.yml'

with open(SWAGGER_FILE, 'r') as f:
    schema = yaml.load(f)

# This is a hacky way to ensure all keys end up as strings, which is required for the validator
schema = json.loads(json.dumps(schema))

try:
    validate_spec(schema)
except Exception as error:
    print(SWAGGER_FILE + ' is not valid: {}'.format(error))
    exit(1)
