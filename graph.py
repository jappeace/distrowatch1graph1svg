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



import argparse
parser = argparse.ArgumentParser(
    description=
        "Distrograph Copyright (C) 2016 Jappie Klooster\n" +
        "This program comes with ABSOLUTELY NO WARRANTY; for details see the \n" +
        "LICENSE file. This is free software, and you are welcome to \n" +
        "redistribute it under certain conditions; see the LICENSE file for details\n"+
        "--\n"
    )
parser.add_argument(
    'jsonInput',
    nargs='+',
    help="The structured json from fetchdists.py"
)

args = parser.parse_args()

import json 
def printjson(item):
    print(json.dumps(item, indent=4))

son = ''.join(args.jsonInput)
categories = json.loads(son)

import strings
import re
datafixes = [
    (re.compile("\((.*?)\)"), ""), # remove brackets with details

    #spelling
    (re.compile("^indpendent$"), strings.independend),
    (re.compile("^indpenendent$"), strings.independend),

    # fixes origin paths
    # way more easy than a proper detection.
    (re.compile("^redhat"), "fedora,redhat"),
    (re.compile("^centos$"), "fedora,redhat,centos"),
    (re.compile("^fedora,centos$"), "fedora,redhat,centos"),
    (re.compile("^trustix$"), "fedora,trustix"),
    (re.compile("^asianux,fedora$"), "fedora,redhat,asianux"),
    (re.compile("^fedora,redhat,trustix$"), "fedora,redhat,fedora,trustix"),

    (re.compile("^thinstation$"), "crux,thinstation"),
    (re.compile("^manjaro$"), "arch,manjaro"),
    (re.compile("^peanut$"), "alinux"),
    (re.compile("^caldera$"), "sco"),
    (re.compile("^vectorlinux$"), "slackware,vector"),

    (re.compile("^opensolaris,solaris$"), "solaris,opensolaris"),
    (re.compile("^opensolaris$"), "solaris,opensolaris"),

    (re.compile("^ubuntu$"), "debian,ubuntu"),
    (re.compile("^damnsmall$"), "debian,knoppix,damnsmall"),
    (re.compile("^debian,damnsmall$"), "debian,knoppix,damnsmall"),
    (re.compile("^debian,freeduc$"), "debian,knoppix,freeduc"),
    (re.compile("^debian,feather$"), "debian,knoppix,damnsmall,feather"),
    (re.compile("^debian,sidux$"), "debian,aptosid"), #rename
    #misses ubuntu
    (re.compile("^debian,kurumin$"), "debian,ubuntu,kurumin"),
    (re.compile("debian,kubuntu"), "debian,ubuntu,kubuntu"),
    (re.compile("^debian,xubuntu$"), "debian,ubuntu,xubuntu"),
    (re.compile("^debian,mint$"), "debian,ubuntu,mint"),
    (re.compile("^debian,lubuntu$"), "debian,ubuntu,lubuntu"),
    (re.compile("^debian,linspire$"), "debian,ubuntu,linspire"),
    # debian clusterfuck
    (re.compile("^debian,ubuntu,knoppix$"), "debian,ubuntu,debian,knoppix"),

    # distrowatch didn't want to put up with the numbers
    (re.compile("m0n0wall"), "monowall"),
]

# They put these comments in the brackets, mostly involing no
# longer relevant information, and it breaks the matching of parents
def removebrackets(item):
    new = item[strings.based].lower()
    # for god sakes get your dependencies straight
    for fix in datafixes:
        new = fix[0].sub(fix[1], new)
    item[strings.based] = new
    item[strings.children] = []
    return item
categories = list(map(removebrackets, categories))
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
printjson(list(map(lambda item: item[1], independents.items())))
