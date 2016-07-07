import collections
import json

tree = lambda: collections.defaultdict(tree)
print type(tree)
some_dict = tree()
print type(some_dict)
some_dict['colours']['favourite'] = "yellow"


print some_dict
print some_dict['colours']
print some_dict['colours']['favourite']

print (json.dumps(some_dict))
print type(json.dumps(some_dict))


