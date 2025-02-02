# setup.py

from setuptools import setup

setup(
    name="papermill-markdown",
    version="0.1.2",
    packages=["papermill_markdown"],
    description="A converter to transform Markdown into Papermill JSON payloads",
    author="Michael Rustell",
    author_email="mike@inframatic.ai",
    url="https://github.com/CivilEngineerUK/papermill-markdown",
    package_dir={"": "src"},
    install_requires=[
        "pydantic",
        "requests",
        "python-dotenv"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
