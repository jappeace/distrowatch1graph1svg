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
    'graphInput',
    nargs='+',
    help="The structured json from graph.py"
)

args = parser.parse_args()

import json 
def printjson(item):
    print(json.dumps(item, indent=4))

def csv(name,color,parent,start,stop,icon,description):
    return "\"N\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"" % (name,color,parent,start,stop,icon,description)
def toCSV(distributions, parent):
    def sortDates(datearray):
        return list(
            sorted(
                map(
                    lambda x: datetime.strptime(x,"%Y-%m-%d"),
                    datearray
                )
            )
        )
    for distro in distributions:
        import strings
        from datetime import datetime
        dates = sortDates(distro[strings.dates])
        enddate = ""
        dateformat = "%Y.%m.%d"
        if not distro[strings.status] == strings.active:
            enddate = dates[-1].strftime(dateformat)

        startdate = dates[0]
        parentName = ""
        if not parent == None:
            parentName = parent[strings.name]
            parentstartdate = sortDates(parent[strings.dates])[0]
            if startdate < parentstartdate:
                startdate = parentstartdate
        print(csv(distro[strings.name], "#f00", parentName, startdate.strftime(dateformat),enddate,"",""))
        toCSV(distro[strings.children],distro)

toCSV(json.loads(''.join(args.graphInput)), None)

