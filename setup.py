from setuptools import setup, find_packages

setup(
    name="breaking-the-block",
    version="0.1.0",
    packages=find_packages(exclude=("tests", "docs")),
    install_requires=[
        "pygame>=2.0.0",
    ],
    author="",
    description="A simple breakout-style game built with pygame",
    long_description=open('README.md', encoding='utf-8').read() if __name__ == '__main__' else '',
)
