import pandas as pd
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import calendar

## Required packages to run all functions : 
# pandas as pd : get excel file, datetime
# netCDF4 : read meteorological data
# numpy as np : numbers, arrays
# matplotlib.pyplot as plt : plot maps
# calendar : string date from number


## To use with netcdf files from Daymet-CH. Some functions will break if used on a "small" (less than a few years) dataset
# Reading such files: "data = nc.Dataset('D:/DaymetCH/ch_prcp_1930-2018_m_ch1903.nc4')"
# You should then explore contents with "data.variables","data.__dict__","data.shape" ; 
# Then dive into dimensions with "data['time']","data['prcp'] before accessing specific values such as in "data.variables['prcp'][1020].compressed().max()" (max precipitation in Switzerland for January 2015)
# Data loaded with the Xarray library instead of netCDF4 should in theory work but in this case I would encourage you to build your own functions, as this may not prove reliable.


def get_coordinates(period=str,file=str):
    """Get coordinates of plots from and to a dataframe.
    Takes inputs : period (LFI), file with plots and swiss coordinates
    pandas package imported as pd"""
    data = pd.read_excel(file,sheet_name=period) 
    x = data['X']/1000 +600 # coordinates accessed in this way are not centered at x/y=6000/2000 on Bern as they should be, but x/y=1200/1260. The array starts at 4800/740.
    y = data['Y']/1000 +1060  
    month = data['DATUMF'].dt.month
    year = data['DATUMF'].dt.year
    new_year = (year-1929)*12
    new_date = new_year - 12 + month - 1 #index in python starts at 0
    df = new_date,x,y
    return pd.DataFrame(df).astype(int)

# example : dataplot = get_coordinates('LFI3','NFI_data/PLOTDATEN.xlsx')

def selected_time(time,file):
    """Returns time for selected element of the dataset.
    Takes inputs : time in coord_df (from func get_coordinates) or int between 0-1067, netcdf file
    netCDF4 package imported as nc"""
    d_time = file.variables['time'][time]
    time_unit = file.variables["time"].getncattr('units')
    time_cal = file.variables["time"].getncattr('calendar')
    local_time = nc.num2date(d_time, units=time_unit, calendar=time_cal) 
    return "Selected time : %s" % (local_time)

# example : selected_time(dataplot[0][0],prcp1930)

def get_prcp_plot(line,data,file,coord_df):
    """Returns current and historical precipitation since previous collection campaign
    Takes inputs : index of plot in coord_df, sheet of previous campaign, prcp netcdf file, coord_df (from func get_coordinates)"""
    file.set_auto_maskandscale(False)   
    month = data['DATUMF'].dt.month
    year = data['DATUMF'].dt.year
    old_year = (year-1929)*12
    old_date = old_year - 12 + month - 1
    date = coord_df[line][0]
    x = coord_df[line][1]
    y = coord_df[line][2]
    current = file['prcp'][date,y,x]
    old_to_current = file['prcp'][old_date[line]:date,x,y]
    return round(sum(old_to_current),4),current

# example : get_prcp_plot(620,previous,dataplot)

def get_tave_plot(line,data,file,coord_df):
    """Returns current and historical temperature average since previous collection campaign
    Takes inputs : index of plot in coord_df, sheet of previous campaign, tave netcdf file, coord_df (from func get_coordinates)
    numpy package imported as np"""
    file.set_auto_maskandscale(False)     
    month = data['DATUMF'].dt.month
    year = data['DATUMF'].dt.year
    old_year = (year-1929)*12
    old_date = old_year - 12 + month - 1
    date = coord_df[line][0]
    y = coord_df[line][1]
    x = coord_df[line][2]
    current = file['tave'][date,y,x]
    old_to_current = file['tave'][old_date[line]:date,x,y]
    return round(np.mean(old_to_current),4),current

#example : get_tave_plot(620,previous,dataplot)

def select_weather_growth_months(line,data,file,kind,coord_df):
    """Returns precipitation or temperature average since previous collection campaign, only for months of growth (april to september)
    Takes inputs : index of plot in coord_df, sheet of previous campaign, netcdf file, kind ('tave' or 'prcp'), coord_df (from func get_coordinates)
    numpy package imported as np"""
    file.set_auto_maskandscale(False)   
    month = data['DATUMF'].dt.month
    year = data['DATUMF'].dt.year
    old_year = (year-1929)*12
    old_date = old_year - 12 + month - 1
    date = coord_df[line][0]
    x = coord_df[line][1]
    y = coord_df[line][2]
    interval_y = int(((date - old_year)/12)[0])
    interval_1 = []
    interval_2 = []
    prcp_result = []
    tave_result = []
    for i in range(interval_y):
        interval_1.append(old_year[line]+(12*i+3))
        interval_2.append(old_year[line]+(12*i+8))
        prcp_result.append(np.sum(file[kind][interval_1[i]:interval_2[i],x,y]))
        tave_result.append(np.mean(file[kind][interval_1[i]:interval_2[i],x,y]))
    if kind == 'prcp':
        return sum(prcp_result)
    elif kind == 'tave':
        return np.mean(tave_result)
    
# example : select_weather_growth_months(0,previous,prcp1930,'prcp',dataplot)


def plot_image(time,file,kind):
    """Plots map of precipitation or temperature average in Switzerland
    Takes inputs : time (in coord_df from func get_coordinates or int between 0-1067), netcdf file, kind ('tave' or 'prcp'), 
    matplotlib.pyplot package imported as plt"""
    if kind == 'prcp':
        palette = 'viridis'
        label = 'Precipitations in cm'
    elif kind == 'tave':
        palette = 'magma'
        label = 'Temperature average in C°'
    d_time = file.variables['time'][time]
    time_unit = file.variables["time"].getncattr('units')
    month = nc.num2date(d_time,units=time_unit).month
    year = nc.num2date(d_time,units=time_unit).year
    plt.figure(figsize=(12,12))
    plt.axis('off')
    plt.imshow(file[kind][time],origin='lower',cmap=palette)
    #plt.gcf().set_facecolor("white")
    plt.colorbar(orientation='horizontal',fraction=0.025,label=label) 
    plt.title(f"{label} for month {month} of year {year}")
    plt.show()

# example : plot_image(dataplot[0][0],prcp1930,'prcp')

def plot_image_interval(meteo_start,meteo_end,file,kind):
    """Plots map of precipitation or temperature average in Switzerland between defined interval
    Takes inputs : start time (in coord_df from func get_coordinates or int between 0-1067), end time, netcdf file, kind ('tave' or 'prcp'), 
    matplotlib.pyplot package imported as plt"""
    if kind == 'prcp':
        palette = 'viridis'
        label = 'Precipitations (in cm)'
    elif kind == 'tave':
        palette = 'magma'
        label = 'Average Surface Air Temperature (in C°)'
    d_time_s = file.variables['time'][meteo_start]
    time_unit = file.variables["time"].getncattr('units')
    month_start = nc.num2date(d_time_s,units=time_unit).month
    year_start = nc.num2date(d_time_s,units=time_unit).year
    d_time_e = file.variables['time'][meteo_end]
    month_end = nc.num2date(d_time_e,units=time_unit).month
    year_end = nc.num2date(d_time_e,units=time_unit).year
    meteo = file[kind][meteo_start]
    for i in range(meteo_start+1,meteo_end+1):
        meteo += file[kind][i]
    if kind == 'tave':
        meteo /= (meteo_end-meteo_start)
    plt.figure(figsize=(12,12))
    plt.axis('off')
    plt.imshow(meteo,origin='lower',cmap=palette)
    plt.gcf().set_facecolor("white")
    plt.colorbar(orientation='horizontal',fraction=0.025,label=label) 
    plt.title(f"{label}, from {calendar.month_name[month_start]} of {year_start} to {calendar.month_name[month_end]} of {year_end}")
    plt.show()

# example : plot_image_interval(903,908,tave1930,'tave')