#!/usr/bin/python2.7
# encoding: utf-8

from __future__ import division
import numpy as np

class _load_adcp:
    """
'Variables' subset in FVCOM class contains the following numpy arrays:
    """
    def __init__(self,cls, debug=False):
        if debug:
            print 'Loading variables...'

        self.lat = cls.Data['lat']
        self.lon = cls.Data['lon']
        self.bins = cls.Data['data']['bins'][:].flatten()
        self.north_vel = cls.Data['data']['north_vel'][:]
        self.east_vel = cls.Data['data']['east_vel'][:]
        self.vert_vel = cls.Data['data']['vert_vel'][:]
        self.dir_vel = cls.Data['data']['dir_vel'][:]
        self.mag_signed_vel = cls.Data['data']['mag_signed_vel'][:]
        self.ucross = cls.Data['data']['Ucross'][:]
        self.ualong = cls.Data['data']['Ualong'][:]
        self.pressure = cls.Data['pres']
        self.surf = self.pressure['surf'][:]
        self.time = cls.Data['time']
        self.mtime = self.time['mtime'][:]

        #Find the depth average of a variable based on percent_of_depth
        #choosen by the user. Currently only working for east_vel (u) and
        #north_vel (v)
        ind = np.argwhere(self.bins < self.percent_of_depth * self.surf[:,None])
        index = ind[np.r_[ind[1:,0] != ind[:-1,0], True]]
        data_ma_u = np.ma.array(self.east_vel, mask=np.arange(self.east_vel.shape[1]) > index[:, 1, None])
        data_ma_v = np.ma.array(self.north_vel, mask=np.arange(self.north_vel.shape[1]) > index[:, 1, None])
        self.ua = np.array(data_ma_u.mean(axis=1))
        self.va = np.array(data_ma_v.mean(axis=1))

        if debug:
            print '...Passed'
