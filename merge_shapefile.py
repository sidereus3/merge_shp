#! /usr/bin/env python

#######################################
# merge_shapefile.py
# A python script to merge shapefiles
# Author: <Francesco Serafin>
# Email: <francesco.serafin.3@gmail.com>
#######################################

import os
import sys
import pandas
import geopandas


class MergeSHPfiles(object):

    # A function which controls the rest of the script
    def run(self, src, dest):

        print(src)
        print(dest)
        if not os.path.exists(src):
            print("Src path " + src + " does not exist")
        elif not os.path.isdir(src):
            print("Src path is not a directory!")
        else:
            # Merge the shapefiles within the filePath
            self.merge_shpfiles(src, dest)

    # A function to control the merging of shapefiles
    def merge_shpfiles(self, src, dest):
        # Get the list of files within the directory
        # provided with the extension .shp
        shpfiles = self.recursive_find_files(src, '.shp')
        print(len(shpfiles))
        # Iterate through the files.
        gdf = pandas.concat([
            geopandas.read_file(shp)
            for shp in shpfiles
        ]).pipe(geopandas.GeoDataFrame)
        gdf.to_file(dest)

    def recursive_find_files(self, directory, extension):
        fileList = list()
        if os.path.exists(directory):
            if os.path.isdir(directory):
                for x in os.walk("."):
                    tmpDir = x[0]
                    self.look_for_shpfile(tmpDir, fileList, extension)
        for file in fileList:
            print("Checked: " + file)
        return  fileList

    def look_for_shpfile(self, directory, file_list, extension):
        if "spatial" in directory:
            dir_file_list = os.listdir(directory)
            for filename in dir_file_list:
                if "mu_a_" in filename:
                    if self.check_file_extension(filename, extension):
                        file_list.append(os.path.join(directory, filename))

    # A function to test the file extension of a file
    def check_file_extension(self, filename, extension):
        # Boolean variable to be returned by the function
        found_extension = False;
        # Split the filename into two parts (name + ext)
        filename_split = os.path.splitext(filename)
        # Get the file extension into a varaiable
        file_extension = filename_split[1].strip()
        # Decide whether extensions are equal
        if file_extension == extension:
            found_extension = True
        # Return result
        return found_extension


# The start of the code
if __name__ == '__main__':

    args = sys.argv

    try:
        src = args[1]
        dest = args[2]
    except IndexError:
        raise SystemExit(f"Usage: {args[0]} <src folder> <dest file>")

    # Make an instance of the class
    obj = MergeSHPfiles()
    # Call the function run()
    obj.run(src, dest)
