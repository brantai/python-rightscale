from distutils.core import setup
setup(name='python-rightscale',
      version='0.1.0',
      description='Python wrapper for the Rightscale API',
      author='Brent Naylor',
      author_email='brantai@gmail.com',
      license='MIT',
      url='https://github.com/brantai/python-rightscale',
      packages=['rightscale',],
      install_requires=["requests",],
     )
