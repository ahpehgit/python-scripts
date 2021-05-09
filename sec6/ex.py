import pandas
from geopy.geocoders import ArcGIS

nom = ArcGIS()
n = nom.geocode("Blk 219 Petir Road, Singapore 670219")
print(n)
print(type(n))

df = pandas.read_csv("supermarkets.csv")
print(df)

# add a new column "Coordinates"
df["Address"] = df["Address"] + "," + df["City"] + "," + df["State"] + "," + df["Country"]
print(df)

df["Coordinates"] = df["Address"].apply(nom.geocode)
print(df["Coordinates"])

print("Row 1 longitude: %s" % (df["Coordinates"][1].longitude))
print("Row 1 latitude: %s" % (df["Coordinates"][1].latitude))

#add 2 new columns
df["Longitude"] = df["Coordinates"].apply(lambda x: x.longitude if x != None else "None")
df["Latitude"] = df["Coordinates"].apply(lambda x: x.latitude if x != None else "None")

print(df)