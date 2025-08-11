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
        elif q.waveform == 3:
            a = FourierWaveImpl2(q, waveform=Waveform.exponential, frequency=2.0)
            self.array.append(a)
            self.array.append(FourierTransformFFT(q, o=a, waveform=Waveform.exponential))
        elif q.waveform == 4:
            a = FourierWaveImpl2(q, waveform=Waveform.cubic, frequency=5.0)
            self.array.append(a)
            self.array.append(FourierTransformFFT(q, o=a, waveform=Waveform.cubic))
        elif q.waveform == 5:
            a = FourierWaveImpl2(q, waveform=Waveform.aperiodic_pulse, frequency=10.0)
            self.array.append(a)
            self.array.append(FourierTransformFFT(q, o=a, waveform=Waveform.aperiodic_pulse))
        elif q.waveform == 6:
            a = FourierWaveImpl2(q, waveform=Waveform.dirac_delta, wave_params={Waveform.dirac_delta_type:
                                                                                Waveform.dirac_delta_rectangular,
                                                                                Waveform.epsilon: 0.001})
            self.array.append(a)
            self.array.append(FourierTransformFFT(q, o=a, waveform=Waveform.dirac_delta))
        elif q.waveform == 7:
            a = FourierWaveImpl2(q, waveform=Waveform.dirac_delta, wave_params={Waveform.dirac_delta_type:
                                                                                Waveform.dirac_delta_gaussian,
                                                                                Waveform.sigma: 0.001})
            self.array.append(a)
            self.array.append(FourierTransformFFT(q, o=a, waveform=Waveform.dirac_delta))


class FourierAnalysisChartVariables(ChartVariables):
    pass
