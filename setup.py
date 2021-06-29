import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="taxidTools",
    version="2.0.0",
    author="Gregoire Denay",
    author_email="gregoire.denay@cvua-rrw.de",
    description="A Python Toolkit for Taxonomy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CVUA-RRW/taxidTools",
    project_urls={
        "Bug Tracker": "https://github.com/CVUA-RRW/taxidTools/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)