
# task_runner.py

## Usage

1.  Create a module named `foo.py` and define a task:

    ```python
    from task_runner import task

    @task
    def hello(r):
        r.run('echo "hello world"')
    ```

    Note: `r` is an instance of `task_runner.Runner`.

2.  Make module `foo.py` executable as a script:

    ```python
    from task_runner import main

    ...

    if __name__ == '__main__':
        main()

3.  Run module `foo.py` as a script, either running all tasks defined in `foo.py` at once:

    ```
    $ python foo.py -a
    ```

    ... or running selected tasks:

    ```
    $ python foo.py hello
    ```

### Change the current working directory

Use the `task_runner.Runner.cd` method as a context manager:

```python
@task
def foo(r):
    with r.cd(<path>) as current_directry:
        print(current_directory)
        r.run(<command>)
```

TODO: implement nested calls to `cd`.

### Run a command as administrator

On Windows, use the `task_runner.Runner.runas` command to run command with elevated privileges. For example,
start apache installed as a service:

```python
@task
def start_apache(r):
    r.runas('net start Apache2.4')
```
