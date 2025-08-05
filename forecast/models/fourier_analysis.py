# fourier_analysis.py

from utils import WaveTypes
from forecast.models.template import GenerateArray, \
    ChartVariables
from forecast.models.fourier import FourierWaveImpl2
from forecast.models.fourier_transform import FourierTransformFFT
from models import ModelRequestObj


class FourierAnalysisArray(GenerateArray):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        q.index_start = 0
        q.index_stop = 1
        q.increment = 0.001

        if q.base_model == 5:
            a = FourierWaveImpl2(q, wave_type=WaveTypes.square, frequency=5.0, duty_cycle=0.5)
            b = FourierWaveImpl2(q, wave_type=WaveTypes.triangle, frequency=5.0, width=0.5)
            self.array.append(a)
            self.array.append(FourierTransformFFT(q, o=a, wave_type=WaveTypes.square))
            self.array.append(b)
            self.array.append(FourierTransformFFT(q, o=b, wave_type=WaveTypes.triangle))


class FourierAnalysisChartVariables(ChartVariables):
    pass

