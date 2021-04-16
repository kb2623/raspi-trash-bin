from datetime import date, datetime
from time import sleep
from multiprocessing import Lock

import numpy as np
import gpiozero as gpio

from default_server import data_dir


# Led diodi
led1, led2 = gpio.RGBLED(red=9, green=10, blue=11), gpio.RGBLED(red=16, green=20, blue=21)
# Vecfunkciski gumbi
button1, button2, button3 = gpio.Button(3), gpio.Button(4), gpio.Button(17)
# Kontrala pokrova (odprt/zaprt)
buttonPO, buttonPZ = gpio.Button(2), gpio.Button(26)
# Kontrola ovir pri voznji, detekcija ovir (spredaj/zadaj)
buttonOZ, buttonOS = gpio.Button(14), gpio.Button(15)
# Senzor razdalje
distance_sensor = gpio.DistanceSensor(23, 24)
# Motor za premikaje pokrova
lid_motor = gpio.Motor(forward=27, backward=22)
# Motorja za premikaje kante
robot = gpio.Robot(left=(5, 6), right=(13, 19))

# Lock za pokrov
lid_lock = Lock()
# Lock za premikanje
robot_lock = Lock()

# Maksimalna hitros motorjev v m/s
motor_max_speed = .5
# Polmer med kolesoma v m
wheel_radius = .2
# Globina posode v metirh
height = 2

# Format za datum
date_format = '%b-%d-%Y %H:%M:%S'

# Logs
log_out = ''
log_err = ''


def prut_fun(fun, rep_time=18000, *args, **kwargs):
	r"""Utility function for creating preriodic rutines.

	Args:
		fun (Callable[[list, dict], None]): Function for periodic activation.
		rep_time (float): Time before every mesurment repeats.
		args (list): Additional arguments.
		kwargs (dict): Keyword arguments.
	"""
	while True:
		fun(*args, **kwargs)
		sleep(rep_time)


def open_lid(*args, **kwargs):
	r"""Open lid of garbage can.

	Args:
		args (list): Additional arguments.
		kwargs (dict): Keyword arguments.
	"""
	lid_lock.acquire()
	if not buttonPZ.is_pressed:
		lid_motor.backward()
		buttonPZ.wait_for_press()
		lid_motor.stop()
	lid_motor.forward()
	buttonPO.wait_for_press()
	lid_motor.stop()
	lid_lock.release()


def close_lid(*args, **kwargs):
	r"""Close lid of garbage can.

	Args:
		args (list): Additional arguments.
		kwargs (dict): Keyword arguments.
	"""
	lid_lock.acquire()
	if not buttonPO.is_pressed:
		lid_motor.forward()
		buttonPO.wait_for_press()
		lid_motor.stop()
	lid_motor.backward()
	buttonPZ.wait_for_press()
	lid_motor.stop()
	lid_lock.release()


def __move_time(distance, speed):
	r"""Get time to apply the movement.

	Args:
		distance (float): Distance in menters.
		speed (float): Speed of movement in meters per second.
	"""
	return distance / speed


def move_forward(distance, *args, **kwargs):
	r"""Move the robot forward for some distance in meters.

	Args:
		distance (float): Distance in meters to move the robot.
		args (list): Additional arguments.
		kwargs (dict): Keyword arguments.

	Keyword Arguments:
		speed (float): Speed ration in [0, 1].
	"""
	speed_ratio = kwargs.get('speed', 1)
	speed = speed_ratio * motor_max_speed
	time_of_movement = __move_time(distance, speed)
	robot_lock.acquire()
	robot.forward(speed_ratio)
	sleep(time_of_movement)
	robot.stop()
	robot_lock.release()


def move_backword(distance, *args, **kwargs):
	r"""Move the robot backword.

	Args:
		distance (float): Distance in meters to move the robot.
		args (list): Additional arguments.
		kwargs (dict): Keyword arguments.

	Keyword Arguments:
		speed (float): Speed ration in [0, 1].
	"""
	speed_ratio = kwargs.get('speed', 1)
	speed = speed_ratio * motor_max_speed
	time_of_movement = __move_time(distance, speed)
	robot_lock.acquire()
	robot.backward(speed_ratio)
	sleep(time_of_movement)
	robot.stop()
	robot_lock.release()


def __rotation_distance(degrees):
	r"""Get the distance of rotation.

	Args:
		degrees (float): Degress to rotate the object.

	Returns:
		float: Distance in methers.
	"""
	return (2 * np.pi * wheel_radius * degrees) / 360


def rotate_right(degrees, *args, **kwargs):
	r"""Rotate the robot clock wise.

	Args:
		degrees (float): Rotation in degrees.
		*args (list): Additional arguments.
		**kwargs (dict): Keyword arguments.

	Keyword Arguments:
		speed (float): Speed ration in [0, 1].
	"""
	speed_ratio = kwargs.get('speed', 1)
	speed = speed_ratio * motor_max_speed
	distance = __rotation_distance(degrees)
	time_of_movement = __move_time(distance, speed)
	robot_lock.acquire()
	robot.right(speed_ratio)
	sleep(time_of_movement)
	robot.stop()
	robot_lock.release()


def rotate_left(degrees, *args, **kwargs):
	r"""Rotate the robot counter clock wise.

	Args:
		degrees (float): Rotation in degrees.
		args (list): Additional arguments.
		kwargs (dict): Keyword arguments.

	Keyword Arguments:
		speed (float): Speed ration in [0, 1].
	"""
	speed_ratio = kwargs.get('speed', 1)
	speed = speed_ratio * motor_max_speed
	distance = __rotation_distance(degrees)
	time_of_movement = __move_time(distance, speed)
	robot_lock.acquire()
	robot.left(speed_ratio)
	sleep(time_of_movement)
	robot.stop()
	robot_lock.release()


def mesure_garbage(*args, **kwargs):
	r"""Get the distance mesured from lid to garbage.

	Args:
		args (list): Additional arguments.
		kwargs (dict): Keyword arguments.

	Returns:
		float: Distance from lid to garbage.
	"""
	return distance_sensor.distance / height


def current_milli_time():
	r"""Get current time in miliseconds.

	Returns:
		int: Current time in miliseconds.
	"""
	return datetime.now().microsecond


def mesure_garbage_rut(rep_time=18000, file_prefix='garbage_', format_tmp='#DATETIME# #GARBAGE#', *args, **kwargs):
	r"""Periodicy Mesure garbage in the trashcan.

	Args:
		file_prefix (str): Prefix for file names of the garbage collection.
		args (list): Additional arguments.
		kwargs (dict): Keyword arguments.
	"""
	today = date.today()
	mdate, time, formated_date = today.strftime('%d/%m/%Y'), today.strftime('%H:%M:%S'), today.strftime(date_format)
	file_name = '%s_%d' % (file_prefix, current_milli_time())
	data = '%s' % format_tmp
	data = data.replace('#FILENAME#', file_name)
	data = data.replace('#DATE#', mdate)
	data = data.replace('#TIME#', time)
	data = data.replace('#DATETIME#', '%s %s' % (date, time))
	data = data.replace('#FORMATEDDATE#', formated_date)
	data = data.replace('#GARBAGE#', mesure_garbage())
	with open(file_name, 'w') as file: file.write(data)


# vim: tabstop=3 noexpandtab shiftwidth=3 softtabstop=3
