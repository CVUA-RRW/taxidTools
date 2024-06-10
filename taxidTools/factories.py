import json
from typing import Iterator, Optional
from .Taxonomy import Taxonomy
from .Node import Node, DummyNode, _BaseNode, MergedNode


def read_taxdump(nodes: str, rankedlineage: str, merged: Optional[str] = None) -> Taxonomy:
    """
    Read a Taxonomy from the NCBI`s taxdump files

    Parameters
    ----------
    nodes:
        Path to the nodes.dmp file
    rankedlineage:
        Path to the rankedlineage.dmp file
    merged:
        Path tothe merged.mp file

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

    # parsing merged
    if merged:
        for line in _parse_dump(merged):
            txd[line[0]] = MergedNode(line[0],line[1])

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
        class_call = eval(record.pop('type'))
        if '_parent' in record:
            parent_dict[record['_taxid']] = record.pop('_parent')

        # Class attributes are hidden and therefore start with "_"
        # Init takes same named arguments with the "_"
        txd[record['_taxid']] = class_call(
            **{k[1:]: v for k, v in record.items()}
        )

    # Update parent info
    for k, v in parent_dict.items():
        if v:
            txd[k].parent = txd[v]

    return Taxonomy(txd)


def _parse_dump(filepath: str) -> Iterator:
    """
    Dump file line iterator, returns a yields of fields
    """
    with open(filepath, 'r') as dmp:
        for line in dmp:
            yield [item.strip() for item in line.split("|")]
