import os, sys
from ij import IJ
import shutil

# Extract command-line arguments

#@String input_path
#@String output_folder

print(input_path)
print(output_folder)

rawfile = input_path
path2save = output_folder

# Get the directory path
raw_folder = os.path.dirname(rawfile)
fileName = os.path.basename(rawfile)
print(fileName)


folderToSaveStitching = os.path.join(path2save,"Downsampled_stitchedImgs")

# Function to process and save the file
def process_and_save(file_path, output_file_path):
    imp = IJ.openImage(file_path)
    imp = imp.resize(250, 250, "bilinear");
    IJ.saveAs(imp,"Tiff",output_file_path)
    imp.close();

# Define the desired permission mode (0o777 for full permissions)
permission_mode = 0o777
if not os.path.exists(folderToSaveStitching): os.makedirs(folderToSaveStitching); os.chmod(folderToSaveStitching, permission_mode)

# Process and save file
process_and_save(rawfile, os.path.join(folderToSaveStitching, "Downsampled_"+fileName))

print(fileName + " successful")
#IJ.run("Quit");
os.system('kill %d' % os.getpid())

 

    
