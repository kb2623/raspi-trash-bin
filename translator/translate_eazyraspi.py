from typing import List, Optional, NoReturn

from textx.export import model_export
from textx.metamodel import TextXMetaMetaModel

import util as utl
import metamodel_eazyraspi as me
import validate_eazyraspi as ve


# Output file variables
DATE_FORMAT = '%b. %d. %Y %H:%M:%S'
LOGGER_FORMAT = 'sample_format.tmp'
LOGGER_PATH = 'data'


def proc_head(stm: me.Head, *args: list, **kwargs: dict) -> str:
	if stm is None: return ''
	prog = ''
	if stm.progName: prog += '# Program %s\n' % (stm.progName.name if stm.progName.name else stm.progName.namen.replace(utl.END, '%s#\t' % utl.END))
	if stm.author: prog += '# Author %s\n' % (stm.author.author if stm.author.author else stm.author.authorn.replace(utl.END, '%s#\t' % utl.END))
	if stm.license: prog += '# License %s\n' % (stm.license.license if stm.license.license else stm.license.licensen.replace(utl.END, '%s#\t' % utl.END))
	return '%s%s' % (prog, utl.END * 2)


def proc_date_format(stm: List[me.Program], *args: list, **kwargs: dict) -> str:
	format, stms = DATE_FORMAT, utl.get_classes('dateFormat', stm)
	for p in stms: format = p.dateformat
	prog = 'date_format = "%s"%s' % (format, utl.END)
	return prog


@ve.validate_logger_format
def proc_logger_format(stm: List[me.Program], *args: list, **kwargs: dict) -> str:
	format, path, stms = None, None, utl.get_classes('logFormat', stm)
	for p in stms:
		if p.format: format = p.format
		if p.path: path = p.path
	prog = 'logger_format = '
	if format: prog += '"""%s"""%s' % (format, utl.END)
	elif path: prog += '"""%s"""%s' % (open(path, 'r').read(), utl.END)
	else: prog += '"""%s"""%s' % (open(LOGGER_FORMAT, 'r').read(), utl.END)
	return prog


@ve.validate_activation_buttons
@ve.validate_activation_rutine_name
@ve.validate_rutine(create=True)
@ve.validate_variable(scope=True)
def proc_rutine(stm: me.Rutine, level: int, erp: me.EazyRasPi, *args: list, **kwargs: dict) -> str:
	if not stm.name:
		stm.name = 'anon_%d' % erp.COUNT
		erp.COUNT += 1
	if stm.rutActivation and stm.rutActivation.button: erp.rutButton.append(stm)
	if stm.rutActivation and stm.rutActivation.time: erp.rutTime.append(stm)
	prog = '%sdef %s():%s' % (utl.insert_indent(level), stm.name, utl.END)
	if stm.statements: prog += proc_statemets(stm.statements, level + 1, *args, erp=erp, **kwargs)
	else: prog += '%sreturn None' % utl.insert_indent(level + 1)
	return '%s%s%s' % (prog, utl.END, utl.END)


def proc_returnstm(stm: me.ReturnStm, level: int, *args: list, **kwargs: dict) -> str:
	expr = proc_expression(stm.expression, *args, **kwargs)
	return '%sreturn %s%s' % (utl.insert_indent(level), expr, utl.END)


@ve.validate_rutine(scope=True)
@ve.validate_variable(scope=True)
def proc_ifstm(stm: me.IfStm, level: int, *args: list, **kwargs: dict) -> str:
	cond_expr = proc_expression(stm.condition, *args, **kwargs)
	prog = '%sif %s:%s' % (utl.insert_indent(level), cond_expr, utl.END)
	prog += proc_statemets(stm.statements, level + 1, *args, **kwargs)
	if stm.elseif:
		for s in stm.elseif:
			cond_elif_expr = proc_expression(s.condition, *args, **kwargs)
			prog += '%selif %s:%s' % (utl.insert_indent(level), cond_elif_expr, utl.END)
			prog += proc_statemets(s.statements, level + 1, *args, **kwargs)
	if stm.melse:
		prog += '%selse:%s' % (utl.insert_indent(level), utl.END)
		prog += proc_statemets(stm.melse.statements, level + 1, *args, **kwargs)
	return prog


@ve.validate_rutine(scope=True)
@ve.validate_variable(scope=True)
def proc_whilestm(stm: me.WhileStm, level: int, *args: list, **kwargs: dict) -> str:
	cond_expr = proc_expression(stm.condition, *args, **kwargs)
	prog = '%swhile %s:%s' % (utl.insert_indent(level), cond_expr, utl.END)
	prog += proc_statemets(stm.statements, level + 1, *args, **kwargs)
	return prog


@ve.validate_rutine(scope=True)
@ve.validate_variable(scope=True)
def proc_controlstm(stm: me.ControlStm, level: int, *args: list, **kwargs: dict) -> str:
	prog = ''
	if   stm.returnstm: prog += proc_returnstm(stm.returnstm, level, *args, **kwargs)
	elif stm.ifstm:     prog += proc_ifstm(stm.ifstm, level, *args, **kwargs)
	elif stm.whilestm:  prog += proc_whilestm(stm.whilestm, level, *args, **kwargs)
	else: print('Bad statement <proc_controlstm>: "%s"!!!' % stm)
	return prog


def proc_static_array(stm: me.StaticArrayStm, *args: list, **kwargs: dict) -> str:
	return '[%s]' % ','.join(proc_expression(e, *args, **kwargs) for e in stm.exprs)


def proc_rand(stm: me.RandStm, *args: list, **kwargs: dict) -> str:
	prog = 'np.random.'
	if stm.arg1:
		prog += 'randint'
		if stm.arg2: prog += '(%s, %s)' % (proc_expression(stm.arg1, *args, **kwargs), proc_expression(stm.arg2, *args, **kwargs))
		else:         prog += '(%s)'     % (proc_expression(stm.arg1, *args, **kwargs))
	else:	prog += 'choice(%s, 1)[0]' % (proc_static_array(stm.argc, *args, **kwargs))
	return prog


def proc_led(stm: me.LedStm, *args: list, **kwargs: dict) -> str:
	color = None
	if   stm.green: color = 'green'
	elif stm.blue:  color = 'blue'
	elif stm.red:   color = 'red'
	else: print('Bad production <proc_lec>: "%s"!!!' % stm)
	return '%s.%s' % (stm.name, color)


@ve.validate_rutine(check=True)
def proc_rutcall(stm: me.RutineCall, *args: list, **kwargs: dict) -> str:
	return '%s()' % stm.rutRef


@ve.validate_variable(check=True)
def proc_variable(stm: me.Element, *args: list, **kwargs: dict) -> str:
	return stm.variable


def proc_element(stm: me.Element, *args: list, **kwargs: dict) -> str:
	if   stm.garbage:  return 'mesure_garbage()'
	elif stm.lid:      return 'buttonOP.is_pressed'
	elif stm.boolean:  return 'False' if stm.boolean == 'false' else 'True'
	elif stm.rand:     return proc_rand(stm.rand, *args, **kwargs)
	elif stm.led:      return proc_led(stm.led, *args, **kwargs)
	elif stm.expr:     return '(%s)' % proc_expression(stm.expr, *args, **kwargs)
	elif stm.rutCall:  return proc_rutcall(stm.rutCall, *args, **kwargs)
	elif stm.float:    return '%s' % stm.float
	elif stm.int:      return '%s' % stm.int
	elif stm.variable: return proc_variable(stm, *args, **kwargs)
	else: print('Bad production <proc_element>: "%s"!!!' % stm)
	return '0'


def proc_factor(stm: me.Factor, *args: list, **kwargs: dict) -> str:
	prog, sign = proc_element(stm.element, *args, **kwargs), stm.sign
	if sign:
		if   sign.neg: prog = 'not %s' % prog
		elif sign.min: prog = '-%s'    % prog
	return prog


def proc_term(stm: me.Term, *args: list, **kwargs: dict) -> str:
	prog = proc_factor(stm.loper, *args, **kwargs)
	for e in utl.merge_list(stm.operations, stm.ropers):
		roper = proc_term(e[1], *args, **kwargs)
		if   e[0].mul: prog += ' * %s' % roper
		elif e[0].div: prog += ' / %s' % roper
		elif e[0].amd: prog += ' and %s' % roper
		elif e[0].pow: prog += ' ** %s' % roper
	return prog


def proc_expression(stm: me.Expression, *args: list, **kwargs: dict) -> str:
	prog = proc_term(stm.loper, *args, **kwargs)
	for e in utl.merge_list(stm.operations, stm.ropers):
		roper = proc_expression(e[1], *args, **kwargs)
		if   e[0].ltq: prog += ' <= %s' % roper
		elif e[0].gtq: prog += ' >= %s' % roper
		elif e[0].equ: prog += ' == %s' % roper
		elif e[0].oor: prog += ' or %s' % roper
		elif e[0].add: prog += ' + %s'  % roper
		elif e[0].sub: prog += ' - %s'  % roper
		elif e[0].gt:  prog += ' > %s'  % roper
		elif e[0].lt:  prog += ' < %s'  % roper
	return prog


def proc_led_set(stm: me.LedStm, *args: list, **kwargs: dict) -> str:
	return '%s = %s' % (proc_led(stm.led, *args, **kwargs), proc_expression(stm.expr, *args, **kwargs))


def proc_rotate(stm: me.RotateStm, *args: list, **kwargs: dict) -> str:
	degre, speed = proc_expression(stm.arg1, *args, **kwargs), 1
	if stm.arg2: speed = proc_expression(stm.arg2, *args, **kwargs)
	return 'rotate_%s(%s, speed=%s)' % ('right' if stm.right else 'left', degre, speed)


def proc_move(stm: me.MoveStm, *args: list, **kwargs: dict) -> str:
	distance, speed = proc_expression(stm.arg1, *args, **kwargs), 1
	if stm.arg2: speed = proc_expression(stm.arg2, *args, **kwargs)
	return 'move_%s(%s, speed=%s)' % ('backword' if stm.backword else 'forward', distance, speed)


@ve.validate_variable(create=True)
def proc_variable_set(stm: me.Variable, *args: list, **kwargs) -> str:
	return '%s = %s' % (stm.name, proc_expression(stm.expression, *args, **kwargs))


@ve.validate_rutine(scope=True)
@ve.validate_variable(scope=True)
def proc_statemets(stm: List[me.Statement], level: int = 0, *args: list, **kwargs: dict) -> str:
	prog = ''
	for s in stm:
		if   utl.is_class(s, 'GarbageStm'): prog += '%s%s%s' % (utl.insert_indent(level), 'mesure_garbage_rut()', utl.END)
		elif utl.is_class(s, 'LidStm'):     prog += '%s%s%s' % (utl.insert_indent(level), 'open_lid()' if s.open else 'close_lid()', utl.END)
		elif utl.is_class(s, 'SleepStm'):   prog += '%s%s(%s)%s' % (utl.insert_indent(level), 'sleep', proc_expression(s.time, *args, **kwargs), utl.END)
		elif utl.is_class(s, 'LedSetStm'):  prog += '%s%s%s' % (utl.insert_indent(level), proc_led_set(s, *args, **kwargs), utl.END)
		elif utl.is_class(s, 'RotateStm'):  prog += '%s%s%s' % (utl.insert_indent(level), proc_rotate(s, *args, **kwargs), utl.END)
		elif utl.is_class(s, 'MoveStm'):    prog += '%s%s%s' % (utl.insert_indent(level), proc_move(s, *args, **kwargs), utl.END)
		elif utl.is_class(s, 'RutineCall'): prog += '%s%s%s' % (utl.insert_indent(level), proc_rutcall(s, *args, **kwargs), utl.END)
		elif utl.is_class(s, 'Variable'):   prog += '%s%s%s' % (utl.insert_indent(level), proc_variable_set(s, *args, **kwargs), utl.END)
		elif utl.is_class(s, 'ControlStm'): prog += proc_controlstm(s, level, *args, **kwargs)
		elif utl.is_class(s, 'ScopeStm'):   prog += proc_statemets(s.statements, level + 1, *args, **kwargs)
		elif utl.is_class(s, 'Rutine'):     prog += proc_rutine(s, level, *args, **kwargs)
		else: print('Bad statement <proc_statemets>: "%s"!!!' % s)
	return '%s' % prog


@ve.validate_rutine(top=True)
@ve.validate_variable(scope=True)
def proc_rutines(stm: List[me.Program], level: int = 0, *args: list, **kwargs: dict) -> str:
	prog, ruts = '', utl.get_classes('rutine', stm)
	for r in ruts: prog += proc_rutine(r, level, *args, **kwargs)
	return '%s' % prog


def make_main(erp: me.EazyRasPi, *args: list, **kwargs: dict) -> str:
	prog = 'if __name__ == "__main__":%s' % utl.END
	prog += '%sos.mkdir(data_dir)%s' % (utl.insert_indent(1), utl.END)
	for r in erp.rutButton:
		for button in r.rutActivation.button.button:
			if   button == 'b1': prog += '%sbutton1.when_pressed = %s%s' % (utl.insert_indent(1), r.name, utl.END)
			elif button == 'b2': prog += '%sbutton2.when_pressed = %s%s' % (utl.insert_indent(1), r.name, utl.END)
			elif button == 'b3': prog += '%sbutton3.when_pressed = %s%s' % (utl.insert_indent(1), r.name, utl.END)
			else: print('Bad button selected!!!')
	prog += '%sruts = [%s' % (utl.insert_indent(1), utl.END)
	prog += '%sProcess(target=start_server),%s' % (utl.insert_indent(2), utl.END)
	prog += '%sProcess(target=prut_fun, args=(mesure_garbage_rut,), kwargs={"format_tmp": logger_format}),%s' % (utl.insert_indent(2), utl.END)
	for r in erp.rutTime:
		for time in r.rutActivation.time.time: prog += '%sProcess(target=prut_fun, args=(%s,), kwargs={"rep_time": %s}),%s' % (utl.insert_indent(2), r.name, time, utl.END)
	prog += '%s]%s' % (utl.insert_indent(1), utl.END)
	prog += '%s%s%s' % (utl.insert_indent(1), 'for r in ruts: r.start()', utl.END)
	prog += '%s%s%s' % (utl.insert_indent(1), 'while input("Exit [yes/no]: "): continue', utl.END)
	prog += '%s%s%s' % (utl.insert_indent(1), 'for r in ruts: r.join()', utl.END)
	return prog


def proc_program(stm: List[me.Program], *args: list, **kwargs: dict) -> str:
	prog = proc_server(stm, *args, **kwargs)
	prog += proc_date_format(stm, *args, **kwargs)
	prog += proc_logger_format(stm, *args, **kwargs)
	prog += '%s%s' % (utl.END * 2, proc_rutines(stm, *args, **kwargs))
	prog += make_main(*args, **kwargs)
	return '%s%s' % (prog, utl.END * 2)


def proc_server(stm: List[me.Program], *args: list, **kwargs: dict) -> str:
	serverData, serverPort, stms = 'data', 8080, utl.get_classes('server', stm)
	for s in stms:
		if s.serverData:   serverData = s.serverData.dataDir
		elif s.serverPort: serverPort = s.serverPort.portNumber
	prog = 'data_dir = "%s"%sserver_port = %d%s' % (serverData, utl.END, serverPort, utl.END)
	return prog


def translate(model: me.EazyRasPi, *args: list, **kwargs: dict) -> str:
	erp = me.EazyRasPi()
	libs = 'import os%sfrom multiprocessing import Process%sfrom default_methods import *%sfrom default_server import *%sfrom default_sound import *%s' % (utl.END, utl.END, utl.END, utl.END, utl.END * 3)
	head = proc_head(model.head, *args, **kwargs)
	prog = proc_program(model.program, *args, erp=erp, **kwargs)
	return '%s%s%s' % (head, libs, prog)


def process_source(model: TextXMetaMetaModel, source: str, source_name: Optional[str] = None, plot: bool = False, write: bool = True) -> NoReturn:
	if source_name is None: source_name = 'test'
	try:
		source_model = model.model_from_str(source)
		model_export(source_model, '%s.dot' % source_name)
		if plot: utl.plot_model_show(source_name)
		prog = translate(source_model)
		if write:
			with open('%s.erp.py' % source_name, 'w') as f: f.write(prog)
		return prog
	except Exception as e: raise e
