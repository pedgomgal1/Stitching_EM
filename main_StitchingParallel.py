# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 17:34:28 2023

@author: Pedro Gomez Galvez
"""

import subprocess
import multiprocessing
import os
from src.callFiji import run_fiji_python_Stitching_macro, run_fiji_python_Downsampling_macro

def find_files_with_name(root_dir, filename):
    file_paths = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if filename in file:
                file_paths.append(os.path.join(root, file))
    return file_paths

def concatenate_files_content(input_files, output_file):
    with open(output_file, 'w') as outfile:
        for input_file in input_files:
            with open(input_file, 'r') as infile:
                outfile.write(infile.read())
            
if __name__ == '__main__':

    root_directory = r"/net/zstore1/FIBSEM/Pedro_parker"
    output_folder = r"/net/zstore1/fibsem_data/A53T/Parker"
    srcPath = os.path.join(os.getcwd(),"src")
    target_filename = "0-0-1.dat"
    target_filename_downsampling = "0-0-0.tif"


    grid_size_x=2 
    grid_size_y=2
    tile_overlap = 2 #percentage of overlapping
    regression_threshold=0.30 #default 0.3
    max_avg_displacement_threshold=2.50 #default 2.5
    absolute_displacement_threshold=3.50 #default 3.5
    allFile_paths = find_files_with_name(root_directory, target_filename)    

    # Specify the output folder for processed images
    #python_macro_path = os.path.join(srcPath,"hello.py")
    python_macroStitching_path = os.path.join(srcPath,"stitchROIs.py")
    python_macroDownsampling_path = os.path.join(srcPath,"saveDownsampled_stitchedImages.py")


    # Create a multiprocessing pool to run Fiji in parallel
    num_workers = 30 #cardona-gpu1 cannot with more than ~30 workers
    #TIMEOUT_SECONDS
    print ("--------------------------------------STITCHING----------------------------------------------")

    #input_path = r"/net/zstore1/FIBSEM/Pedro_parker/M06/D18/Merlin-FIBdeSEMAna_23-06-18_000317_0-0-1.dat"
    #run_fiji_python_Stitching_macro(python_macroStitching_path,input_path, output_folder, grid_size_x, grid_size_y, tile_overlap, regression_threshold,max_avg_displacement_threshold,absolute_displacement_threshold)

    with multiprocessing.Pool(processes=num_workers) as pool:
        pool.starmap(run_fiji_python_Stitching_macro,[(python_macroStitching_path, input_path, output_folder, grid_size_x, grid_size_y, tile_overlap, regression_threshold,max_avg_displacement_threshold,absolute_displacement_threshold) for input_path in allFile_paths])
        pool.close()
        pool.join()


    print ("--------------------------------------DOWNSAMPLING----------------------------------------------")
    
#""""""""""""" IF STITCHING IS DONE, COMMENT IT TO CONTINUE WITH THE DOWNSAMPLING TO DOUBLE CHECK WRONG STITCHED IMAGES -------------------------------------
    csvDirectory = r"/net/zstore1/fibsem_data/A53T/Parker/Displacement_csvs/"
    allCsvFiles_path = find_files_with_name(csvDirectory, ".csv")    
    concatenate_files_content(allCsvFiles_path, os.path.join(csvDirectory,"concatenationAllDisplacements.csv")
    #num_workers = 16 
    ## DOWNSAMPLING THE STITCHED .TIFs
    #allFile_pathsDownsampling = find_files_with_name(output_folder + "/StitchedRawImages", target_filename_downsampling)   
    #with multiprocessing.Pool(processes=num_workers) as pool:
    #    pool.starmap(run_fiji_python_Downsampling_macro,[(python_macroDownsampling_path, input_path, output_folder) for input_path in allFile_pathsDownsampling])
    #    pool.close()
    #    pool.join()
 