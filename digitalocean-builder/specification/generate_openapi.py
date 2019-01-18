"""
This generates staging and production swagger specifications from an env-agnostic swagger.yml file.
"""
import os
import json
import yaml

from swagger_spec_validator.validator20 import validate_spec


def read_yaml(filename):
    with open(filename, 'r') as stream:
        return yaml.load(stream)


def write_yaml(filename, data):
    with open(filename, 'w') as stream:
        return yaml.dump(data, stream)


def merge(swagger, config):
    """
    This does the actual merging of the generic swagger doc with a config, which provides environment-specific
    overrides.
    """
    swagger['info']['title'] = config['title']
    swagger['host'] = config['host']
    swagger['securityDefinitions']['firebase']['x-google-issuer'] = config['firebaseSecurity']['issuer']
    swagger['securityDefinitions']['firebase']['x-google-audiences'] = config['firebaseSecurity']['audiences']

    # This is a hacky way to ensure all keys end up as strings, which is required for the validator
    return json.loads(json.dumps(swagger))


def validate(swagger):
    """
    Perform swagger spec validation, along with additional validation required by cloud endpoints.
    """
    validate_spec(swagger)

    slashed_paths = []
    missing_operations = []

    for path_name, path_definition in swagger['paths'].items():
        if path_name.endswith('/'):
            slashed_paths.append(path_name)

        for method_name, method_definition in path_definition.items():
            if 'operationId' not in method_definition.keys():
                missing_operations.append(f'{method_name} {path_name}')

    if slashed_paths:
        print('The following endpoints end with a slash, which are invalid in cloud endpoints:')
        print('\n'.join(slashed_paths))

    if missing_operations:
        print('The following endpoints are missing an "operationId":')
        print('\n'.join(missing_operations))

    if slashed_paths or missing_operations:
        exit(1)


def main():
    """
    The primary program flow.
    """
    # Make sure we are in the specifications dir
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    swagger = read_yaml('swagger.yml')
    staging_config = read_yaml('staging.yml')
    production_config = read_yaml('production.yml')

    staging_swagger = merge(swagger, staging_config)
    validate(staging_swagger)

    production_swagger = merge(swagger, production_config)
    validate(production_swagger)

    write_yaml('../artifacts/swagger-staging.yml', staging_swagger)
    write_yaml('../artifacts/swagger-production.yml', production_swagger)


if __name__ == '__main__':
    main()
