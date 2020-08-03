import setuptools
import os, sys

# 'setup.py publish' shortcut.
if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    sys.exit()

with open("README.md", "r") as f:
    readme = f.read()

setuptools.setup(
    name="more-kedro",
    version="0.2.0",
    author="Jonathan Löfgren",
    author_email="lofgren021@gmail.com",
    description="A collection of utilities and extensions for Kedro",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/jonathanlofgren/more-kedro",
    packages=["more_kedro"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.6",
    install_requires=["kedro>=0.16.0",],
)
