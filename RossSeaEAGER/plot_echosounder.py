#!/usr/bin/env python

"""
Author: Lori Garzio on 7/2/2021
Last modified: 3/10/2022
Plot echo sounder data.
"""

import os
import pandas as pd
import xarray as xr
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def plot_sv(data, save_file, max_depth=None, title=None, trawl_times=None):
    max_depth = max_depth or None
    title = title or None
    trawl_times = trawl_times or None

    plt_data = data.Sv.values.T
    depth = data.range.values[0]

    if max_depth is not None:
        depth_idx = depth <= max_depth
        depth = depth[depth_idx]
        plt_data = plt_data[depth_idx]
        sfile = '{}_{}m'.format(save_file, str(max_depth))
    else:
        sfile = save_file

    fig, ax = plt.subplots(figsize=(12, 6))
    h = ax.pcolormesh(data.ping_time.values, depth, plt_data, vmin=-80, vmax=-30, cmap='jet', shading='auto')

    cb = plt.colorbar(h, extend='both', pad=0.02)
    cb.set_label(label='Sv')

    # add trawl times as vertical lines
    if trawl_times:
        for t in trawl_times:
            plt.axvline(x=t, ls='--', lw=.75, c='lightgray')

    ax.set_ylabel('Depth (m)')
    if title:
        ax.set_title(title)
    ax.invert_yaxis()

    # format the date axis
    #df = mdates.DateFormatter('%Y-%m-%d %H:%M')
    xfmt = mdates.DateFormatter('%H:%Mh\n%d-%b')
    ax.xaxis.set_major_formatter(xfmt)
    #fig.autofmt_xdate()
    plt.subplots_adjust(bottom=0.25)

    plt.savefig(sfile, dpi=200)


def main(save_dir, expt):
    # open all of the Sv.nc files as one dataset
    sv_data = xr.open_mfdataset(os.path.join(save_dir, 'processed', 'ds_Sv*.nc'),
                                combine='by_coords', data_vars='different')

    # sv_data_clean = ep.preprocess.remove_noise(sv_data, range_bin_num=30, ping_num=5)

    trawls = pd.read_csv('/Users/garzio/Documents/rucool/Saba/Ross_Sea/Ross_Sea_EAGER_ship_acoustic_data/trawl_info.csv')
    trawl_info = trawls[trawls['Expt'] == expt]

    # find the mid-point of the trawl and select ship echo sounder data +/- 12 hours
    start_trawl = pd.to_datetime(trawl_info['start_utc'].values)
    end_trawl = pd.to_datetime(trawl_info['end_utc'].values)
    trawl_time = start_trawl + (end_trawl - start_trawl) / 2
    start = (trawl_time - dt.timedelta(hours=1))[0]
    end = (trawl_time + dt.timedelta(hours=1))[0]

    sv_data_trawl = sv_data.sel(ping_time=slice(start, end))

    for freq in sv_data_trawl.frequency:
        sv_data_trawl_freq = sv_data_trawl.sel(frequency=freq.values)
        sfile = 'EAGER_{}_Sv_{}khz'.format(expt, int(freq.values / 1000))
        sfile_path = os.path.join(save_dir, sfile)

        kwargs = dict()
        kwargs['max_depth'] = 300
        kwargs['title'] = 'Grazing {}: {} kHz'.format(expt, int(freq.values / 1000))
        kwargs['trawl_times'] = [start_trawl[0], end_trawl[0]]

        plot_sv(sv_data_trawl_freq, sfile_path, **kwargs)
        #plot_sv(sv_data_freq, sfile_path, 600)


if __name__ == '__main__':
    fdir = '/Users/garzio/Documents/rucool/Saba/Ross_Sea/Ross_Sea_EAGER_ship_acoustic_data/LegI/GrazingExpt_rep1'
    #fdir = '/Users/garzio/Documents/rucool/Saba/Ross_Sea/Ross_Sea_EAGER_ship_acoustic_data/LegII'
    experiment = 'rep1'
    main(fdir, experiment)
