from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="obsidian_workflows",
    version="0.1.0",
    author="Ishaan Bansal",
    description="Convert Obsidian notes into GitHub repositories and issues",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bshaan77/obsidianWorkflows",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        'PyGithub',
        'python-dotenv'
    ],
) 