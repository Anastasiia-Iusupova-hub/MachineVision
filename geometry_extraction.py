#!/usr/bin/env python

import vtk
from numpy import array
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk


def loadPoints():
    P = polydata.GetPoints().GetData()
    dimensions = P.GetNumberOfComponents()
    nPoints = P.GetNumberOfTuples()

    print ("loading %d points in %d dimensions" % (nPoints, dimensions), end='\n')

    if dimensions == 1:
        points = array([P.GetTuple1(i)
                        for i in range(nPoints)])
    elif dimensions == 2:
        points = array([P.GetTuple2(i)
                        for i in range(nPoints)])
    elif dimensions == 3:
        points = array([P.GetTuple3(i)
                        for i in range(nPoints)])
    elif dimensions == 4:
        points = array([P.GetTuple4(i)
                        for i in range(nPoints)])
    elif dimensions == 9:
        points = array([P.GetTuple9(i)
                        for i in range(nPoints)])
        return dimensions, points


def loadTriangles():
    polyData = polydata.GetPolys().GetData()
    X = [int(polyData.GetTuple1(i))
         for i in range(polyData.GetNumberOfTuples())]

    # assumes that faces are triangular
    X = array(X).reshape((-1, 4))
    nFaces = X.shape[0]
    triangles = X[:, 1:]

    print ("loaded %d faces" % nFaces, end='\n')


# common features description
colors = vtk.vtkNamedColors() 
arrowSource = vtk.vtkArrowSource() # for normals (glyph) display

###### description of the bent_sheet model ######
sheet = vtk.vtkSTLReader() 
sheet.SetFileName("/home/anastasiia/parts/bent_sheet.stl")
sheet.Update()
sheetMapper = vtk.vtkPolyDataMapper()
sheetMapper.SetInputConnection(sheet.GetOutputPort())
sheetActor = vtk.vtkLODActor()
sheetActor.SetMapper(sheetMapper)
sheetActor.SetPosition(-20.0, 5.0, 20.0)
sheetActor.GetProperty().SetColor(0, 0, 1)

sheetActor.GetProperty().SetEdgeVisibility(1) # this and below: functions for edges and vertices display
sheetActor.GetProperty().SetEdgeColor(0.9, 0.9, 0.4)
sheetActor.GetProperty().SetLineWidth(3)
sheetActor.GetProperty().SetPointSize(5)
sheetActor.GetProperty().SetRenderLinesAsTubes(1)
sheetActor.GetProperty().SetRenderPointsAsSpheres(1)
sheetActor.GetProperty().SetVertexVisibility(1)
sheetActor.GetProperty().SetVertexColor(0.5,1.0,0.8)

#################################################

######### description of the base model #########

base = vtk.vtkSTLReader()
base.SetFileName("/home/anastasiia/parts/base.STL")

basePolyData = base.GetOutput()

baseMapper = vtk.vtkPolyDataMapper()
baseMapper.SetInputConnection(base.GetOutputPort())
baseActor = vtk.vtkLODActor()
baseActor.SetMapper(baseMapper)
baseActor.SetPosition(25, 25, 25)
baseActor.GetProperty().SetColor(1, 0, 1)
baseMapper.SetInputConnection(base.GetOutputPort())

##################################################

######### description of the wheel model #########

wheel = vtk.vtkSTLReader()
wheel.SetFileName("/home/anastasiia/parts/wheel.stl")
wheelMapper = vtk.vtkPolyDataMapper()
wheelMapper.SetInputConnection(wheel.GetOutputPort())
wheelMapper.SetResolveCoincidentTopologyToPolygonOffset()
wheelActor = vtk.vtkLODActor()
wheelActor.SetMapper(wheelMapper)
wheelActor.SetPosition(-80.0, 0, 0)
wheelActor.GetProperty().SetColor(0, 1, 0)

##################################################

# The outline gives frame of the object
outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(base.GetOutputPort())
outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInputConnection(outline.GetOutputPort())
outlineActor = vtk.vtkActor()
outlineActor.SetMapper(outlineMapper)
outlineActor.SetPosition(25, 25, 25)
outlineProp = outlineActor.GetProperty()
outlineProp.SetColor(0, 0, 0)

# Work with geometrics
polydata = sheet.GetOutput()

if polydata.GetPoints() == None:
    raise IOError('Error with file loading')
else:
    loadPoints()
    loadTriangles()


# Create the assembly and add parts to it.  Also set the origin, position and orientation in space.
assembly = vtk.vtkAssembly()
assembly.AddPart(baseActor)
assembly.AddPart(sheetActor)
assembly.AddPart(wheelActor)

# Create the Renderer, RenderWindow, and RenderWindowInteractor
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Add the actors to the render; set the background and size
ren.AddActor(assembly)
ren.AddActor(sheetActor)
ren.AddActor(outlineActor)
ren.SetBackground(0.1, 0.2, 0.4)
renWin.SetSize(500, 500)

# Set up the camera to get a particular view of the scene
ren.GetActiveCamera().Zoom(1.5)

camera = vtk.vtkCamera()
#camera.SetClippingRange(21.9464, 30.0179)
#camera.SetFocalPoint(3.49221, 2.28844, -0.970866)
#camera.SetPosition(3.49221, 2.28844, 24.5216)
#camera.SetViewAngle(30)
#camera.SetViewUp(0, 1, 0)

ren.SetActiveCamera(camera)

w = vtk.vtkObject.GlobalWarningDisplayOff()  # disable annoying warnings

iren.Initialize()
renWin.Render()
iren.Start()
