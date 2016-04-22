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

def tohtml(lines, outFile = "output.html"):
    f = open(outFile, "w", encoding='utf8')
    f.writelines(lines)
    f.close()

session = Session()
baseurl = "https://mijn.belastingdienst.nl/"

print('esteblish cookies and shit')
tohtml(
    session.get(
        baseurl + 'Webdiensten/action/welkom.do'
    ).text
    ,
    "get.html"
)
