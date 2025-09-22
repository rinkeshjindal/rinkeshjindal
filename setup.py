"""
Setup script for India Bank Checker package.
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="india-bank-checker",
    version="1.0.0",
    author="India Bank Checker Team",
    author_email="contact@indiabankchecker.com",
    description="A secure Python application for checking bank balances and fixed deposits from major Indian banks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/india-bank-checker",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial",
        "Topic :: Security",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "india-bank-checker=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.json"],
    },
    keywords="banking, finance, india, balance, fixed-deposits, google-sheets, excel",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/india-bank-checker/issues",
        "Source": "https://github.com/yourusername/india-bank-checker",
        "Documentation": "https://github.com/yourusername/india-bank-checker#readme",
    },
)