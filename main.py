import numpy as np
import adi
import matplotlib.pyplot as plt

sample_rate = 1e6
center_freq = 2400e6

sdr = adi.Pluto("ip:192.168.2.1")
sdr.sample_rate = int(sample_rate)

# Config Tx
sdr.tx_rf_bandwidth = int(sample_rate)
sdr.tx_lo = int(center_freq)
sdr.tx_hardwaregain_chan0 = -30

# Config Rx
sdr.rx_lo = int(center_freq)
sdr.rx_rf_bandwidth = int(sample_rate)
sdr.rx_buffer_size = 100000
sdr.gain_control_mode_chan0 = "fast_attack"

# Create QPSK transmit waveform (QPSK, 16 samples per symbol)
num_symbols = 1000
x_int = np.random.randint(0, 4, num_symbols)
x_degrees = x_int*360/4.0 + 45
x_radians = x_degrees*np.pi/180.0
x_symbols = np.cos(x_radians) + 1j*np.sin(x_radians)
samples = np.repeat(x_symbols, 16)

 # The PlutoSDR expects samples to be between -2^14 and +2^14.
samples *= 2**14

# Start the transmitter
sdr.tx_cyclic_buffer = True
sdr.tx(samples)

# Clear buffer first
for i in range (0, 10):
    raw_data = sdr.rx()

# Receive samples
rx_samples = sdr.rx()
print(rx_samples)

# Stop transmitting
sdr.tx_destroy_buffer()

# Calculate power spectral density (frequency domain version of signal)
psd = np.abs(np.fft.fftshift(np.fft.fft(rx_samples)))**2
psd_dB = 10*np.log10(psd)
f = np.linspace(sample_rate/-2, sample_rate/2, len(psd))

# Plot time domain
plt.figure(0)
plt.plot(np.real(rx_samples), np.imag(rx_samples), '.')
plt.plot(np.real(samples/10), np.imag(samples/10), '.')

# Plot freq domain
plt.figure(1)
plt.plot(f/1e6, psd_dB)
plt.xlabel("Frequency [MHz]")
plt.ylabel("PSD")
plt.show()