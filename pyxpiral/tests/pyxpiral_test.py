"""
Unitary tests for pyxpiral.py.

:author: elcodedocle
:contact: gael.abadin@gmail.com

"""

# pylint:disable=C0103,C0111,W0212,W0611

import logging
import unittest
import pytest

import mock

from .. import pyxpiral

class TestPyxpiral(unittest.TestCase):
	"""
	Unitary tests for Pyxpiral.
	"""

	@classmethod
	def setUpClass(cls):
		'''
		Global setUp.
		'''

		logging.basicConfig(level=logging.INFO)

	def setUp(self):
		'''
		Test setUp.
		'''
		self.ppl = pyxpiral.Pyxpiral()
		self.message = u"Never go full electro (AKA Keep calm and read bits cycling in squared spirals).".decode('utf-8').encode('ascii')

	@pytest.fixture(autouse=True)
	def initdir(self, tmpdir):
		tmpdir.chdir()
		self.tmpdir = tmpdir

	def test_encode(self):
		image = self.ppl.encode(self.message)

	def test_decode(self):
		image = self.ppl.encode(self.message)
		image.save(open("test_decode.bmp", "wb"), format='BMP')
		self.assertEquals(self.ppl.decode("test_decode.bmp"), self.message)

	def test_encode_fractal(self):
		images = self.ppl.encode_fractal(self.message)
		images[0].save(open("test_decode_fractal.bmp", "wb"), format='BMP')
		self.assertEquals(self.ppl.decode("test_decode_fractal.bmp"), self.message)

	def tearDown(self):
		'''
		Test tearDown.
		'''

	@classmethod
	def tearDownClass(cls):
		'''
		Global tearDown.
		'''