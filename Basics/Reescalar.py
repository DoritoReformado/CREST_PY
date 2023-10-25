import arcpy

def reescalar(tif_file, output_file, cellsize, OPTION = None):
    
    if OPTION == None:
        OPTION = 'NEAREST'

    output_file = tif_file[:-4]+'_R.tif'

    arcpy.management.Resample(tif_file, 
                              output_file, 
                              "{} {}".format(cellsize, cellsize), 
                              OPTION)
    
    return output_file
