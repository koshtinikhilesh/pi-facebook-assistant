fswebcam -r 1920x1080 --set brightness=50% $1
rm downloads.jpeg
cp  $1 backup/$1
cp $1 downloads.jpeg
git cat-file -e origin/master:downloads.jpeg && echo downloads.jpeg exists
if [ "$?"  -eq  0 ]
then
git rm --cached downloads.jpeg
git add .
git commit -m "deleted"
git push origin master

git add downloads.jpeg 
git commit -m "latest commit at $1"
git push origin master
fi
sleep 4
