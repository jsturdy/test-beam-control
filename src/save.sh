#!/bin/bash        
now=$(date +"%m-%d-%Y")
git !git ls-files --deleted -z | xargs -0 git rm --cached
git add .
git commit -m "Autosave $now"
git push
