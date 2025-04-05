from setuptools import setup, find_packages

setup(
    name="ciaprofilegpt",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai",
        "python-dotenv",
        "pydantic",
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "flake8",
        ],
    },
    author="Stef",
    description="A CIA-style psychological profiling tool using GPT models",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "generate-profile=src.examples.example_profile:main",
        ],
    },
) 