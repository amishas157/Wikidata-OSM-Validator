import requests

import csv
import json
import shapely.geometry
from geopy.distance import vincenty
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

csvfile = open('data.csv', 'r')
jsonfile = open('data.json','w')

fieldnames = ("osm_id","osm_type","Type","name_en","name_zh_mbx","City","lon","lat","name","wikipedia","wikidata","name_zh")
reader = csv.DictReader( csvfile, fieldnames)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')

jsonfile.close()
csvfile.close()

jsonfile = open('data.json', 'r')
outputjson = open('output.json','w')

for line in jsonfile:
        line = json.loads(line)
        try:
            r = requests.get('https://jzvqzn73ca.execute-api.us-east-1.amazonaws.com/api/feature/'+line['osm_type']+'/'+line['osm_id'])
            respons = r.json()

            s = requests.get('https://www.wikidata.org/w/api.php?action=wbgetentities&ids=' + line['wikidata'] + '&format=json')
            response = s.json()
            latitude = response["entities"][line['wikidata']]["claims"]["P625"][0]["mainsnak"]["datavalue"]["value"]["latitude"]
            longitude = response["entities"][line['wikidata']]["claims"]["P625"][0]["mainsnak"]["datavalue"]["value"]["longitude"]

            geom_geojson = shapely.geometry.shape({"type": "Point", "coordinates": [longitude, latitude]})
            geom_db = shapely.geometry.shape(respons['geometry'])


            centroid_geojson = geom_geojson.centroid
            centroid_db = geom_db.centroid

            distance = vincenty((centroid_geojson.x,centroid_geojson.y),(centroid_db.x, centroid_db.y)).km
            line['Distance'] = distance
            outputjson.write(json.dumps(line) + '\n')
        except:
            line['Distance'] = "Error"
            outputjson.write(json.dumps(line) + '\n')
	print line

outputjson.close()
jsonfile.close()

fw = open('output.csv', 'w')
fr = open('output.json', 'r')
csvwriter = csv.writer(fw)
csvwriter.writerow(["osm_id","osm_type","Type","name_en","name_zh_mbx","City","lon","lat","name","wikipedia","wikidata","name_zh","Distance"])

for line in fr:
    line = json.loads(line)
    csvwriter.writerow([line["osm_id"],line["osm_type"],line["Type"],line["name_en"],line["name_zh_mbx"],line["City"],line["lon"],line["lat"],line["name"],line["wikipedia"],line["wikidata"],line["name_zh"],line["Distance"]])

fw.close()
fr.close()
