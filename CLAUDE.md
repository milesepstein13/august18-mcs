# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Research analysis of the August 17–18, 2024 mesoscale convective system (MCS) in the Pacific Northwest. It compares WRF model runs against observations (MRMS, NEXRAD radar, ERA5 reanalysis, daily CONUS lightning grids, SPC hail/wind storm reports). There is no build system, package, or test suite. The work lives in Jupyter notebooks, and their outputs (PNGs, GIFs, NetCDF) are committed to the repo.

## Environment and execution

- Python 3.10/3.11 conda environment. The main libraries are xarray, numpy, pandas, matplotlib, cartopy, metpy, wrf-python (`wrf.getvar`), arm-pyart, osmnx, boto3/botocore, scipy, colorcet, imageio and PIL.
- You run notebooks cell by cell in Jupyter/VS Code. There is nothing to build, lint, or test.
- Notebooks were written across **three machines** and hardcode absolute paths. Check and adjust paths before you run anything:
  - NERSC Perlmutter: `/pscratch/sd/s/smheflin/...` (raw WRF, MRMS, ERA5) and `/global/homes/s/smheflin/august18-mcs/...` (the ERA5 notebooks, WRF preprocessing and MRMS regridding)
  - Local Windows: `C:\Users\miles\Downloads\mcs_side_proj\...` (`explore_wrf.ipynb`, `process_43.ipynb`)
  - Repo-relative paths (radar, lightning and observation notebooks)
- Large raw inputs are gitignored and exist only locally: `radar_files/` (NEXRAD Level II `*_V06` files, e.g. KATX/KLGX/KRTX) and `nc_ltgday_conus/` (`ltgday_NNN.nc`, one file per day of year).
- `cache/` holds OSMnx/Overpass API JSON responses, which are used for city/road overlays on the radar and report maps. It is auto-generated, so don't edit it.

## Pipeline / architecture

1. **WRF tracking prep**: `pre_process_wrf.py` pulls lowest-level `REFL_10CM` out of 4-km WRF output into `*.trim.nc` for PyFLEXTRKR `run_generic_tracking`. It has a bug: it imports `xarray as xxr` but calls `xr`. The tracking itself runs outside this repo. Hourly results land in `mcstracking/4km/mcstracks_*.nc`. The 1.33 km tracks live on Google Drive (link in `mcstracking/filepath.md`). `mcstracking/mcs_masks.ipynb` plots the track masks.
2. **WRF field analysis**: `explore_wrf.ipynb` and `process_43.ipynb` (the fuller version: shear, cloud height, CAPE, absolute vorticity via `wrf.getvar`) produce per-timestep maps and then GIFs under `images/<FIELD>/` (CAPE, OLR, TB, REFL_10CM, RAIN*, Shear, WIND_sfc, …). `olr_to_tb.py` converts WRF OLR to IR brightness temperature (Yang & Slingo 2001). Notebooks use it via `from olr_to_tb import *`, so it must stay at the repo root.
3. **MRMS**: `mrms_regrid.ipynb` regrids 10-min MRMS reflectivity (on NERSC) to the tracking grid. The tracking GIFs are in `tracking_loops/`.
4. **Radar**: `radar_analysis.ipynb` reads NEXRAD Level II with Py-ART, with optional download from the public AWS bucket via unsigned boto. It renders PPI frames and animations into `radar_animations/` (including the `follow/` storm-following view and per-radar subfolders). To switch radars, edit the `radar_code` config at the top.
5. **Storm reports**: `observation_plotting.ipynb` reads `240817_rpts_raw_hail.csv` and `240817_rpts_filtered_wind.csv` (SPC format, times in UTC HHMM for 12Z Aug 17 to 12Z Aug 18). It writes reflectivity and velocity snapshots near each report to `report_plots/{reflectivity,velocity}/`, named `<type>_<location>_<HHMM>.png`.
6. **Climatology/synoptics**: `plot_era5_climatology.ipynb` writes to `era5_climatology/`. `explore_era5_data.ipynb` makes the synoptic loops in `ERA5_loops/`. `lightning_climatology.ipynb` stacks the daily lightning files into a time series and saves `lightning_climatology.png` / `august_lightning_climatology.png`.

`gif_splitter.ipynb` pulls timestamped frames out of GIFs. `test_region.ipynb` is scratch work for choosing map extents.

## Conventions

- Map extents use the cartopy `[west_lon, east_lon, south_lat, north_lat]` ordering, with PlateCarree for data transforms.
- Times are UTC. The event window is 2024-08-17 12Z through 2024-08-18 13Z.
- Generated figures are committed. When you regenerate a figure, overwrite it at its existing path so that references stay valid.
