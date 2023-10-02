# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 17:34:28 2023

@author: Pedro Gomez Galvez
"""

import subprocess
import multiprocessing
import os
import csv
srcPath = r"/lmb/home/pgg/ParkinsonConnectomics/Stitching_EM/src"
sys.path.append(srcPath)
from call_fiji import run_fiji_python_Stitching_macro, run_fiji_python_Downsampling_macro, run_fiji_saveDatFilesAsTiffs

def find_files_with_name(root_dir, filename):
    file_paths = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if filename in file:
                file_paths.append(os.path.join(root, file))
    return file_paths

def concatenate_files_content(input_files, output_file):
    with open(output_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        for input_file in input_files:
            with open(input_file, 'r') as infile:
                writer.writerow([infile.read()])
            
            
if __name__ == '__main__':

    root_directory = r"/net/zstore1/FIBSEM/Pedro_parker"
    output_folder = r"/net/zstore1/fibsem_data/A53T/Parker"
    currentDir = os.getcwd()
    target_allFiles = "0-0-0.dat" #targetting all dat files
    target_allTiledFiles = "0-0-1.dat" #targetting only images acquired multi-tiling.
    target_filename_downsampling = "0-0-0.tif" #targetting stitched slices to be downsampled for a final image-sequence check.

    grid_size_x=2 #number of tiles (columns) per slice
    grid_size_y=2 #number of tiles (rows) per slice
    
    ##PARAMS for Stitching
    tile_overlap = 2 #percentage of overlapping among tiles
    regression_threshold=0.30 #default 0.3
    max_avg_displacement_threshold=2.50 #default 2.5
    absolute_displacement_threshold=3.50 #default 3.5
    
	#Paths images (only tiled and [tiled + non-tiled]) 
    allTiledFile_paths = find_files_with_name(root_directory, target_allTiledFiles)    
    allFile_paths = find_files_with_name(root_directory, target_allFiles)    
    
    # Specify the output folder for processed images 
    python_macroStitching_path = os.path.join(srcPath,"stitch_tiles.py")
    python_macroDownsampling_path = os.path.join(srcPath,"downsampled_images.py")
    python_macroSaveDatAsTif = os.path.join(srcPath,"save_dat_as_tif.py")

    # Create a multiprocessing pool to run Fiji in parallel
    num_workers = 30 #cardona-gpu1 cannot with more than ~30 workers
    
    print ("--------------------------------------1. STITCHING ----------------------------------------------")
          
    with multiprocessing.Pool(processes=num_workers) as pool:
        pool.starmap(run_fiji_python_Stitching_macro,[(python_macroStitching_path, input_path, output_folder, grid_size_x, grid_size_y, tile_overlap, regression_threshold,max_avg_displacement_threshold,absolute_displacement_threshold) for input_path in allTiledFile_paths])
        pool.close()
        pool.join()
    
    #Concatenate all the calculated displacements during stitching
    print("--------------------------------------2. CONCATENATING TILES DISPLACEMENTS DURING STITCHING----------------------------------------------")
    csvDirectory = r"/net/zstore1/fibsem_data/A53T/Parker/Displacement_csvs/"
    allCsvFiles_path = find_files_with_name(csvDirectory, "displacement.csv")
    concatenate_files_content(allCsvFiles_path, os.path.join(csvDirectory,"concatenationAllDisplacements.csv"))
    
    # IF STITCHING IS DONE, COMMENT PREVIOUS STITCHING CODE AND CONTINUE WITH THE DOWNSAMPLING TO DOUBLE CHECK WRONG STITCHED IMAGES -------------------------------------
    print("--------------------------------------3. DOWNSAMPLING----------------------------------------------")
    
    num_workers = 25 # with more than 25 workers cardona-gpu1 [all workers free] crashes

    # DOWNSAMPLING THE STITCHED .TIFs
    allFile_pathsDownsampling = find_files_with_name(os.path.join(output_folder, "StitchedRawImages"), target_filename_downsampling)   

    with multiprocessing.Pool(processes=num_workers) as pool:
        pool.starmap(run_fiji_python_Downsampling_macro,[(python_macroDownsampling_path, input_path, output_folder) for input_path in allFile_pathsDownsampling])
        pool.close()
        pool.join()
    
    print("--------------------------------------4. SAVE ALL THE NON-TILED .DAT IMAGES AS .TIF----------------------------------------------")
    ### save the non-tiled .dat images as .tif to be formatted in the same was as the tiled ones.
    paths_TiledFiles = [string[:-5] +"0.dat" for string in allTiledFile_paths]
    setAllTiledImages = set(paths_TiledFiles)
    setAllFiles = set(allFile_paths)
    nonTiledImages = setAllFiles.symmetric_difference(setAllTiledImages)
    pathNonTiledImages = list(nonTiledImages)
    
    num_workers=20

    with multiprocessing.Pool(processes=num_workers) as pool:
        pool.starmap(run_fiji_saveDatFilesAsTiffs,[(python_macroSaveDatAsTif, input_path, output_folder) for input_path in pathNonTiledImages])
        pool.close()
        pool.join()