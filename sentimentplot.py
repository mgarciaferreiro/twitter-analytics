#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 13:03:59 2018

@author: Marta
"""
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

twitter_data = pd.read_csv('results_trump.csv')

n, bins, patches = plt.hist(x, 50, normed=1, facecolor='green', alpha=0.75)

plt.xlabel('Polarity')
plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
plt.axis([-1, 1, 0, 0.03])
plt.grid(True)

plt.show()