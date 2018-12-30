This document describes the guidelines followed for contributing to this project.

# Project structure
    docs/
    pyxpiral/
        __init__.py
        pyxpiral.py
        tests/
            __init__.py
           pyxpiral_test.py
    .coveragerc
    .gitignore
    .pylintrc
    .travis.yml
    CHANGELOG.md
    CONTRIBUTING.md
    LICENSE
    MANIFEST.in
    pytest.ini
    README.md
    requirements.txt
    setup.py

## Python code
Package names must follow Python conventions. Package folders should contain only Python code. All the common Python standards should be applied in these folders.

### Distributed data
Project data to be packaged on the distributed release must be included in:

- `PACKAGE_DATA` from the setup.py file
- as a global-include on `MANIFEST.in`

## Continuous code quality support files
These files should be located at the root of the project repo.

- `.coveragerc:` Used to configure unitary test coverage analysis.
- `.pytest.ini:` Used to configure unitary test location and options.
- `.pylintrc:` Used to configure violations policy for the project.
- ``.travis.yml:`` Used to define the continuous integration and delivery pipelines.

> Do not modify these files.

## Standard project documentation
The basic project documentation must be stored at the root of the project repo. It is composed by the files `CHANGELOG.md`, `CONTRIBUTING.md`, `LICENSE`, `MANIFEST.in` and `README.md`. Additional documentation files can be added to the project if required.

> The embedded documentation must be written in [Markdown](https://en.wikipedia.org/wiki/Markdown). This is indicated with the extension .md. The `LICENSE` file is plain text, so no .md extension is used.

### README.md
`README.md` contains the following information, if no dedicated file or support has been created for each case:

- Description of the project.
- Disclaimers.
- Support information for deployment and usage on production and test environments.
- Brief description of exposed interfaces.
- Support and contact information.


### CHANGELOG.md
This file must contain a record of any change distributed as a released version of the project.

## Packaging and distribution support files
`setup.py`, `MANIFEST.in` and `requirements.txt` are standard python files used during the distribution process.

> These files must be kept up to date. Any proposed modifications must be discussed and approved before being merged into the project.

## docs/
Contains more detailed documentation, such as auto generated API docs.

## demo/
Contains example code and outputs.

## support/
Resources useful for the development process, not to be present on the binary distribution.

# Deployment

## End user distribution
The end user distribution should be generated following the next steps:

- Update version number stored on `__init__.py`.
- Update `CHANGELOG.md`.
- Run distribution generation script:

```
    python setup.py sdist
```

- *Commit* and *push* the modifications made to `setup.py` and `CHANGELOG.md`. **The generated distribution files must not be committed**. By default all the distribution files are added to the `.gitignore` but be careful if unexpected output is generated.
- Submit a *pull request* to the `master` branch of your project.

### Version numbers
This project uses [Semantic versioning](https://en.wikipedia.org/wiki/Software_versioning#Degree_of_compatibility). The format of each version is `[major].[minor].[patch]`, e.g: `1.2.3`

## Development environment

- Usage of [virtualenv](https://virtualenv.pypa.io/en/latest/) or any other kind of sandboxed python environemnt is recommended.
- *Clone* the repository of the project in your local workspace.
- *Switch/Checkout* to `development` or the appropiate feature branch.
- Run pip install from the cloned repo parent folder:

```
    pip install -U -e pyxpiral
```

- Check if all the requirements in `requirements.txt` have been installed and your project is installed in development mode by running `pip freeze` command on your python environment and verifying the command output displays a reference to the project repo:


```
    pip freeze
    ...
    -e git+https://github.com/elcodedocle/pyxpiral.git@e5cac9411fb47d7cf4e7e20a3b5a35fb7323d7a2#egg=pyxpiral
    ...
```

At this point you should be able to use the installed library the same way it is used when it is installed using the standard pip commands and edit the code at the same time. Check out [Editable Installs](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs) pip tool documentation for more info.

# Continuous code quality
## Violations
The code violations must be checked using [PyLint](https://www.pylint.org/). In order to perform code violations in the local machine PyLint should be installed:

```
    pip install -U pylint
```

PyLint checker rules can be configured using `.pylintrc` file stored at the root of the project repo.

> Modifications to the project's `.pylintrc` file are not allowed without previous discussion and approval.

pylint can be run manually from the system console:

    pylint -f parseable --rcfile=.pylintrc pyxpiral

*Global evaluation* result must be kept above **8.0**.

Pylint violations evaluation criteria:

Target | Optimal | Inadequate | Poor | Unstable
------ | ------- | ---------- | ---- | --------
Pylint violations | 0 - 100 | 100 - 200 | 200 - 1000 | 1000 or more

> pylint can also be configured for running automatically on your IDE and this is strongly encouraged.

## Unitary testing
The unitary tests should be executed, at least, each time before make a push to ensure that no test is failing.

To run the unitary tests install:

```
    pip install pytest pytest-cov
```

And run:

```
    py.test -vv --cov=pyxpiral --cov-config .coveragerc --cov-report term --cov-report html
```

Then check the generated `htmlcov/index.html` test coverage and execution report. Coverage should be kept above 80% on relevant modules, according to the following guidelines:

Target | Optimal | Inadequate | Poor | Unstable
------ | ------- | ---------- | ---- | --------
Packages | 100% - 90.0% | 90% - 60.0% | 60% - 20.0% | 20% - 0%
Files | 100.0% - 90.0% | 90% - 60.0% | 60% - 20.0% | 20% - 0%
Methods | 100.0% - 80.0% | 80.0% - 40.0% | 40.0% - 10.0% | 10.0% - 0%
Lines | 100.0% - 80.0% | 80.0% - 40.0% | 40.0% - 10.0% | 10.0% - 0%
Conditionals | 100.0% - 80.0% | 80.0% - 40.0% | 40.0% - 10.0% | 10.0% - 0%

> The py.test command generates multiple report files that should not be tracked in git, by default they are added to .gitignore file but be careful to not add in the next commit the htmlcov, .cache, .egg-info or any other support or report file generated by the py.test.

### Unitary tests location and format
Each python module, .py files, should have a dedicated unitary test python module. The right placement for the unitary test file is a folder that should be named `tests/` in the same location of the tested module. Inside the folder the unitary test file should be named as `[module under test name]\_test.py`, i.e:

    pyxpiral/
        __init__.py
        pyxpiral.py
        tests/
            __init__.py
            pyxpiral_test.py

The *tests* folder must be a python package, therefore `__init__.py` file must be present in any test folder created.

## Continuous integration/delivery
This project uses [Travis-CI](https://travis-ci.org/elcodedocle/pyxpiral) service for implementing continuous integration and delivery pipelines.

## Inline code documentation

Documentation for this project should be written following [Google's Python Style Guide](https://google.github.io/styleguide/pyguide.html) standards, as shown on [this example](http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).

## Branching and making pull requests
This project's source code management workflow is based on [Gitflow](http://nvie.com/posts/a-successful-git-branching-model/). There are two main branches: `development` and `master`. `development` branch can be updated via pull request by external contributor + pull request approval from an internal team contributor, or via direct commit+push from an internal team contributor. The master branch is updated once per release by merging remote development or hotfix branches into it.

## Pull request approval checklist
- Travis-CI build pass (no failed unit tests and unit test coverage above minimum requirements).
- No unauthorized modifications on `MANIFEST.in`.
- No unauthorized modifications on `requirements.txt`.
- No unauthorized modifications on `.coveragerc`, `.pylintrc`, `pytest.ini`.
- Properly updated release version on `__init__.py` file.
- Properly updated `CHANGELOG.md`.
- Diff code review approved.
