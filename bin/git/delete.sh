


git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch _downloads/Cloudmesh-Feb-2016.pptx.gz' --prune-empty --tag-name-filter cat -- --all

git push origin --force --all
git push origin --force --tags

