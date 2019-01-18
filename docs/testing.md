# Testing

The project is linted with [flake8](http://flake8.pycqa.org/en/latest/) and unittested with standard
[unittest](https://docs.djangoproject.com/en/1.11/topics/testing/overview/).

## Running Tests

The unit and functional tests can be run with:

```bash
make test
```

in the root of the repo.

## Swagger Validation

The project uses a special API Client in its API unittests that loads the swagger definition and validates that
responses conform to the swagger spec. This special API client comes from our
[wpe-django-swagger](https://github.com/wpengine/wpe-django-swagger) python package.
