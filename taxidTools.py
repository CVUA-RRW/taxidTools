#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Provides the Taxdump class to work with the NCBI Taxonomy informations from the taxdump files.
Supports conversion of taxid numbers to rank or names, finding parents, retrieving ancestry and finding lowest common 
ancestor from a list of taxids.
"""


__author__ = "Gregoire Denay"


from collections import UserDict


class _ReadOnlyDict(UserDict):
	"""
	Readonly subclass of UserDict. 
	Can still be updated by using _ReadOnlyDict.data[key] = val (Should only be used for object initialization)
	"""
	def __init__(self, mapping=None):
		"""
		A subclass of Userdict without self-modification capabilities.
		
		Arguments:
		----------
		mapping: dict
			Dict to populate the object 
		"""
		super().__init__()
		if mapping:
			for key, val in dict(mapping).items():
				self.data[key] = val
		
	def __readonly__(self, *args, **kwargs):
		"raise NotImplementedError"
		raise NotImplementedError("This object is read-only")
	
	__setitem__ = __readonly__
	__delitem__ = __readonly__
	pop = __readonly__
	popitem = __readonly__
	clear = __readonly__
	update = __readonly__
	setdefault = __readonly__
	del __readonly__
	

class Taxdump(object):
	"""
	Reads in taxdump files and provides methods to work on lineages.
	"""
	
	def __init__(self, rankedlineage_dmp, nodes_dmp):
		"""
		Create a Taxdump object.
		
		Arguments
		---------
		rankedlineage_dmp: str
			Path to rankedlineage.dmp
		nodes_dmp: str
			Path to nodes.dmp
		"""
		# useful data will be stored in a dict as {taxid: (name, rank, parent_taxid)} 
		# the aim here is to keep data storage at a minimum to use as little memory as nescessary without the hurdle of indexing the files
		self._data = _ReadOnlyDict()
		
		# Parsing name file
		tmp_name = {} # temporary storage for taxid-name pairs
		for line in _parse_dump(rankedlineage_dmp):
			# retriving unique name for each taxid
			taxid = line[0]
			name = line[1]
			tmp_name[taxid] = name

		# Parsing node file and creating the _data dict on the fly
		for line in _parse_dump(nodes_dmp):
			taxid = line[0]
			name = tmp_name.pop(taxid)
			rank = line[2]
			parent = line[1]
			self._data.data[taxid] = (name, rank, parent)
			
	def _check_input(func):
		def wrapper(self, *args, **kwargs):
			if isinstance(args[0], list):
				return [func(self, e, *args[1:], **kwargs) for e in args[0]]
			else:
				return func(self, *args, **kwargs)
		return wrapper
	
	@_check_input
	def getName(self, taxid):
		"""
		Get taxid name
		
		Arguments
		---------
		taxid: str
			Taxonomic identification number
			
		Returns
		-------
		str:
			node name
		"""
		return self._data[taxid][0]
		
	@_check_input
	def getRank(self, taxid):
		"""
		Get taxid rank
		
		Arguments
		---------
		taxid: str
			Taxonomic identification number
			
		Returns
		-------
		str:
			node rank
		"""
		return self._data[taxid][1]
	
	@_check_input
	def getParent(self, taxid):
		"""
		Retrieve parent taxid 
		
		Arguments:
		----------
		taxid: str
			Taxonomic identification number
		
		Returns
		-------
		str:
			Parent taxid
		"""
		return self._data[taxid][2]
	
	@_check_input
	def getTaxid(self, name):
		"""
		Retrieve a list of taxid associated to a given Organism name
		
		Arguments:
		----------
		name: str
			Organism name according to the Taxdump definition files (Case-sensitive)
			
		Returns
		-------
		list:
			list of associated Taxids
		"""
		try:
			return self._flipped[name]
			
		except AttributeError:
			self._flip_dict()
			return self._flipped[name]
			
	@_check_input
	def getAncestry(self, taxid):
		"""
		Retrieve the ancestry of the given taxid
		
		Arguments:
		----------
		taxid: str
			Taxonomic identification number
		
		Returns:
		--------
		list:
			list of ancestors (from the lowest to the highest node)
		"""
		lineage=[taxid]
		parent = self.getParent(taxid)
		
		while parent != '1':
			lineage.append(parent)
			parent = self.getParent(parent)
		
		lineage.append('1')
		
		return lineage
	
	@_check_input
	def isAncestorOf(self, taxid, child):
		"""
		Test if taxid is an ancestor of child
		
		Arguments:
		----------
		taxid: str
			Taxonomic identification number
			
		child: str
			Taxonomic identification number
		
		Returns:
		--------
		bool
		"""
		return taxid in self.getAncestry(child)[1:]
	
	@_check_input
	def isDescendantOf(self, taxid, parent):
		"""
		Test if taxid is an descendant of parent
		
		Arguments:
		----------
		taxid: str
			Taxonomic identification number
			
		parent: str
			Taxonomic identification number
		
		Returns:
		--------
		bool
		"""
		return parent in self.getAncestry(taxid)[1:]
		
	def lowestCommonNode(self, taxid_list):
		"""
		Get lowest common node of a bunch of taxids
		
		Arguments
		---------
		taxid_list: list
			list of taxonomic identification numbers (as str)
			
		Returns
		-------
		str: 
			Lowest common taxid
		"""
		# Generate a top-down (highest node first) list of all ancestries
		ancestries = [self.getAncestry(taxid)[::-1] for taxid in taxid_list]
		
		# iterate over ancestries to find the first mismatch
		i = 0
		size = 0
		while size <= 1:
			size = len(set(l[i] for l in ancestries))
			i += 1
			
		# return taxid from previous node
		i -= 2 # i is incremented in the last while loop
		lca = set(l[i] for l in ancestries)
		return lca.pop()
		
	def filterRanks(self, taxid_list, ranks_list):
		"""
		Filters a list of taxids to specific ranks
		
		Arguments
		----------
		taxid_list: list
			list of taxonomic identification numbers (as str)
		ranks_list: list
			List of ranks to return
		
		Returns
		-------
		list:
			list of taxids
		"""
		return [e for e in taxid_list if self.getRank(e) in ranks_list]
		
	def _flip_dict(self):
		"Creates a flipped dictionnary in the form {'name': 'taxid'}"
		flipped = {}
		for key, value in self._data.items():
			# The flipped dictionnary will not contain rank and parent informations!
			flipped[value[0]] = key
		# Make the flipped dictionnary Read-only
		self._flipped = _ReadOnlyDict(flipped)

	def __len__(self):
		return len(self._data)
		
	def __getitem__(self, index):
		return self._data[index]
		
	def __iter__(self):
		yield from self._data.keys()
	
	def keys(self):
		return self._data.keys()
		
	def values(self):
		return self._data.values()
		
	def items(self):
		return self._data.items()
	
	
def _parse_dump(filepath):
	"""
	Dump file line iterator, returns a yields of fields
	"""
	with open(filepath, 'r') as dmp:
		for line in dmp:
			yield [item.strip() for item in line.split("|")]