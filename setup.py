from setuptools import setup

requirements = [
    'pandas', 
    'requests', 
    'seaborn',
    'jupyter',
    'beautifulsoup4'
]

packages = [
    'mtgstats',
    'mtgstats.scryfall',
    'mtgstats.ligamagic'
]

setup(
    name = "MTG Stats",
    version = "0.0.1",
    author = "Victor Capone",
    install_requires = requirements,
    packages=packages,
    package_dir={'':'src'}
)