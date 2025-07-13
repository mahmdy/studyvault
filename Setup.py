from setuptools import setup, find_packages

setup(
    name="studyvault",
    version="1.0.0",
    author="Mahmoud Neana",
    description="Interactive CLI tool to store, update, and search Markdown-based study notes.",
    url="https://github.com/mahmdy/studyvault",  # 🔗 Your GitHub repo URL
    license="MIT", 
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "rich",
        "markdown2",
        "reportlab",
        "gnureadline; platform_system == 'Linux'"
    ],
    entry_points={
        "console_scripts": [
            "studyvault=studyvault.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
        "Topic :: Documentation",
    ],
    python_requires=">=3.7",
)
