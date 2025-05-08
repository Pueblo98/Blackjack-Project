from setuptools import setup, find_packages

setup(
    name="blackjack_project",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={{"": "src"}},
    install_requires=[
        "numpy",
        "matplotlib",
    ],
    author="Rufushv1",
    author_email="rufushv@gmail.com",
    description="A Blackjack simulation project",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
)