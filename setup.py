from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="elastic_tools",
    version="0.1.0",
    author="Taiki Iwamura",
    author_email="takki.0206@gmail.com",
    description=("Tools for elastic constants calculation"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iwamura-lab/elastic-tools",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">= 3.7",
    install_requires=[
        "click",
        "dataclasses_json",
        "pymatgen",
    ],
    entry_points={
        "console_scripts": [
            "elastic-tools=elastic_tools.scripts.main:main",
        ]
    },
)
