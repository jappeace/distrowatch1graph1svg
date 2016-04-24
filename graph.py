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

# using a lot of strings from te JSON strucutre,
# better group them in a structure
class strings:
    independend = "Independent"
    based = "Basedon"
    name = "Name"
    children = "Children"
import re
regex = re.compile(".*?\((.*?)\)")

# They put these comments in the brackets, mostly involing no
# longer relevant information, and it breaks the matching of parents
def removebrackets(item):
    item[strings.based] = regex.sub("", item[strings.based])
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


def deepen(collection):
    if(len(collection) == 0):
        return True
    current = collection[0]
    basedstr = current[strings.based]
    if "(" in basedstr:
        printjson(current)
    bases = basedstr.split(",")
    for base in bases:
        if base in independents:
            parent = independents[base]
            if not strings.children in parent:
                parent[strings.children] = []
            parent[strings.children].append(current)
        else:
            print("Ignoring %s for %s" % (base, current[strings.name]))
    return deepen(collection[1:])

notindependents = list(filter(lambda x: not x[strings.based] == strings.independend, categories))
deepen(notindependents)
for key,child in independents.items():
    printjson(child)
