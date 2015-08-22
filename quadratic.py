# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 14:53:20 2015

@author: Shalini
"""

# Import vtk package to access VTK classes/functions. 
import vtk


def vtkSliderCallback2(obj, event):
    sliderRepres = obj.GetRepresentation()
    pos = sliderRepres.GetValue()
    print "Position ",pos
    isosurface.SetValue(0, pos)
    
#==============================================================================
# 2. 100^3 Samlping dataset of the Quadric function
#==============================================================================  

# create a data source...an implicit function. 
# F(x,y,z) = a0*x^2 + a1*y^2 + a2*z^2 + a3*x*y + a4*y*z + a5*x*z + a6*x + a7*y + a8*z + a9
# F(x,y,z) = 1*x^2 + 0.5*y^2 + 0.2*z^2 + 0*x*y + 0*y*z + 0.1*x*z + 0.2*x + 0*y + 0*z + 0

quadric = vtk.vtkQuadric() 
quadric.SetCoefficients(1, 0.5, 0.2, 0, 0, 0.1, 0.2, 0, 0, 0) 

#==============================================================================
# Create a filter : A sampling function, which samples an implicit function over the x-y-z range 
#  although this object is not called "filter" it takes an input and process it 
#  and produce an output. 
#==============================================================================
sample = vtk.vtkSampleFunction() 
sample.SetSampleDimensions(100, 100, 100) 
sample.SetImplicitFunction(quadric) 
min = 0.05 #Slider minimum value
max = 1.5 #Slider maximum value


# computing a contour of an input data. 
isosurface = vtk.vtkContourFilter() 
isosurface.SetInputConnection(sample.GetOutputPort())
isosurface.SetValue(0,(min + max) / 2) 

isosurfaceMapper = vtk.vtkPolyDataMapper() 
isosurfaceMapper.SetInput( isosurface.GetOutput() ) 
isosurfaceMapper.SetColorModeToMapScalars()    
isosurfaceActor = vtk.vtkActor() 
isosurfaceActor.SetMapper( isosurfaceMapper )
 
#Create the outline  
outline = vtk.vtkOutlineFilter() 
outline.SetInput( sample.GetOutput() ) 
outlineMapper = vtk.vtkPolyDataMapper() 
outlineMapper.SetInput( outline.GetOutput() )
outlineActor = vtk.vtkActor() 
outlineActor.SetMapper( outlineMapper ) 
outlineActor.GetProperty().SetColor(1,1,1)


# renderer and render window 
ren = vtk.vtkRenderer() 
ren.SetBackground(0, 0, 0)
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

