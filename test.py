
import os
from task_runner import task, main
import tempfile

@task
def hello(r):
    print('Hello world\n')

@task
def pwd(r):

    with tempfile.TemporaryDirectory() as tmpdirname:
        path = os.path.join(tmpdirname, 'white spaces')
        os.mkdir(path)
        with r.cd(path) as cwd:
            ret = r.run('pwd')

@task
def restart(r):
    r.runas('net stop Apache2.4 & net start Apache2.4')

if __name__ == '__main__':
    main()
    