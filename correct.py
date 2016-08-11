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
This file applies changes to the existing data, to correct mistakes or 
inconsistencies
"""

import strings
import re

datafixes = [
    (re.compile("\((.*?)\)"), ""), # remove brackets with details

    #spelling
    (re.compile("^$"), strings.independend),
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
    (re.compile("^mandriva"), "fedora,redhat,mandriva"),
]
# They put these comments in the brackets, mostly involing no
# longer relevant information, and it breaks the matching of parents
def fixrelations(item):
    """fixes the basic relationships to work with help of a bunch of regexes,
    ie parents should be explicit, children should be none"""
    new = item[strings.based].lower().replace(" ", "")
    # for god sakes get your dependencies straight
    for fix in datafixes:
        new = fix[0].sub(fix[1], new)
    item[strings.based] = new
    item[strings.children] = []
    return item

corrections = {
    "funtoo": {
        strings.dates : ["2008-02-01"] # hard to tell exact date, it wasn't January
    },
    "freebsd": {
        strings.dates : ["1993-11-01"] 
    },
    "mandriva":{
        strings.based: "fedora,redhat"
    },
    "mageia":{
        strings.based : "fedora,redhat,mandriva"
    }
}

def correct(item):
    name = item[strings.name]
    if name in corrections:
        for key in corrections[name].keys():
            item[key] = corrections[name][key]
    return item
