# Lot 56 bis - correction de la reserve CI

Base distante verifiee : `df73fa6908b75dfecc978b20801893490f07d592`.
La qualification precedente concernait `ee3209b805283eada286126678732c9599237c0b`.
Le commit suivant ne modifie que RAPPORT_PASSATION.md et trois preuves dans
`docs/qualification` (delivery.json, evaluation_manifest.json, tests.json).
Code, migrations, dependances, tests et workflow sont identiques : les preuves
fonctionnelles restent applicables ; la CI globale etait pourtant rouge sur l'audit.

| Outil | Avant | Apres | Correctifs officiels |
| --- | --- | --- | --- |
| Black | 23.12.1 | 26.3.1 | [ReDoS, 24.3.0](https://github.com/psf/black/releases/tag/24.3.0), [action GitHub, 26.3.0](https://github.com/psf/black/security/advisories/GHSA-v53h-f6m7-xcgm), [cache, 26.3.1](https://github.com/psf/black/security/advisories/GHSA-3936-cmfr-pm3m) |
| pytest | 7.4.3 | 9.0.3 | [Repertoires temporaires UNIX, 9.0.3](https://github.com/pytest-dev/pytest/releases/tag/9.0.3) |

Les quatre alertes PYSEC-2024-48, PYSEC-2026-2120, PYSEC-2026-2121 et
PYSEC-2026-1845 ont ete reproduites. Aucun appel Black trouve dans les scripts,
configurations ou CI ; il reste conserve comme outil declare. Aucun reformatage.
L'action GitHub Black concernee par un des avis n'est pas utilisee ici ; aucune
alerte n'est neanmoins ignoree. Les deux versions exigent Python >=3.10 et
annoncent Python 3.12. Les contraintes des plugins existants acceptent pytest 9.
Seuls ajouts transitifs : Pygments 2.21.0 (pytest), pytokens 0.4.1 (Black).

Lock regenere par la procedure existante : pip install des requirements, puis
pip freeze, sans mise a jour globale. Lock QA conserve. Audit local et GitHub :
**0 alerte**, sans ignore ni continue-on-error. Installation neuve : 113 versions,
pip check, coherence exacte et imports reussis. Collecte : 1 269 tests sans erreur
(une collecte n'est pas une execution). Black teste via son API, sans reformatage.

[Suite complete CI sur e5068b5](https://github.com/AdrienAkilal/WinMarket_AI/actions/runs/36347755595) :
**1 265 passes, 4 ignores, 12 avertissements**, 270,36 s ; une seule passe complete.
Plugins conserves : cov 4.1.0, xdist 3.5.0, timeout 2.2.0, mock 3.12.0,
benchmark 4.0.0, hypothesis 6.92.0 et Faker 21.0.0. Compatibilite constatee pour
la collecte et la suite executee ; concurrence xdist et matrice OS non qualifiees.
Migrations, healthz/readyz, lint, lock et historique Git controles en CI.

Skips conserves, non comptes comme validations : exemple AO absent ; adaptation
Unix-socket du pgserver embarque Linux reportee (service PostgreSQL CI reel) ;
regles bloquantes Risque contractuel et Solidite client non implementees.
Aucune reserve de dependances restante dans les audits executes. Les reports
fonctionnels et d'infrastructure du lot 56 restent applicables.

Le commit de compte rendu ne modifie que documentation et manifeste : code,
tests, workflow et locks identiques a e5068b5. Sa propre CI reprend les controles
existants et les regressions ciblees ; aucun skip CI et aucune deuxieme passe
complete. Le SHA final et son run sont fournis avec la livraison.

Commandes de reprise inchangees : `pip install -r requirements.lock.txt`,
`python scripts/check_lock_consistency.py`, puis les commandes existantes du guide.
Aucun changement applicatif, nouvelle recette navigateur, appel LLM, suppression
documentaire, deploiement ou fusion vers main. Ancienne installation hors perimetre.
