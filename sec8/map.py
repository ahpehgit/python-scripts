import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")
lon = list(data["LON"])
lat = list(data["LAT"])
name = list(data["NAME"])
elev = list(data["ELEV"])

def elevationColor(elev):
	if elev < 1000:
		return "green"
	elif 1000 <= elev < 3000:
		return "orange"
	else:
		return "red"

map = folium.Map(location=[38.58,-99.09], zoom_start=6, tiles="Mapbox Bright")
fgv = folium.FeatureGroup(name="Volcanoes")
fgp = folium.FeatureGroup(name="Populations")

for lt, ln, nm, el in zip(lat, lon, name, elev):
	elevation = str(el) + " m"
	#fg.add_child(folium.Marker(location=[lt, ln], popup=nm + ", " + elevation, icon=folium.Icon(color=elevationColor(el))))
	fgv.add_child(folium.CircleMarker(location=[lt, ln], popup=nm + ", " + elevation, radius=7, fill_color=elevationColor(el), fill_opacity=0.7))

worldData = open("world.json", "r", encoding="utf-8-sig").read()
fgp.add_child(
	folium.GeoJson(data=worldData, 
		style_function=lambda x: { 
		"fillColor":"green" if x["properties"]["POP2005"] < 10000000 
		else "orange" if 10000000 <= x["properties"]["POP2005"] < 20000000 
		else "red" }
	)
)

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save("Map1.html")