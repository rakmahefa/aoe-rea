# Passation de session — projet aoe-rea

**Mise à jour : 13 octobre 2026**  
**Dépôt :** https://github.com/rakmahefa/aoe-rea  
**Dernier run vérifié lors de la rédaction :** [REA binary analysis #22](https://github.com/rakmahefa/aoe-rea/actions/runs/38354872448)

## 1. But du projet

Le projet vise à étudier Age of Empires III à l’aide de REA et Ghidra, puis à reconstruire progressivement les comportements nécessaires dans du code maintenable afin de parvenir, à terme, à un véritable exécutable Linux natif (ELF). Le but n’est pas de se limiter à Wine/Proton, à un lanceur ou à des rapports de décompilation.

**État réel : recherche statique précoce.** Aucun code source original complet n’a été récupéré, aucun port natif complet n’a été construit et aucun exécutable ELF du jeu n’est disponible à ce stade. Les noms `FUN_...` sont générés par l’analyse ; le pseudocode est une interprétation de Ghidra, pas le code original.

## 2. État vérifié du dépôt

- Dépôt GitHub : https://github.com/rakmahefa/aoe-rea
- Branche principale : `main`
- Commit `main` observé lors de cette mise à jour : `ad539edede393f8d954bea01266e8d31fb4121f5` (fusion de la PR #8). Vérifier de nouveau le commit avant de poursuivre.
- Workflow manuel : [REA binary analysis](https://github.com/rakmahefa/aoe-rea/actions/workflows/rea-analysis.yml)
- Fichier analysé par défaut : `retro/exe et dll/age3y.exe`
- SHA-256 du binaire : `b1a1dab7264d2db72e8f8ae1df1e419eecc223b40db00c9d1013a3bc77611d9d`
- Format : PE32 x86 (Windows 32 bits), image base `0x400000`, point d’entrée déclaré `0x5876ac` (RVA `0x1876ac`).
- Toolchain du workflow : REA 6.4.0 et Ghidra 12.1.4.
- La PR #4 a ajouté l’analyse bornée des callees internes : jusqu’à quatre dossiers directs dans `callees/`, accompagnés de `callees/manifest.json`. Cette limite peut sélectionner en priorité des fonctions runtime, d’allocation mémoire ou de chaînes.

## 3. Procédure pour relancer l’analyse

1. Ouvrir **Actions → REA binary analysis → Run workflow** dans le dépôt.
2. Garder `target_path` sur `retro/exe et dll/age3y.exe`, sauf raison claire de changer de binaire.
3. Utiliser `search_query` pour rechercher un terme à la fois : `unit`, `move`, `path`, `food`, `resource`, `build`, `train`, `AI`. Les adresses résultantes pointent vers des chaînes définies ; elles ne doivent pas être passées directement à `function_selector` sans preuve que ce sont des fonctions.
4. Pour une chaîne prometteuse, renseigner `xref_address` avec son adresse (par exemple `0xc36e20` ou `0xc19dc0`). Lire `xrefs.json` pour identifier les références, puis choisir une adresse de code plausible à examiner. Un xref peut être une table d'enregistrement ou une fonction d'interface, donc vérifier son contexte.
5. Relancer avec `function_selector` sur une adresse de fonction plausible pour obtenir pseudocode, références et callees.
6. Lancer le workflow puis attendre son état `success` ou `failure`.
7. Inspecter `metadata.json`, `search.json` et/ou `xrefs.json` selon les inputs. `analysis.json`, `function.json` et `callees/manifest.json` n'existent que si l'étape d'analyse de fonction a été exécutée.
8. Avant de conseiller une nouvelle cible, contrôler le dernier run réel dans GitHub Actions.

Le workflow réalise de l’analyse statique et publie un artifact temporaire (rétention indiquée dans le README/workflow). Il ne génère pas automatiquement du code source, ne produit pas de binaire Linux et n’enregistre pas les rapports dans le dépôt.

## 4. Historique des découvertes utiles

| Run | Cible sélectionnée | Résultat vérifié |
|---|---|---|
| [#6](https://github.com/rakmahefa/aoe-rea/actions/runs/38175888885) | point d’entrée `0x5876ac` | Chemin de démarrage/runtime ; APIs telles que `GetStartupInfoA`, `GetCommandLineA`, `GetVersionExA`, `GetModuleHandleA`. Pas de preuve de gameplay. |
| [#8](https://github.com/rakmahefa/aoe-rea/actions/runs/38177590652) | point d’entrée et quatre callees | `0x401cdd` correspond à une aide de probing de pile ; `0x56cc46` et `0x56cc7d` ressemblent au runtime C ; `0x404ee0` est une routine de traitement de fenêtres/messages et d’erreurs Windows. |
| [#9](https://github.com/rakmahefa/aoe-rea/actions/runs/38180565651) | `0x578439` | Parseur de ligne de commande/token, avec gestion des espaces, guillemets et table de classification des caractères. Piste runtime, peu pertinente pour le moteur. |
| [#10](https://github.com/rakmahefa/aoe-rea/actions/runs/38197841851) | `0x404ee0` | Routine d’événements/UI Windows ; callees principalement utilitaires de chaînes (`MultiByteToWideChar`, `WideCharToMultiByte`, accès/libération de chaînes). Pas le cœur de la simulation démontré. |
| [#11](https://github.com/rakmahefa/aoe-rea/actions/runs/38200459323) | `0x5aa825` | Wrapper de minuterie et de démarrage ; `0x5aa86e` ressemble à une initialisation applicative de haut niveau (fichiers de config/log, COM, curseur, mutex, état global). |
| [#12](https://github.com/rakmahefa/aoe-rea/actions/runs/38203166028) | `0x5561d9` | Constructeur/initialiseur présumé d’un objet volumineux. `0x555fd0` référence `art/effects/particleSetFileList.xml`, piste vers un gestionnaire de ressources/effets. |
| [#13](https://github.com/rakmahefa/aoe-rea/actions/runs/38205614725) | `0x555e86` | Parcourt `particleSetXMLFiles`, les éléments `psetsfile` et leurs attributs `filename`, puis délègue à `0x555c89`. Cette dernière lit `ParticleSetDef` / `ParticleSet` et appelle `0x5562ad`. |
| [#14](https://github.com/rakmahefa/aoe-rea/actions/runs/38249737918) | `0x5562ad` | Parcourt des enfants XML `Particle`, lit notamment `filename` et `timeoff`, construit ou remplit une structure et délègue à `0x598def`. Chaîne de chargement de définitions de particules confirmée ; toujours pas de preuve du moteur de simulation. |
| [#18](https://github.com/rakmahefa/aoe-rea/actions/runs/38264819057) | Recherche de chaînes `unit` | Succès. `search.json` contient 1 307 chaînes définies correspondantes. Pistes : `kbCanPath2` (`0xc19dc0`), `kbCanSimPath` (`0xc19e68`), `kbUnitCount` (`0xc1b0c8`), `hcUnitMoveToPos` (`0xbaee38`) et diagnostic `Unit ... non-unit obstruction` (`0xc36e20`). Ce sont des adresses de chaînes, pas de code ; aucun pseudocode gameplay n'a été récupéré par ce run de recherche seule. |
| [#19](https://github.com/rakmahefa/aoe-rea/actions/runs/38343736085) | Xrefs de `0xc36e20` | Succès. `xrefs.json` retourne une référence directe à `0x6a15ca`. Cette adresse est le site d'une référence ; la fonction qui la contient et son rôle gameplay restent à inspecter. |
| [#20](https://github.com/rakmahefa/aoe-rea/actions/runs/38347489501) | Fonction contenant `0x6a15ca` | Succès. REA résout `FUN_004839bb` (entrée `0x4839bb`). Le pseudocode vérifie un type d'obstruction, puis appelle des helpers de géométrie et de mise à jour spatiale. Piste de gestion d'obstruction/grille spatiale, confiance moyenne, avec limites liées aux plages de fonction non contiguës. |
| [#21](https://github.com/rakmahefa/aoe-rea/actions/runs/38350963849) | `function_selector=0x483d4c` | Succès. `FUN_00483d4c` (89 octets contigus) calcule les quatre coins d’un rectangle à partir de deux coordonnées et de deux dimensions, puis écrit des champs indicateurs. Dans le contexte de #20, cela suggère une empreinte géométrique liée à l’obstruction ; les champs et le rôle exact restent à confirmer. Cette fonction est aussi appelée depuis deux autres procédures. |
| [#22](https://github.com/rakmahefa/aoe-rea/actions/runs/38354872448) | `function_selector=0x4a5558` | Succès. `FUN_004a5558` calcule quatre paires de coordonnées à partir de plusieurs paramètres flottants, puis appelle `FUN_004a5489` pour choisir des indices/champs associés aux sommets. Cette branche semble produire une forme orientée plutôt qu’un simple rectangle aligné sur les axes ; interprétation géométrique plausible, sémantique exacte non confirmée. |

### Dernier run en détail — #22

Le [run #22](https://github.com/rakmahefa/aoe-rea/actions/runs/38354872448) s'est terminé avec succès le 13 octobre 2026. La PR #8, qui documentait les runs #19–21, est fusionnée dans `main`.

- Input effectif : `function_selector=0x4a5558` ; `search_query` et `xref_address` vides.
- Artifact : `rea-analysis` (run ID `38354872448`, artifact ID `11792938137`).
- Binaire : `retro/exe et dll/age3y.exe`.
- SHA-256 : `b1a1dab7264d2db72e8f8ae1df1e419eecc223b40db00c9d1013a3bc77611d9d`.
- Commit analysé : `ad539edede393f8d954bea01266e8d31fb4121f5`.
- REA `6.4.0`, Ghidra `12.1.4`.
- `function-selection.json` indique `selector: 0x4a5558`, `source: manual input`, `status: success`.
- Fonction sélectionnée : `FUN_004a5558`, non externe et non thunk. Corps de 265 octets réparti sur les plages `0x4a5558–0x4a5651` et `0x4b8fdf–0x4b8fed`.
- Callee récupérée : `FUN_004a5489`, entrée `0x4a5489`, dossier `callees/4a5489_FUN_004a5489.json`. Son corps compte 251 octets sur plusieurs plages non contiguës.
- Appelants de `FUN_004a5558` rapportés par Ghidra : `FUN_004839bb`, `FUN_00497884`, `FUN_004e4a30` et `FUN_009c754c`. Le helper peut donc être partagé, même si le contexte de `FUN_004839bb` est lié au chemin d'obstruction étudié.

Résumé du pseudocode de `FUN_004a5558` :
1. Reçoit une structure de sortie, deux coordonnées centrales apparentes et quatre autres paramètres flottants.
2. Calcule quatre points à partir de combinaisons et produits de ces paramètres, puis écrit les coordonnées dans la zone `+0x20` à `+0x3c`.
3. Appelle `FUN_004a5489`. Cette fonction compare les coordonnées de sommets stockées dans la structure et choisit quatre valeurs de type indice qu'elle écrit aux offsets `+0x1c`–`+0x1f`.
4. Écrit un champ additionnel à `+0x19`, calculé à partir d'un paramètre multiplié par 64 et du signe d'un autre paramètre.

Interprétation prudente : l'arithmétique de `FUN_004a5558` s'écarte du rectangle axis-aligned de `FUN_00483d4c` (run #21) et paraît construire quatre points orientés ou un quadrilatère à partir de composantes directionnelles. Dans `FUN_004839bb` (run #20), cette fonction est choisie par une condition de propriété/flag au lieu de `FUN_00483d4c`. La chaîne de preuves combinées suggère un format géométrique avec plusieurs modes dans un chemin lié aux obstructions, sans identifier de façon définitive le type d'objet ou prouver un algorithme de pathfinding.

Limite importante : plusieurs fonctions décompilées par Ghidra ont des plages corporelles non contiguës. Pour `FUN_004a5558`, la taille totale est 265 octets alors que l'étendue d'adresses couvre 80 534 octets. Ne pas considérer automatiquement l'ensemble des blocs distants comme un corps linéaire sans vérifier le graphe de flux et les instructions.

## 5. Prochaine étape conseillée

**Priorité immédiate : analyser `0x483a6a`.**

Dans le workflow manuel, utiliser :

- `target_path=retro/exe et dll/age3y.exe`
- `function_selector=0x483a6a`
- `search_query` vide
- `xref_address` vide

Pourquoi cette cible : `FUN_004839bb` (run #20) appelle `FUN_00483d4c` ou `FUN_004a5558` pour produire des coordonnées géométriques, puis appelle `FUN_00483a6a` avant `FUN_0048380f`, qui semble mettre à jour l'appartenance à une grille spatiale. Le rôle de `FUN_00483a6a` peut aider à relier la forme géométrique aux indices/champs de la structure et à sa mise à jour spatiale.

Ensuite, prioriser les véritables interfaces de pathfinding : retrouver les références de code vers les descriptions `kbCanPath2` (`0xc19dc0`) et `kbCanSimPath` (`0xc19e68`) via `xref_address`, puis analyser seulement les adresses de fonctions confirmées. Maintenir le mouvement, l'économie et l'IA comme pistes séparées au lieu d'assimiler la construction géométrique au pathfinding.

Documenter pour chaque run l'input exact, le hash du binaire, les preuves observées et les incertitudes. Les noms `FUN_...` sont des noms attribués par Ghidra ; le pseudocode n'est pas le code source original.

## 6. Règles de travail pour la prochaine session

- Utiliser les capacités GitHub connectées pour inspecter le dépôt et Actions directement ; ne pas supposer que l’utilisateur doit recopier manuellement tous les résultats.
- Vérifier le dernier run à chaque reprise. L’historique ci-dessus est un instantané daté, et non une affirmation sur des exécutions futures.
- Pour les changements dans le dépôt, travailler sur une branche dédiée et ouvrir une pull request plutôt que de modifier `main` directement.
- Ajouter des notes de preuve : adresse, run/artifact, chaînes, imports, appels, interprétation et niveau de confiance.
- Séparer explicitement les faits observés des hypothèses. Ne pas présenter du pseudocode Ghidra comme code source original récupéré.
- Ne pas promettre ou prétendre qu’un port Linux natif existe tant qu’un ELF compilé et son comportement n’ont pas été validés.
- Respecter les droits d’utilisation. Ne pas publier des exécutables, DLL ou ressources propriétaires du jeu dans des releases sans autorisation ; préférer du code reconstruit, des instructions reproductibles et des fichiers fournis légalement par l’utilisateur.

## 7. Message de démarrage à copier dans une nouvelle session

> Nous poursuivons le projet https://github.com/rakmahefa/aoe-rea. La PR #8 est fusionnée. Le run #22 a réussi avec `function_selector=0x4a5558`. Cette fonction calcule quatre paires de coordonnées à partir de plusieurs paramètres flottants, puis appelle `FUN_004a5489` qui choisit des indices/champs de sommets. Comparée à la forme axis-aligned construite par `FUN_00483d4c` au run #21, elle semble traiter une forme orientée ou un quadrilatère. Avec `FUN_004839bb` et le helper de grille `FUN_0048380f` du run #20, cela étaye une piste géométrie/obstruction (confiance moyenne), sans prouver le pathfinding. Prochaine cible : `function_selector=0x483a6a`, puis xrefs vers `kbCanPath2` (`0xc19dc0`) et `kbCanSimPath` (`0xc19e68`). Prioriser unités/obstacles, grille spatiale, déplacement/pathfinding, simulation, économie et IA. Séparer faits et hypothèses, garder les liens run/artifact et créer une branche + PR pour toute modification.
