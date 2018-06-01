#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 11:56:40 2018

@author: valeria
"""

import glob
import os
import numpy as np
from matplotlib import pyplot as plt

INDIR = '/home/valeria/DATA/Currents/U_V_8days_mean'
OUTDIR_Bar = '/home/valeria/NIERSC/Scripts/Currents/Figs/Barents/difference/'
OUTDIR_Ber = '/home/valeria/NIERSC/Scripts/Currents/Figs/Bering/difference/'


u_files = sorted(glob.glob(os.path.join(INDIR, 'u_*')))
v_files = sorted(glob.glob(os.path.join(INDIR,'v_*')))

y_Bering_bloom = 2000
y_Bering_neg = 2003

y_Barents_bloom = 2001
y_Barents_neg = 1998

u_files_Bering_bloom = []
v_files_Bering_bloom = []

u_files_Bering_neg = []
v_files_Bering_neg = []

u_files_Barents_bloom = []
v_files_Barents_bloom = []

u_files_Barents_neg = []
v_files_Barents_neg = []

for i in range(len(u_files)):
#    print i
    year = u_files[i][-8:-4]
    if int(year) == y_Bering_bloom:
        u_files_Bering_bloom.append(u_files[i])
        v_files_Bering_bloom.append(v_files[i])
    if int(year) == y_Bering_neg:
        u_files_Bering_neg.append(u_files[i])
        v_files_Bering_neg.append(v_files[i])
        
    if int(year) == y_Barents_bloom:
        u_files_Barents_bloom.append(u_files[i])
        v_files_Barents_bloom.append(v_files[i])
    if int(year) == y_Barents_neg:
        u_files_Barents_neg.append(u_files[i])
        v_files_Barents_neg.append(v_files[i])

##Bering
#for i in range(len(u_files_Bering_bloom)):          
#    u_nh = np.load(u_files_Bering_bloom[i])
#    v_nh = np.load(v_files_Bering_bloom[i])
#    u_Bering_bloom = u_nh[0:220,420:900]
#    v_Bering_bloom = v_nh[0:220,420:900]
#    
#    u_nh = np.load(u_files_Bering_neg[i])
#    v_nh = np.load(v_files_Bering_neg[i])
#    u_Bering_neg = u_nh[0:220,420:900]
#    v_Bering_neg = v_nh[0:220,420:900]
#    
#    u_Bering = u_Bering_neg-u_Bering_bloom
#    v_Bering = v_Bering_neg-v_Bering_bloom 
#    
#    fig, (ax0, ax1) = plt.subplots(nrows=2)
#    ax0.set_title('u_'+u_files_Bering_neg[i][-8:]+'-'+u_files_Bering_bloom[i][-8:]+'_Ber')
#    imu = ax0.imshow(u_Bering,vmin=-0.5,vmax=0.5, origin ='lower')
##    imu = ax0.imshow(u_Bering, origin ='lower')
#    cbar = fig.colorbar(imu, ax=ax0)
#    ax1.set_title('v_'+v_files_Bering_neg[i][-8:]+'-'+v_files_Bering_bloom[i][-8:]+'_Ber')
#    imv=ax1.imshow(v_Bering,vmin=-0.5,vmax=0.5, origin ='lower')
##    imv=ax1.imshow(v_Bering, origin ='lower')
#    cbar = fig.colorbar(imv,ax=ax1)
#    fig.tight_layout()
#    plt.savefig(OUTDIR_Ber+'Neg-Bloom_u'+v_files[i][-16:]+'_Bering.png')
#    plt.close()
 
#Barents
for i in range(len(u_files_Barents_bloom)):          
    u_nh = np.load(u_files_Barents_bloom[i])
    v_nh = np.load(v_files_Barents_bloom[i])

    u1_Barents = u_nh[0:,1200:]
    v1_Barents = v_nh[0:,1200:]
    u2_Barents = u_nh[0:,0:300]
    v2_Barents = v_nh[0:,0:300]
    u_Barents_bloom = np.concatenate((u1_Barents,u2_Barents),axis=1)
    v_Barents_bloom = np.concatenate((v1_Barents,v2_Barents),axis=1)
    
    u_nh = np.load(u_files_Barents_neg[i])
    v_nh = np.load(v_files_Barents_neg[i])

    u1_Barents = u_nh[0:,1200:]
    v1_Barents = v_nh[0:,1200:]
    u2_Barents = u_nh[0:,0:300]
    v2_Barents = v_nh[0:,0:300]
    u_Barents_neg = np.concatenate((u1_Barents,u2_Barents),axis=1)
    v_Barents_neg = np.concatenate((v1_Barents,v2_Barents),axis=1)
    
    u_Barents = u_Barents_neg-u_Barents_bloom
    v_Barents = v_Barents_neg-v_Barents_bloom 
    
    fig, (ax0, ax1) = plt.subplots(nrows=2)
    ax0.set_title('u_'+u_files_Barents_neg[i][-8:]+'-'+u_files_Barents_bloom[i][-8:]+'_Ber')
    imu = ax0.imshow(u_Barents,vmin=-0.5,vmax=0.5, origin ='lower')
#    imu = ax0.imshow(u_Bering, origin ='lower')
    cbar = fig.colorbar(imu, ax=ax0)
    ax1.set_title('v_'+v_files_Barents_neg[i][-8:]+'-'+v_files_Bering_bloom[i][-8:]+'_Ber')
    imv=ax1.imshow(v_Barents,vmin=-0.5,vmax=0.5, origin ='lower')
#    imv=ax1.imshow(v_Bering, origin ='lower')
    cbar = fig.colorbar(imv,ax=ax1)
    fig.tight_layout()
    plt.savefig(OUTDIR_Bar+'Neg-Bloom_u'+v_files[i][-16:]+'_Barents.png')
    plt.close()
    
    
