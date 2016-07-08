from setuptools import setup, find_packages

PACKAGE = "foobot"
NAME = "foobot"
DESCRIPTION = "python API wrapper for foobot.io"
AUTHOR = "Welltory"
AUTHOR_EMAIL = "hello@welltory.com"
URL = "https://github.com/Welltory/foobotapi/"
VERSION = __import__(PACKAGE).__version__

REQUIRES = [
    'requests>=2.7',
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=open("README.rst").read(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL,
    packages=find_packages(exclude=["tests.*", "tests"]),
    test_suite='tests',
    install_requires=REQUIRES,
    keywords=['air quality', 'sensor', 'IoT'],
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
    ],
    zip_safe=False,
)