import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="taxidTools", # Replace with your own username
    version="2.1.0",
    author="Gregoire Denay",
    author_email="gregoire.denay@cvua-rrw.de",
    description="Taxonomy ranks toolbox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CVUA-RRW/taxidTools",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=["collections"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ]
)