# WinMarket AI - lot 56

Version isolee avec PostgreSQL, RAG prive et activation manuelle sans paiement.
Aucun compte, document client ni historique ancien n'est fourni. Branche `dev` ;
aucune fusion vers `main` ni mise en ligne.

## Installer et demarrer (Windows, Python 3.12)

Choisir un dossier neuf, hors de l'ancienne installation. Depuis PowerShell :

```powershell
git clone --branch dev https://github.com/AdrienAkilal/WinMarket_AI.git WinMarket_AI_56
cd WinMarket_AI_56
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.lock.txt
.\.venv\Scripts\python.exe scripts/check_lock_consistency.py
$runtime = Join-Path $env:LOCALAPPDATA 'WM56-runtime'
.\.venv\Scripts\python.exe scripts/local_env.py init --runtime $runtime --pg-port 5546 --app-port 8056
.\.venv\Scripts\python.exe scripts/local_env.py migrate --runtime $runtime
.\.venv\Scripts\python.exe scripts/prepare_model.py --cache "$runtime\models"
.\.venv\Scripts\python.exe scripts/local_env.py start --runtime $runtime
```

Ouvrir http://127.0.0.1:8056/register. `init` exige un runtime inexistant et genere
les secrets hors du depot. `.env.example` decrit les options ; les cles LLM restent
facultatives et ne doivent jamais etre commitees. Le modele public est prepare
explicitement, puis verifie et charge localement.

## Activer ou revoquer un compte

Sur le serveur, creer une seule fois l'identite operateur puis relever les UUID :

```powershell
$op = @('--env-file', "$runtime\.env", '--credential-file', "$runtime\operator.token")
.\.venv\Scripts\python.exe scripts/operator_access.py @op bootstrap --actor "$env:USERNAME"
.\.venv\Scripts\python.exe scripts/operator_access.py @op list
$userId = Read-Host 'UUID compte'
$orgId = Read-Host 'UUID organisation'
$expiry = Read-Host 'Echeance ISO UTC avec fuseau'
$quota = Read-Host 'Quota analyses et revisions'
.\.venv\Scripts\python.exe scripts/operator_access.py @op activate --user-id $userId --organization-id $orgId --expires-at $expiry --max-analyses $quota --reason 'Acces manuel autorise'
# Pour retirer ensuite les droits, sans supprimer les donnees :
.\.venv\Scripts\python.exe scripts/operator_access.py @op revoke --user-id $userId --organization-id $orgId --reason 'Fin acces manuel'
```

L'utilisateur active configure son profil, sa politique de scoring et ses capacites,
puis importe ses propres documents. Une inscription seule ne donne aucun acces metier.

## Tester et arreter

```powershell
.\.venv\Scripts\python.exe scripts/run_tests.py --scratch-parent "$env:LOCALAPPDATA\WM56-tests" --embedding-cache "$runtime\models" tests/test_lot56_manual_access.py tests/test_lot56_environment_guard.py tests/test_lot56_migration.py -q
.\.venv\Scripts\python.exe scripts/local_env.py stop --runtime $runtime
```

Les tests utilisent des bases jetables et refusent les cibles conservees.
[Guide detaille](docs/REPRISE_PROJET.md) : configuration, sauvegarde/restauration,
suite complete. [Rapport et limites](RAPPORT_PASSATION.md) : preuves reelles,
simulation LLM, reserves de dependances et validations reportees.
