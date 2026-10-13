# Passation de session — projet aoe-rea

**Mise à jour : 13 octobre 2026**  
**Dépôt :** https://github.com/rakmahefa/aoe-rea  
**Dernier run vérifié lors de la rédaction :** [REA binary analysis #23](https://github.com/rakmahefa/aoe-rea/actions/runs/38363697748)

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

### Dernier run en détail — #23

Le [run #23](https://github.com/rakmahefa/aoe-rea/actions/runs/38363697748) s'est terminé avec succès le 13 octobre 2026.

- Input effectif : `function_selector=0x483a6a` ; `search_query` et `xref_address` vides.
- Artifact : `rea-analysis` (run ID `38363697748`, artifact ID `11797128628`).
- Binaire : `retro/exe et dll/age3y.exe`.
- SHA-256 : `b1a1dab7264d2db72e8f8ae1df1e419eecc223b40db00c9d1013a3bc77611d9d`.
- Commit analysé : `ad539edede393f8d954bea01266e8d31fb4121f5`.
- REA `6.4.0`, Ghidra `12.1.4`.
- `function-selection.json` : `selector=0x483a6a`, `source=manual input`, `status=success`.
- Procédure : `FUN_00483a6a`, adresse d'entrée `0x483a6a`, ni externe ni thunk. Ghidra lui attribue 181 octets de code répartis sur quatre plages : `0x483a6a–0x483af3`, `0x483ee7–0x483eeb`, `0x48ce21–0x48ce2c`, `0x6a157e–0x6a1597`. Étendue totale supérieure à 2,2 MB : segmentation inhabituelle à garder en tête.
- Appelants listés : `FUN_004839bb`, `FUN_00497884` et `FUN_009c754c`.
- Dossiers de callees récupérés : `FUN_00483af4`, `FUN_00487ecc`, `FUN_004883dd`, `FUN_004a5cb7`.

Résumé du pseudocode observé :
1. Appelle un dispatch indirect via un pointeur chargé depuis une table de méthodes à l'offset `+0xac`. Si le résultat est faux, renvoie `0`.
2. Appelle `FUN_004883dd`. Si cette validation échoue, renvoie `4`.
3. Vérifie plusieurs champs de la structure à `this+0x5c`, dont un seuil `+0x54` et un bit `0x10` dans une structure référencée à `+0x50`.
4. Selon le résultat, fait un ou deux dispatchs indirects supplémentaires associés aux offsets de table `+0x90` et `+0x98`. Les résultats choisissent un code de retour `1`, `2` ou `3`.
5. Sur les chemins de résultat `1` ou `2`, met le bit `0x01` dans l'octet à `(objet associé + 0x1b)`. Sur le chemin `3`, met le bit `0x04`. Certaines branches renvoient `3` ou `4` sans suivre toutes les validations.

`FUN_004883dd` vérifie un descripteur attaché à `this+0x5c`; si un chemin de repli est utilisé, il examine un flottant à `this+0x68+8` contre le seuil `1e-6` et peut appeler `FUN_006a0831`. Les trois fonctions `FUN_00483af4`, `FUN_00487ecc` et `FUN_004a5cb7` sont des stubs de dispatch indirect non résolus dans ces rapports de deux octets. Les fonctions ciblées réellement par ces appels et la signification des codes et bits ne sont pas établies.

Interprétation prudente : `FUN_00483a6a` ressemble à une étape de validation/classification qui renvoie un état et met à jour des bits après la préparation d'une forme géométrique. Conjuguée aux runs #20–22, cela renforce la piste de gestion d'obstruction/géométrie/occupation, confiance moyenne, mais ne prouve pas une fonction de pathfinding.

## 5. Prochaine étape conseillée

**Maintenant, passer aux références du pathfinding.**

Lancer le workflow avec ces paramètres :

- `target_path=retro/exe et dll/age3y.exe`
- `xref_address=0xc19dc0` (texte défini associé à `kbCanPath2`)
- `function_selector` vide
- `search_query` vide

Examiner le `xrefs.json` retourné et déterminer si la référence mène à une véritable routine de code ou à une table/script d'enregistrement. N'utiliser l'adresse d'une fonction dans le prochain `function_selector` qu'après cette vérification. Puis répéter pour `kbCanSimPath` à `0xc19e68`.

Pourquoi changer de piste : les runs #20–23 ont établi une chaîne de preuves raisonnable pour la construction de rectangles/quadrilatères, les contrôles d’état, et l'actualisation d'une grille spatiale. Poursuivre le même cluster d'helpers a des rendements décroissants ; il faut maintenant chercher des preuves natives liées directement au pathfinding, puis au déplacement, à l'économie et à l'IA.

Garder les faits et les interprétations séparés. Les fonctions `FUN_...` sont des noms synthétiques Ghidra ; les stubs de dispatch indirect et les corps non contigus doivent être signalés comme limites.

## 6. Règles de travail pour la prochaine session

- Utiliser les capacités GitHub connectées pour inspecter le dépôt et Actions directement ; ne pas supposer que l’utilisateur doit recopier manuellement tous les résultats.
- Vérifier le dernier run à chaque reprise. L’historique ci-dessus est un instantané daté, et non une affirmation sur des exécutions futures.
- Pour les changements dans le dépôt, travailler sur une branche dédiée et ouvrir une pull request plutôt que de modifier `main` directement.
- Ajouter des notes de preuve : adresse, run/artifact, chaînes, imports, appels, interprétation et niveau de confiance.
- Séparer explicitement les faits observés des hypothèses. Ne pas présenter du pseudocode Ghidra comme code source original récupéré.
- Ne pas promettre ou prétendre qu’un port Linux natif existe tant qu’un ELF compilé et son comportement n’ont pas été validés.
- Respecter les droits d’utilisation. Ne pas publier des exécutables, DLL ou ressources propriétaires du jeu dans des releases sans autorisation ; préférer du code reconstruit, des instructions reproductibles et des fichiers fournis légalement par l’utilisateur.

## 7. Message de démarrage à copier dans une nouvelle session

> Nous poursuivons https://github.com/rakmahefa/aoe-rea. La PR #8 est fusionnée et la PR #9 documente les runs #22–23. Le run #23 a réussi avec `function_selector=0x483a6a`. La fonction exécute plusieurs contrôles, renvoie un code 0–4 et met parfois à jour les bits `+0x1b` de l’objet associé ; plusieurs appels sont des dispatchs indirects non résolus et la sémantique métier demeure inconnue. Les runs #20–23 soutiennent à confiance moyenne une piste géométrie/obstruction/occupation spatiale, sans prouver le pathfinding. Prochaine cible : lancer un run xref avec `xref_address=0xc19dc0` pour le texte `kbCanPath2`, puis analyser une fonction de code confirmée. Après cela, répéter pour `kbCanSimPath` (`0xc19e68`). Prioriser gameplay : unités, déplacement/pathfinding, simulation, économie et IA. Séparer faits et hypothèses, conserver les liens run/artifact et créer une branche + PR pour toute modification.
