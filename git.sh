git add .
git commit -m "Base"
key=cat "../git_token/current.key"
git push "https://"$key"@github.com/brendanmarko/Scraper.git"
echo "[GIT COMPLETED]"
