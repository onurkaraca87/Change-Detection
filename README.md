# Change-Detection
@author: Sukru Onur Karaca and Gultekin Erten
This code works for only Landsat8 and Landsat9 !!!



Provides
  1. RGB images, the Line graph of the time series, and the water body as a jpeg
  2. Video of RGB images and Line graphs and also combined video 
  3. Geotiff files for the cut version of RGB and Water Mask
  4. Time series of the lake spatial change Excel file as CSV format

How to use the documentation
----------------------------
 
  
  In the scripts, there is module name "change_detection" which can be used as the below:
      
      cdf.change_detection(raw_path,output,dataset_number, date_range,shp_dir)
      
      raw_path        : it necessary to create raw_path that inculeded raw unzip Landsat 8 and Landsat 9 datasets.
                        Important note: After create direction it necessary yo put "\".
                        For example: "E:\Python_Project\Change_Detection\Bolton\Raw\\Unzip\\"
      
      output          : User has to create "output" file witout "\\" in the end. This file is mandatory cause all 
                        related files will be created inside of "output" files.
                        For example: "E:\Python_Project\Change_Detection\Bolton\Export"
                        For example: "E:\Python_Project\Change_Detection\Bolton\Output
                 
      dataset_number :  It depends how many dataset you want process.
      
      date_range     :  When the scrit run there might be so many dates due to too many dates on the X axes, 
                        it should  reduced the number of date shown.
                        For example: if you have 100 images, date_range remcomend as "5". In this case, X axes illustrate 20 dates.

      shp_dir        :  Desire area has to cut with .shp files.
                        For example: "E:\Python_Project\Change_Detection\Bolton\Roi\Salton_Lake.shp"
                        
     !!! To see how can used this scprit please visit the YouTube Chanel : "........................................"!!!
                        
                        
  For further information  onurkaraca87@gmail.com and gultekinerten@gmail.com
