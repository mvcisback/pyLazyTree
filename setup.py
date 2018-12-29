from setuptools import find_packages, setup

setup(name='lazytree',
      version='0.1',
      description='TODO',
      url='https://github.com/mvcisback/pyLazyTree',
      author='Marcell Vazquez-Chanlatte',
      author_email='marcell.vc@eecs.berkeley.edu',
      license='MIT',
      install_requires=[
          'funcy',
          'attrs'
      ],
      packages=find_packages(),
)
