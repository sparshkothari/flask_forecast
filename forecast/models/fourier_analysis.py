# fourier_analysis.py

import math
from utils import UnitsLabel
from forecast.models.template import GenerateArray, \
    ChartVariables
from forecast.models.fourier import FourierSquareWaveImpl2
from forecast.models.fourier_transform import FourierTransformFFT
from models import ModelRequestObj


class FourierAnalysisArray(GenerateArray):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        q.index_start = 0
        q.index_stop = 1
        q.increment = 0.001

        if q.base_model == 9:
            self.array.append(FourierSquareWave1(q))
            self.array.append(FourierTransformSquareWave1(q))


class FourierAnalysisChartVariables(ChartVariables):
    pass


class FourierSquareWave1(FourierSquareWaveImpl2):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.xAxisTitleText = UnitsLabel.time_seconds
        frequency = 5.0
        duty_cycle = 0.5
        self.wave.populate(q, frequency, duty_cycle)
        self.duration = self.wave.duration
        self.sampling_frequency = self.wave.sampling_frequency
        self.frequency = self.wave.frequency
        self.duty_cycle = self.wave.duty_cycle


class FourierTransformSquareWave1(FourierTransformFFT):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        o = FourierSquareWave1(q)
        self.populate(o.wave.np_wave(q), o.wave.sampling_frequency, o.wave.frequency, o.wave.duration, o.wave.duty_cycle)
