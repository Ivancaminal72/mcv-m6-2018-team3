import sys
from utils import *
from hole_filling import hole_filling, hole_filling2


data_path = '../../databases'
PlotsDirectory = '../plots/Week3/task1/'

if not os.path.exists(PlotsDirectory):
    os.makedirs(PlotsDirectory)

names = ['highway', 'fall', 'traffic']
estimation_range = [np.array([1050, 1200]), np.array([1460, 1510]), np.array([950, 1000])]
prediction_range = [np.array([1201, 1350]), np.array([1511, 1560]), np.array([1001, 1050])]

<<<<<<< HEAD
i=2
[X_est, y_est] = load_data(data_path, names[i], estimation_range[i], grayscale=True)
[X_pred, y_pred] = load_data(data_path, names[i], prediction_range[i], grayscale=True)
=======
# for i in range(len(names)):
#     [X_est, y_est] = load_data(data_path, names[i], estimation_range[i], grayscale=True)
#     [X_pred, y_pred] = load_data(data_path, names[i], prediction_range[i], grayscale=True)
>>>>>>> 1c546f478b75bf2f87551b4157471e216f27107b


def task1(X_est, X_pred, ro, alpha, connectivity=4):
    # from week
    results = week2_masks(X_est, X_pred, ro=ro, alpha=alpha)

    results = hole_filling2(results, connectivity=connectivity, visualize=False)

    return results


if __name__ == "__main__":
    main()



# ================== TESTING ================
im = hole_filling(images=X_pred, visualize=True)    # Manual sequence: press "Enter" to advance in the sequence
hole_filling2(images=X_pred, connectivity=8, visualize=True)  # Manual sequence: press "Enter" to advance in the sequence


