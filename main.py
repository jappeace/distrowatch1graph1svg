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


from requests import Session
from bs4 import BeautifulSoup

import re
from sys import setrecursionlimit

import argparse
parser = argparse.ArgumentParser(
    description=
        "Distrograph Copyright (C) 2016 Jappie Klooster\n" +
        "This program comes with ABSOLUTELY NO WARRANTY; for details see the \n" +
        "LICENSE file. This is free software, and you are welcome to \n" +
        "redistribute it under certain conditions; see the LICENSE file for details"
    )
parser.add_argument('--baseurl', default="https://distrowatch.com/", help="default http://distrowatch.com")
parser.add_argument('--searchOptions', 
        default="ostype=All&category=All&origin=All&basedon=All&notbasedon=None&desktop=All&architecture=All&package=All&rolling=All&isosize=All&netinstall=All&status=All", 
        help="the GET form generates this at distrowatch.com/search.php,"+
        "everything behind the ? can be put in here, "+
        "use this to add constraints to your graph, for example if you're "+
        "only interested in active distro's, specify it at the form and copy "+
        "the resulting GET request in this argument")

args = parser.parse_args()

setrecursionlimit(10000)

def tohtml(lines, outFile = "output.html"):
    with open("out/%s"%outFile, "w", encoding='utf8') as f:
        f.writelines(lines)

session = Session()
baseurl = args.baseurl

website = session.get(
        baseurl + 'search.php?%s' % args.searchOptions
    ).text
soup = BeautifulSoup(website, 'html.parser')

def tagfilter(tag):
    return tag.name == "b" and re.match("[0-9]+\.", tag.text)
print('---')
for element in soup.find_all(tagfilter):
    print(element)
print() # .News tr
