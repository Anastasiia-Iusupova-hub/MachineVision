#!/usr/bin/env python

import vtk


class curvatures():

    def curvatures(self):

        part = vtk.vtkSTLReader()
        part.SetFileName("/home/anastasiia/parts/part_with_circles.stl")

        # The quadric is made of strips, so pass it through a triangle filter as
        # the curvature filter only operates on polys
        tri = vtk.vtkTriangleFilter()
        tri.SetInputConnection(part.GetOutputPort())

        # The quadric has nasty discontinuities from the way the edges are generated
        # so let's pass it though a CleanPolyDataFilter and merge any points which
        # are coincident, or very close

        cleaner = vtk.vtkCleanPolyData()
        cleaner.SetInputConnection(tri.GetOutputPort())
        cleaner.SetTolerance(0.005)

        # Now we have the sources, lets put them into a list.
        sources = list()
        sources.append(cleaner)
        sources.append(cleaner)

        # Colour transfer function.
        ctf = vtk.vtkColorTransferFunction()
        ctf.SetColorSpaceToDiverging()
        ctf.AddRGBPoint(0.0, 0.230, 0.299, 0.754)
        ctf.AddRGBPoint(1.0, 0.706, 0.016, 0.150)
        cc = list()
        for i in range(256):
            cc.append(ctf.GetColor(float(i) / 255.0))

        # Lookup table.
        lut = list()
        for idx in range(len(sources)):
            lut.append(vtk.vtkLookupTable())
            lut[idx].SetNumberOfColors(256)
            for i, item in enumerate(cc):
                lut[idx].SetTableValue(i, item[0], item[1], 1.0)
            if idx == 0:
                lut[idx].SetRange(0, 0.5)
            if idx == 1:
                lut[idx].SetRange(0, 0.5)
            lut[idx].Build()

        curvatures = list()
        for idx in range(len(sources)):
            curvatures.append(vtk.vtkCurvatures())
            if idx % 2 == 0:
                curvatures[idx].SetCurvatureTypeToGaussian()
            else:
                curvatures[idx].SetCurvatureTypeToMean()

        renderers = list()
        mappers = list()
        actors = list()
        textmappers = list()
        textactors = list()

        # Create a common text property.
        textProperty = vtk.vtkTextProperty()
        textProperty.SetFontSize(10)
        textProperty.SetJustificationToCentered()

        names = ['Part - Gaussian Curvature', 'Part - Mean Curvature']

        # Link the pipeline together.
        for idx, item in enumerate(sources):
            sources[idx].Update()

            curvatures[idx].SetInputConnection(sources[idx].GetOutputPort())

            mappers.append(vtk.vtkPolyDataMapper())
            mappers[idx].SetInputConnection(curvatures[idx].GetOutputPort())
            mappers[idx].SetLookupTable(lut[idx])
            mappers[idx].SetUseLookupTableScalarRange(1)

            actors.append(vtk.vtkActor())
            actors[idx].SetMapper(mappers[idx])
            actors[idx].GetProperty().LightingOff() # to remove shadows

            textmappers.append(vtk.vtkTextMapper())
            textmappers[idx].SetInput(names[idx])
            textmappers[idx].SetTextProperty(textProperty)

            textactors.append(vtk.vtkActor2D())
            textactors[idx].SetMapper(textmappers[idx])
            textactors[idx].SetPosition(150, 16)

            renderers.append(vtk.vtkRenderer())

        gridDimensions = 2

        for idx in range(len(sources)):
            if idx < gridDimensions * gridDimensions:
                renderers.append(vtk.vtkRenderer)

        rendererSize = 300

        # Create the RenderWindow
        #
        renderWindow = vtk.vtkRenderWindow()
        renderWindow.SetSize(rendererSize * gridDimensions,
                             rendererSize * gridDimensions)

        # Add and position the renders to the render window.
        viewport = list()
        for row in range(gridDimensions):
            for col in range(gridDimensions):
                idx = row * gridDimensions + col

                viewport[:] = []
                viewport.append(float(col) * rendererSize /
                                (gridDimensions * rendererSize))
                viewport.append(float(gridDimensions - (row+1))
                                * rendererSize / (gridDimensions * rendererSize))
                viewport.append(float(col+1)*rendererSize /
                                (gridDimensions * rendererSize))
                viewport.append(float(gridDimensions - row) *
                                rendererSize / (gridDimensions * rendererSize))

                if idx > (len(sources) - 1):
                    continue

                renderers[idx].SetViewport(viewport)
                renderWindow.AddRenderer(renderers[idx])

                renderers[idx].AddActor(actors[idx])
                renderers[idx].AddActor(textactors[idx])
                renderers[idx].SetBackground(0.4, 0.3, 0.2)

        interactor = vtk.vtkRenderWindowInteractor()
        interactor.SetRenderWindow(renderWindow)

        renderWindow.Render()

        interactor.Start()


if __name__ == "__main__":
    po = curvatures()
    po.curvatures()
