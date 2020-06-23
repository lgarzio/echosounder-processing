#!/usr/bin/env python

"""
Author: Lori Garzio on 6/22/2020
Last modified: 6/2/2020
Convert raw echo sounder files to netCDF using echopype
"""

import os
import glob
from echopype.convert import Convert
from echopype.model import EchoData


def convert_raw_to_nc(fname, sDir):
    data_tmp = Convert(fname)
    data_tmp.raw2nc(save_path=sDir)


def main(rdir):
    save_dir = os.path.join(os.path.dirname(rdir), 'processed')
    os.makedirs(save_dir, exist_ok=True)
    rawfiles = sorted(glob.glob(os.path.join(rdir, '*.raw')))

    # convert from raw file to netCDF
    for filename in rawfiles:
        convert_raw_to_nc(filename, save_dir)

    # process files, calculate Sv and MVBS
    ncfiles = sorted(glob.glob(os.path.join(save_dir, '*.nc')))
    for filename in ncfiles:
        ed = EchoData(filename)  # create an echo data processing object
        ed.calibrate(save=True)  # obtain volume backscattering strength (Sv)

        # bin the data (1 = keep full resolution of data)
        ed.get_MVBS(MVBS_range_bin_size=1, MVBS_ping_size=1, save=True)


if __name__ == '__main__':
    raw_dir = '/Users/lgarzio/Documents/rucool/Saba/Ross_Sea/Ross_Sea_EAGER_ship_acoustic_data/LegI/GrazingExpt_rep1/raw_files'
    main(raw_dir)
