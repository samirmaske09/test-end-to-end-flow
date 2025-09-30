from setuptools import setup, find_packages
import os

requirements = []
if os.path.exists("requirements.txt"):
    with open("requirements.txt") as f:
        requirements = [r.strip() for r in f if r.strip() and not r.startswith("#")]

setup(
    name="strands-agentcore",
    version="0.1.0",
    description="Strands AgentCore utils",
    packages=find_packages(exclude=("tests",)),
    install_requires=requirements,
    python_requires=">=3.8",
)
