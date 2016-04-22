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

from sys import setrecursionlimit
setrecursionlimit(10000)

def tohtml(lines, outFile = "output.html"):
    with open("out/%s"%outFile, "w", encoding='utf8') as f:
        f.writelines(lines)

session = Session()
baseurl = "https://distrowatch.com/"

website = session.get(
        baseurl + 'search.php?ostype=All&category=All&origin=All&basedon=All&notbasedon=None&desktop=All&architecture=All&package=All&rolling=All&isosize=All&netinstall=All&status=All'
    ).text
soup = BeautifulSoup(website, 'html.parser')

print(soup.body.find(class_="Logo").find(class_="News").find_all("tr")[2].find("td").get_text()) # .News tr
