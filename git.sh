echo "[GIT START]"
git add .
git commit -m "Base"
key=$(<../git_token/current.key)
git push https://"$key"@github.com/brendanmarko/Scraper.git
echo "[GIT FIN]"
