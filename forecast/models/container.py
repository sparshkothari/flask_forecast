# container.py
from forecast.models.fourier_series import FourierSeriesArray, FourierSeriesChartVariables
from forecast.models.fourier_analysis import FourierAnalysisArray, FourierAnalysisChartVariables
from models import ModelRequestObj


class Container:

    def __init__(self, q: ModelRequestObj):
        self.models = []
        self.simulated_models = []
        self.chartVariables = {}
        self.spliceData = [True]
        if q.base_model == 2:
            self.models = FourierSeriesArray(q).array
            self.chartVariables = FourierSeriesChartVariables().__dict__
        elif q.base_model == 3:
            self.spliceData[0] = False
            self.models = FourierAnalysisArray(q).array
            self.chartVariables = FourierAnalysisChartVariables().__dict__

    def run(self):
        o = []
        for model in self.models:
            model.simulate_model()
            self.simulated_models.append(model.__dict__)
        o.append(self.chartVariables)
        o.append(self.simulated_models)
        o.append(self.spliceData)
        return o
