from estimator_adaptative import EstimatorAdaptative
from mpl_toolkits.mplot3d import Axes3D
from grid_search import GridSearch
import matplotlib.pyplot as plt
import matplotlib as mpl
from utils import *
import numpy as np
import os
import sys

data_path = '../../databases'
PlotsDirectory = '../plots/Week2/task2/'

if not os.path.exists(PlotsDirectory):
    os.makedirs(PlotsDirectory)

names = ['highway', 'fall', 'traffic']
estimation_range = [np.array([1050, 1200]), np.array([1460, 1510]), np.array([950, 1000])]
prediction_range = [np.array([1201, 1350]), np.array([1511, 1560]), np.array([1001, 1050])]

a = [{'min':2, 'max':3, 'step':0.01}, {'min':3, 'max':6, 'step':0.1},{'min':0, 'max':6, 'step':0.05}]
r = [{'min':0.13, 'max':0.21, 'step':0.001}, {'min':0, 'max':0.12, 'step':0.01},{'min':0, 'max':0.4, 'step':0.005}]

for i in range(len(names)):
    if len(sys.argv) > 1:
        i = names.index(str(sys.argv[1]))

    print('computing ' + names[i] +' ...')

    [X_est, y_est] = load_data(data_path, names[i], estimation_range[i], grayscale=True)
    [X_pred, y_pred] = load_data(data_path, names[i], prediction_range[i], grayscale=True)

    alpha_range = np.arange(a[i].get('min'),a[i].get('max'),a[i].get('step'))
    rho_range = np.arange(r[i].get('min'),r[i].get('max'),r[i].get('step'))

    parameters = {'alpha': alpha_range, 'rho': rho_range}
    gs = GridSearch(EstimatorAdaptative(metric="f1"), parameters)
    gs.fitAndPredict(X_est, X_pred, None, y_pred)

    print('best_metric: '+str(gs.best_score))
    print('best_params: '+str(gs.best_params))
    scores = np.array(gs.results).reshape(len(parameters['alpha']), len(parameters['rho']))


    fig = plt.figure()
    ax = fig.gca(projection='3d')

    X, Y = np.meshgrid(rho_range, alpha_range)
    Z = np.array(gs.results).reshape(len(alpha_range), len(rho_range))

    # Plot the surface.
    ax.set_zlim(0, 1)
    ax.set_title(names[i])
    ax.set_xlabel('rho')
    ax.set_ylabel('alpha')
    ax.set_zlabel('F1-score')
    ax.ticklabel_format(style='sci')
    colormap = plt.cm.viridis
    normalize = mpl.colors.Normalize(vmin=0, vmax=max(gs.results))
    ax.plot_surface(X, Y, Z, cmap=colormap, norm=normalize)

    plt.show()

    if len(sys.argv) > 1:
        break

