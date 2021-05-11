from os.path import splitext, basename

from glob import glob
from setuptools import setup, find_packages

setup(name='zoom2youtube',
      version='0.0.1',
      description='Transfer video recordings from the Zoom to YouTube',
      url='https://github.com/Welltory/Zoom2Youtube/',
      author='Welltory',
      author_email='github@welltory.com',
      license='MIT',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
      entry_points={
          'console_scripts': [
              'zoom2youtube=zoom2youtube.main:main',
          ],
      },
      zip_safe=False)
