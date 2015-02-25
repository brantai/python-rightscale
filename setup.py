try:
    from setuptools import setup
except:
    from distutils.core import setup

packages = ['rightscale']


setup(name='python-rightscale',
      version=open('version.txt').read().strip(),
      description='Python wrapper for the Rightscale API',
      author='Brent Naylor',
      author_email='brantai@gmail.com',
      license='MIT',
      package_dir={'rightscale': 'rightscale'},
      url='https://github.com/brantai/python-rightscale',
      packages=packages,
      install_requires=open('requirements.txt').readlines()
      )
