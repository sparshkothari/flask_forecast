# fourier_analysis.py

from forecast.models.template import GenerateArray, \
    ChartVariables
from forecast.models.fourier import FourierSquareWave
from forecast.models.fourier_transform import FourierTransformSquareWave
from models import ModelRequestObj


class FourierAnalysisArray(GenerateArray):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        q.index_start = -10.0
        q.index_stop = 10.0
        q.increment = 0.01

        if q.base_model == 9:
            self.array.append(FourierSquareWave1(q))
            self.array.append(FourierTransformSquareWave1(q))


class FourierAnalysisChartVariables(ChartVariables):
    pass


class FourierSquareWave1(FourierSquareWave):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.wave.populate(100)


class FourierTransformSquareWave1(FourierTransformSquareWave):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.wave_transform.populate(1.0, 1.0)
