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

def fetch_dist_list_from(baseurl, search_options):
    # TODO: not use this by choosing a propper html parser (
    # the html.parser tries to enclose every <br> element with </br>,
    # which is uneccisary and creates a huge stack. This is a workaround.
    from sys import setrecursionlimit
    setrecursionlimit(10000)

    # for debugging...
    def tohtml(lines, outFile = "output.html"):
        with open("out/%s"%outFile, "w", encoding='utf8') as f:
            f.writelines(lines)

    from requests import Session
    from bs4 import BeautifulSoup
    session = Session()
    website = session.get('%s/search.php?%s' % (baseurl, search_options)).text
    searchSoup = BeautifulSoup(website, 'html.parser')

    from re import match
    def tagfilter(tag):
        return tag.name == "b" and match("[0-9]+\.", tag.text)
    from logging import info
    def jsondumps(item):
        import json
        return json.dumps(item, indent=4)
    import strings

    result = "["
    # some missing root elements
    godfathers = [
        ["android", "2008-10-23"]
    ]
    for godfather in godfathers:
        result += jsondumps({
            strings.name:godfather[0],
            strings.based:strings.independend,
            strings.dates:[godfather[1]],
            strings.status:strings.active
        })+","

    foundDistributions = searchSoup.find_all(tagfilter)
    for distrobution in foundDistributions:
        print("downloading and parsing %s" % distrobution.a.text)
        aname = distrobution.a.get("href")
        hname =distrobution.a.text 
        aname = hname.split(' ')[0].lower() if aname == '' else aname
        link = "%s/%s" % (baseurl, aname)
        distrosoup = BeautifulSoup(session.get(link).text)
        structure = {
            strings.name:aname,
            "Human Name":hname ,
            "Link":link
        }
        anchor = distrosoup.find('ul')
        print(structure)
        for attribute in anchor.find_all('li'):
            # I'll be happy if this works
            print(attribute)
            name = attribute.b.extract().text[:-1]
            structure[name] = attribute.text[1:].replace("\\n","")
        comma = ","

        #find all dates and do some data sanitation if neccisarry
        def sanatizeDate(element):
            date = element.text
            if not "-" in date:
                date += "-XX-XX" # note this already exist in distrowatch input
            return date.replace("XX","01")

        structure[strings.dates] = list(map(
            sanatizeDate,
            distrosoup.find_all("td",class_="Date")
        ))
        if foundDistributions[-1] == distrobution:
            comma = ""
        result += "%s%s"% (jsondumps(structure),comma)
    return result + "]"
