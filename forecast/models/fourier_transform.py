# fourier_transform.py

import numpy as np
from utils import UtilsJSONEncoder, UnitsLabel, WaveTypes
from forecast.models.template import Template
from forecast.models.fourier import FourierWaveImpl2
from models import ModelRequestObj


class FourierTransformFFT(Template):

    def __init__(self, q: ModelRequestObj, o: FourierWaveImpl2, wave_type: str):
        super().__init__(q)

        self.xAxisTitleText = UnitsLabel.frequency_hertz
        self.yAxisTitleText = UnitsLabel.units

        self.model += "_wave_type:_" + wave_type
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

        if wave_type == WaveTypes.square:
            self.populate(o.wave.np_wave(q), o.wave.sampling_frequency, o.wave.frequency, o.wave.duration,
                          duty_cycle=o.wave.duty_cycle)
        elif wave_type == WaveTypes.triangle:
            self.populate(o.wave.np_wave(q), o.wave.sampling_frequency, o.wave.frequency, o.wave.duration,
                          width=o.wave.width)

    def populate(self, signal, sampling_frequency, frequency, duration, duty_cycle: float = None, width: float = None):

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
