# fourier_transform.py

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

    def iterate(self, index):
        super().iterate(index)
        x = index
        self.data_point = self.wave_transform.method(x)


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
