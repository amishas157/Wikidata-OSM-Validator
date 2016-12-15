# Wikidata-OSM-Validator

### Reads an input csv containing osm feature type and Id, and corresponding wikidata Id and finds out the distance between osm feature and wikidata Id

Install shapely package:

```pip install shapely```

Install geopy package:

```pip install geopy```


Greater the distance  more is the suspicion

Input : data.csv 

**Field names:** ("Location","Type","Name","Custom Name","Chinese Name","osm_type","osm_id","Wikidata ID")

Output : output.csv

**Field names:** ("Location","Type","Name","Custom Name","Chinese Name","osm_type","osm_id","Wikidata ID","Distance")

### Usage
Place data.csv in the same folder of the script.

Run the command in termainal.

`python script.py`
