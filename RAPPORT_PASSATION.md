# Passation lot 56 - 27 septembre 2026

**Perimetre livre.** Copie autonome, installation Python 3.12 verrouillee,
PostgreSQL/pgvector isoles, modele local epingle, inscription en attente,
activation/revocation operateur avec echeance, quota et audit. README et guide de
reprise ; CI de qualification et audit des dependances. Livraison sur `dev`
uniquement, sans deploiement ni fusion vers `main`.

**Preservation.** Aucun compte reel, document prive, secret, `.env`, SQLite ou
sauvegarde n'est inclus. L'ancien code, sa base et son serveur ne sont pas des
cibles de ces operations. Les 351 fichiers de code captures sont identiques a
leur capture initiale (empreintes dans `docs/qualification`). Ce controle ne
pretend pas figer l'activite concurrente de l'ancienne base. Aucune migration
complete de l'historique : anciennes analyses et dependances volontairement
exclues. Les anciens PDF/DOCX signales absents au lot 55 bis ne sont ni requis ni
reconstitues par ce lot ; la source et ses sauvegardes restent conservees.

**Tests executes.** Installation neuve : 111 distributions du lock, `pip check`
et coherence exacts reussis. Suite complete unique : 1 244 succes, 18 echecs,
4 ignores ; apres correction des fixtures historiques et contrats de tests,
les 18 cas en echec ont tous reussi (17,44 s), sans relancer la suite entiere.
75 controles cibles anterieurs reussis. Recette Edge : 10 controles reussis,
inscription/attente/activation/configuration/document/analyse/resultat/revision,
isolation et revocation sur session existante. Sauvegarde/restauration reelle :
24 tables, 52 lignes, 8 fichiers, empreintes egales ; connexion, historique,
PDF/DOCX, document prive et recherche verifies apres restauration.
PostgreSQL, pgvector et embeddings reels ; LLM simule pour la recette,
aucun appel fournisseur reel. Petit corpus RAG : rappel@3 2/2 et citations 6/6,
sans pretention de performance generale. Quatre ignores : exemple AO absent,
symlink Windows sans privilege, deux regles bloquantes non implementees.

**Reserves et reports.** Audit : quatre alertes sur Black 23.12.1
(PYSEC-2024-48, PYSEC-2026-2120, PYSEC-2026-2121) et pytest 7.4.3
(PYSEC-2026-1845). Black non execute ; tests dans une racine privee neuve.
Le job d'audit reste bloquant, sans exclusion d'identifiants : aucune CI
entierement verte n'est revendiquee. Mise a jour/requalification de ces outils
reportee avant promotion. Matrice Windows/Linux complete, second PC,
multi-navigateurs, concurrence, service Windows automatique et automatismes
de deploiement reportes. Aucun email, paiement ni LLM reel qualifie.

**Cloture technique.** Verification du clone propre, du SHA distant et du run CI
consignee dans la preuve de livraison finale ; ne pas confondre configuration
CI presente et run effectivement reussi.
