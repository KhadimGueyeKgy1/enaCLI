from setuptools import setup, find_packages

with open('readme.txt', 'r') as file:
    description = file.read()

setup(
    name='enaCLI',
    version='1.0.5',
    packages=find_packages(),
    package_data={
        'enaCLI.packages': ['webin-cli-7.0.1.jar', 'antibiotics.txt'],
    },
    install_requires=[
        'argparse',
        'Pandas3',
        'lxml',
        'openpyxl>=3.1.0', 
    ],
    entry_points={
        'console_scripts': [
            'enaCLI = enaCLI.__main__:main',
        ],
    },
    author='Khadim GUEYE, Colman O\'Cathail',
    author_email='khadim@ebi.ac.uk , ocathail@ebi.ac.uk',
    description='This script facilitates the submission of projects, samples, runs, assemblies, and other analyses to the public repository ENA (European Nucleotide Archive). It also assists in validating AMR (Antimicrobial Resistance) antibiograms before submission.',
    url='https://github.com/KhadimGueyeKgy1/enaCLI',
    long_description=description,
    long_description_content_type='text/markdown',
)


