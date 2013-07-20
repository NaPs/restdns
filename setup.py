from setuptools import setup, find_packages
import os

version = '1.0~dev'

base = os.path.dirname(__file__)

readme = open(os.path.join(base, 'README.rst')).read()
changelog = open(os.path.join(base, 'CHANGELOG.rst')).read()

setup(name='restdns',
      version=version,
      description='Rest API for DNS',
      long_description=readme + '\n' + changelog,
      classifiers=[],
      keywords='django dns rest',
      author='Antoine Millet',
      author_email='antoine@inaps.org',
      url='https://github.com/NaPs/Restdns',
      license='MIT',
      data_files=(
          ('/etc/', ('etc/restdns.conf',)),
      ),
      scripts=['restdnsadm'],
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=['django'])
