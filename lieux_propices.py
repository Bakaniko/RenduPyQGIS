# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink, 
                       QgsProcessingParameterDistance,
                      QgsProcessingParameterVectorDestination )
from qgis import processing


class ProximiteAlgorithm(QgsProcessingAlgorithm):
    """
    Retourne les objets d'une couche à proximité d'une autre couche.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    OUTPUT = 'OUTPUT'  # couche en sortie
    POI1 = 'POI1'  # couche qui sera intersectée
    POI2 = 'POI2' # couche de trucs interessants
    POI3 = 'POI3' # couche de trucs interessants 
    POI4 = 'POI4' # couche de trucs interessants
    BUFFER_OUTPUT = 'BUFFER_OUTPUT' # stockage du buffer

    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ProximiteAlgorithm()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. 
        """
        return 'proximite'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Objets à proximite')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Example scripts')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'examplescripts'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("Example algorithm short description")

    def initAlgorithm(self, config=None):
        """
        Initialisation de l'algorithme: définition des
        paramètres en entrée et en sortie
        """

        # Données source
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.POI1,
                self.tr("Couche d'interet 1 (par exemple les gares SNCF) "),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )
        # Distance du tampon
        self.addParameter(
            QgsProcessingParameterDistance(
                'BUFFERDIST1',
                self.tr('Distance du tampon'),
                defaultValue = 1000.0,
                # Make distance units match the INPUT layer units:
                parentParameterName='POI1'
            )
        )
        
        # Données source
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.POI2,
                self.tr("Couche d'interet 2 ( par exemple les stations de metro)"),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )
        # Distance du tampon
        self.addParameter(
            QgsProcessingParameterDistance(
                'BUFFERDIST2',
                self.tr('Distance du tampon'),
                defaultValue = 300.0,
                # Make distance units match the INPUT layer units:
                parentParameterName='POI2'
            )
        )
        # Données source
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.POI3,
                self.tr("Couche d'interet 3 (par exemple les espaces verts)"),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )
        # Distance du tampon
        self.addParameter(
            QgsProcessingParameterDistance(
                'BUFFERDIST3',
                self.tr('Distance du tampon'),
                defaultValue = 200.0,
                # Make distance units match the INPUT layer units:
                parentParameterName='POI3'
            )
        )
        # Données source
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.POI4,
                self.tr("Couche d'interet 4 (par exemples les piscines)"),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )
            
        # Distance du tampon
        self.addParameter(
            QgsProcessingParameterDistance(
                'BUFFERDIST4',
                self.tr('Distance du tampon'),
                defaultValue = 500.0,
                # Make distance units match the INPUT layer units:
                parentParameterName='POI4'
            )
        )
        # Récupération de la destination.
        self.addParameter(
            QgsProcessingParameterVectorDestination(
                self.OUTPUT,
                self.tr('Sortie')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        
        # récupération des paramètres
        outputFile = self.parameterAsOutputLayer(parameters,self.OUTPUT, context)
        bufferdist1 = self.parameterAsDouble(parameters, 'BUFFERDIST1', context)
        bufferdist2 = self.parameterAsDouble(parameters, 'BUFFERDIST2', context)
        bufferdist3 = self.parameterAsDouble(parameters, 'BUFFERDIST3', context)
        bufferdist4 = self.parameterAsDouble(parameters, 'BUFFERDIST4', context)
                                            
        POI1 = self.parameterAsLayer(parameters, 'POI1', context)
        POI2 = self.parameterAsLayer(parameters, 'POI2', context)
        POI3 = self.parameterAsLayer(parameters, 'POI3', context)
        POI4 = self.parameterAsLayer(parameters, 'POI4', context)
        
        #Tampon autour d'un km des gares
        buffer_gares = processing.run(
            "native:buffer", 
            {'INPUT':POI1,'DISTANCE':bufferdist1,'SEGMENTS':5,'END_CAP_STYLE':0,'JOIN_STYLE':0,'MITER_LIMIT':2,'DISSOLVE':False,'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']
            
        #tampon autours de 300 m des métro
        buffer_metro = processing.run(
            "native:buffer", 
            {'INPUT':POI2,'DISTANCE':bufferdist2,'SEGMENTS':5,'END_CAP_STYLE':0,'JOIN_STYLE':0,'MITER_LIMIT':2,'DISSOLVE':False,'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']
            
        #♥Tampon 200 m espaces verts
        buffer_vert = processing.run(
            "native:buffer", 
            {'INPUT':POI3,'DISTANCE':bufferdist3,'SEGMENTS':5,'END_CAP_STYLE':0,'JOIN_STYLE':0,'MITER_LIMIT':2,'DISSOLVE':False,'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']
            
        #Tampon 500 m piscines 
        buffer_piscines = processing.run(
            "native:buffer", 
            {'INPUT':POI4,'DISTANCE':bufferdist4,'SEGMENTS':5,'END_CAP_STYLE':0,'JOIN_STYLE':0,'MITER_LIMIT':2,'DISSOLVE':False,'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']
            

        #Intersections tampon 
        intersection = processing.run(
            "native:intersection", 
            {'INPUT':buffer_gares,'OVERLAY':buffer_metro,'INPUT_FIELDS':[],'OVERLAY_FIELDS':[],'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']

        intersection2 = processing.run(
            "native:intersection", 
            {'INPUT':buffer_vert,'OVERLAY':intersection,'INPUT_FIELDS':[],'OVERLAY_FIELDS':[],'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']
            
        intersection3 = processing.run(
            "native:intersection", 
            {'INPUT':buffer_piscines,'OVERLAY':intersection2,'INPUT_FIELDS':[],'OVERLAY_FIELDS':[],'OUTPUT':outputFile}, context=context, feedback=feedback)
            
        # Retourne le résultat
        return {self.OUTPUT: intersection3}
