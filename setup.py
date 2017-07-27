import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='koala-serializer',
    version='0.1.0',
    description='A tool for creating serializable objects among programming languages',
    long_description='',
    author='k04la',
    author_email='mdan.hagh@gmail.com',
    url='https://github.com/k04la/serializer',
    keywords=['serialize', 'deserialize', 'object', 'binary'],

    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: GPL License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities'
    ],
    
    license='GPL License, Version 3.0',
    install_requires=[
        'configparser==3.5.0',
        'enum34==1.1.6'
    ],

    packages=[
        'koala_serializer',
        'koala_serializer.code_generators'
    ],

    # Make this executable from command line when installed
    scripts=['koalasc'],
    provides=['koalasc']
)