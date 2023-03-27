from setuptools import setup
#https://betterscientificsoftware.github.io/python-for-hpc/tutorials/python-pypi-packaging/

setup(
    name='truthometer',
    version='0.1.2',
    description='Fact checker for GPT and other LLMs',
    url='https://github.com/bgalitsky/Truth-O-Meter-Making-ChatGPT-Truthful',
    author='Boris Galitsky',
    author_email='bgalitsky@hotmail.com',
    license='BSD 2-clause',
    packages=['truthometer'],
    install_requires=[
                      'numpy',
                      'spacy',
                    'requests',
                    'pandas'
                      ],

    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.9',
    ],
)