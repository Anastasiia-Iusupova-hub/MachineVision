#!/usr/bin/env python

import vtk

# Create the reader and read a data file.  Connect the mapper and
# actor.
base = vtk.vtkSTLReader()
base.SetFileName("/home/anastasiia/parts/base.STL")
baseMapper = vtk.vtkPolyDataMapper()
baseMapper.SetInputConnection(base.GetOutputPort())
baseActor = vtk.vtkLODActor()
baseActor.SetMapper(baseMapper)
baseActor.SetPosition(2.25, 3, 3)
baseActor.GetProperty().SetColor(1, 0, 1)

sheet = vtk.vtkSTLReader()
sheet.SetFileName("/home/anastasiia/parts/bent_sheet.stl")
sheetMapper = vtk.vtkPolyDataMapper()
sheetMapper.SetInputConnection(sheet.GetOutputPort())
sheetActor = vtk.vtkLODActor()
sheetActor.SetMapper(sheetMapper)
sheetActor.SetPosition(20.0, 5.0, 20.0)
sheetActor.GetProperty().SetColor(0, 0, 1)

wheel = vtk.vtkSTLReader()
wheel.SetFileName("/home/anastasiia/parts/wheel.stl")
wheelMapper = vtk.vtkPolyDataMapper()
wheelMapper.SetInputConnection(wheel.GetOutputPort())
wheelMapper.SetResolveCoincidentTopologyToPolygonOffset()
wheelActor = vtk.vtkLODActor()
wheelActor.SetMapper(wheelMapper)
sheetActor.SetPosition(-60.0, 0, 0)
wheelActor.GetProperty().SetColor(0, 1, 0)

# Create the assembly and add the 4 parts to it.  Also set the origin,
# position and orientation in space.
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
#ren.AddActor(sheetActor)
ren.SetBackground(0.1, 0.2, 0.4)
renWin.SetSize(500, 500)

# Set up the camera to get a particular view of the scene
camera = vtk.vtkCamera()
camera.SetClippingRange(21.9464, 30.0179)
camera.SetFocalPoint(3.49221, 2.28844, -0.970866)
camera.SetPosition(3.49221, 2.28844, 24.5216)
camera.SetViewAngle(30)
camera.SetViewUp(0, 1, 0)
ren.SetActiveCamera(camera)

iren.Initialize()
renWin.Render()
iren.Start()

