# fourier_series.py

from utils import UnitsLabel, WaveTypes
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

        if q.base_model == 2:
            q.index_stop = 10.0
            self.array.append(FourierWaveImpl1(q, n_sum_limit=3, wave_type=WaveTypes.square))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=5, wave_type=WaveTypes.square))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=20, wave_type=WaveTypes.square))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=2, wave_type=WaveTypes.triangle))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=3, wave_type=WaveTypes.triangle))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=10, wave_type=WaveTypes.triangle))
        elif q.base_model == 3:
            q.index_stop = 10.0
            self.array.append(FourierWaveImpl1(q, n_sum_limit=3, wave_type=WaveTypes.square))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=5, wave_type=WaveTypes.square))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=7, wave_type=WaveTypes.square))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=9, wave_type=WaveTypes.square))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=11, wave_type=WaveTypes.square))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=15, wave_type=WaveTypes.square))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=20, wave_type=WaveTypes.square))
        elif q.base_model == 4:
            q.index_stop = 5.0
            self.array.append(FourierWaveImpl1(q, n_sum_limit=2, wave_type=WaveTypes.triangle))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=3, wave_type=WaveTypes.triangle))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=4, wave_type=WaveTypes.triangle))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=5, wave_type=WaveTypes.triangle))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=6, wave_type=WaveTypes.triangle))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=10, wave_type=WaveTypes.triangle))


class FourierSeriesChartVariables(ChartVariables):

    def __init__(self):
        super().__init__()
        self.title += "Fourier Series"
        self.xAxisTitleText = UnitsLabel.time_nano_seconds
        self.yAxisTitleText = UnitsLabel.units


