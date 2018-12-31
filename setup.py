import sys

from setuptools import setup, find_packages

if sys.version_info < (3, 5):
    sys.exit('Oops! Python < 3.5 is not supported')

setup(
    name='2434-youtube-wikiwiki',
    version=0.1,
    url='https://github.com/KarageAgeta/2434-youtube-wikiwiki.git',
    author='Yoko Karasaki',
    author_email='yoko.karasaki@gmail.com',
    description='CLI app to generate statement for WIKIWIKI.jp from にじさんじ\'s Youtube video list',
    packages=find_packages(),
    install_requires=[
        'Flask>=0.12.2',
        'python-dotenv',
        'requests',
        'python-dateutil'
    ],
    tests_require=[
        'pytest>=3',
        'flake8'
    ],
    extras_require={
        'debug': [
            'pytest>=3',
            'flake8'
        ]
    },
)
