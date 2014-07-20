from setuptools import setup
from distutils.sysconfig import get_python_lib
import os

try:
    long_description = open('README.md').read()
except:
    long_description = u"Blog generator for hackers."

setup(
    name='micropress',
    version='0.2.4',
    author='Oleksandr Glushchenko',
    author_email='contact@fluder.co',
    url='https://github.com/glushchenko/micropress',
    scripts = ['micropress'],
    data_files= [(get_python_lib() + '/micropress/%s' % (x[0]), map(lambda y: x[0]+'/'+y, x[2])) for x in os.walk('init/')],
    license='LICENSE.txt',
    description='Blog generator for hackers.',
    long_description=long_description,
    install_requires=[
        'Jinja2',
        'markdown',
        'Werkzeug',
        'watchdog',
    ],
)