# fourier_analysis.py

import math
from forecast.models.template import GenerateArray, \
    ChartVariables
from forecast.models.fourier import FourierSquareWaveImpl2
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


class FourierSquareWave1(FourierSquareWaveImpl2):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        frequency = 5.0
        duty_cycle = 0.5
        self.wave.populate(q, frequency, duty_cycle)


class FourierTransformSquareWave1(FourierTransformSquareWave):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.wave_transform.populate(period=(2.0*math.pi), amplitude=1.0)
