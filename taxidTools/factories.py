import json
from copy import copy
from typing import Iterator, Optional
from .Taxonomy import Taxonomy
from .Node import Node, DummyNode, _BaseNode


def read_taxdump(nodes: str, rankedlineage: str) -> Taxonomy:
    """
    Read a Taxonomy from the NCBI`s taxdump files

    Parameters
    ----------
    nodes:
        Path to the nodes.dmp file
    rankedlineage:
        Path to the rankedlineage.dmp file

    Examples
    --------
    >>> tax = read_taxdump("nodes.dmp', 'rankedlineage.dmp')

    See Also
    --------
    read_json
    """
    txd = {}
    parent_dict = {}

    # Creating nodes
    for line in _parse_dump(nodes):
        txd[line[0]] = Node(taxid=line[0], rank=str(line[2]))
        parent_dict[str(line[0])] = line[1]  # storing parent id

    # Add names from rankedlineage
    for line in _parse_dump(rankedlineage):
        txd[line[0]].name = line[1]

    # Update parent info
    for k, v in parent_dict.items():
        txd[k].parent = txd[v]

    return Taxonomy(txd)


def read_json(path: str) -> Taxonomy:
    """
    Load a Taxonomy from a previously exported json file.

    Parameters
    ----------
    path:
        Path of file to load

    See Also
    --------
    Taxonomy.write
    load_ncbi
    """
    # parse json
    with open(path, 'r') as fi:
        parser = json.loads(fi.read())

    txd = {}
    parent_dict = {}

    # Create nodes from records
    for record in parser:
        class_call = eval(record['type'])
        txd[record['_taxid']] = class_call(taxid=record['_taxid'],
                                            name=record['_name'],
                                            rank=record['_rank'])
        parent_dict[record['_taxid']] = record['_parent']

    # Update parent info
    for k, v in parent_dict.items():
        try:
            txd[k].parent = txd[v]
        except KeyError:
            pass

    return Taxonomy(txd)


def _parse_dump(filepath: str) -> Iterator:
    """
    Dump file line iterator, returns a yields of fields
    """
    with open(filepath, 'r') as dmp:
        for line in dmp:
            yield [item.strip() for item in line.split("|")]
