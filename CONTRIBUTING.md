# Contributing Guidelines

Thank you for your interest in contributing to our project. Whether it's a bug report, new feature, correction, or additional
documentation, we greatly value feedback and contributions from our community.

Please read through this document before submitting any issues or pull requests to ensure we have all the necessary
information to effectively respond to your bug report or contribution.


## Reporting Bugs/Feature Requests

We welcome you to use the GitHub issue tracker to report bugs or suggest features.

When filing an issue, please check existing open, or recently closed, issues to make sure somebody else hasn't already
reported the issue. Please try to include as much information as you can. Details like these are incredibly useful:

* A reproducible test case or series of steps
* The version of our code being used
* Any modifications you've made relevant to the bug
* Anything unusual about your environment or deployment


## Contributing via Pull Requests
Contributions via pull requests are much appreciated. Before sending us a pull request, please ensure that:

1. You are working against the latest source on the *main* branch.
2. You check existing open, and recently merged, pull requests to make sure someone else hasn't addressed the problem already.
3. You open an issue to discuss any significant work - we would hate for your time to be wasted.

To send us a pull request, please:

1. Fork the repository.
2. Modify the source; please focus on the specific change you are contributing. If you also reformat all the code, it will be hard for us to focus on your change.
3. Ensure local tests pass.
4. Commit to your fork using clear commit messages.
5. Send us a pull request, answering any default questions in the pull request interface.
6. Pay attention to any automated CI failures reported in the pull request, and stay involved in the conversation.

GitHub provides additional document on [forking a repository](https://help.github.com/articles/fork-a-repo/) and
[creating a pull request](https://help.github.com/articles/creating-a-pull-request/).


## Finding contributions to work on
Looking at the existing issues is a great way to find something to contribute on. As our projects, by default, use the default GitHub issue labels (enhancement/bug/duplicate/help wanted/invalid/question/wontfix), looking at any 'help wanted' issues is a great place to start.


## Code of Conduct
This project has adopted the [Amazon Open Source Code of Conduct](https://aws.github.io/code-of-conduct).
For more information see the [Code of Conduct FAQ](https://aws.github.io/code-of-conduct-faq) or contact
opensource-codeofconduct@amazon.com with any additional questions or comments.


## Security issue notifications
If you discover a potential security issue in this project we ask that you notify AWS/Amazon Security via our [vulnerability reporting page](http://aws.amazon.com/security/vulnerability-reporting/). Please do **not** create a public github issue.


## Licensing

See the [LICENSE](LICENSE) file for our project's licensing. We will ask you to confirm the licensing of your contribution.


## Setup a development environment

You can have a look at the Python documentation about [virutal environments](https://docs.python.org/3/library/venv.html).

1. Fork the repository

GitHub provides additional document on [forking a repository](https://help.github.com/articles/fork-a-repo/) and
[creating a pull request](https://help.github.com/articles/creating-a-pull-request/).

2. Install virtual environment

```
python3 -m venv venv    
```

3. Activate virtual environment

```
source venv/bin/activate   
```

4. Deactivate virtual environment

```
(venv) > deactivate   
```

5. Install package locally from source

```
pip install -e .
```

#### Install package dependencies

```
pip install click numpy pandas matplotlib
```


## Publish on PyPI

1. Update the [CHANGELOG.md](CHANGELOG.md) file with a comprehensive list of the changes made since the last release. You can list the commit from the last release.

```
git log <last_tag>..HEAD --oneline
```

2. Commit the [CHANGELOG.md](CHANGELOG.md) file and push it to the origin

```
git add -A
git commit -m "Update CHANGELOG.md for version v0.1.0"
git push
```

3. Create a tag on the main branch (ex: v0.1.0) matching the release version you have used in the change log and push it to the origin

```
git tag v0.1.0
git push origin --tags
```

4. Create a release from the Github interface and add the version [CHANGELOG.md](CHANGELOG.md) content into the release description

## Test Publish on PyPI

1. Create an account on [Test PYPI](https://test.pypi.org/manage/projects/)

2. Create or edit a ~/.pypirc file:

```
[distutils]
  index-servers =
    pypi
    pypitest
  
  [pypi]
  repository=https://pypi.python.org/pypi
  username=__token__
  
  [pypitest]
  repository=https://test.pypi.org/legacy/
  username=__token__

```

3. Create a PyPI account and create a token

4. Build the package:

```
python3 -m build 
```

5. Upload the package:

```
python setup.py sdist upload -r pypitest
```