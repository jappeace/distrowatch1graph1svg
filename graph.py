# This program tries to parse distrowatch and create a svg graph simliar to: <https://en.wikipedia.org/wiki/Linux_distribution#/media/File:Linux_Distribution_Timeline_with_Android.svg>
# Copyright (C) 2016 Jappe Klooster

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.If not, see <http://www.gnu.org/licenses/>.

"""
This file makes a graph from the data structure
this is mostly usefull to make sure the structure of the collected data is
sound, We expect a tree (mostly, maybe some code sharings but that's not
implemented now)
"""

import json 
import strings
from correct import fixrelations, correct

def to_graph(son):
    def dumps(item):
        return json.dumps(item, indent=4)
    def printjson(item):
        print(dumps(item))
    categories = json.loads(son)
    categories = [correct(fixrelations(i)) for i in categories]
    independents = filter(
        lambda x: x[strings.based] == strings.independend,
        categories
    )

    def listToDict(keyFunction, values):
        return dict((keyFunction(v), v) for v in values)

    # A list is just a great way to waste time for this usecase
    independents = listToDict(lambda x: x["Name"], independents)

    def addChildTo(parent, child):
        parent[strings.children].append(child)
        return parent

    # Recursivly find the parents. True on succes, False on failure
    # If succesfull the child will be added to the found parents.
    def findparents(child, bases, parents):
        if len(bases) == 0:
            for p in parents:
                addChildTo(p, child)
            return True
        current = bases[0]
        if len(parents) == 0:
            try:
                parents.insert(0,independents[current])
            except KeyError as e:
                printjson(child)
                raise e
            return findparents(child, bases[1:], parents)
        base = next(
            (x for x in parents[0][strings.children] if x[strings.name] == current),
            None
        )
        if base == None:
            if not current in independents:
                if current == child[strings.name]:
                    # ubuntu dependson ubuntu... yes distrowatch thats just bullshit
                    return findparents(child,[], parents)
                # the base is not added yet to the structure
                # lets just ignore this one for now.
                return False
            parents.insert(0,independents[current])
            return findparents(child, bases[1:], parents)
        parents[0] = base
        return findparents(child, bases[1:], parents)

    def deepen(collection):
        counter = 0
        while len(collection) > 0:
            current = collection[0]
            basedstr = current[strings.based]
            bases = basedstr.split(",")
            if not findparents(current,bases,[]):
                counter += 1
                if counter > len(collection) * 10:
                    printjson(list(collection))
                    raise Exception(
                        "Made five full circles in the deque, the data is just invalid, deque size %i " % counter
                    )
                collection.append(current)
            else:
                counter = 0
            collection.popleft()
        return collection

    from collections import deque
    notindependents = deque(filter(lambda x: not x[strings.based] == strings.independend, categories))
    deepen(notindependents)
    return dumps(list(map(lambda item: item[1], independents.items())))
