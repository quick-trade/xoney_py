# Copyright 2022 Vladyslav Kochetov. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
from setuptools import find_packages
from distutils.core import setup


with open('README.md') as file:
    long_desc = file.read()

__version__ = "0.0.9dev"

packages = find_packages()
for package in packages:
    if package.startswith("tests"):
        packages.remove(package)

repository_url = "https://github.com/quick-trade/xoney"

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
        "pandas==1.5.1",
        "optuna==2.10.0",
        "scipy==1.9.3"
    ],
    download_url=f"{repository_url}/archive/{__version__}.tar.gz",
    keywords=[
        "trading-bot",
        "trading",
        "portfolio-management",
        "algorithmic-trading",
        "risk-management"
    ],
    license='Apache 2.0',
    classifiers=[
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
)
