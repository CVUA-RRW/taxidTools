"""
Misc. utility functions
"""


import warnings
import random
import string


def linne() -> list:
    """
    Returns the linnean Taxonomy:

    species,
    genus,
    family,
    order,
    class,
    phylum,
    kingdom
    """
    return ['species',
            'genus',
            'family',
            'order',
            'class',
            'phylum',
            'kingdom']


def _rand_id(ncar: int = 8) -> str:
    """Random hash"""
    return ''.join([random.choice(
                    string.ascii_letters + string.digits)
                    for n in range(ncar)])


def deprecation(depr, replace):
    warnings.warn(
        f"'{depr}' is pending deprecation, use the '{replace}' instead",
        DeprecationWarning, stacklevel=2
    )
