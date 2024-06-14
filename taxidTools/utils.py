"""
Misc. utility functions
"""


import warnings
import random
import string


def linne() -> list:
    """
    Linnean Taxonomy:

    Returns
    -------
    list
        ['species',
        'genus',
        'family',
        'order',
        'class',
        'phylum',
        'kingdom']
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


def _deprecation(depr, replace):
    """Standard deprecation warning"""
    warnings.warn(
        f"'{depr}' is pending deprecation, use the '{replace}' instead",
        DeprecationWarning, stacklevel=2
    )
