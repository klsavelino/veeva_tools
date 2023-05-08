from setuptools import setup, find_packages

setup(
    name="veeva_tools",
    version="1.0.0",
    description="Toolkit para o Veeva.",
    long_description=open("README.md").read(),
    url="https://github.com/klsavelino/veeva_tools",
    author="Alícia Avelino",
    author_email="aliciamel@ufrrj.br",
    license="MIT",
    packages=find_packages(),
    package_dir="veeva_tools",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=[
        "selenium",
        "keyring",
    ],
)
