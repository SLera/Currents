#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 15:35:38 2018

@author: valeria
"""
import glob
import os
import numpy as np
from matplotlib import pyplot as plt

INDIR = '/home/valeria/DATA/Currents/U_V_8days_mean'
OUTDIR_Bar = '/home/valeria/NIERSC/Scripts/Currents/Figs/Barents/1/'
OUTDIR_Ber = '/home/valeria/NIERSC/Scripts/Currents/Figs/Bering/1/'
#ind_Bering = [0,220,420,900]
#Barents_a = u [0:, 1200:]
#Barents_b = u[0:,0:300]
#Barents_full = np.concatenate((c,d),axis = 1)


u_files = sorted(glob.glob(os.path.join(INDIR, 'u_*')))
v_files = sorted(glob.glob(os.path.join(INDIR,'v_*')))

for i in range(len(u_files)):
    print i
    u_nh = np.load(u_files[i])
    v_nh = np.load(v_files[i])
    u_Bering = u_nh[0:220,420:900]
    v_Bering = v_nh[0:220,420:900]
    u1_Barents = u_nh[0:,1200:]
    v1_Barents = v_nh[0:,1200:]
    u2_Barents = u_nh[0:,0:300]
    v2_Barents = v_nh[0:,0:300]
    u_Barents = np.concatenate((u1_Barents,u2_Barents),axis=1)
    v_Barents = np.concatenate((v1_Barents,v2_Barents),axis=1)
    
    fig, (ax0, ax1) = plt.subplots(nrows=2)
    ax0.set_title(u_files[i][-16:]+'_Ber')
    imu = ax0.imshow(u_Bering,vmin=-0.5,vmax=0.5, origin ='lower')
#    imu = ax0.imshow(u_Bering, origin ='lower')
    cbar = fig.colorbar(imu, ax=ax0)
    ax1.set_title(v_files[i][-16:]+'_Ber')
    imv=ax1.imshow(v_Bering,vmin=-0.5,vmax=0.5, origin ='lower')
#    imv=ax1.imshow(v_Bering, origin ='lower')
    cbar = fig.colorbar(imv,ax=ax1)
    fig.tight_layout()
    plt.savefig(OUTDIR_Ber+'u_'+v_files[i][-16:]+'_Bering.png')
    plt.close()
    
    fig, (ax0, ax1) = plt.subplots(nrows=2)
    ax0.set_title(u_files[i][-16:]+'_Bar')
    imu = ax0.imshow(u_Barents,vmin=-0.5,vmax=0.5,  origin ='lower')
#    imu = ax0.imshow(u_Barents,  origin ='lower')
    cbar = fig.colorbar(imu,ax=ax0)
    ax1.set_title(v_files[i][-16:]+'_Bar')
    imv=ax1.imshow(v_Barents,vmin=-0.5,vmax=0.5, origin ='lower')
#    imv=ax1.imshow(v_Barents, origin ='lower')
    cbar = fig.colorbar(imv,ax=ax1)
    fig.tight_layout()
    plt.savefig(OUTDIR_Bar+'u_'+v_files[i][-16:]+'_Barents.png')
    plt.close()