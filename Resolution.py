from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from osgeo import gdal_array

import numpy as np

class Resolution:

  def __init__(self, input_file, output_file,
                     x_res=None, y_res=None,
                     new_x_res=None, new_y_res=None):
    
    self.input_file = input_file
    self.output_file = output_file
    self.x_res = None
    self.y_res = None
    self.new_x_res = new_x_res
    self.new_y_res = new_y_res
   
  def get_resolution(self):
      """Get the spatial resolution (cell size) of a raster dataset.
      Args:
          FileName (str): The filename (with path and extension) of the raster.
      Returns:
          tuple: A tuple containing the X and Y spatial resolutions (cell sizes) in the dataset.
      Author: MYW
      """

      SourceDS = gdal.Open(self.input_file, gdal.GA_ReadOnly)
      if SourceDS is None:
          raise Exception("Unable to read the data file")

      geo_transform = SourceDS.GetGeoTransform()
      self.x_res = geo_transform[1]  # Cell size in the X direction
      self.y_res = -geo_transform[5]  # Cell size in the Y direction (usually negative)

      print(f"X Resolution: {self.x_res} units per pixel")
      print(f"Y Resolution: {self.y_res} units per pixel")

      return (self.x_res,  self.y_res)
  

  def resample_raster(self, new_x_res, new_y_res):
    """Resample a raster dataset to a lower resolution using GDAL.

    Args:
        input_file (str): The filename (with path and extension) of the input raster.
        output_file (str): The filename (with path and extension) of the output resampled raster.
        new_x_resolution (float): The new X resolution (cell size) in the output raster.
        new_y_resolution (float): The new Y resolution (cell size) in the output raster.

    Author: MYW
    """

    # Open the input dataset
    input_ds = gdal.Open(self.input_file, gdal.GA_ReadOnly)
    if input_ds is None:
        raise Exception("Unable to read the input data file")

    # Define resampling options
    resample_options = [
        '-r', 'bilinear',  # Use bilinear interpolation for resampling
        '-tr', str(new_x_res), str(new_y_res)  # Set the new resolution
    ]

    # Perform the resampling
    gdal.Warp(self.output_file, input_ds, options=resample_options)

    # Close the datasets
    input_ds = None

    print("Drone imagery compressed")
