from setuptools import find_packages
from distutils.core import setup


with open('README.md') as file:
    long_desc = file.read()

__version__ = "0.0.3dev"

packages = find_packages()
for package in packages:
    if package.startswith("tests"):
        packages.remove(package)

repository_url = "https://github.com/quick-trade/xoney"

extras_requirements = {
    "optimization": [
        "optuna==2.10.0"
    ]
}

setup(
    name="xoney",
    author="Vlad Kochetov",
    author_email="quick.trade.proj@gmail.com",
    packages=packages,
    version=__version__,
    description="The powerful python trading framework",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    project_urls={
        'Documentation': 'https://quick-trade.github.io/xoney',
        'Source': 'https://github.com/quick-trade/xoney',
        'Twitter': 'https://twitter.com/quick_trade_tw',
        'Bug Tracker': f"{repository_url}/issues"
    },
    install_requires=[
        "numpy==1.23.1"
    ],
    extras_requirements=extras_requirements,
    download_url=f"{repository_url}/archive/{__version__}.tar.gz",
    keywords=[
        "python3",
        "trading-bot",
        "trading",
        "portfolio-management"
    ],
    license='Apache 2.0',
    classifiers=[
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
)
