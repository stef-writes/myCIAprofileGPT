from setuptools import setup, find_packages
import os
from pathlib import Path

# Get the absolute path to the README file
README_PATH = Path(__file__).parent / "docs" / "README.md"

setup(
    name="ciabot",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=0.19.0",
        "pydantic>=2.0.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.22.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "mypy>=1.0.0",
        ],
    },
    python_requires=">=3.8",
    author="Stefano Paolina",
    author_email="stefano.paolina99@gmail.comm",
    description="CIA Profile Generator using OpenAI's ChatGPT API",
    long_description=README_PATH.read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ciabot",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 