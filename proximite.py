#Chargement des donnÃ©es ----

## arrondissements
uri = "/Téléchargements/lyon/arrondissements.shp"
arrondissements = iface.addVectorLayer(uri,"arrondissements", "ogr")

## gares
uri = "/Téléchargements/lyon/gares_sncf.shp"
gares = iface.addVectorLayer(uri,"gares", "ogr")
gares_reproject = processing.runAndLoadResults(
    "native:reprojectlayer", 
    {'INPUT':gares,
    'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:2154'),
    'OUTPUT':'memory:'})['OUTPUT']



#Tampon autour d'un km des points d'interets
buffer_gares = processing.run(
    "native:buffer", 
    {'INPUT':gares_reproject,'DISTANCE':1000,'SEGMENTS':5,'END_CAP_STYLE':0,'JOIN_STYLE':0,'MITER_LIMIT':2,'DISSOLVE':False,'OUTPUT':'memory:'})['OUTPUT']
    

#Intersections points d'interets et couche de superposition
intersection = processing.runAndLoadResults(
    "native:intersection", 
    {'INPUT':arrondissements,'OVERLAY':buffer_gares,'INPUT_FIELDS':[],'OVERLAY_FIELDS':[],'OUTPUT':'memory:'})['OUTPUT']


## sauvegarder de la couche
project = QgsProject.instance()
layer = project.mapLayersByName('Intersection')[0]
output_path="/Téléchargements/lyon/proximite.gpkg"
QgsVectorLayerExporter.exportLayer(layer = layer, uri = output_path, providerKey = 'ogr', destCRS = QgsCoordinateReferenceSystem('EPSG:2154'))


