#!/bin/bash
set -e
echo -e " ... running twine to deploy ... "
pip install twine
echo -e "twine upload --skip-existing --username \"${PYPI_USERNAME}\" --password \"${PYPI_PASSWORD}\" ${TRAVIS_BUILD_DIR}/wheelhouse/*"
#twine upload --skip-existing --username "${PYPI_USERNAME}" --password "${PYPI_PASSWORD}" ${TRAVIS_BUILD_DIR}/wheelhouse/*
