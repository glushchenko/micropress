from setuptools import setup
from distutils.sysconfig import get_python_lib
from distutils.version import StrictVersion
import os, platform

try:
    long_description = open('README.md').read()
except:
    long_description = u"Blog generator for hackers."

prefix = ''
if StrictVersion('15.0.0') > StrictVersion(platform.release()):
    prefix = get_python_lib()

platform.release()
setup(
    name='micropress',
    version='0.2.19',
    author='Oleksandr Glushchenko',
    author_email='contact@fluder.co',
    url='https://github.com/glushchenko/micropress',
    scripts = ['micropress'],
    data_files= [(prefix + '/micropress/%s' % (x[0]), map(lambda y: x[0]+'/'+y, x[2])) for x in os.walk('init/')],
    license='LICENSE.txt',
    description='Blog generator for hackers.',
    long_description=long_description,
    install_requires=[
        'Jinja2',
        'markdown',
        'Werkzeug',
        'watchdog',
        's3cmd'
    ],
)
