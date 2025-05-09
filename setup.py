from setuptools import setup, find_packages

# Read in your README for the long description
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="blackjack_project",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,            # if you have extra files
    install_requires=[
        "numpy",
        "matplotlib",
    ],
    extras_require={                       # optional dev dependencies
        "dev": ["pytest", "black", "mypy"],
    },
    author="Rufushv1",
    author_email="rufushv@gmail.com",
    description="A Blackjack simulation project",
    long_description=long_description,     # now defined above
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
)
