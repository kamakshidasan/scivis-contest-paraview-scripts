import fileinput
import re
import os
from helper import *
import inspect
from datetime import datetime

# used in run: sort files according to characters and numeric
def sort_files(s):
	# seperate on 'index.extension'
	index, sep, extension = s.partition('.')
	# isnumeric only works for unicode strings
	if unicode(index, 'utf-8').isnumeric():
		return int(index)
	return float('inf')

# get current file path
file_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
parent_path = cwd()
data_path = get_input_path(parent_path)
file_list = os.listdir(data_path)

# custom sort for ascending order of timesteps
file_list = sorted(file_list, key=sort_files)

# insert a wildcard at the beginning
file_list.insert(0, 'adhitya.vtk')

#num_files = len(file_list)
num_files = 500

print file_list

for i in range(1, num_files+1):

	compute_file = get_output_path(file_path, [COMPUTE_SCRIPT], folder_name = SCRIPTS_FOLDER)
	replace_wildcard(compute_file, file_list[i-1], file_list[i])
	replace_wildcard(compute_file, 'tv-'+"{:03}".format(i-2), 'tv-'+"{:03}".format(i-1))
	run_paraview_script(compute_file)

	#split_make_tree_file = get_output_path(file_path, [SPLIT_MAKE_TREE_SCRIPT], folder_name = SCRIPTS_FOLDER)
	#run_python_script(split_make_tree_file, [file_list[i]])

	#files_left = num_files - i
	#print file_list[i], 'Done :)', files_left, ' files remaining'


# Back to normalcy :P
#replace_wildcard(compute_file, file_list[i], 'adhitya.vtk')

for i in range(1, num_files+1):
	print i, file_list[i]
