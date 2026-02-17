from setuptools import find_packages, setup
from typing import List


def get_requirements(file_path: str) -> List[str]:
    

    try:
        # Reading requirements from file_path
        with open(file_path, 'r') as file:
            requirements = file.read().splitlines()
            # Filter out editable installs (e.g., -e . or -e git+...)
            requirements = [req for req in requirements if req and not req.startswith('-e')]           
            return requirements
    except FileNotFoundError as e:
        print(f"Error reading requirements file: {e}")
        return []

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
