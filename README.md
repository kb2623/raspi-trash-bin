# raspi-trash-bin
Domain specific language for Raspberry Pi for trash bin.

## EBNF

```
EazyRasPi :=
	Head? Program
;

Head :=
	(
		(Author? License? ProgramName?) |
		(License? Author? ProgramName?) |
		(ProgramName? License? Author?) |
		(ProgramName? Author? License?) |
		(License? ProgramName? Author?) |
		(Author? ProgramName? License?) 
	) END*
;

Program :=
	((
		Server       | 
		DateFormat   | 
		LoggerFormat | 
		Rutine
	) END)+
;

DateFormat :=
	'date' 'format' DATEFORMAT
;

LoggerFormat :=
	'logger' 'format' (
		PATH          | 
		LOGGER_FORMAT
	)
;

Server :=
	'server' (
		ServerData |
		ServerPort
	)
;

ServerData :=
	'data' PATH
;

ServerPort :=
	'port' FULLNUM
;

License :=
	'license' '"'? STRING '"'? END
;

ProgramName :=
	'program' '"'? STRING '"'? END
;

Author :=
	'author' '"'? STRING '"'? END
;

Rutine :=
	'rut' ID? RutineActivation? 'begin' END? Statement+ 'end'
;

RutineActivation :=
	ButtonActivation | 
	TimeActivation
;

ButtonActivation :=
	'(' (BUTTON',')* BUTTON ')'
;

TimeActivation :=
	'[' (FULLNUM',')* FULLNUM ']'
;

Statement :=
	(
		Variable   |
		ControlStm |
		Rutine     |
		RutineCall |
		SleepStm   |
		MoveStm    |
		RotateStm  |
		LedSetStm  |
		LidStm     |
		ScopeStm   |
		GarbageStm
	) END
;

ScopeStm :=
	'begin' Statement+ 'end'
;

LidStm :=
	LID (':' (
		'close' |
		'open')
	)
;

GarbageStm :=
	GARBAGE
;

LedSetStm :=
	LedStm Expression
;

SleepStm :=
	'sleep' FLOAT
;

MoveStm :=
	'move' ':' (
		'forward' |
		'backword'
	) Expression Expression?
;

RotateStm :=
	'rotate' ':' (
		'left' |
		'right'
	) Expression Expression?
;

ControlStm :=
	IfStm     |
	WhileStm  | 
	ReturnStm
;

IfStm :=
	'if' Expression 'then' END? Statement+ 'end' (END? ElifStm)* (END? ElseStm)?
;

ElifStm :=
	'elif' Expression 'then' END? Statement+ 'end'
;

ElseStm :=
	'else' END? Statement+ 'end'
;

WhileStm :=
	'while' Expression 'then' END? Statement+ 'end'
;

ReturnStm :=
	'return' Expression?
;

Variable :=
	'var' ID '=' Expression END
;

Expression :=
	(
		Expression (
			'+'   |
			'-'   |
			'and'
		)
	)? Term
;

RandStm :=
	'rand' ((':' 'choice' StaticArrayStm) | Expression)? Expression? END?
;

StaticArrayStm :=
	'[' Expression (',' Expression)* ']'
;

LedStm :=
	ID ':' (
		'r'     |
		'g'     |
		'b'     |
		'red'   |
		'green' |
		'blue'
	)
;

Term :=
	(Term (
		'*' |
		'/' |
		'or'
	))? Factor
;

Factor :=
	Primary ('^' Expression)?
;

Primary :=
	('not' | '-')? Element
;

Element :=
	('(' Expression ')') |
	RutineCall           |
	ID                   |
	INT                  |
	FLOAT                |
	GARBAGE              |
	RandStm              |
	LidStm               |
	LID
;

RutineCall :=
	ID '(' ')'
;

END :=
	'\n' |
	';'
;

BUTTON :=
	'B1' |
	'B2' |
	'B3' |
	'LO' |
	'LC'
;

LED :=
	'led1' |
	'led2' |
	'LED1' |
	'LED2'
;

STRING :=
	(
		'0'..'9' |
		'a'..'z' |
		'A'..'Z' |
		'_'
	)*
;

LOGGER_FORMAT :=
	'"' (
		'0'..'9' |
		'a'..'z' |
		'A'..'Z' |
		'_'      |
		'#'
	)* '"'
;

ID :=
	(
		'a'..'z' |
		'A'..'Z' |
		'_'
	)(
		'1'..'0' |
		'a'..'z' |
		'A'..'Z' |
		'_'
	)*
;

FULLNUM :=
	('0'..'9')+
;

SIGN :=
	'-' |
	'+'
;

INT :=
	SIGN? FULLNUM
;

FLOAT :=
	SIGN? FULLNUM '.' FULLNUM
;

PATH :=
	STRING ('/' STRING)*
;

DATEFORMAT :=
	'"'? (
		DATEFORMATCODES | 
		DATEFORMATSEPARATORS
	)+ '"'?
;

DATEFORMATSEPARATORS :=
	' ' |
	'.' |
	'-' |
	':' |
	'/'
;

DATEFORMATCODES :=
	'%' (
		'a' |
		'A' |
		'w' |
		'd' |
		'b' |
		'B' |
		'm' |
		'y' |
		'Y' |
		'H' |
		'I' |
		'p' |
		'M' |
		'S' |
		'f' |
		'z' |
		'Z' |
		'j' |
		'U' |
		'W' | 
		'c' |
		'x' |
		'X' |
		'G' |
		'u' |
		'V' |
		'%'
	)
;
```