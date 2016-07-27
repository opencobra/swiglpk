#!/bin/bash
set -e
echo -e " ... running twine to deploy ... "
twine upload --skip-existing --username Nikolaus.Sonnenschein --password "${PYPIPWD}" ${TRAVIS_BUILD_DIR}/wheelhouse/*
