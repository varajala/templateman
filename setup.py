from setuptools import find_packages, setup


LONG_DESCRIPTION = """# templateman
A simple project template manager written in Python.

Create Python scripts to automate boilerplate code creation,
project templates, or other tasks. Templateman provides a simple
CLI for managing these scripts.

"""


setup(
    name = 'templateman',
    version = '1.0.0',
    description = 'A simple project template manager written in Python.',
    long_description = LONG_DESCRIPTION,
    long_description_content_type = "text/markdown",
    url = "https://github.com/varajala/templateman",
    
    author = 'Valtteri Rajalainen',
    author_email = 'rajalainen.valtteri@gmail.com',

    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        
        "Topic :: Software Development",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],
    
    python_requires = '>=3.7',
    packages = find_packages(),
)
