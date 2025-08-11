# fourier_series.py

from utils import UnitsLabel, Waveform
from forecast.models.fourier_utils import FourierWaveImpl1
from forecast.models.template import GenerateArray, \
    ChartVariables
from models import ModelRequestObj


class FourierSeriesArray(GenerateArray):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        q.index_start = 0.0
        q.index_stop = 50.0
        q.increment = 0.01

        if q.waveform == 0:
            q.index_stop = 10.0
            self.array.append(FourierWaveImpl1(q, n_sum_limit=5, waveform=Waveform.square))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=7, waveform=Waveform.square))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=9, waveform=Waveform.square))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=11, waveform=Waveform.square))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=15, waveform=Waveform.square))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=20, waveform=Waveform.square))
        elif q.waveform == 1:
            q.index_stop = 5.0
            self.array.append(FourierWaveImpl1(q, n_sum_limit=2, waveform=Waveform.triangle))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=3, waveform=Waveform.triangle))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=4, waveform=Waveform.triangle))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=5, waveform=Waveform.triangle))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=6, waveform=Waveform.triangle))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=10, waveform=Waveform.triangle))
        elif q.waveform == 2:
            q.index_stop = 15
            self.array.append(FourierWaveImpl1(q, n_sum_limit=2, waveform=Waveform.parabola))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=3, waveform=Waveform.parabola))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=4, waveform=Waveform.parabola))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=5, waveform=Waveform.parabola))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=10, waveform=Waveform.parabola))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=20, waveform=Waveform.parabola))
        elif q.waveform == 3:
            q.index_stop = 15
            self.array.append(FourierWaveImpl1(q, n_sum_limit=5, waveform=Waveform.exponential))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=7, waveform=Waveform.exponential))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=10, waveform=Waveform.exponential))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=15, waveform=Waveform.exponential))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=25, waveform=Waveform.exponential))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=35, waveform=Waveform.exponential))
        elif q.waveform == 4:
            q.index_stop = 15
            self.array.append(FourierWaveImpl1(q, n_sum_limit=5, waveform=Waveform.cubic))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=10, waveform=Waveform.cubic))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=15, waveform=Waveform.cubic))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=25, waveform=Waveform.cubic))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=50, waveform=Waveform.cubic))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=100, waveform=Waveform.cubic))


class FourierSeriesChartVariables(ChartVariables):

    def __init__(self):
        super().__init__()
        self.title += "Fourier Series"
        self.xAxisTitleText = UnitsLabel.time_nano_seconds
        self.yAxisTitleText = UnitsLabel.units


