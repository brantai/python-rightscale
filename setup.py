from distutils.core import setup
setup(name='python-rightscale',
      version='0.1.0',
      description='Python wrapper for the Rightscale API',
      author='Brent Naylor',
      author_email='brantai@gmail.com',
      url='https://github.com/brantai/python-rightscale',
      package_dir={'rightscale': 'lib'},
      packages=['rightscale'],
     )
