try:
	from setuptools import setup
except:
        from distutils.core import setup

packages = ['rightscale']
requires = ['requests']


setup(name='python-rightscale',
      version='0.1.0',
      description='Python wrapper for the Rightscale API',
      author='Brent Naylor',
      author_email='brantai@gmail.com',
      license='MIT',
      package_dir={'rightscale': 'rightscale'},
      url='https://github.com/brantai/python-rightscale',
      packages=packages,
      install_requires=requires,
     )
