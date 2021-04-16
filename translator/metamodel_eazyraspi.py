from typing import TypeVar, List

from textx.metamodel import TextXMetaMetaModel
from textx import metamodel_from_file

# Types
EazyRasPi = TypeVar('textx:eazyraspi.EazyRasPi')
Head = TypeVar('textx:eazyraspi.Head')
Program = TypeVar('textx:eazyraspi.Program')
Rutine = TypeVar('textx:eazyraspi.Rutine')
Variable = TypeVar('textx:eazyraspi.Variable')
Statement = TypeVar('textx:eazyraspi.Statement')
ControlStm = TypeVar('textx:eazyraspi.ControlStm')
Expression = TypeVar('textx:eazyraspi.Expression')
Term = TypeVar('textx:eazyraspi.Term')
Factor = TypeVar('textx:eazyraspi.Factor')
Element = TypeVar('textx:eazyraspi.Element')
RandStm = TypeVar('textx:eazyraspi.RandStm')
LedStm = TypeVar('textx:eazyraspi.LedStm')
RutineCall = TypeVar('textx:eazyraspi.RutineCall')
StaticArrayStm = TypeVar('textx:eazyraspi.StaticArrayStm')
IfStm = TypeVar('textx:eazyraspi.IfStm')
ReturnStm = TypeVar('textx:eazyraspi.ReturnStm')
WhileStm = TypeVar('textx:eazyraspi.WhileStm')
RotateStm = TypeVar('textx:eazyraspi.RotateStm')
MoveStm = TypeVar('textx:eazyraspi.MoveStm')


# white spaces in sources files
WS = ' \t'


class EazyRasPi:
	# Appendix for anonymous functions
	COUNT: int = 0
	# For time activated rutines
	rutTime: List[Rutine] = []
	# For button activated functions
	rutButton: List[Rutine] = []


def metamodel_file(file: str, skipws: bool, ws: str, debug: bool = False, *args: list, **kwargs: dict) -> TextXMetaMetaModel:
	return metamodel_from_file(file, skipws=skipws, ws=ws, debug=debug)


def eazyraspi_metamodel() -> TextXMetaMetaModel:
	return metamodel_file('eazyraspi.tx', skipws=True, ws=WS)
