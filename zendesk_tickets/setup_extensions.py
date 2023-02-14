import distutils.log
import os

import setuptools


class ManagementCommand(setuptools.Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from django.core.management import call_command

        self.announce(self.description, level=distutils.log.INFO)
        cwd = os.getcwd()
        try:
            os.chdir(os.path.dirname(__file__))
            call_command(self.management_command, **self.management_command_kargs)
        finally:
            os.chdir(cwd)


class MakeMessages(ManagementCommand):
    description = 'update localisation messages files'
    management_command = 'makemessages'
    management_command_kargs = dict(all=True, no_wrap=True, keep_pot=True)


class CompileMessages(ManagementCommand):
    description = 'compile localisation messages files'
    management_command = 'compilemessages'
    management_command_kargs = dict(fuzzy=False)


command_classes = {
    'makemessages': MakeMessages,
    'compilemessages': CompileMessages,
}
