import os, sys
from ij import IJ, ImagePlus

# Add IsoView-GCaMP to the path if open_datFiles_customDatReader is used
#pathIsoViewGCaMP = "/lmb/home/pgg/ParkinsonConnectomics/IsoView-GCaMP/"
#sys.path.append(pathIsoViewGCaMP)
#from lib.io import readFIBSEMdat


# Extract command-line arguments
#@String input_path
#@String output_folder

print(input_path)
print(output_folder)

rawfile = input_path
path2save = output_folder
folderToSaveTif = os.path.join(path2save,"NonTiledImgs")

# Function to process and save the file
#def open_datFiles_customDatReader(file_path):
#	imp = readFIBSEMdat(file_path, channel_index=0, asImagePlus=True, toUnsigned=True)[0]
#	maxDisplayValue = int(imp.getDisplayRangeMax())
#
#	return imp, maxDisplayValue	

def open_datFiles_fijiOpener(file_path):
	imp = IJ.openImage(file_path)
	imp = IJ.getImage()
	IJ.run(imp, "Next Slice [>]", "")
	IJ.run(imp, "Delete Slice", "")

	return imp



# Define the desired permission mode (0o777 for full permissions)
permission_mode = 0o777
if not os.path.exists(folderToSaveTif): os.makedirs(folderToSaveTif); os.chmod(folderToSaveTif, permission_mode)

fileName = os.path.basename(rawfile)

fileName = fileName[:-5]
imp = open_datFiles_fijiOpener(rawfile)
IJ.saveAs(imp,"Tiff",os.path.join(folderToSaveTif,fileName+"0.tif"))

os.system('kill %d' % os.getpid())
    
