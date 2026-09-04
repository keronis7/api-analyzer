from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="api-analyzer",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="API Analyzer - инструмент для анализа API-вызовов на веб-сайтах",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/api-analyzer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "selenium>=4.6.0",
        "webdriver-manager>=4.0.0",
        "psutil>=5.9.0",
    ],
    entry_points={
        "console_scripts": [
            "api-analyzer=api_analyzer:main",
        ],
    },
)