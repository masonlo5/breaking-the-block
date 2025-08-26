######################載入套件######################
from setuptools import setup, find_packages


######################專案設定######################
def read_readme():
    """
    讀取 README.md 檔案內容\n
    返回值：README.md 的內容字串，讀取失敗時返回預設描述
    """
    try:
        with open('README.md', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "A simple breakout-style game built with pygame"


setup(
    name="breaking-the-block",
    version="0.1.0",
    packages=find_packages(exclude=("tests", "docs")),
    install_requires=[
        "pygame>=2.0.0",
    ],
    author="",
    description="A simple breakout-style game built with pygame",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
)
