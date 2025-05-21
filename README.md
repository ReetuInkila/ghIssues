# GitHub Issue Creator from Jira CSV

Tämä skripti lukee Jira-exportoidun backlog CSV-tiedoston ja luo siitä GitHub-issueita käyttäen [PyGithub](https://pygithub.readthedocs.io/en/latest/):ia.

## 🔧 Vaatimukset

- GitHub-tunnus ja  access token (tai käytä `gh` CLI:tä)
- `PyGithub`-kirjasto
- CSV-tiedostossa tulee olla seuraavat sarakkeet:
  - `Summary`
  - `Priority`
  - `Description`

## 🔨 Käyttö

1. **Asenna riippuvuudet:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Jos et käytä gh CLI:tä**, aseta access token skriptiin nimellä `ACCESS_TOKEN`.
3. **Aseta `REPO_NAME`** suoraan skriptiin.

4. **Suorita ohjelma:**

   ```bash
   python3 create_issues.py csv_tiedosto.csv
   ```