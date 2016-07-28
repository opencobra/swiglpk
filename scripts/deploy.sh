#!/bin/bash
set -e
if [[ -n "$TRAVIS_TAG" && "$TRAVIS_BRANCH" == "feature/auto-wheel" ]]; then
	echo -e " ... running twine to deploy ... "
	pip install twine
	twine upload --skip-existing --username "${PYPI_USERNAME}" --password "${PYPI_PASSWORD}" ${TRAVIS_BUILD_DIR}/wheelhouse/*
else
	echo -e " ... skipping deploy as no tagged detected: $TRAVIS_TAG - $TRAVIS_BRANCH ... "
fi
exit 0;
