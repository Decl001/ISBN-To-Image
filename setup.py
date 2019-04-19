from setuptools import setup
from setuptools import find_packages


with open('requirements.txt') as reqs_f:
    requirements = [line for line in reqs_f]

setup(
    name='ISBNToImage',
    version='1.0',
    description='Module to take an ISBN code and return the cover image of'
        + ' the book it refers to',
    author='Declan Atkins',
    author_email='declanatkins@gmail.com',
    url='https://www.github.com/Decl001/ISBN-to-image',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'image-extractor=isbn_to_image.images_from_excel:main'
        ]
    }
)