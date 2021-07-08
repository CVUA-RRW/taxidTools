import os
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))


about = {}
with open(os.path.join(here, 'taxidTools', '__version__.py'), 'r') as f:
    exec(f.read(), about)

with open(os.path.join(here, "README.md"), "r") as fh:
    long_description = fh.read()

packages = ['taxidTools']

setup(
    name=about['__title__'],
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    description=about['__description__'],
    long_desription=long_description,
    long_description_content_type="text/markdown",
    url=about['__url__'],
    license=about['__licence__'],
    project_urls={
        "Bug Tracker": "https://github.com/CVUA-RRW/taxidTools/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    package_dir={"taxidTools": "taxidTools"},
    packages=packages,
    python_requires=">=3.9",
    include_package_data=True,
)
