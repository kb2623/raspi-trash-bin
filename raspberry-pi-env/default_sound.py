from multiprocessing import Process, Queue
from threading import Lock

import numpy as np
import pyaudio as pa
import soundfile as sf


audio = pa.PyAudio()
sound_lock = Lock()


class Microphone:
	FORMAT = pa.paFloat32
	CHANNELS = 2
	RATE = 44100
	CHUNK = 1024

	def __init__(self, audio=audio):
		r"""Initialize the microphone

		Args:
			audio (PyAudio): Audio class instance for opening streams.
		"""
		self.stream = audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
		self.queue = Queue
		self.freq_ind = np.arange(self.CHUNK) / (self.CHUNK / self.RATE)

	def run(self):
		r"""Main reading loop."""
		while True: self.queue.put(stream.read(self.CHUNK))

	def get(self):
		r"""Get next data.

		Returns:
			numpy.ndarray: Data samples of size `self.CHUNK`.
		"""
		return self.queue.get()

	def get_processed(self):
		r"""Get processed data.

		1. Data is multiplied with Hamming window.
		2. Data is being prossed with FFT.
		3. Data is presented as absolute value of FFT.

		Returns:
			Tuple[numpy.ndarray, numpy.ndarray]:
				1. Processed data with FFT.
				2. Table of frequencis.
		"""
		return np.abs(np.fft.fft(self.get() * np.hamming(self.CHUNK))), self.freq_ind


def close_audio(*args, **kwargs):
	r"""Terminate all audio devices.

	Args:
		args (list): Additional arguments.
		kwargs (dict): Keyword arguments.
	"""
	if audio is None: return
	sound_lock.acquire()
	audio.terminate()
	audio = None
	sound_lock.release()


def start_recording(mic, *args, **kwargs):
	r"""Start recording in background thread.

	Args:
		mic (Microphone): Instance of microfon to record from.
		args (list): Additional arguments.
		kwargs (dict): Keyword arguments.
	"""
	mic.run()


def play_sound(file_name, *args, **kwargs):
	r"""Method to play a sound from a file in blocking mode.

	Args:
		file_name (str): Path and file name to sound file to play.
		args (list): Additional arguments.
		kwargs (dict): Keyword arguments.
	"""
	if audio is None: return
	sound_lock.acquire()
	sound_data, rate = sf.read(file_name, dtype='float32')
	stream = audio.open(format=pa.paFloat32, channels=sound_data.shape[1], rate=rate, output=True)
	stream.write(data.tostring())
	stream.stop_stream()
	stream.close()
	sound_lock.release()


def play_sound_background(file_name, *args, **kwargs):
	r"""Play sound on a thread.

	Args:
		file_name (str): Path and file name to sound to play.
		args (list): Additional arguments.
		kwargs (dict): Keyword arguments.
	"""
	play_sound_thread = Process(target=play_sound, args=(file_name,))
	play_sound_thread.start()
	play_sound_thread.join()


# vim: tabstop=3 noexpandtab shiftwidth=3 softtabstop=3
