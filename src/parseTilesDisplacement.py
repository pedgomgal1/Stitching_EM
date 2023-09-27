# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 12:44:31 2023

@author: Pedro Gomez Galvez
"""

def find_largest_displacement(originalTilesTxtPath, stitchedTilesTxtPath):
    def read_coordinates_from_file(file_path):
        coordinates = {}
        try:
            with open(file_path, "r") as file:
                for line in file:
                    parts = [part.strip() for part in line.split(';')]
                    if len(parts) == 3 and parts[2].startswith('(') and parts[2].endswith(')'):
                        tile_name = parts[0]
                        coordinates_str = parts[2][1:-1]  # Remove parentheses
                        x, y = map(float, coordinates_str.split(','))
                        coordinates[tile_name] = (x, y)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        return coordinates

    originalTiles_coordinates = read_coordinates_from_file(originalTilesTxtPath)
    stitchedTiles_coordinates = read_coordinates_from_file(stitchedTilesTxtPath)

    largest_displacement = 0

    for tile_name in originalTiles_coordinates:
        if tile_name in stitchedTiles_coordinates:
            original_x, original_y = originalTiles_coordinates[tile_name]
            stitched_x, stitched_y = stitchedTiles_coordinates[tile_name]

            displacement_x = original_x - stitched_x
            displacement_y = original_y - stitched_y

            displacement = (displacement_x**2 + displacement_y**2) ** 0.5  # Euclidean distance

            if displacement > largest_displacement:
                largest_displacement = displacement
                
            return largest_displacement

