# fourier_analysis.py

from utils import Waveform
from forecast.models.template import GenerateArray, \
    ChartVariables
from forecast.models.fourier_utils import FourierWaveImpl2, FourierTransformFFT
from models import ModelRequestObj


class FourierAnalysisArray(GenerateArray):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        q.index_start = 0
        q.index_stop = 1
        q.increment = 0.001

        if q.waveform == 0:
            a = FourierWaveImpl2(q, waveform=Waveform.square, frequency=5.0, duty_cycle=0.5)
            self.array.append(a)
            self.array.append(FourierTransformFFT(q, o=a, waveform=Waveform.square))
        elif q.waveform == 1:
            a = FourierWaveImpl2(q, waveform=Waveform.triangle, frequency=5.0, width=0.5)
            self.array.append(a)
            self.array.append(FourierTransformFFT(q, o=a, waveform=Waveform.triangle))
        elif q.waveform == 2:
            a = FourierWaveImpl2(q, waveform=Waveform.parabola, frequency=5.0)
            self.array.append(a)
            self.array.append(FourierTransformFFT(q, o=a, waveform=Waveform.parabola))


class FourierAnalysisChartVariables(ChartVariables):
    pass

