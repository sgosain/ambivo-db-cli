#!/usr/bin/env python3
"""
Setup script for Ambivo MySQL CLI

Professional MySQL CLI client with enhanced features and Ambivo branding.

Author: Hemant Gosain 'Sunny'
Company: Ambivo
License: MIT
"""

from setuptools import setup, find_packages
import os

# Read the README file
current_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open(os.path.join(current_directory, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="ambivo-mysql-cli",
    version="1.0.0",
    author="Hemant Gosain",
    author_email="sgosain@ambivo.com",
    description="Professional MySQL CLI client  - Powered by Ambivo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sgosain@live.com/ambivo-mysql-cli",
    project_urls={
        "Bug Reports": "https://github.com/sgosain@live.com/ambivo-mysql-cli/issues",
        "Source": "https://github.com/sgosain@live.com/ambivo-mysql-cli",
        "Documentation": "https://github.com/sgosain@live.com/ambivo-mysql-cli/wiki",
        "Company": "https://www.ambivo.com",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Database",
        "Topic :: Database :: Database Engines/Servers",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ambivo-mysql=mysql_cli:main",
            "amysql=mysql_cli:main",  # Short alias
        ],
    },
    scripts=["mysql_cli.py"],
    license="MIT",
    keywords="mysql cli database admin terminal interactive ambivo gosain",
)
