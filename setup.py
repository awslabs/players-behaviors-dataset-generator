import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="players-behaviors-dataset-generator",
    version="0.1.0",
    author="Frederic Nowak",
    author_email="fredenow@amazon.com",
    description="A simple comand line tool to create game events data for analytics and machine learning use cases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='game machine learning analytics dataset generator player behavior',
    url="https://github.com/aws-labs/players-behaviors-dataset-generator",
    project_urls={
        "Project Tracker": "https://github.com/aws-labs/players-behaviors-dataset-generator/projects",
        "Issue Tracker": "https://github.com/aws-labs/players-behaviors-dataset-generator/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT-0 License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'click',
        'numpy',
        'pandas',
        'matplotlib'
    ],
    entry_points='''
        [console_scripts]
        pbdg=pbdg.main:main
    ''',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)