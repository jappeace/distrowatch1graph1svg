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


## TODO
recognize distributions by name if based on occurs.
create the svg result image.
