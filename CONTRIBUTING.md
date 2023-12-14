# Contributing

## Issues

You can find our open issues in the project's
[issue tracker](https://github.com/vizzu-streamlit/vizzu-builder/issues). Please
let us know if you find any issues or have any feature requests there.

## Contributing

If you want to contribute to the project, your help is very welcome. Just fork
the project, make your changes and send us a pull request. You can find the
detailed description of how to do this in
[Github's guide to contributing to projects](https://docs.github.com/en/get-started/quickstart/contributing-to-projects).

Our [Roadmap page](https://github.com/vizzuhq/.github/wiki/Roadmap) is a
comprehensive list of tasks we want to do in the future. It is a good place to
start if you want to contribute to `Vizzu`. In case you have something else in
mind, that's awesome and we are very interested in hearing about it.

## CI-CD

### Development environment

For contributing to the project, it is recommended to use `Python` `3.10` as the
primary programming language for most parts of the source code.

The following steps demonstrate how to set up the development environment on an
`Ubuntu` `22.04` operating system. However, the process can be adapted for other
operating systems as well.

To start using the `vizzu-builder` development environment, you need to create a
virtual environment and install `pdm` within it.

```sh
python3.10 -m venv ".venv"
source .venv/bin/activate
pip install pdm==2.11.0
```

Once set up, you can install development dependencies:

```sh
pdm install
```

The development requirements are installed based on the `pdm.lock` file. To
update the development requirements, you can use the command `pdm run lock`.

**Note:** For all available `pdm` scripts, run `pdm run --list`.

### CI

The CI pipeline includes code formatting checks, code analysis and typing
validation for the `vizzu-builder` project.

To run the entire CI pipeline, execute the following `pdm` script:

```sh
pdm run ci
```

#### Formatting

You can check the code's formatting using the `format` script:

```sh
pdm run format
```

If you need to fix any formatting issues, you can use the `fix-format` script:

```sh
pdm run fix-format
```

#### Code analyses

To perform code analyses, you can use the `lint` script:

```sh
pdm run lint
```

#### Typing

For type checking, you can use the `type` script:

```sh
pdm run type
```
