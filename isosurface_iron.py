# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 14:53:20 2015

@author: Shalini
"""

# Import vtk package to access VTK classes/functions. 
import vtk

#==============================================================================
# 1. Iron Protein dataset
#==============================================================================

# Read the Iron Protien dataset
print ("Exlporing Iso-surfaces Iron Protein dataset is in Process")   

 #change the path if necessary
filename = "ironProt.vtk"
reader = vtk.vtkStructuredPointsReader()
reader.SetFileName(filename)
print("Reading volume dataset from " + filename + " ...")
reader.Update()  # executes the reader
print("Dataset successfully loaded")   
width, height, depth = reader.GetOutput().GetDimensions()
print("Dimensions: %i %i %i" % (width, height, depth))
min = 0 #Slider minimum value
max = 256 #Slider maximum value

# iso surface
isosurface = vtk.vtkContourFilter() 
isosurface.SetInput( reader.GetOutput() ) 
isosurface.SetValue( 0, (min + max) / 2 )

# Clean up duplicate points
clean = vtk.vtkCleanPolyData()
clean.SetInput( isosurface.GetOutput() ) 

normals = vtk.vtkPolyDataNormals()
normals.SetInput( isosurface.GetOutput() )
normals.SetFeatureAngle(45)

isosurfaceMapper = vtk.vtkPolyDataMapper() 
isosurfaceMapper.SetInput( normals.GetOutput() ) 
isosurfaceMapper.SetColorModeToMapScalars()    

isosurfaceActor = vtk.vtkActor() 
isosurfaceActor.SetMapper( isosurfaceMapper )
  
#Create the outline  
outline = vtk.vtkOutlineFilter() 
outline.SetInput( reader.GetOutput() ) 
outlineMapper = vtk.vtkPolyDataMapper() 
outlineMapper.SetInput( outline.GetOutput() )
outlineActor = vtk.vtkActor() 
outlineActor.SetMapper( outlineMapper ) 
outlineActor.GetProperty().SetColor(0.0,0.0,0.0)

# renderer and render window 
ren = vtk.vtkRenderer() 
ren.SetBackground(0.90, 0.03, 0.03)
renWin = vtk.vtkRenderWindow() 
renWin.SetSize( 500, 500 ) 
renWin.AddRenderer( ren ) 


# render window interactor 
iren = vtk.vtkRenderWindowInteractor() 
iren.SetSize(1500,1500)
iren.SetRenderWindow( renWin ) 
 
# add the actors 
ren.AddActor( outlineActor ) 
ren.AddActor( isosurfaceActor )    

#==============================================================================
#  Interactive Slider representation
#==============================================================================

def vtkSliderCallback2(obj, event):
    sliderRepres = obj.GetRepresentation()
    pos = sliderRepres.GetValue()
    print "Position ",pos
    isosurface.SetValue(0, pos)
  
SliderRepres = vtk.vtkSliderRepresentation2D()
SliderRepres.SetMinimumValue(min)
SliderRepres.SetMaximumValue(max)
SliderRepres.SetValue((min + max) / 2)

SliderRepres.SetTitleText("Interactive Slider")
SliderRepres.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
SliderRepres.GetPoint1Coordinate().SetValue(0.3, 0.05)
SliderRepres.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
SliderRepres.GetPoint2Coordinate().SetValue(0.7, 0.05)

SliderRepres.SetSliderLength(0.02)
SliderRepres.SetSliderWidth(0.03)
SliderRepres.SetEndCapLength(0.01)
SliderRepres.SetEndCapWidth(0.03)
SliderRepres.SetTubeWidth(0.005)
SliderRepres.SetLabelFormat("%3.0lf")
SliderRepres.SetTitleHeight(0.02)
SliderRepres.SetLabelHeight(0.02)
SliderRepres.GetSelectedProperty().SetColor(0,1,0)

SliderWidget = vtk.vtkSliderWidget()
SliderWidget.SetInteractor(iren)
SliderWidget.SetRepresentation(SliderRepres)
SliderWidget.KeyPressActivationOff()
SliderWidget.SetAnimationModeToAnimate()
SliderWidget.SetEnabled(True)
SliderWidget.AddObserver("EndInteractionEvent", vtkSliderCallback2)

# Execute the Pipeline
renWin.Render() 

# initialize and start the interactor 
iren.Initialize() 
iren.Start() 




