from typing import Callable, Optional, Dict, List

import util as utl
import metamodel_eazyraspi as me
import exceptions_eazyraspi as ee


def validate_activation_buttons(func):
	def wraped(stm: me.Rutine, *args: list, erp: me.EazyRasPi, **kwargs: dict) -> str:
		if stm.rutActivation and stm.rutActivation.button:
			ruts = [stm.name]
			tbutton = stm.rutActivation.button.button
			for r in erp.rutButton:
				button = r.rutActivation.button.button
				if tbutton == button: ruts.append(r.name)
			if len(ruts) > 1: print('Rutines "%s" on same button "%s"!!!' % (ruts, tbutton))
		return func(stm, *args, erp=erp, **kwargs)
	return wraped


def validate_activation_rutine_name(fun: Callable[[list, dict], str]) -> Callable:
	def wraped(stm: me.Rutine, *args: list, **kwargs: dict) -> str:
		if stm.rutActivation and stm.name == None: print('Rutines that are being activeted by an activation method should have names!!!')
		return fun(stm, *args, **kwargs)
	return wraped


def validate_logger_format(func):
	def wraped(stm: List[me.Program], *args: list, **kwargs: dict) -> str:
		stms, format = utl.get_classes('logFormat',  stm), None
		for p in stms:
			if p.format: format = p.format
			if p.path: open(p.path, 'r').read()
		if format != None:
			ok = False
			if '#FILENAME#' in format: ok = True
			elif '#DATE#' in format: ok = True
			elif '#TIME#' in format: ok = True
			elif '#DATETIME#' in format: ok = True
			elif '#FORMATEDDATE#' in format: ok = True
			elif '#GARBAGE#' in format: ok = True
			if not ok: print('Bad log format!!!')
		return func(stm, *args, **kwargs)
	return wraped


def run_def(fun: Callable[[list, dict], str]) -> Callable[[list, dict], str]:
	return lambda *args, **kwargs: fun(*args, **kwargs)


def rutine_fun_check(fun: Callable[[list, dict], str]) -> Callable:
	def wraped(stm: me.RutineCall, *args: list, ruts: Dict[str, me.Rutine], **kwargs: dict) -> str:
		if ruts.get(stm.rutRef, None) == None: raise ee.SematicRutineError('Rutine "%s" does not exist!!!' % stm.rutRef, stm)
		return fun(stm, *args, ruts=ruts, **kwargs)
	return wraped


def rutine_fun_create(fun: Callable[[list, dict], str]) -> Callable:
	def wraped(stm: me.Rutine, *args: list, ruts: Dict[str, me.Rutine], **kwargs: dict) -> str:
		if stm.name: ruts[stm.name] = stm
		return fun(stm, *args, ruts=ruts, **kwargs)
	return wraped


def rutine_fun_socpe(fun: Callable[[list, dict], str]) -> Callable:
	def wraped(*args: list, ruts: Optional[Dict[str, me.Rutine]] = None, **kwargs: dict) -> str:
		if ruts == None: ruts = {}
		nruts = dict(ruts)
		return fun(*args, ruts=nruts, **kwargs)
	return wraped


def rutine_fun_top(fun: Callable[[list, dict], str]) -> Callable:
	def wraped(stm: me.Program, *args, **kwargs) -> str:
		ruts = {r.name: r for r in utl.get_classes('rutine', stm)}
		return fun(stm, *args, ruts=ruts, **kwargs)
	return wraped


def validate_rutine(top: bool = False, scope: bool = False, create: bool = False, check: bool = False) -> Callable:
	if   top:    return rutine_fun_top
	elif scope:  return rutine_fun_socpe
	elif create: return rutine_fun_create
	elif check:  return rutine_fun_check
	else: return run_def


def variable_fun_check(fun: Callable[[list, dict], str]) -> Callable:
	def wraped(stm: me.Element, *args: list, vars: Dict[str, me.Variable], **kwargs: dict) -> str:
		if vars.get(stm.variable, None) == None: raise ee.SematicVariableError('Variable "%s" does not exist!!!' % stm.variable, stm)
		return fun(stm, *args, **kwargs)
	return wraped


def variable_fun_create(fun: Callable[[list, dict], str]) -> Callable:
	def wraped(stm: me.Variable, *args: list, vars: Dict[str, me.Variable], **kwargs: dict) -> str:
		vars[stm.name] = stm
		return fun(stm, *args, vars=vars, **kwargs)
	return wraped


def variable_fun_socpe(fun: Callable[[list, dict], str]) -> Callable:
	def wraped(*args: list, vars: Optional[Dict[str, me.Variable]] = None, **kwargs: dict) -> str:
		if vars == None: vars = {}
		nvars = dict(vars)
		return fun(*args, vars=nvars, **kwargs)
	return wraped


def validate_variable(scope: bool = False, create: bool = False, check: bool = False) -> Callable:
	if   scope:  return variable_fun_socpe
	elif create: return variable_fun_create
	elif check:  return variable_fun_check
	else: return run_def


# vim: tabstop=3 noexpandtab shiftwidth=3 softtabstop=3
