import os
import sys
import unittest

from flake8.main import application
from six import StringIO


class CodeStyleTestCase(unittest.TestCase):
    def test_app_python_code_style(self):
        current_path = os.getcwd()
        root_path = os.path.dirname(os.path.dirname(__file__))
        stdout, stderr = sys.stdout, sys.stderr
        try:
            os.chdir(root_path)
            output = StringIO()
            sys.stdout, sys.stderr = output, output
            app = application.Application()
            app.run()
            if app.result_count:
                self.fail('Code style errors:\n%s' % output.getvalue())
        finally:
            sys.stdout, sys.stderr = stdout, stderr
            os.chdir(current_path)
