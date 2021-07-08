"""
Misc. functions
"""


import random
import string


def linne() -> list:
    """
    Returns the linnean Taxonomy:
    
    species
    genus
    family
    order
    class
    phylum
    kingdom
    """
    return ['species',
            'genus',
            'family',
            'order',
            'class',
            'phylum',
            'kingdom']

def _rand_id(ncar = 8):
    return ''.join([random.choice(string.ascii_letters
        + string.digits) for n in range(ncar)])
    