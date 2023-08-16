from distutils.util import convert_path
from setuptools import find_packages, setup

module_name = "autonogame"
main_ns = {}
ver_path = convert_path(f"src/{module_name}/version.py")
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
    name=module_name,
    version=main_ns["__version__"],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    license="MIT",
    description="Ogame bot",
    keywords=["ogame", "bot", "hack", "script"],
    long_description_content_type="text/markdown",
    long_description=open("README.md", encoding="utf8").read(),
    install_requires=[
        "cryptography==41.0.3",
        "ogame==8.4.0.22",
    ],
    url="https://github.com/tassoneroberto/autonogame",
    author="Roberto Tassone",
    author_email="roberto.tassone@proton.me",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={
        "console_scripts": [
            "autonogame = autonogame.gui:main",
        ],
    },
)
