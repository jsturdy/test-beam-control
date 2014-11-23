#!/bin/bash        
now=$(date +"%Y-%m-%d %H:%M:%S")
git ls-files --deleted -z | xargs -0 git rm --cached
git add .
git commit -m "Autosave $now"
git push
echo "Saved!"
