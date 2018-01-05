# Basic test of parsing.
# Note that since adabot is not a proper Python module with installation in
# site-packages, setup.py, etc. it's somewhat hacky to run unit tests against.
# These tests assume you're running from the root of the adabot repo, for
# example run them as a module from that location as:
#   python3 -m tests.test_circuitpython_libraries
# This is necessary to ensure the tests can import the code they intend to test.
import sys
import unittest

import adabot.circuitpython_libraries as circuitpython_libraries


class TestParseGitmodules(unittest.TestCase):

    def test_real_input(self):
        test_input = \
"""
[submodule "libraries/register"]
	path = libraries/helpers/register
	url = https://github.com/adafruit/Adafruit_CircuitPython_Register.git
[submodule "libraries/bus_device"]
	path = libraries/helpers/bus_device
	url = https://github.com/adafruit/Adafruit_CircuitPython_BusDevice.git
[submodule "libraries/helpers/simpleio"]
	path = libraries/helpers/simpleio
	url = https://github.com/adafruit/Adafruit_CircuitPython_SimpleIO.git
"""
        results = circuitpython_libraries.parse_gitmodules(test_input)
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0][0], 'libraries/register')
        self.assertDictEqual(results[0][1], {
                'path': 'libraries/helpers/register',
                'url': 'https://github.com/adafruit/Adafruit_CircuitPython_Register.git'
            })
        self.assertEqual(results[1][0], 'libraries/bus_device')
        self.assertDictEqual(results[1][1], {
                'path': 'libraries/helpers/bus_device',
                'url': 'https://github.com/adafruit/Adafruit_CircuitPython_BusDevice.git'
            })
        self.assertEqual(results[2][0], 'libraries/helpers/simpleio')
        self.assertDictEqual(results[2][1], {
                'path': 'libraries/helpers/simpleio',
                'url': 'https://github.com/adafruit/Adafruit_CircuitPython_SimpleIO.git'
            })

    def test_empty_string(self):
        results = circuitpython_libraries.parse_gitmodules('')
        self.assertSequenceEqual(results, [])

    def test_none(self):
        results = circuitpython_libraries.parse_gitmodules(None)
        self.assertSequenceEqual(results, [])

    def test_invalid_variable_ignored(self):
        test_input = \
"""
[submodule "libraries/register"]
	path = libraries/helpers/register
	ur l = https://github.com/adafruit/Adafruit_CircuitPython_Register.git
"""
        results = circuitpython_libraries.parse_gitmodules(test_input)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], 'libraries/register')
        self.assertDictEqual(results[0][1], {
                'path': 'libraries/helpers/register'
            })


class TestIsRepoInBundle(unittest.TestCase):

    def test_in_bundle(self):
        bundle_submodules = [('libraries/register', {
            'path': 'libraries/helpers/register',
            'url': 'https://github.com/adafruit/Adafruit_CircuitPython_Register.git'})]
        result = circuitpython_libraries.is_repo_in_bundle(
            'https://github.com/adafruit/Adafruit_CircuitPython_Register.git',
            bundle_submodules)
        self.assertTrue(result)

    def test_differing_url_scheme(self):
        bundle_submodules = [('libraries/register', {
            'path': 'libraries/helpers/register',
            'url': 'https://github.com/adafruit/Adafruit_CircuitPython_Register.git'})]
        result = circuitpython_libraries.is_repo_in_bundle(
            'http://github.com/adafruit/Adafruit_CircuitPython_Register.git',
            bundle_submodules)
        self.assertTrue(result)

    def test_not_in_bundle(self):
        bundle_submodules = [('libraries/register', {
            'path': 'libraries/helpers/register',
            'url': 'https://github.com/adafruit/Adafruit_CircuitPython_Register.git'})]
        result = circuitpython_libraries.is_repo_in_bundle(
            'https://github.com/adafruit/Adafruit_CircuitPython_SimpleIO.git',
            bundle_submodules)
        self.assertFalse(result)


if __name__=='__main__':
    unittest.main()
