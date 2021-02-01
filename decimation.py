#!/usr/bin/env python

import vtk

def main():

    # Define colors
    colors = vtk.vtkNamedColors()
    backFaceColor = colors.GetColor3d('Gold')
    inputActorColor = colors.GetColor3d('NavajoWhite')
    decimatedActorColor = colors.GetColor3d('NavajoWhite')
    # colors.SetColor('leftBkg', [0.6, 0.5, 0.4, 1.0])
    # colors.SetColor('rightBkg', [0.4, 0.5, 0.6, 1.0])

    reader = vtk.vtkSTLReader()
    reader.SetFileName("/home/anastasiia/parts/motor.stl")
    reader.Update()
    poly_data = reader.GetOutput()

    triangles = vtk.vtkTriangleFilter()
    triangles.SetInputData(poly_data)
    triangles.Update()
    inputPolyData = triangles.GetOutput()

    print('Before decimation')
    print(f'There are {inputPolyData.GetNumberOfPoints()} points.')
    print(f'There are {inputPolyData.GetNumberOfPolys()} polygons.')

    decimate = vtk.vtkDecimatePro()
    decimate.SetInputData(inputPolyData)
    decimate.SetTargetReduction(0.55)
    decimate.PreserveTopologyOn()
    decimate.Update()

    decimated = vtk.vtkPolyData()
    decimated.ShallowCopy(decimate.GetOutput())

    print('After decimation')
    print(f'There are {decimated.GetNumberOfPoints()} points.')
    print(f'There are {decimated.GetNumberOfPolys()} polygons.')
    print(
        f'Reduction: {(inputPolyData.GetNumberOfPolys() - decimated.GetNumberOfPolys()) / inputPolyData.GetNumberOfPolys()}')

    inputMapper = vtk.vtkPolyDataMapper()
    inputMapper.SetInputData(inputPolyData)

    backFace = vtk.vtkProperty()
    backFace.SetColor(backFaceColor)

    inputActor = vtk.vtkActor()
    inputActor.SetMapper(inputMapper)
    inputActor.GetProperty().SetInterpolationToFlat()
    inputActor.GetProperty().SetColor(inputActorColor)
    inputActor.SetBackfaceProperty(backFace)

    decimatedMapper = vtk.vtkPolyDataMapper()
    decimatedMapper.SetInputData(decimated)

    decimatedActor = vtk.vtkActor()
    decimatedActor.SetMapper(decimatedMapper)
    decimatedActor.GetProperty().SetColor(decimatedActorColor)
    decimatedActor.GetProperty().SetInterpolationToFlat()
    decimatedActor.SetBackfaceProperty(backFace)

    # There will be one render window
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetSize(600, 300)
    renderWindow.SetWindowName('Decimation');

    # And one interactor
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)

    # Define viewport ranges
    # (xmin, ymin, xmax, ymax)
    leftViewport = [0.0, 0.0, 0.5, 1.0]
    rightViewport = [0.5, 0.0, 1.0, 1.0]

    # Setup both renderers
    leftRenderer = vtk.vtkRenderer()
    renderWindow.AddRenderer(leftRenderer)
    leftRenderer.SetViewport(leftViewport)
    # leftRenderer.SetBackground((colors.GetColor3d('leftBkg')))
    leftRenderer.SetBackground((colors.GetColor3d('Peru')))

    rightRenderer = vtk.vtkRenderer()
    renderWindow.AddRenderer(rightRenderer)
    rightRenderer.SetViewport(rightViewport)
    # rightRenderer.SetBackground((colors.GetColor3d('rightBkg')))
    rightRenderer.SetBackground((colors.GetColor3d('CornflowerBlue')))

    # Add the sphere to the left and the cube to the right
    leftRenderer.AddActor(inputActor)
    rightRenderer.AddActor(decimatedActor)

    # Shared camera
    # Shared camera looking down the -y axis
    camera = vtk.vtkCamera()
    camera.SetPosition(0, -1, 0)
    camera.SetFocalPoint(0, 0, 0)
    camera.SetViewUp(0, 0, 1)
    camera.Elevation(30)
    camera.Azimuth(30)

    leftRenderer.SetActiveCamera(camera)
    rightRenderer.SetActiveCamera(camera)

    leftRenderer.ResetCamera()
    leftRenderer.ResetCameraClippingRange()

    renderWindow.Render()
    renderWindow.SetWindowName('Decimation')

    interactor.Start()

if __name__ == '__main__':
    main()
