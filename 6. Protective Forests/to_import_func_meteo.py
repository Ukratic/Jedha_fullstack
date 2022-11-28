import pandas as pd
import netCDF4 as nc


def get_coordinates(period=str,file=str):
    """Get coordinates of plots from and to a dataframe.
    Takes inputs : period (LFI), file with plots and swiss coordinates
    pandas package imported as pd"""
    data = pd.read_excel(file,sheet_name=period) 
    x = data['X']/1000 +650 # coordinates are not centered at y/x=600/200 on Bern as they should be, but y/x=1250/1250
    y = data['Y']/1000 +1050 
    month = data['DATUMF'].dt.month
    year = data['DATUMF'].dt.year
    new_year = (year-1929)*12
    new_date = new_year - 12 + month - 1 #index in python starts at 0
    df = new_date,x,y
    return pd.DataFrame(df).astype(int)

# example : dataplot = get_coordinates('LFI3','NFI_data/PLOTDATEN.xlsx')

def selected_time(coords_df,file):
    """Returns time for selected element of the dataset.
    Takes inputs : coord_df (from func get_coordinates) and netcdf file
    netCDF4 package imported as nc"""
    d_time = file.variables['time'][coords_df]
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


def plot_image(coord_df,file,kind):
    """Returns precipitation or temperature average since previous collection campaign, only for months of growth (april to september)
    Takes inputs : time in coord_df (from func get_coordinates), netcdf file, kind ('tave' or 'prcp'), 
    matplotlib.pyplot package imported as plt"""
    if kind == 'prcp':
        palette = 'viridis'
        label = 'Precipitations in cm'
    elif kind == 'tave':
        palette = 'magma'
        label = 'Temperature average in C°'
    d_time = file.variables['time'][coord_df]
    time_unit = file.variables["time"].getncattr('units')
    month = nc.num2date(d_time,units=time_unit).month
    year = nc.num2date(d_time,units=time_unit).year
    plt.figure(figsize=(12,12))
    plt.axis('off')
    plt.imshow(file[kind][coord_df],origin='lower',cmap=palette)
    #plt.gcf().set_facecolor("white")
    plt.colorbar(orientation='horizontal',fraction=0.025,label=label) 
    plt.title(f"{label} for month {month} of year {year}")
    plt.show()

# example : plot_image(dataplot[0][0],prcp1930,'prcp')