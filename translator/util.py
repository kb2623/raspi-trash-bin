from os.path import join, dirname
from typing import Optional, List, NoReturn

from graphviz import Source

from textx.export import metamodel_export
from textx.metamodel import TextXMetaMetaModel


# Default formating for output file
IND: str = '\t'
END: str = '\n'


def insert_indent(level: int) -> str:
	res = ''
	for i in range(level): res += '%s' % IND
	return res


def join_dict(d1: Optional[dict] = None, d2: Optional[dict] = None) -> dict:
	ndict = {}
	if d1: ndict.update(d1)
	if d2: ndict.update(d2)
	return ndict


def join_list(l1: Optional[list] = None, l2: Optional[list] = None) -> list:
	nl = []
	if l1: nl.extend(l1)
	if l2: nl.extend(l2)
	return nl


def merge_list(l1: Optional[list] = None, l2: Optional[list] = None) -> List[tuple]:
	if not l1 or not l2: return []
	return [(l1[i], l2[i]) for i in range(0, len(l1))]


def get_classes(name: str, items: list) -> list:
	return [getattr(e, name) for e in items if getattr(e, name, False)]


def is_class(o: type, name: str) -> bool:
	return type(o).__name__ == name


def plot_model_show(file_name: str) -> NoReturn:
	s = Source.from_file('%s.dot' % file_name)
	print('Showing model %s' % file_name)
	s.view()


def plot_model(model: TextXMetaMetaModel) -> NoReturn:
	this_folder = dirname(__file__)
	metamodel_export(model, join(this_folder, 'eazyraspi.dot'))
	plot_model_show('eazyraspi')


# vim: tabstop=3 noexpandtab shiftwidth=3 softtabstop=3
