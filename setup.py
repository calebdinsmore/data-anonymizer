import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="data_anonymizer",
    version="0.1.7",
    author="Caleb Dinsmore",
    author_email="caleb.dinsmore@edusource.us",
    description="A tool to anonymize data within a CSV",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/calebdinsmore/data-anonymizer',
    license='MIT',
    entry_points={
        'console_scripts': ['data-anonymizer=data_anonymizer.cli:main']
    },
    packages=setuptools.find_packages(),
    install_requires=[
        'faker',
        'ruamel.yaml',
        'pyhashxx',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
