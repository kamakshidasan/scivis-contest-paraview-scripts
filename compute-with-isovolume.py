import os
from helper import *

from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'XML Image Data Reader'
full_file_name = '49978.vti'
timestep = 'tv-476'

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

# create a new 'Iso Volume'
isoVolume1 = IsoVolume(Input=vtkFile)
isoVolume1.InputScalars = ['POINTS', 'v02']
isoVolume1.ThresholdRange = [0.0, 1.0]
isoVolume1Display = Show(isoVolume1, renderView1)
isoVolume1Display.Representation = 'Surface'

renderView1.Update()
Hide(vtkFile, renderView1)

# create a new 'Slice'
slice1 = Slice(Input=isoVolume1)
slice1.SliceType.Normal = [0.0, 0.0, 1.0]
slice1.SliceType.Normal = [0.0, 0.0, 1.0]
slice1Display = Show(slice1, renderView1)
slice1Display.Representation = 'Surface'

Hide(isoVolume1, renderView1)
renderView1.Update()

# create a new 'Extract Surface'
extractSurface1 = ExtractSurface(Input=slice1)
extractSurface1Display = Show(extractSurface1, renderView1)
extractSurface1Display.Representation = 'Surface'

Hide(slice1, renderView1)
renderView1.Update()

# set scalar coloring
ColorBy(extractSurface1Display, ('POINTS', 'v02'))

# rescale color and/or opacity maps used to include current data range
extractSurface1Display.RescaleTransferFunctionToDataRange(True, False)
extractSurface1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'v02'
v02LUT = GetColorTransferFunction('v02')

# create a new 'Contour'
contour1 = Contour(Input=extractSurface1)
contour1.ContourBy = ['POINTS', 'v02']
contour1.Isosurfaces = [1.0]
contour1Display = Show(contour1, renderView1)
contour1Display.Representation = 'Surface'

# hide data in view
Hide(extractSurface1, renderView1)
renderView1.Update()

# get layout
layout1 = GetLayout()
layout1.SplitVertical(0, 0.5)
SetActiveView(None)

# Create a new 'SpreadSheet View'
spreadSheetView1 = CreateView('SpreadSheetView')
spreadSheetView1.ColumnToSort = ''
spreadSheetView1.BlockSize = 1024L

# place view in the layout
layout1.AssignView(2, spreadSheetView1)

# get active source.
contour1 = GetActiveSource()
contour1Display = Show(contour1, spreadSheetView1)

# export view
output_folder = '/Users/adhitya/Desktop/results/'
other_output_folder = '/Users/adhitya/Desktop/scivis-contest-paraview/output/'

ExportView(output_folder + file_name + CSV_EXTENSION, view=spreadSheetView1, FilterColumnsByVisibility=1)
SaveData(other_output_folder + timestep + VTK_EXTENSION, proxy=contour1, FileType='Ascii')
#os._exit(0)
