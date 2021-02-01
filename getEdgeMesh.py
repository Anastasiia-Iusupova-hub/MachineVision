#!/usr/bin/env python

import vtk
import meshio

def main():

    mesh = meshio.Mesh.read(
    "/home/anastasiia/parts/motor.stl",  # string, os.PathLike, or a buffer/open file
    file_format="stl",  # optional if filename is a path; inferred from extension
)

    mesh.write("/home/anastasiia/parts/motorMesh.vtk")

    colors = vtk.vtkNamedColors()

    part = vtk.vtkUnstructuredGridReader()
    part.SetFileName("/home/anastasiia/parts/motorMesh.vtk")
    part.Update()

    featureEdges = vtk.vtkExtractEdges()
    featureEdges.SetInputConnection(part.GetOutputPort())

    featureEdges.Update()

    # Visualize
    edgeMapper = vtk.vtkPolyDataMapper()
    edgeMapper.SetInputConnection(featureEdges.GetOutputPort())
    edgeActor = vtk.vtkActor()
    edgeActor.SetMapper(edgeMapper)

    diskMapper = vtk.vtkPolyDataMapper()
    diskMapper.SetInputConnection(part.GetOutputPort())
    diskActor = vtk.vtkActor()
    diskActor.SetMapper(diskMapper)
    diskActor.GetProperty().SetColor(colors.GetColor3d('Gray'))

    # Create a renderer, render window, and interactor
    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetWindowName('BoundaryEdges')

    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    renderer.AddActor(edgeActor)
    renderer.AddActor(diskActor)
    renderer.SetBackground(colors.GetColor3d('DimGray'))
    renderWindow.Render()
    renderWindowInteractor.Start()


if __name__ == '__main__':
    main()
