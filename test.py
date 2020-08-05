import os
import logging
from task_runner import task, main
import tempfile


@task
def hello(r):
    print("Hello world\n")


@task
def pwd(r):

    with tempfile.TemporaryDirectory() as tmpdirname:
        path = os.path.join(tmpdirname, "white spaces")
        os.mkdir(path)
        with r.cd(path):
            r.run("pwd")


@task
def restart(r):
    r.runas("net stop Apache2.4 & net start Apache2.4")


@task
def log(r):
    logging.info("Hello World!")


if __name__ == "__main__":
    main()
