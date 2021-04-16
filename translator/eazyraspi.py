import sys
from typing import List, NoReturn, Optional

from textx.metamodel import TextXMetaMetaModel

import util as utl
import metamodel_eazyraspi as me
import translate_eazyraspi as te


# For paring complex programs
sys.setrecursionlimit(4000)

# Formating for output file
utl.END = '\n'


def process_source_files(model: TextXMetaMetaModel, source_files: Optional[List[str]] = None, plot: bool = False) -> NoReturn:
	for sourcef in source_files:
		text_file = open(sourcef, 'r')
		source = text_file.read()
		text_file.close()
		te.process_source(model, source, sourcef, plot=plot)


def main(source_files: list = None, debug: bool = False, plot: bool = False) -> NoReturn:
	eazyraspi_mm = me.metamodel_file('eazyraspi.tx', skipws=True, ws=me.WS, debug=debug)
	if plot: utl.plot_model(eazyraspi_mm)
	if source_files != None: process_source_files(eazyraspi_mm, source_files, plot)


if __name__ == "__main__":
	source_files = ['primer1.erp', 'primer2.erp', 'primer3.erp']
	main(source_files, plot=True)


# vim: tabstop=3 noexpandtab shiftwidth=3 softtabstop=3
