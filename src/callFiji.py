# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 16:56:38 2023

@author: Pedro Gomez Galvez
"""

import subprocess
import os
import signal

# Define a function to run Fiji in headless mode with the specified Python macro and input folder
def run_fiji_python_Stitching_macro(python_macro_path,input_path, output_folder,grid_size_x,grid_size_y,tile_overlap, regression_threshold,max_avg_displacement_threshold,absolute_displacement_threshold):
    # Construct the command to run Fiji in headless mode with the Python macro
    inputInstruction = 'input_path="'+input_path+'", output_folder="'+output_folder+'", grid_size_x="'+str(grid_size_x)+'", grid_size_y="'+str(grid_size_y)+'", tile_overlap="'+str(tile_overlap)+'", regression_threshold="'+str(regression_threshold)+'", max_avg_displacement_threshold="'+str(max_avg_displacement_threshold)+'", absolute_displacement_threshold="'+str(absolute_displacement_threshold)+'"'
    print(inputInstruction)
    command = [
        r'/lmb/home/pgg/Fiji.app/ImageJ-linux64',  # Adjust the path to your Fiji installation
        '--ij2',
        '--headless',  # Run in headless mode
        #'--console',
        '--run', python_macro_path,  # Path to your Python macro
        inputInstruction # Pass inputs as a parameters
    ]

    # Run Fiji with the specified command
    fileName = os.path.basename(input_path)
    print("Stitching:", fileName[:-10])
    try:
        if not os.path.exists(output_folder + "/StitchedRawImages/" + fileName[:-5]+ "0.tif"):
                 subprocess.run(command,stderr=subprocess.PIPE, stdout=subprocess.PIPE); #os.killpg(os.getpid(subp.pid),signal.SIGTERM)

    except subprocess.CalledProcessError as e:
        print("Error running the subprocess:")
        print("Return code:", e.returncode)
        print("Error output:", e.stderr)

def run_fiji_python_Downsampling_macro(python_macro_path,input_path, output_folder):
    # Construct the command to run Fiji in headless mode with the Python macro
    inputInstruction = 'input_path="'+input_path+'", output_folder="'+output_folder+'"'
    #print(inputInstruction)
    command = [
        r'/lmb/home/pgg/Fiji.app/ImageJ-linux64',  # Adjust the path to your Fiji installation
        '--ij2',
        '--headless',  # Run in headless mode
        #'--console',
        '--run', python_macro_path,  # Path to your Python macro
        inputInstruction # Pass inputs as a parameters
    ]

    # Run Fiji with the specified command
    fileName = os.path.basename(input_path)
    print("Downsampling:", fileName)

    if os.path.exists(input_path): subprocess.run(command,stderr=subprocess.PIPE, stdout=subprocess.PIPE); #os.killpg(os.getpid(subp.pid),signal.SIGTERM)
