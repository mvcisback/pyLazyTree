from setuptools import find_packages, setup

setup(
    name='lazytree',
    version='0.2.0',
    description='Python library for manipulating infinite trees.',
    url='https://github.com/mvcisback/pyLazyTree',
    author='Marcell Vazquez-Chanlatte',
    author_email='marcell.vc@eecs.berkeley.edu',
    license='MIT',
    install_requires=[
        'attrs',
        'funcy',
    ],
    packages=find_packages(),
)
