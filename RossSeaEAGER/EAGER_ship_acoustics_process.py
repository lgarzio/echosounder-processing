#!/usr/bin/env python

"""
Author: Lori Garzio on 6/22/2020
Last modified: 3/10/2022
Convert raw echo sounder files to netCDF using echopype
"""

import os
import glob
import echopype as ep


def main(rdir, model):
    save_dir = os.path.join(os.path.dirname(rdir), 'processed')
    os.makedirs(save_dir, exist_ok=True)
    rawfiles = sorted(glob.glob(os.path.join(rdir, '*.raw')))

    # convert from raw file to netCDF
    for filename in rawfiles:
        data_tmp = ep.open_raw(filename, sonar_model=model)
        data_tmp.to_netcdf(save_path=save_dir)

    # process files, calculate Sv and MVBS
    ncfiles = sorted(glob.glob(os.path.join(save_dir, '*.nc')))
    for ncpath in ncfiles:
        ed = ep.open_converted(ncpath)  # create an EchoData object

        # get a dataset containing Sv, range and the calibration and environmental parameters
        ds_Sv = ep.calibrate.compute_Sv(ed)

        # bin the data
        # ds_Sv = calibrated Sv dataset
        # range_meter_bin = bin size to average along range in meters
        # ping_time_bin = bin size to average along ping_time in seconds
        ds_MVBS = ep.preprocess.compute_MVBS(ds_Sv, range_meter_bin=5, ping_time_bin='20S')

        # remove noise
        # ds_Sv = calibrated Sv dataset
        # range_bin_num = number of samples along the range_bin dimension for estimating noise
        # ping_num = number of pings for estimating noise
        ds_Sv_clean = ep.preprocess.remove_noise(ds_Sv, range_bin_num=30, ping_num=5)

        # save files to disk
        ed_filename = ncpath.split('/')[-1]
        print('\nWriting {} Sv and MVBS datasets to file'.format(ed_filename))
        ds_Sv.to_netcdf(os.path.join(save_dir, f'ds_Sv_{ed_filename}'))
        #ds_Sv_clean.to_netcdf(os.path.join(save_dir, f'ds_Sv_clean_{ed_filename}'))
        ds_MVBS.to_netcdf(os.path.join(save_dir, f'ds_MVBS_{ed_filename}'))


if __name__ == '__main__':
    raw_dir = '/Users/garzio/Documents/rucool/Saba/Ross_Sea/Ross_Sea_EAGER_ship_acoustic_data/LegI/GrazingExpt_rep2/raw_files'
    sonar_model = 'EK60'  # EK60  EK80
    main(raw_dir, sonar_model)
