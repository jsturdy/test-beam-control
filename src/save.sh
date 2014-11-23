#!/bin/bash        
now=$(date +"%m-%d-%Y %h-%m-%s")
echi ${now}
git ls-files --deleted -z | xargs -0 git rm --cached
git add .
git commit -m "Autosave $now"
git push
