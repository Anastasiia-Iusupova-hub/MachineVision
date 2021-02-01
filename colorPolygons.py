#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import vtk

def MakeLUT(tableSize):
    '''
    Make a lookup table from a set of named colors.
    :param: tableSize - The table size
    :return: The lookup table.
    '''
    nc = vtk.vtkNamedColors()

    lut = vtk.vtkLookupTable()
    lut.SetNumberOfTableValues(tableSize)
    lut.Build()

    # Fill in a few known colors, the rest will be generated if needed
    lut.SetTableValue(0,nc.GetColor4d("Black"))
    lut.SetTableValue(1,nc.GetColor4d("Banana"))
    lut.SetTableValue(2,nc.GetColor4d("Tomato"))
    lut.SetTableValue(3,nc.GetColor4d("Wheat"))
    lut.SetTableValue(4,nc.GetColor4d("Lavender"))
    lut.SetTableValue(5,nc.GetColor4d("Flesh"))
    lut.SetTableValue(6,nc.GetColor4d("Raspberry"))
    lut.SetTableValue(7,nc.GetColor4d("Salmon"))
    lut.SetTableValue(8,nc.GetColor4d("Mint"))
    lut.SetTableValue(9,nc.GetColor4d("Peacock"))

    return lut

def MakeCellData(tableSize, lut, colors):
    '''
    Create the cell data using the colors from the lookup table.
    :param: tableSize - The table size
    :param: lut - The lookup table.
    :param: colors - A reference to a vtkUnsignedCharArray().
    '''
    for i in range(1,tableSize):
        rgb = [0.0, 0.0, 0.0]
        lut.GetColor(float(i) / (tableSize - 1),rgb)
        ucrgb = list(map(int, [x * 255 for x in rgb]))
        colors.InsertNextTuple3(ucrgb[0], ucrgb[1], ucrgb[2])
        s = '['+ ', '.join(['{:0.6f}'.format(x) for x in rgb]) + ']'
        print(s, ucrgb)

def main():
    nc = vtk.vtkNamedColors()

    resolution = 49

    plane11 = vtk.vtkSTLReader() # bottom
    plane11.SetFileName("/home/anastasiia/parts/part_with_circles.stl")

    plane12 = vtk.vtkSTLReader() 
    plane12.SetFileName("/home/anastasiia/parts/part_with_circles.stl") # up

    tableSize = max(resolution * resolution + 1, 10)

    #  Force an update so we can set cell data
    plane11.Update()
    plane12.Update()

    #  Get the lookup table mapping cell data to colors
    lut1 = MakeLUT(tableSize)

    colorData = vtk.vtkUnsignedCharArray()
    colorData.SetName('colors')
    colorData.SetNumberOfComponents(3)
    print('Using a lookup table from a set of named colors.')
    MakeCellData(tableSize, lut1, colorData)

    #plane11.GetOutput().GetCellData().SetScalars(colorData) # color POLYGONS
    plane11.GetOutput().GetPointData().SetScalars(colorData) # color POINTS

    # Set up actor and mapper
    mapper11 = vtk.vtkPolyDataMapper()
    mapper11.SetInputConnection(plane11.GetOutputPort())
    mapper11.SetScalarModeToUseCellData()
    mapper11.SetScalarModeToUsePointData()
    mapper11.Update()

    mapper12 = vtk.vtkPolyDataMapper()
    mapper12.SetInputConnection(plane12.GetOutputPort())
    mapper12.SetScalarModeToUseCellData()
    mapper12.Update()

    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName('pdlut.vtp')
    writer.SetInputData(mapper11.GetInput())
    # This is set so we can see the data in a text editor.
    writer.SetDataModeToAscii()
    writer.Write()
    writer.SetFileName('pdctf.vtp')
    writer.SetInputData(mapper12.GetInput())
    writer.Write()

    actor11 = vtk.vtkActor()
    actor11.SetMapper(mapper11)
    actor11.GetProperty().SetVertexVisibility(1)
    
    actor12 = vtk.vtkActor()
    actor12.SetMapper(mapper12)

    # Let's read in the data we wrote out.
    reader1 = vtk.vtkXMLPolyDataReader()
    reader1.SetFileName("pdlut.vtp")

    # Define viewport ranges.
    # (xmin, ymin, xmax, ymax)
    viewport11 = [0.0, 0.0, 1.0, 0.5]
    viewport12 = [0.0, 0.5, 1.0, 1.0]

    # Set up the renderers.
    ren11 = vtk.vtkRenderer()
    ren12 = vtk.vtkRenderer()

    # Setup the render windows
    renWin = vtk.vtkRenderWindow()
    renWin.SetSize(800, 800)
    renWin.AddRenderer(ren11)
    renWin.AddRenderer(ren12)
    ren11.SetViewport(viewport11)
    ren12.SetViewport(viewport12)
    ren11.SetBackground(nc.GetColor3d('MidnightBlue'))
    ren12.SetBackground(nc.GetColor3d('MidnightBlue'))
    ren11.AddActor(actor11)
    ren12.AddActor(actor12)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    renWin.Render()

    return iren

if __name__ == '__main__':

    iren = main()
    iren.Start()
