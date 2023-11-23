import plotly.express as px
import json
import pandas as pd

# Charger le GeoJSON des régions de France
with open('./data/regions.geojson') as map:
    region = json.load(map)

# Supprimer les données hors métropole
out = ["01", "02", "03", "04", "06", "94"]
region['features'] = [f for f in region['features'] if f['properties']['code'] not in out]

# Créer un dataframe avec les données de la carte
features = region['features']
data = {'code': [], 'nom': [], 'geometry': []}

for feature in features:
    data['code'].append(feature['properties']['code'])
    data['nom'].append(feature['properties']['nom'])
    data['geometry'].append(feature['geometry'])

df = pd.DataFrame(data)

# Utiliser Plotly Express pour créer une carte choropleth
fig = px.choropleth(df, 
                    geojson=region,  # Utiliser le GeoJSON
                    featureidkey="properties.nom",  # Clé identifiant la région dans le GeoJSON
                    locations="nom",  # Colonne dans le DataFrame correspondant aux régions
                    color="code",  # Colonne dans le DataFrame correspondant aux valeurs pour la coloration
                    color_continuous_scale="Viridis",  # Échelle de couleurs
                    title="Carte des régions de France")

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Afficher la carte
fig.show()
