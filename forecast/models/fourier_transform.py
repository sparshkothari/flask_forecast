# fourier_transform.py

import numpy as np
import utils
from utils import UtilsJSONEncoder, UnitsLabel
from forecast.models.template import Template, GenerateArray, \
    ChartVariables
from models import ModelRequestObj


class FourierTransformArray(GenerateArray):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        q.index_start = -10.0
        q.index_stop = 10.0
        q.increment = 0.01

        if q.base_model == 5:
            self.array.append(FourierTransformSquareWave1(q))
            self.array.append(FourierTransformTriangleWave1(q))
        elif q.base_model == 6:
            self.array.append(FourierTransformSquareWave1(q))
            self.array.append(FourierTransformSquareWave2(q))
            self.array.append(FourierTransformSquareWave3(q))
        elif q.base_model == 7:
            self.array.append(FourierTransformTriangleWave1(q))


class FourierTransformChartVariables(ChartVariables):

    def __init__(self):
        super().__init__()
        self.title += "Fourier Transform"
        self.xAxisTitleText = UnitsLabel.frequency_hertz
        self.yAxisTitleText = UnitsLabel.units


class FourierTransform(Template):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.xAxisTitleText = UnitsLabel.frequency_hertz
        self.yAxisTitleText = UnitsLabel.units
        self.wave_transform = WaveTransform()

        t = UtilsJSONEncoder()
        t.encode(self.wave_transform)

    def iterate(self, index, i):
        super().iterate(index, i)
        x = i
        self.data_point = self.wave_transform.method(x)


class FourierTransformFFT(Template):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.xAxisTitleText = UnitsLabel.frequency_hertz
        self.yAxisTitleText = UnitsLabel.units
        self.sampling_frequency = 0
        self.frequency = 0.0
        self.duration = 0.0
        self.duty_cycle = "N/A"
        self.width = "N/A"
        self.fft_shifted = []
        self.freq_shifted = []

    def populate(self, signal, sampling_frequency, frequency, duration, duty_cycle: float = 0.0, width: float = 0.0):

        self.sampling_frequency = sampling_frequency
        self.frequency = frequency
        self.duration = duration
        self.duty_cycle = duty_cycle
        self.width = width

        # Perform the FFT
        # The FFT result is complex, so we take the absolute value for magnitude
        # and shift the zero-frequency component to the center for better visualization.
        fft_result = np.fft.fft(signal)
        fft_magnitude = np.abs(fft_result)
        self.fft_shifted = np.fft.fftshift(fft_magnitude).tolist()

        # Generate frequency array
        # The frequencies corresponding to the FFT result
        frequencies = np.fft.fftfreq(len(signal), 1 / self.sampling_frequency)
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


class FourierTransformSquareWave(FourierTransform):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.wave_transform = SquareWaveTransform()

        t = UtilsJSONEncoder()
        t.encode(self.wave_transform)


class FourierTransformTriangleWave(FourierTransform):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.wave_transform = TriangleWaveTransform()

        t = UtilsJSONEncoder()
        t.encode(self.wave_transform)


class FourierTransformSquareWave1(FourierTransformSquareWave):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.wave_transform.populate(1.0, 1.0)


class FourierTransformSquareWave2(FourierTransformSquareWave):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.wave_transform.populate(3.0, 1.0)


class FourierTransformSquareWave3(FourierTransformSquareWave):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.wave_transform.populate(5.0, 1.0)


class FourierTransformTriangleWave1(FourierTransformTriangleWave):

    def __init__(self, q: ModelRequestObj):
        super().__init__(q)
        self.wave_transform.populate(1.0, 1.0)


class WaveTransform:

    def __init__(self, period: float = 0.0, amplitude: float = 0.0):
        self.period = period
        self.amplitude = amplitude

    def populate(self, period: float = 0.0, amplitude: float = 0.0):
        self.period = period
        self.amplitude = amplitude

    def method(self, frequency: float = 0.0):
        return frequency


class SquareWaveTransform(WaveTransform):

    def method(self, frequency: float = 0.0):
        super().method(frequency)
        return self.amplitude*utils.sinc_f(frequency * self.period)


class TriangleWaveTransform(WaveTransform):

    def method(self, frequency: float = 0.0):
        super().method(frequency)
        return 0.0
