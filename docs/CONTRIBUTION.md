# Contribution et promotion

Destination du lot 56 : `AdrienAkilal/WinMarket_AI`, branche `dev`. Le commit initial de `main` est conserve comme ancetre ; son README est conserve dans `docs/README_DEPOT_INITIAL.md` et sa licence reste a la racine. L'ancien depot `winmarket-ai` et son remote ne sont pas modifies.

Pour la suite : branche courte `feature/sujet` ou `fix/sujet` depuis dev, commit cible, tests pertinents, puis PR revue vers dev. Une seule suite principale par commit de reference ; ne pas dupliquer toutes les recettes Windows/Linux sans difference a qualifier. Utiliser les fixtures synthetiques, jamais les comptes ou documents clients.

Promotion : PR explicite dev vers main apres recette, controles CI et revue des reserves ; puis tag de version et notes de livraison. Aucun push direct ni force-push vers main dans le workflow de l'equipe. Aucun merge vers main ou tag de production n'est effectue par le lot 56.

Protections proposees : PR obligatoire, au moins une revue, controles qualification et dependency-audit obligatoires, conversations resolues, interdiction des force-push et suppressions. Etat observe initialement : main existe et est non protegee ; dev etait absente. Ces recommandations ne constituent PAS une protection GitHub active ; aucune regle d'administration n'est modifiee silencieusement.

CI : push dev, PR dev/main, lancement manuel ; permissions contents:read ; pas de pull_request_target, pas de secret fournisseur, actions epinglees sur des SHA verifies via l'API GitHub. PostgreSQL/pgvector de test sur 5547 ; regressions de livraison ciblees avec preparation explicite du modele ; les passes completes Windows et CI deja executees sont conservees dans le rapport. L'audit de dependances reste un job visible, y compris lorsqu'il echoue sur la dette preexistante. JUnit et audit conserves 7 jours. Les traces navigateur et backups prives ne sont pas televerses par la CI.
