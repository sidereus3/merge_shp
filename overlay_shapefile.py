import geopandas as gpd
import os
import sys
import threading

class Preproc():

    def recursive_find_files(self, directory, extension):
        file_list = list()
        if os.path.exists(directory):
            if os.path.isdir(directory):
                for x in os.walk(directory):
                    tmp_dir = x[0]
                    self.look_for_shpfile(tmp_dir, file_list, extension)
        return file_list

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
        found_extension = False
        # Split the filename into two parts (name + ext)
        filename_split = os.path.splitext(filename)
        # Get the file extension into a variable
        file_extension = filename_split[1].strip()
        # Decide whether extensions are equal
        if file_extension == extension:
            found_extension = True
        # Return result
        return found_extension

class ClientThread(threading.Thread):

    def __init__(self, id, cult, shapefileList):
        threading.Thread.__init__(self)
        self.id = id
        self.cult = cult
        self.shapefileList = shapefileList

    def run(self):

        lock.acquire()
        ssa = self.get_shapefile()
        cultivated = gpd.read_file(self.cult)
        lock.release()

        while ssa is not None:

            dir = os.path.split(os.path.abspath(ssa))
            dir = os.path.split(os.path.abspath(dir[0]))
            savepath = dir[0]

            iassa = gpd.read_file(ssa)

            print(ssa)
            over = gpd.overlay(iassa, cultivated, how="intersection")
            centr = over.representative_point()

            oversavepath = os.path.join(savepath, "over")
            centrsavepath = os.path.join(savepath, "centr")
            os.mkdir(oversavepath)
            os.mkdir(centrsavepath)

            over.to_file(os.path.join(oversavepath, "over.shp"))
            centr.to_file(os.path.join(centrsavepath, "centr.shp"))

            lock.acquire()
            ssa = self.get_shapefile()
            lock.release()

    def get_shapefile(self):
        if not self.shapefileList:
            return None
        else:
            return self.shapefileList.pop(0)


if __name__ == "__main__":

    args = sys.argv

    try:
        mapunits = args[1]
        cultiv = args[2]
    except IndexError:
        raise SystemExit(f"Usage: {args[0]} <mapunits path> <cultivated US map>")

    pp = Preproc()
    shapefileList = pp.recursive_find_files(mapunits, '.shp')

    count = 8
    lock = threading.Lock()
    threads = [ClientThread(i, cultiv, shapefileList) for i in range(count)]

    for i in range(count):
        threads[i].start()

    for i in range(count):
        threads[i].join()
