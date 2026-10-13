# Passation de session — projet aoe-rea

**Mise à jour : 13 octobre 2026**  
**Dépôt :** https://github.com/rakmahefa/aoe-rea  
**Dernier run vérifié lors de la rédaction :** [REA binary analysis #21](https://github.com/rakmahefa/aoe-rea/actions/runs/38350963849)

## 1. But du projet

Le projet vise à étudier Age of Empires III à l’aide de REA et Ghidra, puis à reconstruire progressivement les comportements nécessaires dans du code maintenable afin de parvenir, à terme, à un véritable exécutable Linux natif (ELF). Le but n’est pas de se limiter à Wine/Proton, à un lanceur ou à des rapports de décompilation.

**État réel : recherche statique précoce.** Aucun code source original complet n’a été récupéré, aucun port natif complet n’a été construit et aucun exécutable ELF du jeu n’est disponible à ce stade. Les noms `FUN_...` sont générés par l’analyse ; le pseudocode est une interprétation de Ghidra, pas le code original.

## 2. État vérifié du dépôt

- Dépôt GitHub : https://github.com/rakmahefa/aoe-rea
- Branche principale : `main`
- Commit `main` observé lors de cette mise à jour : `97a2e081d5cbf72c161756dba16599cf80fb61f8` (fusion de la PR #7). Vérifier de nouveau le commit avant de poursuivre.
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

### Dernier run en détail — #21

Le [run #21](https://github.com/rakmahefa/aoe-rea/actions/runs/38350963849) s'est terminé avec succès le 13 octobre 2026.

- Input effectif : `function_selector=0x483d4c` ; recherche et xrefs vides.
- Artifact : `rea-analysis` (run ID `38350963849`, artifact ID `11791420795`).
- Binaire : `retro/exe et dll/age3y.exe`.
- SHA-256 : `b1a1dab7264d2db72e8f8ae1df1e419eecc223b40db00c9d1013a3bc77611d9d`.
- Commit analysé : `97a2e081d5cbf72c161756dba16599cf80fb61f8`.
- REA `6.4.0`, Ghidra `12.1.4`.
- `function-selection.json` indique `selector: 0x483d4c`, `source: manual input`, `status: success`.
- La procédure sélectionnée est `FUN_00483d4c`, non externe et non thunk ; corps unique `0x483d4c–0x483da4`, 89 octets, sans plage non contiguë.
- Il s'agit d'une fonction feuille : aucun callee ni chaîne référencée dans ce dossier.
- Les références entrantes comprennent `FUN_004839bb` via l'appel à `0x483d4c` au site `0x483a47`, ainsi que les procédures `FUN_00497884` et `FUN_004e4a30`. Ce dernier point indique que la routine peut être partagée.

Résumé du pseudocode :
1. Lit l'objet de sortie reçu en premier argument.
2. Calcule les bornes `x-w`, `y-h`, `x-w`, `y+h`, `x+w`, `y+h`, `x+w`, `y-h`, puis les écrit à partir des offsets `+0x20` à `+0x3c`. Ce sont les quatre coins d'un rectangle exprimés sous forme de quatre paires de coordonnées.
3. Écrit aussi les octets `+0x1e=4`, `+0x1f=5`, `+0x1c=0`, `+0x1d=1`, et `+0x19=0x40`. Le sens exact de ces champs n'est pas établi.

Interprétation : l'arithmétique rectangulaire est observée directement. Comme run #20 montre que le caller sélectionne ce helper dans une branche normale d'un chemin lié au type d'obstruction et lui transmet des coordonnées/dimensions apparentes, il est raisonnable de soupçonner une construction d'empreinte ou de géométrie d'obstruction. Il faut cependant éviter de présenter la fonction comme « le collisionneur d'unités » sans preuve supplémentaire : elle est également appelée depuis deux autres procédures et son dossier ne contient pas de chaînes métier.

## 5. Prochaine étape conseillée

**Priorité immédiate : analyser le helper alternatif `0x4a5558`.**

Dans la prochaine exécution du workflow, utiliser :

- `target_path=retro/exe et dll/age3y.exe`
- `function_selector=0x4a5558`
- `search_query` vide
- `xref_address` vide

Pourquoi cette cible : `FUN_004a5558` est la branche alternative appelée par `FUN_004839bb` selon un test de propriété/flag, là où le chemin normal appelle `FUN_00483d4c`. Le dernier run a confirmé que `FUN_00483d4c` écrit les quatre coins d'une forme rectangulaire et des champs indicateurs. Comparer les deux helpers peut révéler si le chemin alternatif construit une empreinte différente ou ajoute un autre traitement.

Puis, examiner `0x483a6a`, également appelé après la branche géométrique, si son rôle reste inconnu. Ensuite, si la piste d'occupation spatiale se confirme, lancer des recherches ciblées de xrefs autour de `kbCanPath2` (`0xc19dc0`) et `kbCanSimPath` (`0xc19e68`) pour séparer calcul géométrique et véritable pathfinding.

Continuer à noter le run, l'input, le binaire/hash, les adresses et extraits qui fondent l'interprétation, ainsi que les inconnues. Les fonctions `FUN_...` sont des noms synthétiques de Ghidra ; ne pas traiter le pseudocode comme la source originale.

## 6. Règles de travail pour la prochaine session

- Utiliser les capacités GitHub connectées pour inspecter le dépôt et Actions directement ; ne pas supposer que l’utilisateur doit recopier manuellement tous les résultats.
- Vérifier le dernier run à chaque reprise. L’historique ci-dessus est un instantané daté, et non une affirmation sur des exécutions futures.
- Pour les changements dans le dépôt, travailler sur une branche dédiée et ouvrir une pull request plutôt que de modifier `main` directement.
- Ajouter des notes de preuve : adresse, run/artifact, chaînes, imports, appels, interprétation et niveau de confiance.
- Séparer explicitement les faits observés des hypothèses. Ne pas présenter du pseudocode Ghidra comme code source original récupéré.
- Ne pas promettre ou prétendre qu’un port Linux natif existe tant qu’un ELF compilé et son comportement n’ont pas été validés.
- Respecter les droits d’utilisation. Ne pas publier des exécutables, DLL ou ressources propriétaires du jeu dans des releases sans autorisation ; préférer du code reconstruit, des instructions reproductibles et des fichiers fournis légalement par l’utilisateur.

## 7. Message de démarrage à copier dans une nouvelle session

> Nous poursuivons le projet https://github.com/rakmahefa/aoe-rea. Le run #21 a réussi avec `function_selector=0x483d4c`. `FUN_00483d4c` écrit les quatre coins d'un rectangle à partir de deux coordonnées et de deux dimensions, plus des champs indicateurs. Dans le contexte du run #20 (`FUN_004839bb`), cela suggère une géométrie/empreinte liée aux obstructions, mais le rôle exact des champs reste inconnu et la routine est aussi appelée depuis deux autres fonctions. Le run #20 montrait également un helper qui met à jour une grille spatiale ; la preuve combinée suggère des traitements d'obstruction/occupation de carte mais pas encore le pathfinding. Prochaine cible : `function_selector=0x4a5558`, l'autre branche de `FUN_004839bb`, puis `0x483a6a`. Prioriser unités/obstacles, grille spatiale, déplacement/pathfinding, simulation, économie et IA. Séparer faits et hypothèses, garder les liens run/artifact et créer une branche + PR pour toute modification.
