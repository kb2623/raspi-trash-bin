from multiprocessing import Process

from default_methods import *
from default_server import *
from default_sound import *


if __name__ == "__main__":
	server_thread = Process(target=start_server)
	server_thread.start()
	while input('Exit [yes/no]: ') != 'yes': continue
	server_thread.join()


# vim: tabstop=3 noexpandtab shiftwidth=3 softtabstop=3
