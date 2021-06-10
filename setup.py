from setuptools import setup

setup(
    name='simpleFEA',
    author='Rob Siegwart',
    description='Simple structural finite element program',
    version=0.1,
    packages=['simpleFEA'],
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'tabulate'
    ]
)