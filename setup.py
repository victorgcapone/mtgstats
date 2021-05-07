from setuptools import setup

requirements = [
    'pandas', 
    'requests', 
    'seaborn',
    'jupyter'
]

setup(
    name = "MTG Stats",
    version = "0.0.1",
    author = "Victor Capone",
    install_requires = requirements
)