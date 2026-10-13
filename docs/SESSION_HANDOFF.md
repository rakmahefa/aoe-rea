# Passation de session — projet aoe-rea

**Mise à jour : 13 octobre 2026**  
**Dépôt :** https://github.com/rakmahefa/aoe-rea  
**Dernier run vérifié lors de la rédaction :** [REA binary analysis #27](https://github.com/rakmahefa/aoe-rea/actions/runs/38433174077)

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
| [#23](https://github.com/rakmahefa/aoe-rea/actions/runs/38363697748) | `function_selector=0x483a6a` | Succès. `FUN_00483a6a` effectue des contrôles conditionnels, renvoie un code entre 0 et 4 et définit des bits d’état sur un objet associé. Plusieurs contrôles passent par des dispatchs indirects non résolus ; les codes et bits n’ont donc pas encore de sémantique métier confirmée. Après cette étape, priorité à l’analyse des xrefs du texte `kbCanPath2` (`0xc19dc0`). |
| [#24](https://github.com/rakmahefa/aoe-rea/actions/runs/38373803219) | Xrefs vers `kbCanPath2` à `0xc19dc0` | Succès. `xrefs.json` donne une référence directe à `0x889735` (confidence observée). Le rapport n'indique pas encore le type de référence ni la procédure englobante : la prochaine étape est d'analyser `function_selector=0x889735`. |
| [#25](https://github.com/rakmahefa/aoe-rea/actions/runs/38383598678) | `function_selector=0x889735` | Succès. L'adresse appartient à `FUN_00885d07`, routine d'enregistrement des APIs knowledge-base accessibles aux scripts. Le pseudocode enregistre `kbCanPath2` avec le callback `0x8827cc` et `kbCanSimPath` avec `0x88277e`, chacun avec 8 arguments. Ces callbacks sont les prochaines cibles ; leurs implémentations doivent encore être analysées. |
| [#26](https://github.com/rakmahefa/aoe-rea/actions/runs/38424403596) | `function_selector=0x8827cc` | Échec dans l'analyse de fonction : REA renvoie `No procedure exists at the requested address: 0x8827cc`. `LAB_008827cc` est une étiquette de callback dans le pseudocode d'enregistrement, pas une entrée de procédure reconnue à cette adresse. Le workflow et Ghidra se préparent correctement ; il faut résoudre le contexte de cette étiquette avant de sélectionner une fonction. |
| [#27](https://github.com/rakmahefa/aoe-rea/actions/runs/38433174077) | Input répété : `function_selector=0x8827cc` | Même échec que #26. Les logs confirment que `FUNCTION_SELECTOR=0x8827cc` est encore fourni et que `xref_address` est vide ; le diagnostic xref demandé n'a donc pas eu lieu. La prochaine exécution doit mettre `0x8827cc` dans le champ `xref_address` et laisser `function_selector` vide. |

### Dernier run en détail — #27

Le [run #27](https://github.com/rakmahefa/aoe-rea/actions/runs/38433174077) s'est terminé en échec le 13 octobre 2026.

- Input réellement utilisé : `function_selector=0x8827cc`; `search_query` et `xref_address` étaient vides.
- Artifact : `rea-analysis` (run ID `38433174077`, artifact ID `11832516485`).
- Binaire : `retro/exe et dll/age3y.exe`.
- SHA-256 : `b1a1dab7264d2db72e8f8ae1df1e419eecc223b40db00c9d1013a3bc77611d9d`.
- Commit analysé : `d8a134911c04bb51cd3f3369563ccedd9ad96a06`.
- REA `6.4.0`, Ghidra `12.1.4`.
- Installation et contrôle de disponibilité Ghidra : réussis. Étape `Analyze selected binary` : échec.
- `function-selection.json` indique `selector=0x8827cc`, `source=manual input`, `status=pending`.
- `function.json` renvoie `code=invalid_request`, `category=invalid_input`, `operation=analyze_function`, avec le message `No procedure exists at the requested address: 0x8827cc`.

Ce run n'est pas un essai du champ xref. Le journal d'environnement montre explicitement `FUNCTION_SELECTOR: 0x8827cc`. Le champ `xref_address` vide signifie que l'étape `Inspect address cross-references` a été sautée. Le run #27 reproduit donc l'erreur du run #26 sans tester la piste diagnostique.

## 5. Prochaine étape conseillée

**Relancer un xref-only en renseignant le bon champ.**

Dans **Actions → REA binary analysis → Run workflow**, configure exactement :

- `target_path=retro/exe et dll/age3y.exe`
- `xref_address=0x8827cc`
- `function_selector` vide
- `search_query` vide

Attention : les deux dernières tentatives ont saisi `0x8827cc` dans `function_selector`; ne répète pas ce réglage. Le workflow a alors cherché une entrée de fonction que Ghidra ne reconnaît pas. L'objectif du prochain run est au contraire de rechercher les références à cette adresse de callback. Ce test n'est pas garanti de trouver le corps réel, mais il est nécessaire avant de modifier le workflow.

Si le résultat ne montre que la référence depuis la routine d'enregistrement `FUN_00885d07`, il faudra ajouter une capacité au workflow/REA pour désassembler une plage de code ou résoudre la procédure contenant une adresse interne/étiquette. N'essaie pas encore `function_selector=0x88277e` : l'adresse de l'autre callback est elle aussi une étiquette `LAB_...` et n'a pas été confirmée comme entrée de procédure.

Les runs #20–23 documentent séparément la piste géométrie/obstruction/occupation spatiale. Ne pas conclure au pathfinding natif avant de comprendre les callbacks. Préserver les preuves, les erreurs exactes et les limites de segmentation Ghidra.

## 6. Règles de travail pour la prochaine session

- Utiliser les capacités GitHub connectées pour inspecter le dépôt et Actions directement ; ne pas supposer que l’utilisateur doit recopier manuellement tous les résultats.
- Vérifier le dernier run à chaque reprise. L’historique ci-dessus est un instantané daté, et non une affirmation sur des exécutions futures.
- Pour les changements dans le dépôt, travailler sur une branche dédiée et ouvrir une pull request plutôt que de modifier `main` directement.
- Ajouter des notes de preuve : adresse, run/artifact, chaînes, imports, appels, interprétation et niveau de confiance.
- Séparer explicitement les faits observés des hypothèses. Ne pas présenter du pseudocode Ghidra comme code source original récupéré.
- Ne pas promettre ou prétendre qu’un port Linux natif existe tant qu’un ELF compilé et son comportement n’ont pas été validés.
- Respecter les droits d’utilisation. Ne pas publier des exécutables, DLL ou ressources propriétaires du jeu dans des releases sans autorisation ; préférer du code reconstruit, des instructions reproductibles et des fichiers fournis légalement par l’utilisateur.

## 7. Message de démarrage à copier dans une nouvelle session

> Nous poursuivons https://github.com/rakmahefa/aoe-rea. La PR #10 est fusionnée. Run #25 a montré que `kbCanPath2` est enregistré avec l'étiquette callback `LAB_008827cc` et `kbCanSimPath` avec `LAB_0088277e`. Runs #26 et #27 ont tous deux échoué parce que l'input était `function_selector=0x8827cc`, et non parce que Ghidra était indisponible : REA dit `No procedure exists at the requested address: 0x8827cc`. Dans le run #27, `xref_address` était encore vide, donc le diagnostic attendu n'a pas eu lieu. Prochaine exécution : mettre `xref_address=0x8827cc`, laisser `function_selector` et `search_query` vides. Si le xref ne suffit pas, il faudra améliorer le workflow pour inspecter une adresse de code/résoudre une procédure contenant une étiquette. Les runs #20–23 étayent une piste distincte de géométrie/obstruction/occupation. Séparer faits, hypothèses et limites, garder les liens run/artifact et créer une branche + PR pour les changements.
