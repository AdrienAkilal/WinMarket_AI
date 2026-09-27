# Passation lot 56 - 27 septembre 2026

**Livre sur dev.** Version autonome : PostgreSQL/pgvector isoles, dependances
verrouillees, modele local epingle, inscription en attente et activation/revocation
operateur sans paiement (echeance, quota, audit). README : installer, configurer,
demarrer, tester et administrer les comptes. Aucun deploiement ni fusion vers main.

**Preservation.** Aucun compte reel, document prive, secret, .env, SQLite ou backup
publie. L'ancienne installation, sa base et son serveur ne sont pas des cibles de
ces operations. Les 351 fichiers de code captures sont restes identiques ; cette
preuve ne pretend pas figer l'activite concurrente de l'ancienne base. Anciennes
analyses et dependances volontairement non importees : ce n'est pas une migration
complete de l'historique. Les deux anciens PDF/DOCX manquants du lot 55 bis restent
signales absents, sans bloquer cette version. Source et sauvegardes conservees.

**Preuves executees.** Clone propre de dev installe : 111/111 versions exactes,
pip check, dependances et imports conformes. Historique Git distant inspecte ;
fichiers du clone initial identiques octet par octet a la copie testee.
Suite Windows unique : 1 244 succes, 18 echecs, 4 ignores ; les 18 cas corriges
ont ensuite tous reussi. 75 tests cibles anterieurs et 38 derniers controles reussis.
Suite CI Linux : 1 257 succes, 6 echecs de fixtures/portabilite, 3 ignores ;
corrections ciblees et un report explicite, sans nouvelle suite complete.
[CI finale du code ee3209b](https://github.com/AdrienAkilal/WinMarket_AI/actions/runs/36305277828) :
qualification reussie, **68 tests passes, 1 ignore**, migrations, healthz/readyz,
lock, lint et controle de l'historique Git reussis. Demarrage/arret local reel
verifie apres renforcement de l'identification des processus PostgreSQL.

Recette Edge : 10 controles reussis, de l'inscription au resultat/revision,
isolation et revocation comprises. Restauration : 24 tables, 52 lignes, 8 fichiers,
empreintes egales, connexion et livrables verifies. PostgreSQL, pgvector et embeddings
reels ; LLM simule, aucun appel fournisseur reel. Corpus RAG cible : rappel@3 2/2,
citations 6/6 ; aucune generalisation de performance.

**Reserve de cloture.** Audit CI en echec : quatre alertes sur Black 23.12.1
(PYSEC-2024-48, PYSEC-2026-2120, PYSEC-2026-2121) et pytest 7.4.3
(PYSEC-2026-1845). Black non execute ; tests dans une racine privee neuve.
Aucune alerte masquee : mise a jour/requalification reportee avant promotion,
CI globale non verte. Details et empreintes : `docs/qualification`.

**Reportes.** Matrice Windows/Linux complete, second PC, multi-navigateurs,
concurrence, service Windows automatique, deploiement avance et demarrage pgserver
embarque sous Linux (la CI utilise un service PostgreSQL reel). Autres ignores :
exemple AO absent, symlink Windows sans privilege et deux regles bloquantes non
implementees. Aucun paiement, email ou LLM reel qualifie.
