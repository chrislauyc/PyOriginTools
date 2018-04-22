from setuptools import setup

# pull version from this file in a way that doesn't require importing
exec(open("PyOriginTools/version.py").read())

setup(
    name='PyOriginTools',
    version=__version__,
    author='Scott W Harden',
    author_email='SWHarden@gmail.com',
    packages=[
                'PyOriginTools',
            ],
    url='http://github.com/swharden/PyOriginTools',
    license='MIT License',
    platforms='any',
    description='tools to simplify interaction with OriginLab using PyOrigin',
    long_description=open("README.rst").read(),
    install_requires=[
       'numpy>=1.8.1',
       'matplotlib>=1.3.1',
    ],
    classifiers=[
       'Programming Language :: Python :: 3',
       'Intended Audience :: Developers',
       'Intended Audience :: Science/Research',
    ]
)