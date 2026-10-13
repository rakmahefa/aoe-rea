# Passation de session — projet aoe-rea

**Mise à jour : 13 octobre 2026**  
**Dépôt :** https://github.com/rakmahefa/aoe-rea  
**Dernier run vérifié lors de la rédaction :** [REA binary analysis #20](https://github.com/rakmahefa/aoe-rea/actions/runs/38347489501)

## 1. But du projet

Le projet vise à étudier Age of Empires III à l’aide de REA et Ghidra, puis à reconstruire progressivement les comportements nécessaires dans du code maintenable afin de parvenir, à terme, à un véritable exécutable Linux natif (ELF). Le but n’est pas de se limiter à Wine/Proton, à un lanceur ou à des rapports de décompilation.

**État réel : recherche statique précoce.** Aucun code source original complet n’a été récupéré, aucun port natif complet n’a été construit et aucun exécutable ELF du jeu n’est disponible à ce stade. Les noms `FUN_...` sont générés par l’analyse ; le pseudocode est une interprétation de Ghidra, pas le code original.

## 2. État vérifié du dépôt

- Dépôt GitHub : https://github.com/rakmahefa/aoe-rea
- Branche principale : `main`
- Commit `main` observé lors de cette mise à jour : `2af4177c8962a3bb0dba40d2594f98d43eef6ff1` (fusion de la PR #4). Vérifier de nouveau le commit avant de poursuivre.
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

### Dernier run en détail — #20

Le [run #20](https://github.com/rakmahefa/aoe-rea/actions/runs/38347489501) s'est terminé avec succès le 13 octobre 2026.

- Input effectif : `function_selector=0x6a15ca` ; recherche et xrefs vides.
- Binaire : `retro/exe et dll/age3y.exe`.
- SHA-256 : `b1a1dab7264d2db72e8f8ae1df1e419eecc223b40db00c9d1013a3bc77611d9d`.
- Commit analysé : `97a2e081d5cbf72c161756dba16599cf80fb61f8`.
- REA `6.4.0`, Ghidra `12.1.4`.
- `function-selection.json` indique `selector: 0x6a15ca`, `source: manual input`, `status: success`.
- La procédure sélectionnée est `FUN_004839bb`, entrée `0x4839bb`, avec 9 appelants et 7 callees répertoriés.
- Son corps contient trois plages non contiguës : `0x4839bb–0x483a69`, `0x4b8f9e–0x4b8fc8`, et `0x6a1598–0x6a15e8`. La plage de la référence qui pousse l'adresse de chaîne est la dernière (`0x6a15ca`). Le fait que Ghidra regroupe ces blocs distants reste une limite de segmentation à garder à l'esprit.

Pseudocode de `FUN_004839bb`, résumé de l'observation :
1. Retourne faux si le paramètre ou le pointeur à `this+0x90` est nul.
2. Lit le champ à l'offset `0x18` de l'objet associé. Si sa valeur n'est pas `1`, appelle les utilitaires de journalisation/chaîne, émet le diagnostic d'obstruction d'unité et retourne faux.
3. Dans le chemin normal, inspecte un seuil à l'offset `0x54` et un bit dans une table de propriétés à partir de `this+0x5c`. Selon ce test, appelle `FUN_00483d4c` ou `FUN_004a5558`, en transmettant l'objet associé, des valeurs de coordonnées et des dimensions.
4. Appelle `FUN_00483a6a`, passe sa valeur de retour ainsi que l'objet associé à `FUN_0048380f`, puis retourne le résultat de ce dernier.

Le dossier séparé de `FUN_0048380f` récupéré dans `callees/48380f_FUN_0048380f.json` arrondit quatre bornes flottantes, les limite aux dimensions de la grille, calcule une cellule spatiale, vérifie si l'entrée a changé de cellule, retire l'ancien rattachement le cas échéant puis appelle un helper d'insertion et actualise les coordonnées/index stockés. C'est une preuve convergente d'une structure spatiale ou d'un registre d'occupation. Les noms `FUN_...` restent synthétiques et aucune étiquette officielle du moteur n'a été établie.

## 5. Prochaine étape conseillée

**Priorité immédiate : analyser le helper `0x483d4c`.**

Dans la prochaine exécution du workflow, utiliser :

- `target_path=retro/exe et dll/age3y.exe`
- `function_selector=0x483d4c`
- `search_query` vide
- `xref_address` vide

Pourquoi cette cible : `FUN_00483d4c` est appelée sur le chemin normal de `FUN_004839bb`, avec l'objet d'obstruction et des coordonnées/dimensions apparentes. Son dossier devrait aider à dire si elle calcule, applique ou parcourt une empreinte spatiale. Examiner son pseudocode, ses instructions, ses références, ses appelants et les callees, sans attribuer de noms métiers non confirmés.

Ensuite, analyser `0x4a5558` pour comprendre le chemin alternatif sélectionné par le test de propriété/flag, puis `0x483a6a` si son rôle reste flou. Si les résultats conduisent vers le calcul d'obstacles ou la mise à jour d'occupation de carte, cette famille de fonctions devient notre première piste native corroborée autour des unités et de la grille spatiale. Le pathfinding proprement dit reste à explorer à part via `kbCanPath2` (`0xc19dc0`) et `kbCanSimPath` (`0xc19e68`).

Documenter à chaque fois le run, le sélecteur, les adresses, les extraits de preuve, le niveau de confiance et les limites de segmentation Ghidra. Ne pas traiter du pseudocode décompilé comme du code source original.

## 6. Règles de travail pour la prochaine session

- Utiliser les capacités GitHub connectées pour inspecter le dépôt et Actions directement ; ne pas supposer que l’utilisateur doit recopier manuellement tous les résultats.
- Vérifier le dernier run à chaque reprise. L’historique ci-dessus est un instantané daté, et non une affirmation sur des exécutions futures.
- Pour les changements dans le dépôt, travailler sur une branche dédiée et ouvrir une pull request plutôt que de modifier `main` directement.
- Ajouter des notes de preuve : adresse, run/artifact, chaînes, imports, appels, interprétation et niveau de confiance.
- Séparer explicitement les faits observés des hypothèses. Ne pas présenter du pseudocode Ghidra comme code source original récupéré.
- Ne pas promettre ou prétendre qu’un port Linux natif existe tant qu’un ELF compilé et son comportement n’ont pas été validés.
- Respecter les droits d’utilisation. Ne pas publier des exécutables, DLL ou ressources propriétaires du jeu dans des releases sans autorisation ; préférer du code reconstruit, des instructions reproductibles et des fichiers fournis légalement par l’utilisateur.

## 7. Message de démarrage à copier dans une nouvelle session

> Nous poursuivons le projet https://github.com/rakmahefa/aoe-rea. Le run #20 a réussi `function_selector=0x6a15ca` et a résolu `FUN_004839bb` (entrée `0x4839bb`). Son pseudocode vérifie le type d'obstruction d'un objet d'unité, puis appelle `FUN_00483d4c` ou `FUN_004a5558`, `FUN_00483a6a` et `FUN_0048380f`. Ce dernier helper recalcule une cellule spatiale à partir de bornes, retire/réinsère l'objet si elle change ; cela suggère une gestion d'obstruction/grille, confiance moyenne. Attention : Ghidra regroupe trois plages non contiguës dans la fonction. Prochaine cible : relancer avec `function_selector=0x483d4c`, puis examiner les résultats réels. Prioriser unités/obstacles, grille spatiale, déplacement/pathfinding, simulation, économie et IA. Séparer faits et hypothèses, garder les liens run/artifact et créer une branche + PR pour toute modification.
