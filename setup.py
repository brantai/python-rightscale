try:
    from setuptools import setup
except:
    from distutils.core import setup

from rightscale import VERSION

packages = ['rightscale']
requires = ['requests']


setup(name='python-rightscale',
      version=VERSION,
      description='Python wrapper for the Rightscale API',
      author='Brent Naylor',
      author_email='brantai@gmail.com',
      license='MIT',
      package_dir={'rightscale': 'rightscale'},
      url='https://github.com/brantai/python-rightscale',
      packages=packages,
      install_requires=requires,
      )
