import glob
import os
import setuptools

with open("README.txt", "r", encoding="utf-8") as fh:
    long_description = fh.read()

required_files = [
    os.path.join('model', name)
    for name in ('a1_old.txt', 'a2_old.txt', 'a3_old.txt', 'a4_old.txt', 'a5_old.txt')
]

setuptools.setup(
    name="model",
    version="0.0.1",
    author="Liron Data and Avishai Wool",
    description="Context Aware Password Guessability via Multi-Dimensional Rank Estimation",
    long_description=long_description,
    url="",
    packages=['model', 'model.UI'],
    package_data={'': required_files},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
)
