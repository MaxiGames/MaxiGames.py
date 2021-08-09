#! /usr/bin/sh

if [ ! $(git branch --show-current) = "main" ]; then
    echo "Can only deploy from branch main."
    exit 1
fi

tar cf tar serviceAccountKey.json serviceAccountKey2.json config.json 
s=$?
bruh=0

function cleanup()
{
    if [ $bruh -eq 0 ]; then
        git reset --hard HEAD~
        tar xf tar 2>&1 >/dev/null  # oh, shut up
        rm -f tar
        bruh=1
    fi
}

trap cleanup SIGINT

if [ $s -eq 0 ]; then
    git add -f serviceAccountKey.json serviceAccountKey2.json config.json
    s1=$?
    git commit --allow-empty -m heroku

    if [ $s1 -eq 0 ]; then
        heroku restart
        heroku builds:clear
        git push -f heroku main
    else
        echo 'Failed to add config files...'
    fi
    cleanup
fi
