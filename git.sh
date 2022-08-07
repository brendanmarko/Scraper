git add .
git commit -m "Base"
key=echo ../git_token/current.key
echo $key
git push https://$key@github.com/brendanmarko/Scraper.git
echo "[GIT COMPLETED]"
