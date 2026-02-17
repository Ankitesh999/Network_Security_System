from setuptools import find_packages, setup
from typing import List
# from networksecurity.logging import logging
# from networksecurity.exception import custom_exception

def get_requirements(file_path: str) -> List[str]:
    
    try:
        with open(file_path, 'r') as file:
            requirements = file.read().splitlines()
            #handle -e.
            requirements = [req for req in requirements if req and not req.startswith('-e.')]
            return requirements

    except FileNotFoundError:
        print(f"Requirements file not found: {file_path}")
        return []
    # except custom_exception as e:
    #     print(f"Error reading requirements file: {e}")
    #     return []

setup(
    name='networksecurity',
    version='0.1.0',
    author= 'Ankitesh Tiwari',
    author_email= 'official.ankitesh@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
    description='A package for network security tools and utilities.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)
