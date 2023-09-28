import os, sys
from ij import IJ, ImagePlus
import shutil
# Add IsoView-GCaMP to the path if open_datFiles_customDatReader is used
#pathIsoViewGCaMP = "/lmb/home/pgg/ParkinsonConnectomics/IsoView-GCaMP/"
#sys.path.append(pathIsoViewGCaMP)
#from lib.io import readFIBSEMdat
pathCalculateDisplacement = "/lmb/home/pgg/ParkinsonConnectomics/Stitching_EM/src/"
sys.path.append(pathCalculateDisplacement)
from calculate_displacement import find_largest_displacement

# Extract command-line arguments
#@String input_path
#@String output_folder
#@String grid_size_x
#@String grid_size_y
#@String tile_overlap
#@String regression_threshold
#@String max_avg_displacement_threshold
#@String absolute_displacement_threshold

print(input_path)
print(output_folder)

rawfile = input_path
path2save = output_folder


#rawfile = r"/net/zstore1/FIBSEM/Pedro_parker/M06/D15/Merlin-FIBdeSEMAna_23-06-15_000153_0-0-1.dat"
#path2save = r"/net/zstore1/fibsem_data/A53T/Parker"

# Get the directory path
raw_folder = os.path.dirname(rawfile)
fileName = os.path.basename(rawfile)
print(fileName)

folderForTemporalSaving = os.path.join(path2save,"TemporalTiles")
folderToSaveStitching = os.path.join(path2save,"StitchedRawImages")
folderToSaveCsvDispl = os.path.join(path2save,"Displacement_csvs")
# Function to process and save the file
#def open_datFiles_customDatReader(file_path):
#	imp = readFIBSEMdat(file_path, channel_index=0, asImagePlus=True, toUnsigned=True)[0]
#	maxDisplayValue = int(imp.getDisplayRangeMax())
#
#	return imp, maxDisplayValue	

def open_datFiles_fijiOpener(file_path):
	imp = IJ.openImage(file_path)
	imp = IJ.getImage()
	maxDisplayValue = int(imp.getDisplayRangeMax())
	IJ.run(imp, "Next Slice [>]", "")
	IJ.run(imp, "Delete Slice", "")

	return imp, maxDisplayValue

def process_and_save_tifFiles(file_paths, output_folder):
    imp_list=[]
    max_display_values=[]
    for i, file_path in enumerate(file_paths):
		#imp, max_display_value = open_datFiles_customDatReader(file_path)
        imp, max_display_value = open_datFiles_fijiOpener(file_path)
        imp_list.append(imp)
        max_display_values.append(max_display_value)
    max_of_max = max(max_display_values)
	
    for i, imp in enumerate(imp_list):
        imp.setDisplayRange(0,max_of_max)
        IJ.saveAs(imp,"Tiff",os.path.join(output_folder,"Tile_"+str(i+1)+".tif"))

fileName = fileName[:-10]
tempFolder = folderForTemporalSaving + "_" + fileName
# Define the desired permission mode (0o777 for full permissions)
permission_mode = 0o777
print(tempFolder)
if not os.path.exists(tempFolder): os.makedirs(tempFolder); os.chmod(tempFolder, permission_mode)
if not os.path.exists(folderToSaveStitching): os.makedirs(folderToSaveStitching); os.chmod(folderToSaveStitching, permission_mode)
if not os.path.exists(folderToSaveCsvDispl): os.makedirs(folderToSaveCsvDispl); os.chmod(folderToSaveCsvDispl, permission_mode)

#Define the file paths for the grid components
file_paths = []
for row in range(int(grid_size_x)):
    for col in range(int(grid_size_y)):
        file_paths.append(os.path.join(raw_folder,fileName+"_0-"+str(row)+"-"+str(col)+".dat"))


process_and_save_tifFiles(file_paths,tempFolder)

IJ.run("Grid/Collection stitching", "type=[Grid: row-by-row] order=[Right & Down                ] grid_size_x="+grid_size_x+" grid_size_y="+grid_size_y+" tile_overlap="+tile_overlap+" first_file_index_i=1 directory="+tempFolder+" file_names=Tile_{i}.tif output_textfile_name="+fileName + "_0-0-0.txt" + " fusion_method=[Linear Blending] regression_threshold="+regression_threshold+" max/avg_displacement_threshold="+max_avg_displacement_threshold+" absolute_displacement_threshold="+absolute_displacement_threshold+" compute_overlap subpixel_accuracy computation_parameters=[Save computation time (but use more RAM)] image_output=[Write to disk] output_directory=["+tempFolder+"]");

print(os.path.join(tempFolder, fileName + "_0-0-0.txt"))
largest_displacement = find_largest_displacement(os.path.join(tempFolder, fileName + "_0-0-0.txt"), os.path.join(tempFolder,fileName + "_0-0-0.registered.txt"))
displacement_filename = os.path.join(folderToSaveCsvDispl, fileName + "_displacement.csv")
with open(displacement_filename, "w") as file:
    file.write(fileName + " - Largest Displacement (pixels), " + str(largest_displacement))

shutil.move(os.path.join(tempFolder,"img_t1_z1_c1"), os.path.join(folderToSaveStitching,fileName + "_0-0-0.tif"))
shutil.rmtree(tempFolder)
print(fileName + " successful")
#IJ.run("Quit");
os.system('kill %d' % os.getpid())
    
