## JEDHA PROJECT INFORMATION. TEAM

## Protective Forests

*Final link to dashboard and presentation coming soon*

Analysis of the state of protective forests in Switzerland and main factors of growth<br>

Datasets:<br>
Climate and Protective Forests' evolution since 1982, provided by the Swiss <a href="https://www.lfi.ch/">National Forest Inventory</a><br>
Meteorological data in Switzerland (Daymet 100/100m), Satellite (Landsat, Sentinel) data.<br>
Sat ref : <a href="https://eo4geocourses.github.io/IGIK_Sentinel2-Data-and-Vegetation-Indices/#/23">eo4geocourses on stl2 data</a><br>

Deliverables :
- Presentation of the data, workflow and results
- Maps featuring rate of growth (or withering) and protective effect of forests, in relation to climate
- Dashboard with plots and results

Main contributors :
- Satellite data : <a href="https://github.com/Jesshuan">Jesshuan</a>
- Meteorological data : Myself
- Dashboard : Marjory
- Scientific expertise : Estelle
- EDA & modeling : All project members

#### Navigate through the folders and files 
**Folders**<br>
*NFI_data*:
- Source data from the Swiss National Forest Inventory. Variable names & description in German
- Concatenation & initial EDA notebooks
- Modified files from concatenation and translation of variables and description in French

*meteo_data*:
- Excel file containing precipitations (in cm/square km) and temperature averages (in °C) for each forest plot
- Example plots and maps for each collection campaign<br>
Does NOT contain actual full meteorological files in netcdf (30 GB)

*docs*:<br>
Useful documentation on Silva Protect Swiss framework and conversion from Swiss to WGS84 coordinates

**Docker*:
- Dockerfile to easily run Earth Engine (SAT notebooks in this repository) on Windows<br>
Add a requirements.txt with the following values (1 line each): earthengine-api numpy matplotlib pandas plotly requests datetime openpyxl

**Files**<br>
*meteo_1, meteo_2, meteo_3.ipynb*:
1. Understanding netcdf, what is in the files and how to access it
2. Defining functions to extract data and plotting maps for given time and intervals
3. Trends in temperature and precipitations through the years

*to_import_func_meteo.py*:<br>
To import predefined meteorological functions (provided you have the netcdf files) 

*eda.ipynb*:<br>
Understanding data from NFI collection campaigns, preparing the presentation and graphs

*modeling.ipynb*:<br>
- Modeling to describe the current state of protective forests and determine useful features and targets
- Attempt to predict the future state of protective forests

*SAT_img_to_array_LANDSAT-5, SAT_aggreg.ipynb*:
- Collect satellite imagery for NFI campaigns (results in 8 to 10 GB files for each)
- Aggregate results into a csv file with NDVI,EVI,NDMI,NDWI,DSWI formulas

*coords_swiss_to_geo.ipynb*:<br>
Convert coordinates from Swiss LV95 to WGS84


Libraries used :
Pandas, Numpy, Openpyxl, Json, Xarray, netCDF4, Earth Engine, Matplotlib, Plotly, Scikit-learn, Streamlit<br>
Storage and Cloud Computing : Google Cloud Platform

Additional documentation : <a href="https://www.researchgate.net/profile/Urs-Beat-Braendli/publication/342143876_Inventaire_forestier_national_suisse_Resultats_du_quatrieme_inventaire_2009_-_2017/links/5ee43ba0299bf1faac52615a/Inventaire-forestier-national-suisse-Resultats-du-quatrieme-inventaire-2009-2017.pdf">4th inventory results 2009-2017</a>