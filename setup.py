from setuptools import setup, find_packages

setup(
    name="trex-pro",
    version="1.0",
    packages=find_packages(),
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "T-Rex=trex.main:run"
        ]
    },
)