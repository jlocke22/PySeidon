#!/usr/bin/python2.7
# encoding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as Tri
import matplotlib.ticker as ticker
import seaborn

class PlotsFvcom:
    """'Plots' subset of FVCOM class gathers plotting functions"""
    def __init__(self, cls):
        self._var = cls.Variables
        self._grid = cls.Grid
        self._debug = cls._debug

    def graph_grid(self, cmin=[], cmax=[], debug=False):
        ''' 2D xy plot of bathymetry and mesh.
            No inputs required so far'''
        if debug or self._debug:
            print 'Plotting grid...'
        nv = self._grid.nv[:].T -1
        h = -1.0*self._grid.h
        tri = Tri.Triangulation(self._grid.lon, self._grid.lat, triangles=nv)
        #setting limit of colormap
        if cmin==[]:
            cmin=round(h[:].min())
        if cmax==[]:
            cmax=round(h[:].max())
        step = round(round(cmax-cmin) / 50)
        levels=np.arange(cmin, (cmax+step), step)   # depth contours to plot
        #Figure window params
        fig = plt.figure(figsize=(18,10))
        plt.rc('font',size='22')
        ax = fig.add_subplot(111,aspect=(1.0/np.cos(np.mean(self._grid.lat)*np.pi/180.0)))
        #Plotting functions
        plt.tricontourf(tri, h,levels=levels,shading='faceted',cmap=plt.cm.gist_earth)
        plt.triplot(tri)
        #Label and axis parameters
        plt.ylabel('Latitude')
        plt.xlabel('Longitude')
        plt.gca().patch.set_facecolor('0.5')
        cbar=plt.colorbar()
        cbar.set_label('Water Depth (m)', rotation=-90,labelpad=30)
        scale = 1
        ticks = ticker.FuncFormatter(lambda lon, pos: '{0:g}'.format(lon/scale))
        ax.xaxis.set_major_formatter(ticks)
        ax.yaxis.set_major_formatter(ticks)
        plt.grid()
        plt.show()
        if debug or self._debug:
            print '...Passed'

    #def spatial

