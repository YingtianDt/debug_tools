
from setuptools import setup, find_packages

requirements = [

]

setup(
    name='debug-tools',
    version='0.1',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=requirements,
    test_suite='tests',
)
