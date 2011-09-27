"""
Conversion functions.
"""

# taken form the UFO spec

def convertUFO1OrUFO2KerningToUFO3Kerning(kerning, groups,
	firstKerningGroupPrefix="@KERN_1_",
	secondKerningGroupPrefix="@KERN_2_"):
	# The prefixes must be unique.
	assert firstKerningGroupPrefix != secondKerningGroupPrefix
	# Make lists of groups referenced in kerning pairs.
	firstReferencedGroups = set()
	secondReferencedGroups = set()
	for first, seconds in kerning.items():
		if first in groups:
			if not first.startswith(firstKerningGroupPrefix):
				firstReferencedGroups.add(first)
		for second in seconds.keys():
			if second in groups:
				if not second.startswith(secondKerningGroupPrefix):
					secondReferencedGroups.add(second)
	# Create new names for these groups.
	firstRenamedGroups = {}
	for first in firstReferencedGroups:
		# Make a list of existing group names.
		existingGroupNames = groups.keys() + firstRenamedGroups.keys()
		# Add the prefix to the name.
		newName = firstKerningGroupPrefix + first
		# Make a unique group name.
		newName = makeUniqueGroupName(newName, existingGroupNames)
		# Store for use later.
		firstRenamedGroups[first] = newName
	secondRenamedGroups = {}
	for second in secondReferencedGroups:
		# Make a list of existing group names.
		existingGroupNames = groups.keys() + secondRenamedGroups.keys()
		# Add the prefix to the name.
		newName = secondKerningGroupPrefix + second
		# Make a unique group name.
		newName = makeUniqueGroupName(newName, existingGroupNames)
		# Store for use later.
		secondRenamedGroups[second] = newName
	# Populate the new group names into the kerning dictionary as needed.
	newKerning = {}
	for first, seconds in kerning.items():
		first = firstRenamedGroups.get(first, first)
		newSeconds = {}
		for second, value in seconds.items():
			second = secondRenamedGroups.get(second, second)
			newSeconds[second] = value
		newKerning[first] = newSeconds
	# Make copies of the referenced groups and store them
	# under the new names in the overall groups dictionary.
	allRenamedGroups = firstRenamedGroups.items()
	allRenamedGroups += secondRenamedGroups.items()
	for oldName, newName in allRenamedGroups:
		group = list(groups[oldName])
		groups[newName] = group
	# Return the kerning and the groups.
	return newKerning, groups

def makeUniqueGroupName(name, groupNames, counter=0):
	# Add a number to the name if the counter is higher than zero.
	newName = name
	if counter > 0:
		newName = "%s%d" % (newName, counter)
	# If the new name is in the existing group names, recurse.
	if newName in groupNames:
		return makeUniqueGroupName(name, groupNames, counter + 1)
	# Otherwise send back the new name.
	return newName

def test():
	"""
	>>> testKerning = {
	...   "A" : {
	...     "A" : 1,
	...     "B" : 2,
	...     "CGroup" : 3,
	...     "DGroup" : 4
	...   },
	...   "BGroup" : {
	...     "A" : 5,
	...     "B" : 6,
	...     "CGroup" : 7,
	...     "DGroup" : 8
	...   },
	...   "CGroup" : {
	...     "A" : 9,
	...     "B" : 10,
	...     "CGroup" : 11,
	...     "DGroup" : 12
	...   },
	... }
	>>> testGroups = {
	...   "BGroup" : ["B"],
	...   "CGroup" : ["C"],
	...   "DGroup" : ["D"],
	... }
	>>> kerning, groups = convertUFO1OrUFO2KerningToUFO3Kerning(
	...   testKerning, testGroups)
	>>> expected = {
	...   "A" : {
	...     "A": 1,
	...     "B": 2,
	...     "@KERN_2_CGroup": 3,
	...     "@KERN_2_DGroup": 4
	...   },
	...   "@KERN_1_BGroup": {
	...     "A": 5,
	...     "B": 6,
	...     "@KERN_2_CGroup": 7,
	...     "@KERN_2_DGroup": 8
	...   },
	...   "@KERN_1_CGroup": {
	...     "A": 9,
	...     "B": 10,
	...     "@KERN_2_CGroup": 11,
	...     "@KERN_2_DGroup": 12
	...   }
	... }
	>>> kerning == expected
	True
	>>> expected = {
	...   "BGroup": ["B"],
	...   "CGroup": ["C"],
	...   "DGroup": ["D"],
	...   "@KERN_1_BGroup": ["B"],
	...   "@KERN_1_CGroup": ["C"],
	...   "@KERN_2_CGroup": ["C"],
	...   "@KERN_2_DGroup": ["D"],
	... }
	>>> groups == expected
	True
	"""

if __name__ == "__main__":
	import doctest
	doctest.testmod()