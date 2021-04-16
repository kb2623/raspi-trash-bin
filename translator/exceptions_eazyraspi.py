class SematicVariableError(Exception):
	def __init__(self, msg, stm=None, *args, **kwargs):
		self.msg = msg
		self.stm = stm


class SematicRutineError(Exception):
	def __init__(self, msg, stm=None, *args, **kwargs):
		self.msg = msg
		self.stm = stm
