# Parses distrowatch into a graph

from this graph a nice svg image is created.

## Progress/Architecture
* the fetchdists.py screenscrapes distrowatch into a JSON structure.
	This makes retrieving data a lot more convenient as distrowatch uses
	ancient/broken html. (but thats quite obvious I guess, it still functions
	so who cares)
* start.sh glues the different python programs together. Its designed in 
this way so I just have to fetch the json once, and then can use a file,
this gives a huge speedup in debugging.
* You can specify criteria that the search.php form generates. See
fetchdists.py --help for details.
* the graph.py program eats the output of fetchdists.py. It then transforms that
output json into a tree structure, however while doing it it modifies the 
dependson variables (there were some unstructured formating which is
replaced with regexes, crude but effective). Currently this json graph could
be used for other querring purposes in principle.


## TODO
create the svg result image.
Add dates of inception and major releases of the distributions. (requires
some extra screenscraping but doable)

# How to help
Feel free to use this code according to the GNU license.
You can use the github interface for creating pull requests,
alternativly I also accept patches.

Please sponser either distrowatch or gnuclad.
