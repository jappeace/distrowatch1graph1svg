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
Regression test for issue #6: a distro listed as based on devuan (a debian
fork) used to crash to_graph with KeyError: 'devuan', because findparents
assumed the first element of an origin path is an independent distro.

Run with: python3 test_devuan.py
"""

import json
import strings
from graph import to_graph


def find_child(node, name):
    """Return the child of node whose Name equals name, or None."""
    for child in node[strings.children]:
        if child[strings.name] == name:
            return child
    return None


def test_devuan_based_distro_nests_under_debian():
    """A devuan-based distro must resolve back to the independent debian root,
    ending up as debian -> devuan -> child rather than raising KeyError."""
    data = [
        {strings.name: "debian", strings.based: strings.independend,
         strings.dates: ["1993-08-01"], strings.status: strings.active,
         strings.image: ""},
        {strings.name: "devuan", strings.based: "debian",
         strings.dates: ["2016-05-01"], strings.status: strings.active,
         strings.image: ""},
        {strings.name: "daedalus", strings.based: "devuan",
         strings.dates: ["2023-08-01"], strings.status: strings.active,
         strings.image: ""},
    ]

    roots = json.loads(to_graph(json.dumps(data)))

    debian = find_child({strings.children: roots}, "debian")
    assert debian is not None, "debian should be an independent root"
    devuan = find_child(debian, "devuan")
    assert devuan is not None, "devuan should be a child of debian"
    daedalus = find_child(devuan, "daedalus")
    assert daedalus is not None, "the devuan-based distro should nest under devuan"


if __name__ == "__main__":
    test_devuan_based_distro_nests_under_debian()
    print("ok")
