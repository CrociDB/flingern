from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="flingern",
    version="0.1.0",
    packages=find_packages(),
    install_requires=required,
    entry_points={
        "console_scripts": [
            "flingern = flingern.main:main",
        ],
    },
    author="Bruno Croci",
    author_email="crocidb@gmail.com",
    description="a simple static gallery website generator",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/CrociDB/flingern",
)
