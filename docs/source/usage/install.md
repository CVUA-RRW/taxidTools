# Installation guide

This part presents the different possibilities to install
taxidTools.
To run properly make sure you are using Python 3.9 or above.

## Using pip

Simply run in any terminal:

```bash
$ python -m pip install taxidTools
```

## Using conda

You can install taxidTools in the current env by running:

```bash
$ conda install -c conda-forge taxidtools
```

## Docker

taxidTools is available from DockerHub:

```bash
docker pull gregdenay/taxidtools
```

## Development version

To get the latest development version, clone the git repository:

```bash
$ git clone https://github.com/CVUA-RRW/taxidTools
```

Once you have a copy of the repository, you can transfer it to 
your own Python package or install it using pip:

```bash
$ cd taxidTools
$ python -m pip install .
```

Or use the Docker image:
