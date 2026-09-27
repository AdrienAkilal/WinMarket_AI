# Déploiement Render — préparé, non exécuté (lot 58)

**Statut : fichiers prêts (`render.yaml`, ce guide) ; aucune ressource Render n'a été créée depuis cette
session (pas d'accès Dashboard/API/CLI Render ici).** Toute création de service/base ci-dessous est
**facturée** — valider ressources, région et coût avant de cliquer quoi que ce soit.

Cible : une instance FastAPI (Uvicorn, 1 worker), PostgreSQL managé Render + `pgvector` dans la même
région, disque persistant privé. Branche `dev`, déploiement contrôlé (jamais automatique à chaque push).

## 0. Ce qui bloquait avant ce lot (corrigé)

Trois emplacements distincts refusaient structurellement toute URL non-loopback ou tout `BASE_URL` non
`http://127.0.0.1:...` : `src/core/environment_guard.py::validate_environment` (config au démarrage),
`src/core/db_target.py::resolve_database_url` (Alembic), `src/web/database/session.py::get_engine`
(la connexion réelle de l'application). Les trois acceptent désormais une cible réelle explicitement
sous `APP_ENV=production` (validée séparément — hôte non-loopback, rôle/base explicites, `BASE_URL`
HTTPS public, `SESSION_SECRET` réel — jamais un simple contournement des règles locales). Voir
`tests/test_lot58_deployment_environment.py`.

## 1. Base de données (Render PostgreSQL managé)

- Créer une base PostgreSQL Render (`postgresMajorVersion: "16"` ou supérieur — `pgvector` nécessite
  PostgreSQL 13+, confirmé par la documentation Render). Choisir la MÊME région que le service web.
- `pgvector` doit être activé explicitement : `CREATE EXTENSION vector;` — la migration `0015` de ce
  dépôt le fait déjà conditionnellement sur PostgreSQL ; elle s'exécute via `preDeployCommand`
  (ci-dessous), avec le rôle applicatif fourni par Render (suffisant par défaut d'après la documentation
  Render — à confirmer en pratique lors du premier déploiement réel).
- `DATABASE_URL` est fourni automatiquement au service web via `fromDatabase` (voir `render.yaml`) —
  jamais recopié à la main, jamais affiché dans une commande.

## 2. Disque persistant

- **Le disque n'est monté QUE pendant l'exécution du service (runtime) — jamais pendant `buildCommand`
  ni `preDeployCommand`** (confirmé, documentation Render : « you can't access persistent disks during
  a service's build command or pre-deploy command »). Conséquence directe sur l'ordonnancement
  ci-dessous : les migrations (qui n'ont besoin que de la base) passent en pre-deploy ; la préparation du
  modèle d'embeddings (qui écrit sur le disque) passe dans la commande de démarrage elle-même.
- Ajouter un disque **empêche les déploiements sans coupure** : Render arrête l'instance existante avant
  de démarrer la nouvelle (quelques secondes d'indisponibilité, annoncées ici — jamais promis "zéro
  downtime").
- Tout le stockage privé durable (`DATA_DIR`, `OUTPUT_DIR`, `LOCAL_STORAGE_PATH`, `LOGS_DIR`,
  `EMBEDDING_CACHE_DIR`) est routé sous le point de montage unique (`/var/data/...` dans `render.yaml`) —
  jamais un chemin hors disque pour une donnée qui doit survivre à un redéploiement.

## 3. Commandes (voir `render.yaml` pour la syntaxe exacte)

| Étape | Commande | Disque monté ? |
|---|---|---|
| Build | `pip install -r requirements.lock.txt` | non |
| Pre-Deploy | `python -m alembic upgrade head` | non (n'en a pas besoin — base de données uniquement) |
| Start | `python scripts/prepare_model.py --cache "$EMBEDDING_CACHE_DIR" && python -m uvicorn main:app --host 0.0.0.0 --port "$PORT" --workers 1` | oui |

`--workers 1` est **obligatoire** : `main.py` réconcilie les jobs interrompus et démarre un balayage
périodique (`expiry_sweeper`) à chaque démarrage de processus — plusieurs workers dupliqueraient ces
deux mécanismes contre la même base, jamais qualifié à ce jour.

`scripts/prepare_model.py` est idempotent et vérifié par hash (`src/rag/model_artifact.json`) : une fois
le modèle présent sur le disque persistant, les redémarrages suivants ne retéléchargent rien.

## 4. Variables d'environnement

Voir `render.yaml` pour la liste complète. Points notables :
- `APP_ENV=production` est LE commutateur qui active à la fois la validation de déploiement (§0) et les
  cookies `Secure` déjà conditionnés dessus (`src/web/security/csrf.py`, `src/web/auth/session_cookie.py`
  — code déjà existant, aucun changement nécessaire ici).
- `SESSION_SECRET`/les clés LLM/`PAPPERS_API_TOKEN` sont `sync: false` : Render demande leur valeur une
  fois à la création, jamais stockée dans `render.yaml` ni dans Git. Générer `SESSION_SECRET`
  localement : `python -c "import secrets; print(secrets.token_urlsafe(48))"`.
- `BASE_URL` est `sync: false` car son hôte réel (`<service>.onrender.com` ou un domaine personnalisé)
  n'est connu qu'après la première création du service.
- Aucune clé LLM n'est fournie ici — `LLM_ENABLED=false` par défaut dans `render.yaml` ; les activer est
  une décision produit séparée, à prendre explicitement.

## 5. Opérateur (activation manuelle, sans paiement)

`scripts/operator_access.py` accepte désormais une configuration par variables d'environnement réelles
(sans `--env-file`) — même autorité, même règles métier qu'en local :
```
python scripts/operator_access.py --credential-file /var/data/operator.token bootstrap --actor "<nom>"
python scripts/operator_access.py --credential-file /var/data/operator.token list
python scripts/operator_access.py --credential-file /var/data/operator.token activate --user-id <uuid> --organization-id <uuid> --expires-at <ISO_UTC> --max-analyses <n> --reason "Accès manuel autorisé"
```
Exécuter ces commandes via le Shell Render du service déployé (les variables d'environnement du service
sont déjà celles du process — aucun fichier `.env` à fournir).

## 6. Vérifications avant d'ouvrir le service (voir aussi §G du lot)

1. `/healthz` et `/readyz` répondent (déjà implémentés, `qa/smoke.py` les vérifie déjà en CI) — configurer
   le "Health Check Path" du service Render sur `/healthz`.
2. Une inscription passe en attente, une activation manuelle via `operator_access.py` la débloque.
3. Un document synthétique s'indexe, se télécharge, et reste présent après un redémarrage du service
   (le disque est bien celui qui persiste) puis après un redéploiement contrôlé.
4. Recherche RAG en mode `hybrid`/`hybrid_partial` réel (jamais seulement annoncé) une fois
   `RAG_HYBRID_MODE_ENABLED=true` et l'extension `vector` confirmée active.

## 7. Retour arrière

Aucune bascule de trafic public n'a lieu tant que ces vérifications ne sont pas faites sur
l'environnement de validation Render (déployé depuis `dev`, jamais `main`). `main` ne reçoit une
promotion que par PR explicite après recette — jamais une fusion automatique.

## 8. Ce qui reste explicitement à décider (jamais tranché ici)

- Plan payant exact (base de données, service web, taille du disque) et coût mensuel associé — les
  valeurs dans `render.yaml` sont des placeholders conservateurs, pas un choix validé.
- Activation ou non des clés LLM réelles.
- Domaine personnalisé ou sous-domaine `onrender.com` par défaut.
- Durée de la fenêtre de validation avant toute annonce publique.
