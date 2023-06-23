from setuptools import setup, find_packages
#https://betterscientificsoftware.github.io/python-for-hpc/tutorials/python-pypi-packaging/

setup(
    name='truthometer',
    version='0.1.13',
    description='Fact checker for GPT and other LLMs',
    url='https://github.com/bgalitsky/Truth-O-Meter-Making-ChatGPT-Truthful',
    author='Boris Galitsky',
    author_email='bgalitsky@hotmail.com',
    license='BSD 2-clause',
    #packages=find_packages(where="truthometer"),
    packages=['truthometer', 'truthometer.external_apis', 'truthometer.nlp_utils', 'truthometer.html',
                'truthometer.nlp_utils.allow_list_manager', 'truthometer.nlp_utils.ner', 'truthometer.nlp_utils.allow_list_manager.resources',
              'truthometer.third_party_models' ],
    install_requires=[
                      'numpy',
                      'spacy',
                    'requests',
                    'pandas'
                      ],
    #include_package_data=True,
    #package_dir={"": "truthometer.nlp_utils.allow_list_manager/resources"},
    #include_package_data=True
    #package_data={'truthometer':['truthometer/nlp_utils/allow_list_manager/resources/*']},
    #                        'truthometer/*.txt']},
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.9',
    ],
)