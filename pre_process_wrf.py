import xarray as xxr
import numpy as np 
import glob

def preprocess_wrf():
    ''' 
    This script pre-processes WRF data for use with PyFLEXTRKR's run_generic_tracking function 
    '''
    # Note that the file path below points to explicitly 4-km resolution WRF ouput 
    files = sorted(glob.glob('/pscratch/sd/s/smheflin/uw_wrf/for_tracking/*.0000'))
    for file in files: 
        print (file)
        ds = xr.open_dataset(file)
        ds_radar = np.squeeze(ds.REFL_10CM)
        ds_radar = ds_radar.isel(bottom_top = 0)
        ds_radar.to_netcdf(file + '.trim.nc')
