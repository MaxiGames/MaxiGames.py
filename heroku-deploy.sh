#! /bin/sh

if [ ! $(git branch --show-current) = "main" ]; then
    echo "Can only deploy from branch main. Abort."
    exit 1
fi

rm -f tar
echo "Archiving configs."
tar cf tar serviceAccountKey.json serviceAccountKey2.json config.json 2>&1 >/dev/null  # shh
echo "Archiving configs complete."
s=$?
bruh=0  # bruh

function cleanup()
{
    if [ $bruh -eq 0 ]; then
        echo "Cleaning up, unarchiving configs."
        git reset --hard HEAD~ 2>&1 >/dev/null  # oh, shut up
        tar xf tar 2>&1 >/dev/null  # you shut up too
        rm -f tar
        echo "Cleaning up, unarchiving configs complete."
        bruh=1
    fi
}

trap cleanup SIGINT

if [ ! $s -eq 0 ]; then
    echo "Config files do not exist. Abort."
    exit 1
fi

git add -f serviceAccountKey.json serviceAccountKey2.json config.json 2>&1 >/dev/null  # please just shut up
s1=$?
git commit --allow-empty -m heroku 2>&1 >/dev/null  # please just shut up as well

if [ $s1 -eq 0 ]; then
    heroku restart 2>&1 >/dev/null
    heroku buildpacks:clear 2>&1 >/dev/null
    git push -f heroku main
else
    echo 'Failed to add config files. Abort.'
    cleanup
    exit 1
fi
cleanup
exit 0
