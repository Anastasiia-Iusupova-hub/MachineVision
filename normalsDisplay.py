import vtk
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk

filename = "/home/anastasiia/parts/loop.STL"
reader = vtk.vtkSTLReader()
reader.SetFileName(filename)

colors = vtk.vtkNamedColors() 
arrow = vtk.vtkArrowSource() # for normals (glyph) display

normals = vtk.vtkPPolyDataNormals()
normals.SetInputConnection(reader.GetOutputPort())

#normals.ComputePointNormalsOn() # use when centers are OFF (i.e. with arrows)
#normals.ComputeCellNormalsOff()

normals.ComputePointNormalsOff() # use when centers are ON
normals.ComputeCellNormalsOn()

normals.SplittingOff()
normals.FlipNormalsOff()
normals.ConsistencyOn()
normals.AutoOrientNormalsOn()
normals.Update()

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(0, 0.5, 0.5)
actor.GetProperty().LightingOff() # to remove shadows

centers = vtk.vtkCellCenters()
centers.SetInputConnection(normals.GetOutputPort())

readerPolyData = reader.GetOutput()

glyph3D = vtk.vtkGlyph3D()
glyph3D.SetInputData(normals.GetOutput())
#glyph3D.SetSourceConnection(arrow.GetOutputPort()) # use with PointNormalsOn and CellNormalsOff
glyph3D.SetInputConnection(centers.GetOutputPort()) # use with PointNormalsOff and CellNormalsOn
glyph3D.SetVectorModeToUseNormal()
glyph3D.SetVectorModeToUseNormal()
glyph3D.SetScaleFactor(5)
glyph3D.OrientOn()
glyph3D.Update()
glyphMapper = vtk.vtkPolyDataMapper()
glyphMapper.SetInputData(glyph3D.GetOutput())
glyphMapper = vtk.vtkPolyDataMapper()
glyphMapper.SetInputConnection(glyph3D.GetOutputPort())
glyphActor = vtk.vtkActor()
glyphActor.SetMapper(glyphMapper)
glyphActor.GetProperty().SetColor(colors.GetColor3d('Yellow'))
glyphActor.SetPosition(0,0,0)
glyphActor.GetProperty().SetLineWidth(3);
glyphActor = vtk.vtkActor()
glyphActor.SetMapper(glyphMapper)

# Create a rendering window and renderer
renderer = vtk.vtkRenderer()
renderingwindow = vtk.vtkRenderWindow()
renderingwindow.AddRenderer(renderer)


# Create a renderwindowinteractor
renderwindowinteractor = vtk.vtkRenderWindowInteractor()
renderwindowinteractor.SetRenderWindow(renderingwindow)

# Assign actor to the renderer
renderer.AddActor(actor)
renderer.AddActor(glyphActor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Enable user interface interactor
renderwindowinteractor.Initialize()
renderingwindow.Render()
renderwindowinteractor.Start()
