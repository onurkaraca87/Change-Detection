
"""


@author: Sukru Onur Karaca and Gultekin Erten



-----------------------------------------Descripton-----------------------------------------
-----------------------------------------Descripton-----------------------------------------
-----------------------------------------Descripton-----------------------------------------

This codes works for only Landsat8 and Landsat9 !!!



Provides
  1. RGB images, Line graph of time series and water body as jpeg
  2. Video of RGB images and Line graphs and also combined video 
  3. Geotiff files for cut version of RGB and Water Mask
  4. Time series of the lake spatial change excel file as csv format

How to use the documentation
----------------------------

The docstring examples assume that "change_detection" has been imported as `cdf`:


  >>> import change_detection as cdf
  
  
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
                        
                        
  For further information gultekinerten@gmal.com and onurkaraca87@gmail.com
  
 
"""
from tkinter import *
import tkinter as tk
import matplotlib.pyplot as plt
import osgeo._gdal
import osgeo
from osgeo import gdal
import os
from PIL import Image
import numpy as np
import cv2
import glob
from moviepy.editor import VideoFileClip, clips_array
import csv

def change_detection(raw_path,output,dataset_number, date_range,shp_dir):


    
    #file create
    
    os.mkdir(output + "\\Cut" )
    os.mkdir(output + "\\Stack_RGB_jpeg" )
    os.mkdir(output + "\\Water_body_jpeg" )
    os.mkdir(output + "\\Water_body_geotiff")
    os.mkdir(output +"\\Stack_geotiff")
    os.mkdir(output +"\\Excel")
    os.mkdir(output +"\\Line_Graph_jpeg")
    os.mkdir(output +"\\Video")



    #İlk olarak dosya directiry buluyoruz. Sonra içinde 5 olan dosyalar var ----------------------------------------------------------------------------------------
    
    #dosyanın yeri (string)
    raw_path_5=os.listdir(raw_path)
    #dosyanın içindeki 5 ayrı dosya
    #output_path=("E:\Python_Project\Change_Detection\Deneme_1\Output//NDWI//")
    
    liste_area=[]   #AŞAĞIDA NDWI URETİLEN SULAK ALANI BU LİSTEYE EKLİYECEZ
    for n in range(dataset_number):
        one_file=raw_path_5[n]
        one_file_inside=os.listdir(raw_path+one_file)
        #bandların oldugu klasörü açıyoruz!!!----------------------------------------------------------------------------------------
        
        bandlar=[] #hangi bandı açmak istedğimiz için liste yaptık----------------------------------------------------------------------------------------
        for p in range(4):
            bands=one_file_inside[p+7]
            band=raw_path+one_file+ "/" + bands
            # ustekı tek bir bandı acıyor----------------------------------------------------------------------------------------
            bandlar.append(band)
            
        ds_liste=[]  
        os.mkdir(output + "\\Cut\\" + one_file)
        # os.mkdir("E:\\Python_Project\\Change_Detection\\Deneme_1\\Output\GDAL\\Jpeg\\water_body\\")----------------------------------------------------------------------------------------
        for z in range(4):
            ds = gdal.Open(bandlar[z]) # band2
            bantlar=bandlar[z]
            
            OutTile = gdal.Warp(output + "\\Cut\\" + one_file+ "\\" +bantlar[108:154]+"_cut.tif", 
                        ds,     #-"/home/zeito/pyqgis_data/utah_demUTM12.tif"    bu normalde noyledı ama bızım ds dosyası tiiff dosyyası
                        cutlineDSName=shp_dir,
                        cropToCutline=True,
                        dstNodata = 0)
            # OutTile.GetMetadata()
            band_image=OutTile.GetRasterBand(1).ReadAsArray() 
            ds_liste.append(band_image)
            gt = OutTile.GetGeoTransform()
            proj= OutTile.GetProjection()
            OutTile = None 
    
           
        ndwi=(ds_liste[1].astype(float)-ds_liste[3].astype(float))/(ds_liste[1].astype(float)+ds_liste[3].astype(float))
        water_body=np.where(ndwi > 0, 1, np.nan) # ndwi 0 dan buyuk değerleri 1 yap geri kalanı nan yap(1 değer su)
        plt.imshow(water_body)
        plt.show()
        # zeros = np.sum(water_body == 0)*0.0009 #km2 bosluk
        ones = np.sum(water_body == 1)*0.0009  #km2 water body
        liste_area.append(int(ones))
        
        
    
        
        # Burada sadace görüntüyü rgb olarak matplotlibte açıyoruz----------------------------------------------------------------------------------------
        # Burada sadace görüntüyü rgb olarak matplotlibte açıyoruz----------------------------------------------------------------------------------------
        b=ds_liste[0]/65536   #2 üzeri 16 dan 65536 sayısı gelir
        g=ds_liste[1]/65536
        r=ds_liste[2]/65536
        rgb_uint8 = (np.dstack((r,g,b)) * 255.999) .astype(np.uint8)
    
        # Burada sadace görüntüyü rgb olarak matplotlibte açıyoruz----------------------------------------------------------------------------------------
        # Burada sadace görüntüyü rgb olarak matplotlibte açıyoruz----------------------------------------------------------------------------------------
    
       
        # Burada sadace görüntüyü rgb olarak histogram eşitleme yapıyoruz ve RGB olarak jpeg olarak kayıt ediyoruz----------------------------------------------------------------------------------------
        # Burada sadace görüntüyü rgb olarak histogram eşitleme yapıyoruz RGB olarak jpeg olarak kayıt ediyoruz----------------------------------------------------------------------------------------
        assert rgb_uint8 is not None, "file could not be read, check with os.path.exists()"
        hist,bins = np.histogram(rgb_uint8.flatten(),256,[0,256])
        cdf = hist.cumsum()
        cdf_normalized = cdf * float(hist.max()) / cdf.max()
        plt.plot(cdf_normalized, color = 'b')
        plt.hist(rgb_uint8.flatten(),256,[0,256], color = 'r')
        plt.xlim([0,256])
        plt.legend(('cdf','histogram'), loc = 'upper left')
        plt.show()    
        
        cdf_m = np.ma.masked_equal(cdf,0)
        cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
        cdf = np.ma.filled(cdf_m,0).astype('uint8')
        img2 = cdf[rgb_uint8]
        
        font                   = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (10,150)
        fontScale              = 2
        fontColor              = (255,0,0)
        thickness              = 2
        lineType               = 2
        
        cv2.putText(img2,"DATES: " + bantlar[111:119], 
            bottomLeftCornerOfText, 
            font, 
            fontScale,
            fontColor,
            thickness,
            lineType)
            
        plt.imshow(img2)
        plt.show()
        img4 = Image.fromarray(img2, "RGB")
        img4.save(output + "\\Stack_RGB_jpeg\\" + one_file + "_rgb_image_strecth.jpeg", dpi=(100,100))
        # Burada sadace görüntüyü rgb olarak histogram eşitleme yapıyoruz RGB olarak jpeg olarak kayıt ediyoruz----------------------------------------------------------------------------------------
        # Burada sadace görüntüyü rgb olarak histogram eşitleme yapıyoruz RGB olarak jpeg olarak kayıt ediyoruz----------------------------------------------------------------------------------------
    
    
        # Burada sadace WATER BODY jpeg olarak kayıt ediyoruz----------------------------------------------------------------------------------------   
        # Burada sadace WATER BODY jpeg olarak kayıt ediyoruz----------------------------------------------------------------------------------------
        water_body_jpeg=np.where(ndwi > 0, 256, np.nan)
        cv2.imwrite(output + "\\Water_body_jpeg\\" + one_file + "_water_body_image.png", water_body_jpeg)
        # Burada sadace WATER BODY jpeg olarak kayıt ediyoruz ----------------------------------------------------------------------------------------
        # Burada sadace WATER BODY jpeg olarak kayıt ediyoruz----------------------------------------------------------------------------------------
    
        # Output dosyasını WATER BODY İÇİN  GEITIF OALARAK burda yazdırıyoruz!!!----------------------------------------------------------------------------------------
        # Output dosyasını WATER BODY İÇİN  GEITIF OALARAK burda yazdırıyoruz!!!----------------------------------------------------------------------------------------
        [rows, cols] = water_body.shape
        driver = gdal.GetDriverByName("GTiff")
        outdata = driver.Create(output + "\\Water_body_geotiff\\" + one_file + "_ stack_water_body_geotiff.tif", cols, rows, 1, gdal.GDT_UInt16)
        outdata.SetGeoTransform(gt)
        outdata.SetProjection(proj)
        outdata.GetRasterBand(1).WriteArray(water_body)
        outdata.GetRasterBand(1).SetNoDataValue(10000)
        outdata.FlushCache()   
        outdata = None
        # Output dosyasını WATER BODY İÇİN  GEITIF OALARAK burda yazdırıyoruz!!!----------------------------------------------------------------------------------------
        # Output dosyasını WATER BODY İÇİN  GEITIF OALARAK burda yazdırıyoruz!!!----------------------------------------------------------------------------------------
    
             
    
        # Burada sadace görüntüyü RGB olarak jpeg olarak kayıt ediyoruz ----------------------------------------------------------------------------------------
        # Burada sadace görüntüyü RGB olarak jpeg olarak kayıt ediyoruz ----------------------------------------------------------------------------------------
        # img = Image.fromarray(rgb_uint8, "RGB")
        # img.save("E:\\Python_Project\\Change_Detection\\Burdur_Lake\\Output\GDAL\\Stack_RGB_jpeg\\" + one_file + "_rgb_image.jpeg")
        # Burada sadace görüntüyü RGB olarak jpeg olarak kayıt ediyoruz
        # Burada sadace görüntüyü RGB olarak jpeg olarak kayıt ediyoruz ----------------------------------------------------------------------------------------
    
    
        # Output dosyasını stack İÇİN  burda yazdırıyoruz!!!----------------------------------------------------------------------------------------          
        # Output dosyasını stack İÇİN  burda yazdırıyoruz!!!----------------------------------------------------------------------------------------
        [rows, cols] = water_body.shape
        driver = gdal.GetDriverByName("GTiff")
        outdata = driver.Create(output +"\\Stack_geotiff\\" + one_file + "_ stack_RGB_geotiff.tif", cols, rows, 3, gdal.GDT_UInt16)
        outdata.SetGeoTransform(gt)
        outdata.SetProjection(proj)
        outdata.GetRasterBand(1).WriteArray(ds_liste[0])
        outdata.GetRasterBand(1).SetNoDataValue(10000)
        outdata.GetRasterBand(2).WriteArray(ds_liste[1])
        outdata.GetRasterBand(2).SetNoDataValue(10000)
        outdata.GetRasterBand(3).WriteArray(ds_liste[2])
        outdata.GetRasterBand(3).SetNoDataValue(10000)
        outdata.FlushCache()   
        outdata = None
        # Output dosyasını stack İÇİN  burda yazdırıyoruz!!!----------------------------------------------------------------------------------------
        # Output dosyasını stack İÇİN  burda yazdırıyoruz!!!----------------------------------------------------------------------------------------
    
    
    
    
    
    #-------------------------------------------CVS SAVE------------------------------------------------------------------------
    #-------------------------------------------CVS SAVE------------------------------------------------------------------------
    #tarihleri almak için yapıyoruz
    liste_tarih=[]
    tarihx=[]
    for h in range(dataset_number):
        input_veri2=raw_path_5[h]
        tarih=int(input_veri2[17:25])
        liste_tarih.append(tarih)
        tarihx.append(str(liste_tarih[h]))
    tarihx.append("")
    tarihx.append("")    
    
    arr=np.full((len(liste_area)+2),np.nan)
    list_1 = arr.tolist()
    list_1[len(liste_area)+1]=1
    
    for ok in range(dataset_number):
        list_1[ok]=liste_area[ok]
        plt.ylim(min(liste_area)-20,max(liste_area)+20)
        label="Area" + "\n" + str(liste_area[ok])+" km2"
        plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')
        plt.plot(tarihx, list_1, color=(float(48/255), float(214/255), float(200/255)), label=label, marker='o', linewidth=3, markersize=6)
        plt.xlabel("Dates", fontweight='bold', color=(float(229/255), float(204/255), float(255/255)))
        plt.ylabel("Surface Area of the Lake (Km2)", fontweight='bold', color=(float(229/255), float(204/255), float(255/255)))
        plt.xticks(tarihx[::date_range], rotation = 45, color=(float(255/255), float(255/255), float(204/255)), fontweight='bold')
        plt.yticks(color=(float(255/255), float(255/255), float(204/255)), fontweight='bold')
        plt.title("Spatial Change in the Lake", fontweight='bold', color=(float(204/255), float(255/255), float(204/255)))
        plt.legend(loc="upper left")
        # plt.text(2.5, 174, "Dates: " + bantlar[120:128], fontsize = 12, c="red" )
        plt.savefig(output +"\\Line_Graph_jpeg\\"  + str(ok) + ".jpeg", bbox_inches='tight', dpi=300)
        plt.show()
    
    
    
    
    # csv create yaptık
    a=0
    with open(output +"\\Excel\\statistics3.csv", 'w', newline="") as csv_file:
        fieldnames = ['Dates', 'Area']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for alan in liste_area:
            writer.writerow({'Dates':liste_tarih[a], 'Area': alan})
            a=a+1
    #-------------------------------------------CVS SAVE------------------------------------------------------------------------
    #-------------------------------------------CVS SAVE------------------------------------------------------------------------
    
    
    
    
    #-------------------------------------------STEP BY STEP MAKE GRAPH------------------------------------------------------------------------
    #-------------------------------------------STEP BY STEP MAKE GRAPH------------------------------------------------------------------------
    
    # Biz beş elemanı bir liste kullandık ama tek tek çizdirmesi için +2 değer verdik son değer bir sayı
    # sondan önceki değer ise NAN oldu
    
    
    #-------------------------------------------STEP BY STEP MAKE GRAPH------------------------------------------------------------------------
    #-------------------------------------------STEP BY STEP MAKE GRAPH------------------------------------------------------------------------
    
     
    
    
        # ---------------------------------------------------------------------VİDEOOOOOOOOO GRAPHS---------------------------------------------------------------------
        # ---------------------------------------------------------------------VİDEOOOOOOOOO GRAPS--------------------------------------------------------------------
    img_array = []
    for filename in range(dataset_number):
        img = cv2.imread(output +"\\Line_Graph_jpeg\\" + str(filename) + ".jpeg")
        # height, width, layers = img.shape
        # size = (height,width)
        img_array.append(img)
    
    out = cv2.VideoWriter(output +"\\Video\\Line_Graphs.avi",cv2.VideoWriter_fourcc(*'DIVX'), 2, (img.shape[1],img.shape[0]))
    
    for i in range(len(img_array)):
        out.write(img_array[i])
    
    out.release()
        # ---------------------------------------------------------------------VİDEOOOOOOOOO water_body---------------------------------------------------------------------
        # ---------------------------------------------------------------------VİDEOOOOOOOOO water_body---------------------------------------------------------------------
    
    
    #     # ---------------------------------------------------------------------VİDEOOOOOOOOO RGB---------------------------------------------------------------------
    #     # ---------------------------------------------------------------------VİDEOOOOOOOOO RGB---------------------------------------------------------------------
    img_array_RGB = []
    for filename_RGB in glob.glob(output + "\\Stack_RGB_jpeg\\*.jpeg"):
        img_RGB = cv2.imread(filename_RGB)
        # height, width, layers = img_RGB.shape
        # size = (height, width)
        # img_RGB=cv2.resize(img_RGB,(3967,3707))
        img_array_RGB.append(img_RGB)
        
    out_RGB = cv2.VideoWriter(output +"\\Video\\video_RGB.avi",cv2.VideoWriter_fourcc(*'DIVX'), 2.0, (img_RGB.shape[1],img_RGB.shape[0]))
    
    for k in range(len(img_array_RGB)):
        out_RGB.write(img_array_RGB[k])
    
    out_RGB.release()
    #     # ---------------------------------------------------------------------VİDEOOOOOOOOO RGB---------------------------------------------------------------------
    #     # ---------------------------------------------------------------------VİDEOOOOOOOOO RGB---------------------------------------------------------------------
    
    
    
    #     # ---------------------------------------------------------------------VİDEOOOOOOOOO SIDE BY SIDE---------------------------------------------------------------------
    #     # ---------------------------------------------------------------------VİDEOOOOOOOOO SIDE BY SIDE---------------------------------------------------------------------
    # video loading
    Video1 = VideoFileClip(output +"\\Video\\Video_RGB.avi")
    Video2 =  VideoFileClip(output +"\\Video\\Line_Graphs.avi")
    #concatenate videos
    final_clip=clips_array([[Video1, Video2]])
    #write and save merged videp
    final_clip.write_videofile(output +"\\Video\\RGB_and_Line_Graphs.mp4")    # ---------------------------------------------------------------------VİDEOOOOOOOOO SIDE BY SIDE---------------------------------------------------------------------
        # ---------------------------------------------------------------------VİDEOOOOOOOOO SIDE BY SIDE---------------------------------------------------------------------


#-------------------------------------------------ARAYUZ - INTERFACE---------------------------------------------------------------
pencere=tk.Tk()
pencere.title("CHANGE DETECTION FOR LANDSAT-8 AND LANDSAT-9")
pencere.geometry("1000x500")
canvas= Canvas(pencere, width= 600, height= 100, bg="SpringGreen2")
canvas.create_text(300, 50, text="Change Detection for Landsat-8 and Landsat-9" +"\n"+"Sukru Onur Karaca & Gultekin Erten", justify='center',fill="Red", font=('Helvetica 15 bold'))
pencere.configure(background='white')

canvas.pack()
#-------------------------------------------------ARAYUZ - INTERFACE FOR DEFINITION---------------------------------------------------------------

def giris():
    #entry den bilgileri alma
    global input_verisi
    input_verisi=giris_verisi.get()
    
def output():
    global output_verisi
    output_verisi=output_path.get()
    
def file_num():   
    global ana_dosya
    ana_dosya=int(main_folder.get())
    
    
def shp_file():   
    global shp_dir
    shp_dir=shp_folder.get()
        
    
def data_gap():   
    global pixel_choose_number
    pixel_choose_number=int(secli_pixel.get())

    
def Close():
    pencere.destroy()
#-------------------------------------------------ARAYUZ - INTERFACE FOR DEFINITION---------------------------------------------------------------
#-------------------------------------------------ARAYUZ - INTERFACE FOR DEFINITION---------------------------------------------------------------
#-------------------------------------------------ARAYUZ - INTERFACE FOR DEFINITION---------------------------------------------------------------
    


#-------------------------------------------------ARAYUZ - INTERFACE LABES---------------------------------------------------------------
#-------------------------------------------------ARAYUZ - INTERFACE LABES---------------------------------------------------------------
#-------------------------------------------------ARAYUZ - INTERFACE LABES---------------------------------------------------------------
    


e1=tk.Label(text="Input Dataset",font="Verdana 18")
e1.pack()
giris_verisi=tk.Entry(width=150,)
giris_verisi.insert(0, "E:\Python_Project\Change_Detection\Bolton\Raw\\Unzip//")
giris_verisi.pack()


e2=tk.Label(text="Output Files",font="Verdana 18")
e2.pack()
output_path=tk.Entry(width=150)
output_path.insert(0, "E:\Python_Project\Change_Detection\Bolton\Output")
output_path.pack()


e3=tk.Label(text="File Numbers",font="Verdana 18")
e3.pack()
main_folder=tk.Entry(width=150)
main_folder.insert(0, "3")
main_folder.pack()


e4=tk.Label(text="shp file location with extension",font="Verdana 18")
e4.pack()
shp_folder=tk.Entry(width=150)
shp_folder.insert(0, "E:\Python_Project\Change_Detection\Bolton\Roi\Salton_Lake.shp")
shp_folder.pack()


e5=tk.Label(text="Range Gap for Dates",font="Verdana 18")
e5.pack()
secli_pixel=tk.Entry(width=150)
secli_pixel.insert(0, "1")
secli_pixel.pack()
b5=tk.Button(text="Onay", command=lambda: [giris(),output(),file_num(), data_gap(), shp_file(), Close()])
b5.pack()
   



pencere.mainloop()    
#-------------------------------------------------ARAYUZ - INTERFACE---------------------------------------------------------------
#-------------------------------------------------ARAYUZ - INTERFACE---------------------------------------------------------------
#-------------------------------------------------ARAYUZ - INTERFACE---------------------------------------------------------------

change_detection(input_verisi, output_verisi, ana_dosya, pixel_choose_number, shp_dir)