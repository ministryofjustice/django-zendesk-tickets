import os
import re
import sys
import unittest

from flake8.engine import get_style_guide
from six import StringIO


class CodeStyleTestCase(unittest.TestCase):
    def test_app_python_code_style(self):
        root_path = os.path.dirname(os.path.dirname(__file__))
        flake8_style = get_style_guide(
            config_file=os.path.join(root_path, 'setup.cfg'),
            paths=[root_path],
        )
        stdout, sys.stdout = sys.stdout, StringIO()
        report = flake8_style.check_files()
        output, sys.stdout = sys.stdout, stdout
        if report.total_errors:
            message = '\n\n'
            line_prefix = re.compile(r'^%s' % root_path)
            output.seek(0)
            for line in output.readlines():
                line = line_prefix.sub('', line).lstrip('/')
                message += line
            self.fail(message)
