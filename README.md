# Parses distrowatch into a graph

from this graph a nice svg image is created.

![The example timeline](https://upload.wikimedia.org/wikipedia/commons/7/7c/FOSS_landscape_2016.png "Example result")

Note that you can use the search form from Distrowatch to create a more constraint
variant (for example if you're only interested in Linux or the Debian family,
that search form is very extensive).

## Progress/Architecture
* the fetchdists.py screenscrapes distrowatch into a JSON structure.
	This makes retrieving data a lot more convenient as distrowatch uses
	ancient/broken html. (but thats quite obvious I guess, it still functions
	so who cares)
* start.sh glues the different python programs together. Its designed in 
this way so I just have to fetch the JSON once, and then can use a file,
this gives a huge speedup in debugging.
* You can specify criteria that the search.php form generates. See
fetchdists.py --help for details.
* the graph.py program eats the output of fetchdists.py. It then transforms that
output json into a tree structure, however while doing it it modifies the 
dependson variables (there were some unstructured formating which is
replaced with regexes, crude but effective). Currently this json graph could
be used for other querring purposes in principle.
* The svg.py program creates a csv output from the graph.py programs output.
* gnu clad should eat the csv output to create the final svg.

I'm thinking about recreating the entire svg rendering in python and circumventing
gnu clad, because gnuclad is written in C (or C++, I didn't check).
(also the gnu clad project seems dead-ish and I want to add some features, such
as small figures for each release. This is difficult to feed to gnu clad in
csv format so I think its easier to just look at their source and reimplement
it in python. We share the same license so it shouldn't be a problem), although
looking at all the config options now I know that I won't be doing that any
time soon.

# Todo
* Add the images from the original.
* Maybe add automatically the logos in the circles, I think this should be
possible with some extra screenscraping (distrowatch already collects the logos)
* Add domain support (backgrounds for example for debian)
* Add some sort of combine mechanism to supplement data from distrowatch (for example
for android, since distrowatch ignores that for some reason)
* Preferably I would let svg.py do all the rendering, but that's a pipe dream for now.
* Code sharing support? (the original had this but I didn't think it was that
usefull honestly)

# How to help
Feel free to use this code according to the GNU license.
You can use the github interface for creating pull requests,
alternatively I also accept patches.

Please sponser either distrowatch or gnuclad.
