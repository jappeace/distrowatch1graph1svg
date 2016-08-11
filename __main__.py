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

from fetchdists import fetch_dist_list_from
from graph import to_graph
from svg import toCSV
from subprocess import call

import os
import argparse
import json

parser = argparse.ArgumentParser(
    description=
        "Distrograph Copyright (C) 2016 Jappie Klooster\n" +
        "This program comes with ABSOLUTELY NO WARRANTY; for details see the \n" +
        "LICENSE file. This is free software, and you are welcome to \n" +
        "redistribute it under certain conditions; see the LICENSE file for details\n"+
        "--\n"
    )
parser.add_argument(
    '--baseurl',
    default="https://distrowatch.com",
    help="default http://distrowatch.com"
)
parser.add_argument(
    '--searchOptions',
    default="ostype=All&category=All&origin=All&basedon=All&notbasedon=None"+
    "&desktop=All&architecture=All&package=All&rolling=All&isosize=All"+
    "&netinstall=All&status=All",
    help="the GET form generates this at distrowatch.com/search.php,"+
    "everything behind the ? can be put in here, "+
    "use this to add constraints to your graph, for example if you're "+
    "only interested in active distro's, specify it at the form and copy "+
    "the resulting GET request in this argument"
)

args = parser.parse_args()
os.chdir(os.path.dirname(os.path.realpath(__file__)))
outputdir = "out"
if not os.path.isdir(outputdir):
    os.mkdir(outputdir)
os.chdir(outputdir)

fetched_dists_file = "dists.json"
son = ""
if os.path.isfile(fetched_dists_file):
    with open(fetched_dists_file, "r") as cached:
        print("using cached file %s/%s" % (outputdir, fetched_dists_file))
        son = "".join(cached.readlines())
if son == "":
    url = args.baseurl
    print("fetching distros from %s" % url)
    son = fetch_dist_list_from(url, args.searchOptions)
    with open(fetched_dists_file, "w") as cached:
        print("wrote cache file %s/%s" % (outputdir, fetched_dists_file))
        cached.write(son)

son = to_graph(son)

csv = toCSV(json.loads(son), "").result
csvfile = "dists.csv"
print("writing csv to %s/%s" % (outputdir, csvfile))
with open(csvfile, "w") as cached:
    cached.write(csv)
os.chdir("../")
call("gnuclad %s/%s %s" % (outputdir, csvfile, "SVG"), shell=True)
call("inkscape -z -e dists.png dists.svg", shell=True)
