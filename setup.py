from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="task_runner",
    description="A task runner to run shell commands on a local computer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Martin Bierbaum",
    license="MIT",
    py_modules=["task_runner"],
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    install_requires=[],
    python_requires=">=3.6.2",
)
