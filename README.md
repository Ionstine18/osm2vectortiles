# osm2vectortiles

This package converts the osm data in geojson format into different layers (defined into different layers) of data in geojson format. By using tippecanoe, the layers are converted into vector tiles (in .mbtiles format). A map server is set up for map service (for larger map, this is faster than directly using geojson data on convas).

Please follow the steps below

1. run test.py to get layers in geojson in data_layers folder

3. run tippecanoe -z18 -Z11 -o map_full.mbtiles --no-line-simplification --no-tiny-polygon-reduction ./*.geojson

tippecanoe can be installed on mac by 
brew install tippecanoe

3. run node server.js to start the map server (please check https://gis.stackexchange.com/questions/125037/self-hosting-mapbox-vector-tiles)
3.1 Install Node.js
3.2 Grab the node packages with npm install tilelive mbtiles express
3.3 node server.js

4. open index.html
