if($env:appveyor_repo_tag -eq 'True') {
    "echo [pypi] > %USERPROFILE%\\.pypirc"
    "echo username: Nikolaus.Sonnenschein >> %USERPROFILE%\\.pypirc"
    "echo password: %password% >> %USERPROFILE%\\.pypirc"
    "%WITH_COMPILER% %PYTHON%/python setup.py bdist_wheel sdist upload"
}