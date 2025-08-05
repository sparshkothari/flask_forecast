# fourier_utils.py

import math
import numpy as np
from scipy import signal
from utils import UtilsJSONEncoder, UnitsLabel, Waveform
from forecast.models.template import Template
from models import ModelRequestObj


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

    def __init__(self, q: ModelRequestObj, n_sum_limit: int, waveform: str):
        super().__init__(q)
        self.model += "_waveform:_" + waveform + "_n_sum_limit:_" + str(n_sum_limit)
        self.title = self.model
        self.lineSeriesValueY = "y_" + self.model
        self.lineSeriesName = self.lineSeriesValueY
        self.wave = None
        if waveform == Waveform.square:
            self.wave = SquareWaveImpl1()
        elif waveform == Waveform.triangle:
            self.wave = TriangleWaveImpl1()
        elif waveform == Waveform.parabola:
            self.wave = ParabolaWaveImpl1()

        self.wave.populate(n_sum_limit)
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


class ParabolaWaveImpl1(WaveImpl1):

    def __init__(self, n_sum_limit: int = 0):
        super().__init__(n_sum_limit)
        self.a_initial = math.pow(math.pi, 2) / 3

    def method_impl(self, i: float = 0.0, time: float = 0.0):
        super().method_impl(i, time)
        t = time
        h = (4 * math.pow(-1, i)) / math.pow(i, 2)
        return h * math.cos(i * t)


class FourierWaveImpl2(Fourier):
    def __init__(self, q: ModelRequestObj, waveform: str, frequency: float = 0.0, duty_cycle=None, width=None):
        super().__init__(q)
        self.model += "_waveform:_" + waveform
        self.title = self.model
        self.lineSeriesValueY = "y_" + self.model
        self.lineSeriesName = self.lineSeriesValueY
        self.wave = None
        self.duty_cycle = None
        self.width = None
        if waveform == Waveform.square:
            self.wave = SquareWaveImpl2(q)
            self.wave.populate(q, frequency=frequency, duty_cycle=duty_cycle)
            self.duty_cycle = self.wave.duty_cycle
        elif waveform == Waveform.triangle:
            self.wave = TriangleWaveImpl2(q)
            self.wave.populate(q, frequency=frequency, width=width)
            self.width = self.wave.width
        elif waveform == Waveform.parabola:
            self.wave = ParabolaWaveImpl2(q)
            self.wave.populate(q, frequency=frequency)

        self.duration = self.wave.duration
        self.sampling_frequency = self.wave.sampling_frequency
        self.frequency = self.wave.frequency

        t = UtilsJSONEncoder()
        t.encode(self.wave)


class WaveImpl2:

    def __init__(self, q: ModelRequestObj, frequency: float = 0.0, duty_cycle: float = 0.0, width: float = 0.0):
        self.duration = q.index_stop - q.index_start
        self.sampling_frequency = self.duration / q.increment
        self.frequency = frequency
        self.duty_cycle = duty_cycle
        self.width = width
        self.wave_data = []
        self.custom_params = {}

    def set_custom_params(self, params: dict):
        self.custom_params = params

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

    def populate(self, q: ModelRequestObj, frequency: float = 0.0, duty_cycle: float = 0.0, width: float = 0.0):
        super().populate(q=q, frequency=frequency, width=width)
        t = np.linspace(q.index_start, q.index_stop, int(self.sampling_frequency), endpoint=False)
        self.wave_data = signal.sawtooth(2 * np.pi * self.frequency * t, width=self.width).tolist()

    def np_wave(self, q: ModelRequestObj):
        super().np_wave(q)
        t = np.linspace(q.index_start, q.index_stop, int(self.sampling_frequency), endpoint=False)
        return signal.sawtooth(2 * np.pi * self.frequency * t, width=self.width).tolist()


class CustomWaveImpl2(WaveImpl2):

    def __init__(self, q: ModelRequestObj, frequency: float = 0.0, duty_cycle: float = 0.0, width: float = 0.0):
        super().__init__(q=q, frequency=frequency)
        self.custom_params["a"] = -1.0

    def populate(self, q: ModelRequestObj, frequency: float = 0.0, duty_cycle: float = 0.0, width: float = 0.0):
        super().populate(q=q, frequency=frequency)
        t_partial = self.fetch_t_partial(q)
        self.wave_data = self.generate_wave(q, t_partial).tolist()

    def fetch_t_partial(self, q: ModelRequestObj):
        return np.linspace(q.index_start, q.index_start + self.duration / self.frequency,
                                int(self.sampling_frequency / self.frequency), endpoint=False)

    def generate_wave(self, q: ModelRequestObj, t_partial):
        o = self.wave_equation(q, t_partial)
        o_add = self.wave_equation(q, t_partial)
        for i in range(0, int(self.frequency - 1)):
            o = np.concatenate((o, o_add))
        return o

    def wave_equation(self, q: ModelRequestObj, t):
        return t

    def np_wave(self, q: ModelRequestObj):
        super().np_wave(q)
        t_partial = self.fetch_t_partial(q)
        return self.generate_wave(q, t_partial)


class ParabolaWaveImpl2(CustomWaveImpl2):

    def wave_equation(self, q: ModelRequestObj, t):
        super().wave_equation(q, t)
        a = float(self.custom_params["a"])
        x0 = q.index_start
        x1 = q.index_start + self.duration/self.frequency
        return a * (t - x0) * (t - x1)


class FourierTransformFFT(Template):

    def __init__(self, q: ModelRequestObj, o: FourierWaveImpl2, waveform: str):
        super().__init__(q)

        self.xAxisTitleText = UnitsLabel.frequency_hertz
        self.yAxisTitleText = UnitsLabel.units

        self.model += "_waveform:_" + waveform
        self.title = self.model
        self.lineSeriesValueY = "y_" + self.model
        self.lineSeriesName = self.lineSeriesValueY

        self.sampling_frequency = None
        self.frequency = None
        self.duration = None
        self.duty_cycle = None
        self.width = None
        self.fft_shifted = []
        self.freq_shifted = []

        if waveform == Waveform.square:
            self.populate(o.wave.np_wave(q), o.wave.sampling_frequency, o.wave.frequency, o.wave.duration,
                          duty_cycle=o.wave.duty_cycle)
        elif waveform == Waveform.triangle:
            self.populate(o.wave.np_wave(q), o.wave.sampling_frequency, o.wave.frequency, o.wave.duration,
                          width=o.wave.width)
        elif waveform == Waveform.parabola:
            self.populate(o.wave.np_wave(q), o.wave.sampling_frequency, o.wave.frequency, o.wave.duration)

    def populate(self, signal_s, sampling_frequency, frequency, duration, duty_cycle: float = None,
                 width: float = None):

        self.sampling_frequency = sampling_frequency
        self.frequency = frequency
        self.duration = duration
        self.duty_cycle = duty_cycle
        self.width = width

        # Perform the FFT
        # The FFT result is complex, so we take the absolute value for magnitude
        # and shift the zero-frequency component to the center for better visualization.
        fft_result = np.fft.fft(signal_s)
        fft_magnitude = np.abs(fft_result)
        self.fft_shifted = np.fft.fftshift(fft_magnitude).tolist()

        # Generate frequency array
        # The frequencies corresponding to the FFT result
        frequencies = np.fft.fftfreq(len(signal_s), 1 / self.sampling_frequency)
        self.freq_shifted = np.fft.fftshift(frequencies).tolist()

    def iterate(self, index, i):
        super().iterate(index, i)
        self.data_point = self.fft_shifted[index]

    def simulate_model(self):
        index = 0
        for i in np.arange(self.index_start, self.index_stop, self.increment):
            self.iterate(index, i)
            f = self.freq_shifted[index]
            bounds = self.frequency * 10
            if (self.limit_bounds and np.abs(f) < bounds) or not self.limit_bounds:
                data_item = {self.lineSeriesValueX: f, self.lineSeriesValueY: self.data_point}
                self.data.append(data_item)
            index += 1
