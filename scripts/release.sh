
if [[ "$NEW_GLPK_VERSION" != "$SWIGLPK_VERSION" ]]
then
    echo "swiglpk version on PyPI ($SWIGLPK_VERSION) and latest GLPK release ($NEW_GLPK_VERSION) differ. Creating new release on GitHub."
    PAYLOAD=$(printf '{"tag_name": "%s.0","target_commitish": "master","name": "%s.0","body": "Release of version %s","draft": false,"prerelease": false}' $NEW_GLPK_VERSION $NEW_GLPK_VERSION $NEW_GLPK_VERSION)
    curl --data "$PAYLOAD" https://api.github.com/repos/phantomas1234/wheels/releases\?access_token\=$GH_TOKEN
else
    echo "Everything up to date, swiglpk bindings still match latest GLPK release. Moving on ..."
fi


