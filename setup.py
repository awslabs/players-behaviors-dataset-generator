import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="players-behaviors-dataset-generator",
    version="0.1.2",
    author="Frederic Nowak",
    author_email="fredenow@amazon.com",
    description="A simple comand line tool to create game datasets for analytics and machine learning use cases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='game machine learning analytics dataset generator player behaviour',
    url="https://github.com/awslabs/players-behaviors-dataset-generator",
    project_urls={
        "Project Tracker": "https://github.com/awslabs/players-behaviors-dataset-generator/projects",
        "Issue Tracker": "https://github.com/awslabs/players-behaviors-dataset-generator/issues"
    },
    classifiers=[
        "Topic :: Utilities",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT No Attribution License (MIT-0)",
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