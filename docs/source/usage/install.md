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

If using conda from the command line, simply activate 
your environment and install taxidTools using pip:

```bash
$ conda create -n myenv 'python>=3.9' 
$ conda activate myenv
$ python -m pip install taxidTools
```

You can also create an environemnt definition file to 
use with workflow manager or to distribute your environment:

```yaml
name: myenv
dependencies:
  - python>=3.9
  - pip
  - pip:
    - taxidTools
```

Save the above file as myenv.yml and create your environment 
the usual way:

```bash
$ conda env create -f myenv.yml
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