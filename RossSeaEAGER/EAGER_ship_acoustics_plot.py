#!/usr/bin/env python

"""
Author: Lori Garzio on 6/22/2020
Last modified: 6/22/2020
Plot echo sounder data.
"""

import os
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def plot_mvbs(data, save_file, max_depth=None):
    data = data.swap_dims({'range_bin': 'depth'})
    # create an index where depth is < 200
    if max_depth is not None:
        depth_ind = data.depth.values <= max_depth
        depth = data.depth.values[depth_ind]
        plt_data = data.values.T[depth_ind]
        sfile = '{}_{}m'.format(save_file, str(max_depth))
    else:
        depth = data.depth.values
        plt_data = data.values.T
        sfile = save_file

    fig, ax = plt.subplots(figsize=(12, 6))
    h = ax.pcolormesh(data.ping_time.values, depth, plt_data, vmin=-80, vmax=-30, cmap='jet')

    cb = plt.colorbar(h, extend='both')
    cb.set_label(label='MVBS')

    ax.set_ylabel('Depth (m)')
    ax.set_title('{} kHz'.format(int(data.frequency.values / 1000)))
    ax.invert_yaxis()

    # format the date axis
    df = mdates.DateFormatter('%Y-%m-%d %H:%M')
    ax.xaxis.set_major_formatter(df)
    fig.autofmt_xdate()
    plt.subplots_adjust(bottom=0.25)

    plt.savefig(sfile, dpi=200)


def main(save_dir):
    # open all of the MVBS.nc files as one dataset
    mvbs_data = xr.open_mfdataset(os.path.join(save_dir, 'processed', '*MVBS.nc'),
                                  combine='by_coords', data_vars='different')

    # add depth as a new coordinate
    depth = mvbs_data.range_bin * mvbs_data.MVBS_range_bin_size
    mvbs_data.coords['depth'] = (['range_bin', 'frequency'], depth)

    for freq in mvbs_data.frequency:
        mvbs_data_freq = mvbs_data.MVBS.sel(frequency=freq.values)
        sfile = 'EAGER_{}_MVBS_{}khz'.format(os.path.basename(save_dir), int(freq.values/1000))
        sfile_path = os.path.join(save_dir, sfile)

        plot_mvbs(mvbs_data_freq, sfile_path, 600)
        plot_mvbs(mvbs_data_freq, sfile_path, 200)


if __name__ == '__main__':
    fdir = '/Users/lgarzio/Documents/rucool/Saba/Ross_Sea/Ross_Sea_EAGER_ship_acoustic_data/LegI/GrazingExpt_rep1'
    main(fdir)
