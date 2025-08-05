# fourier.py

import math
import numpy as np
from scipy import signal
from utils import UtilsJSONEncoder, UnitsLabel, WaveTypes
from forecast.models.template import Template, GenerateArray, \
    ChartVariables
from models import ModelRequestObj


class FourierArray(GenerateArray):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        q.index_start = 0.0
        q.index_stop = 50.0
        q.increment = 0.01

        if q.base_model == 2:
            q.index_stop = 10.0
            self.array.append(FourierWaveImpl1(q, n_sum_limit=20, wave_type=WaveTypes.square))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=10, wave_type=WaveTypes.triangle))
        elif q.base_model == 3:
            q.index_stop = 10.0
            self.array.append(FourierWaveImpl1(q, n_sum_limit=3, wave_type=WaveTypes.square))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=5, wave_type=WaveTypes.square))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=20, wave_type=WaveTypes.square))
        elif q.base_model == 4:
            q.index_stop = 5.0
            self.array.append(FourierWaveImpl1(q, n_sum_limit=2, wave_type=WaveTypes.triangle))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=3, wave_type=WaveTypes.triangle))
            self.array.append(FourierWaveImpl1(q, n_sum_limit=10, wave_type=WaveTypes.triangle))


class FourierChartVariables(ChartVariables):

    def __init__(self):
        super().__init__()
        self.title += "Fourier Series"
        self.xAxisTitleText = UnitsLabel.time_nano_seconds
        self.yAxisTitleText = UnitsLabel.units


class Fourier(Template):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.xAxisTitleText = UnitsLabel.time_nano_seconds
        self.yAxisTitleText = UnitsLabel.units
        self.wave = WaveImpl1()

        t = UtilsJSONEncoder()
        t.encode(self.wave)

    def iterate(self, index, i):
        super().iterate(index, i)
        x = i
        self.data_point = self.wave.method(index, x)


class FourierWaveImpl1(Fourier):

    def __init__(self, q: ModelRequestObj, n_sum_limit: int, wave_type: str):
        super().__init__(q)
        self.model += "_wave_type:_" + wave_type + "_n_sum_limit:_" + str(n_sum_limit)
        self.title = self.model
        self.lineSeriesValueY = "y_" + self.model
        self.lineSeriesName = self.lineSeriesValueY
        self.wave = None
        if wave_type == WaveTypes.square:
            self.wave = SquareWaveImpl1()
        elif wave_type == WaveTypes.triangle:
            self.wave = TriangleWaveImpl1()

        self.wave.populate(n_sum_limit)
        t = UtilsJSONEncoder()
        t.encode(self.wave)


class FourierWaveImpl2(Fourier):
    def __init__(self, q: ModelRequestObj, wave_type: str, frequency: float = 0.0, duty_cycle=None, width=None):
        super().__init__(q)
        self.model += "_wave_type:_" + wave_type
        self.title = self.model
        self.lineSeriesValueY = "y_" + self.model
        self.lineSeriesName = self.lineSeriesValueY
        self.wave = None
        self.duty_cycle = None
        self.width = None
        if wave_type == WaveTypes.square:
            self.wave = SquareWaveImpl2(q)
            self.wave.populate(q, frequency=frequency, duty_cycle=duty_cycle)
            self.duty_cycle = self.wave.duty_cycle
        elif wave_type == WaveTypes.triangle:
            self.wave = TriangleWaveImpl2(q)
            self.wave.populate(q, frequency=frequency, width=width)
            self.width = self.wave.width

        self.duration = self.wave.duration
        self.sampling_frequency = self.wave.sampling_frequency
        self.frequency = self.wave.frequency

        t = UtilsJSONEncoder()
        t.encode(self.wave)


class WaveImpl1:

    def __init__(self, n_sum_limit: int = 0):
        self.n_sum_limit = n_sum_limit
        self.a_initial = 0.0

    def populate(self, n_sum_limit: int = 0):
        self.n_sum_limit = n_sum_limit

    def method(self, index: int, time: float = 0.0):
        v = 0.0
        v += self.a_initial
        for i in range(1, self.n_sum_limit):
            v += self.method_impl(float(i), time)
        return v

    def method_impl(self, i: float = 0.0, time: float = 0.0):
        return time


class SquareWaveImpl1(WaveImpl1):

    def __init__(self, n_sum_limit: int = 0):
        super().__init__(n_sum_limit)
        self.a_initial = 0.5

    def method_impl(self, i: float = 0.0, time: float = 0.0):
        super().method_impl(i, time)
        t = time
        h = (2.0 * i) - 1.0
        h1 = 2.0 / (h * math.pi)
        return h1 * math.sin(h * t)


class TriangleWaveImpl1(WaveImpl1):

    def __init__(self, n_sum_limit: int = 0):
        super().__init__(n_sum_limit)
        self.a_initial = 0.5

    def method_impl(self, i: float = 0.0, time: float = 0.0):
        super().method_impl(i, time)
        t = time
        h = (2.0 * i) - 1.0
        h1 = 4.0 / math.pow(h * math.pi, 2)
        return h1 * math.cos(h * math.pi * t) * -1.0


class WaveImpl2:

    def __init__(self, q: ModelRequestObj, frequency: float = 0.0, duty_cycle: float = 0.0, width: float = 0.0):
        self.duration = q.index_stop - q.index_start
        self.sampling_frequency = self.duration/q.increment
        self.frequency = frequency
        self.duty_cycle = duty_cycle
        self.width = width
        self.wave_data = []

    def populate(self, q: ModelRequestObj, frequency: float = 0.0, duty_cycle: float = 0.0, width: float = 0.0):
        self.duration = q.index_stop - q.index_start
        self.sampling_frequency = self.duration / q.increment
        self.frequency = frequency
        self.duty_cycle = duty_cycle
        self.width = width

    def np_wave(self, q: ModelRequestObj):
        return ""

    def method(self, index: int, time: float = 0.0):
        return self.wave_data[index]


class SquareWaveImpl2(WaveImpl2):

    def __init__(self, q: ModelRequestObj, frequency: float = 0.0, duty_cycle: float = 0.0, width: float = 0.0):
        super().__init__(q=q, frequency=frequency, duty_cycle=duty_cycle)
        t = np.linspace(q.index_start, q.index_stop, int(self.sampling_frequency), endpoint=False)
        self.wave_data = signal.square(2 * np.pi * self.frequency * t, duty=self.duty_cycle).tolist()

    def populate(self, q: ModelRequestObj, frequency: float = 0.0, duty_cycle: float = 0.0, width: float = 0.0):
        super().populate(q=q, frequency=frequency, duty_cycle=duty_cycle)
        t = np.linspace(q.index_start, q.index_stop, int(self.sampling_frequency), endpoint=False)
        self.wave_data = signal.square(2 * np.pi * self.frequency * t, duty=self.duty_cycle).tolist()

    def np_wave(self, q: ModelRequestObj):
        super().np_wave(q)
        t = np.linspace(q.index_start, q.index_stop, int(self.sampling_frequency), endpoint=False)
        return signal.square(2 * np.pi * self.frequency * t, duty=self.duty_cycle)


class TriangleWaveImpl2(WaveImpl2):

    def __init__(self, q: ModelRequestObj, frequency: float = 0.0, duty_cycle: float = 0.0, width: float = 0.0):
        super().__init__(q=q, frequency=frequency, width=width)
        t = np.linspace(q.index_start, q.index_stop, int(self.sampling_frequency), endpoint=False)
        self.wave_data = signal.sawtooth(2 * np.pi * self.frequency * t, width=self.width).tolist()

    def populate(self, q: ModelRequestObj, frequency: float = 0.0, duty_cycle: float = 0.0, width: float = 0.0):
        super().populate(q=q, frequency=frequency, width=width)
        t = np.linspace(q.index_start, q.index_stop, int(self.sampling_frequency), endpoint=False)
        self.wave_data = signal.sawtooth(2 * np.pi * self.frequency * t, width=self.width).tolist()

    def np_wave(self, q: ModelRequestObj):
        super().np_wave(q)
        t = np.linspace(q.index_start, q.index_stop, int(self.sampling_frequency), endpoint=False)
        return signal.sawtooth(2 * np.pi * self.frequency * t, width=self.width).tolist()
