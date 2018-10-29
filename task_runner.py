
import argparse
import os, subprocess, sys
import ctypes
from contextlib import contextmanager

class RunnerException(Exception):
    pass

class Task(object):

    def __init__(self, body):
        self.body = body
        self.__name__ = getattr(body, "__name__", "")

    def __call__(self):
        print('Running task "{}":\n'.format(self.__name__))
        return self.body(Runner())

    def __repr__(self):
        return 'Task "{}"'.format(self.__name__)

def task(func):
    return Task(func)


class Runner(object):

    def __init__(self):
        self.cwd = ''

    @staticmethod
    def normalize_path(path):
        path = os.path.expanduser(path)
        path = os.path.normpath(path)
        return path

    @contextmanager
    def cd(self, path):
        self.cwd = self.normalize_path(path)
        yield self.cwd
        self.cwd = ''

    def run(self, cmd):
        if self.cwd and not os.path.isdir(self.cwd):
            raise RunnerException('{} is not a directory'.format(self.cwd))
        if self.cwd:
            cmd = 'cd {} && {}'.format(self.cwd, cmd)
        ret = self._run(cmd)
        print(ret.stdout or ret.stderr)
        return ret

    @staticmethod
    def _run(cmd):
        return subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf8',
        )

    def runas(self, cmd):
        # https://stackoverflow.com/questions/130763/request-uac-elevation-from-within-a-python-script/131092
        # https://docs.microsoft.com/en-us/windows/desktop/api/shellapi/nf-shellapi-shellexecutew
        # https://ss64.com/vb/shellexecute.html

        parameters = ('-c "import subprocess; '
            "subprocess.run('{}', shell=True)"
            '"'
        ).format(cmd)

        ret = ctypes.windll.shell32.ShellExecuteW(
            None, # handle to parent window
            'runas', # lpOperation ('verb'): action to be performed
            sys.executable, # lpFile: executable file
            parameters, # lpParameters: parameters to be passed to the application
            None, # lpDirectory: default working directory
            1
        )

        print((
            'Running command:\n'
            'python {}\n'
            'Return code {}'
            ).format(parameters, ret)
        )


def collect_tasks():
    tasks = {}
    module = __import__('__main__')
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, Task):
            tasks[name] = obj
    return tasks

def parse_args(tasks={}):
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--all',
        help='Run all available tasks',
        action='store_true')
    parser.add_argument('command', 
        nargs='*',
        # choices=tasks.keys(), # Causes error in combination with nargs='*', if no arguments are given
        help='Select one or more of: {}'.format(', '.join(tasks.keys())),
        metavar='command',
    )
    args = parser.parse_args()
    if args.all and args.command:
        print('Warning: if the "--all" option is given, no commands need to be specified.\n')
    if args.all:
        return tasks.keys()
    if args.command:
        for command in args.command:
            if command not in tasks:
                print('Error: Invalid command: {}. Select one or more of: {}.\n'.format(
                    command, ', '.join(tasks.keys())
                ))
                return []
        return args.command
    parser.print_help()
    return []
        
def main():
    tasks = collect_tasks()
    commands = parse_args(tasks)
    for command in commands:
        tasks[command]()
