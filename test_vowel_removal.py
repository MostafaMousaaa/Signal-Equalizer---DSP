import scipy.fftpack as fft
import numpy as np
import soundfile as sf



# Read the audio file
signal, sampling_rate = sf.read('ILOVE_10sec [vocals].wav')

if len(signal.shape) > 1:
    signal = signal[:, 1]
# Perform FFT on the signal
freq = fft.fft(signal)
# calc magnitude of the signal
magnitude = np.abs(freq)

freqs_bins = fft.fftfreq(len(signal), 1 / sampling_rate)
vowel_formant_ranges = [
    # # # Define formant frequency ranges for "a" vowels (example ranges)
    # (320,340),
    # (640,675),
    # (980,1000),
    # (1300, 1335),
    # (3286,3310),
    # (3950,3969),
    # # # # ####################################################################
    # # # # # Define formant frequency ranges for "O" vowels (example ranges)
    # (210, 220),
    # (270,330),
    # (600,630),
    # (920,940),
    # (1230,1260),
    # (2790,2810),
    # # # ####################################################################
    # bass
    #(0,400),
    #####################################################################
    # (400,530),
    # (600,670),
    # (730,750),
    # (920,950),
    # (980,1010),
    # (1230,1250),
    # (1550,1570),
    # (1650,1660),
    # (1730,1750),
    # (1870,1890),
]   
# Apply bandstop filter: Zero out frequencies around Formant 2 (1000 Hz to 2000 Hz)
# for range in vowel_formant_ranges:
#     low_cutoff = range[0]  # Hz
#     high_cutoff = range[1]  # Hz
#     freq[(np.abs(freqs_bins) >= low_cutoff) & (np.abs(freqs_bins) <= high_cutoff)]*=0

# amplify the signal
freq[(np.abs(freqs_bins) >= 0) & (np.abs(freqs_bins) <= 10000)]*=5

# Perform inverse FFT to get the modified signal
modified_signal = np.real(fft.ifft(freq))

# Write the modified signal to a new file
sf.write('removed.wav', modified_signal, sampling_rate)

    # Define formant frequency ranges for "a" vowels (example ranges)
