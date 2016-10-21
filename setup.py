from setuptools import setup, find_packages

PACKAGE = "foobot"
NAME = "foobot"
DESCRIPTION = "python API wrapper for foobot.io"
AUTHOR = "Welltory"
AUTHOR_EMAIL = "hello@welltory.com"
URL = "https://github.com/Welltory/python-foobot"
VERSION = __import__(PACKAGE).__version__


requirements = [i.strip() for i in open("requirements.txt").readlines()]

test_requirements = [i.strip() for i in
                     open("requirements_test.txt").readlines()]


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
    tests_require=test_requirements,
    install_requires=requirements,
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