import os
from helper import *

from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'XML Image Data Reader'
full_file_name = '49551.vti'
# replace this with 'tvi--1'
timestep = 'tv-461'

parent_path = cwd()
data_path = get_input_path(parent_path)
data_path = get_input_path(parent_path)
file_path = join_file_path(data_path, full_file_name)
file_name = get_file_name(full_file_name)

vtkFile = XMLImageDataReader(FileName=[file_path])
renderView1 = GetActiveViewOrCreate('RenderView')
vtkFileDisplay = Show(vtkFile, renderView1)
vtkFileDisplay.Representation = 'Outline'

renderView1.ResetCamera()
renderView1.Update()

# create a new 'Extract Subset'
extractSubset = ExtractSubset(Input=vtkFile)
extractSubset.VOI = [0, 299, 0, 299, 0, 299]
extractSubsetDisplay = Show(extractSubset, renderView1)
extractSubsetDisplay.Representation = 'Volume'
extractSubsetDisplay.SetScalarBarVisibility(renderView1, True)
renderView1.Update()
Hide(vtkFile, renderView1)

# create a new 'Slice'
slice1 = Slice(Input=extractSubset)
slice1.SliceType.Normal = [0.0, 0.0, 1.0]
slice1.SliceType.Normal = [0.0, 0.0, 1.0]
slice1Display = Show(slice1, renderView1)
slice1Display.Representation = 'Surface'

Hide(extractSubset, renderView1)
renderView1.Update()

# set scalar coloring
ColorBy(slice1Display, ('POINTS', 'v02'))
slice1Display.RescaleTransferFunctionToDataRange(True, False)
slice1Display.SetScalarBarVisibility(renderView1, True)
v02LUT = GetColorTransferFunction('v02')
v02LUTColorBar = GetScalarBar(v02LUT, renderView1)
v02LUTColorBar.LabelFontSize = 0

# create a new 'Contour'
contour1 = Contour(Input=slice1)
contour1.ContourBy = ['POINTS', 'v02']
contour1.Isosurfaces = [1.0]
contour1Display = Show(contour1, renderView1)
contour1Display.Representation = 'Surface'
#Hide(slice1, renderView1)
renderView1.Update()

# create a new 'Tube'
tube = Tube(Input=contour1)
tube.Vectors = [None, '']
tube.Radius = 14260.0
tubeDisplay = Show(tube, renderView1)
tubeDisplay.Representation = 'Surface'
Hide(contour1, renderView1)
tubeDisplay.SetScalarBarVisibility(renderView1, False)
tubeDisplay.DiffuseColor = [0.0, 1.0, 0.0]
renderView1.Update()

# take screenshot of scalar field
screen_file_arguments = [timestep, PNG_EXTENSION]
screen_file_path = get_output_path(file_path, screen_file_arguments, folder_name = SCREENSHOT_FOLDER)
SaveScreenshot(screen_file_path, magnification=1, quality=100, view=renderView1)

Hide(slice1, renderView1)
Hide(contour1, renderView1)
Hide(tube, renderView1)
slice1Display = Show(slice1, renderView1)
ColorBy(slice1Display, ('POINTS', 'v03'))

slice1Display.SetScalarBarVisibility(renderView1, True)
v03LUT = GetColorTransferFunction('v03')
v03LUTColorBar = GetScalarBar(v03LUT, renderView1)
v03LUTColorBar.LabelFontSize = 0

renderView1.Update()

screen_file_arguments = [timestep, PNG_EXTENSION]
screen_file_path = get_output_path(file_path, screen_file_arguments, folder_name = PERSISTENCE_FOLDER)
SaveScreenshot(screen_file_path, magnification=1, quality=100, view=renderView1)



os._exit(0)
