from sklearn.model_selection import ParameterGrid

class GridSearch:

    def __init__(self, estimator, param_grid):
        """
        Initialization
        """
        self.estimator = estimator
        self.param_grid=param_grid

    def fitAndPredict(self, X_est, X_pred, y_est, y_pred):
        params = list(ParameterGrid(self.param_grid))
        self.results = list()
        for idx, param in enumerate(params):
            print(str(idx) + "/" + str(len(params)) +" "+ str(param))
            self.estimator.set_alpha(param['alpha'])
            self.estimator.set_rho(param['rho'])
            self.estimator.fit(X_est, y_est)
            self.results.append(self.estimator.score(X_pred, y_pred))

        self.best_score = max(self.results)
        for i, j in enumerate(self.results):
            if j == self.best_score:
                self.best_params = params[i]
                break


