import pytest

from textx.exceptions import TextXSyntaxError

import metamodel_eazyraspi as me
import translate_eazyraspi as te
import exceptions_eazyraspi as ee


def test_bad_var_ref():
	test = """rut test begin
		a = 10 + 10
		a = b + 100
	end
	"""
	with pytest.raises(Exception) as e:
		metamodel = me.eazyraspi_metamodel()
		te.process_source(metamodel, test, write=False)
	assert e.type == ee.SematicVariableError


def test_bad_var_ref_scope():
	test = """rut test begin
		a = 10 + 10
		begin
			b = a + 100
		end
		a = b + 100
	end
	"""
	with pytest.raises(Exception) as e:
		metamodel = me.eazyraspi_metamodel()
		te.process_source(metamodel, test, write=False)
	assert e.type == ee.SematicVariableError


def test_bad_rut_ref():
	test = """
	rut test begin
		rut test_one begin
		return 10
		end
		a = test_two() + test()
	end
	"""
	with pytest.raises(Exception) as e:
		metamodel = me.eazyraspi_metamodel()
		te.process_source(metamodel, test, write=False)
	assert e.type == ee.SematicRutineError


def test_bad_rut_ref_socpe():
	test = """
	rut test begin
		rut test_one begin
			return 10
			rut test_tow begin
				return 20
			end
			b = test_two() + test_one()
		end
		a = test_two() + test()
	end
	"""
	with pytest.raises(Exception) as e:
		metamodel = me.eazyraspi_metamodel()
		te.process_source(metamodel, test, write=False)
	assert e.type == ee.SematicRutineError


def test_bad_server_data():
	test = """
	server data = "test/dela"
	
	rut test begin
		a = 10 + 10
	end
	"""
	with pytest.raises(Exception) as e:
		metamodel = me.eazyraspi_metamodel()
		te.process_source(metamodel, test, write=False)
	assert e.type == TextXSyntaxError


def test_bad_logger_format():
	test = """
	logger format "test in dela"

	rut test begin
		a = 10 + 10
	end
	"""
	metamodel = me.eazyraspi_metamodel()
	te.process_source(metamodel, test, write=False)


# vim: tabstop=3 noexpandtab shiftwidth=3 softtabstop=3
