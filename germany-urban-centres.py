
#import necessary packages

import pandas as pd
import numpy as np
import wget
import os
import openpyxl

#import visualization packages
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from pylab import rcParams
#%matplotlib inline

#get the data

#download_url = "https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/Archiv/GVAuszugQ/AuszugGV2QAktuell.xlsx?__blob=publicationFile"
#location = os.getcwd()
#file = wget.download(download_url, location)
file = "#" #add your file path here

workbook = openpyxl.load_workbook(file)
worksheet = workbook["Onlineprodukt_Gemeinden"]

raw_data = pd.DataFrame(worksheet.values)

#data wrangling
wrangled_data = raw_data
wrangled_data = wrangled_data.iloc[6: , :]

# add column names
wrangled_data.columns = ['Satzart', 'Textkennzeichen', 'ARS_Land', 'ARS_RB', 'ARS_Kreis', 'ARS_VB', 'ARS_Gemeinde',
                         'Gemeindename', 'Flaeche_km2', 'Bevoelkerung_insg', 'Bevoelkerung_maennlich', 'Bevoelkerung_weiblich',
                         'Bevoelkerung_je_km2', 'PLZ', 'Laengengrad', 'Breitengrad', 'Reisegebiet_Schluessel',
                         'Reisegebiet_Bezeichnung', 'Verstaedterungsgrad_Schluessel', 'Verstaedterungsgrad_Bezeichnung']

# take only features i am interested in
features = wrangled_data[['ARS_Gemeinde','Gemeindename', 'Bevoelkerung_insg', 'Bevoelkerung_je_km2','Laengengrad', 'Breitengrad']]

#drop any values solely used to make the Excel more organized
features = features.fillna(value=pd.np.nan, inplace=False) #fill all None with NaN
features = features.dropna(subset=['ARS_Gemeinde'], inplace = False) #drop all NaN in ARS_Gemeinde
features = features.reset_index(inplace = False, drop = True) #reset index and drop previous index

#replace commas with dots as the original file is German
features['Breitengrad'] = features['Breitengrad'].str.replace(",", ".").astype(float)
features['Laengengrad'] = features['Laengengrad'].str.replace(",", ".").astype(float)

#low_pop = features[features['Bevoelkerung_insg'] < 1]
#print(low_pop['Gemeindename'].head(50))
#print(low_pop['Bevoelkerung_insg'].head(50))

#set diagram parameters
rcParams['figure.figsize'] = (14,10)
llon=-140
ulon=-50
llat=40
ulat=65

my_map = Basemap(projection='merc',
            resolution = 'l', area_thresh = 1000.0,
            llcrnrlon=llon, llcrnrlat=llat, #min longitude (llcrnrlon) and latitude (llcrnrlat)
            urcrnrlon=ulon, urcrnrlat=ulat) #max longitude (urcrnrlon) and latitude (urcrnrlat)

my_map.drawcoastlines()
my_map.drawcountries()
