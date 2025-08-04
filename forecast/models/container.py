# container.py
from forecast.models.fourier import FourierArray, FourierChartVariables
from forecast.models.fourier_transform import FourierTransformArray, FourierTransformChartVariables
from forecast.models.fourier_analysis import FourierAnalysisArray, FourierAnalysisChartVariables
from models import ModelRequestObj


class Container:

    def __init__(self, q: ModelRequestObj):
        self.models = []
        self.simulated_models = []
        self.chartVariables = {}
        self.spliceData = [True]
        if q.base_model == 2 or q.base_model == 3 or q.base_model == 4:
            self.models = FourierArray(q).array
            self.chartVariables = FourierChartVariables().__dict__
        elif q.base_model == 5 or q.base_model == 6 or q.base_model == 7:
            self.models = FourierTransformArray(q).array
            self.chartVariables = FourierTransformChartVariables().__dict__
        elif q.base_model == 8:
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
