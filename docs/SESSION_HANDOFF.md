# Passation de session — projet aoe-rea

**Mise à jour : 17 octobre 2026**  
**Dépôt :** https://github.com/rakmahefa/aoe-rea  
**Dernière analyse principale vérifiée :** [REA binary analysis #30](https://github.com/rakmahefa/aoe-rea/actions/runs/38452908507) ; dossier de fonction `FUN_0087157b` : [sonde ponctuelle #32, Actions run ID 38733263497](https://github.com/rakmahefa/aoe-rea/actions/runs/38733263497) ([artefact 11970339116](https://github.com/rakmahefa/aoe-rea/actions/runs/38733263497/artifacts/11970339116)) ; dossier helper `FUN_00799898` : [sonde #33](https://github.com/rakmahefa/aoe-rea/actions/runs/38734503232) ([artefact 11972660987](https://github.com/rakmahefa/aoe-rea/actions/runs/38734503232/artifacts/11972660987)) ; dossier du résolveur `FUN_00798492` : [sonde #35](https://github.com/rakmahefa/aoe-rea/actions/runs/38736569975) ([artefact 11974527446](https://github.com/rakmahefa/aoe-rea/actions/runs/38736569975/artifacts/11974527446)) ; dossier de l'itérateur `FUN_004af0c9` : [sonde #36](https://github.com/rakmahefa/aoe-rea/actions/runs/38737601357) ([artefact 11973429389](https://github.com/rakmahefa/aoe-rea/actions/runs/38737601357/artifacts/11973429389)) ; dossier de `FUN_004aefe9` : [sonde #37](https://github.com/rakmahefa/aoe-rea/actions/runs/38739802167) ([artefact 11975426935](https://github.com/rakmahefa/aoe-rea/actions/runs/38739802167/artifacts/11975426935)) ; dossier `FUN_004af120` : [sonde #38](https://github.com/rakmahefa/aoe-rea/actions/runs/38740230871) ([artefact 11975947354](https://github.com/rakmahefa/aoe-rea/actions/runs/38740230871/artifacts/11975947354)) ; dossier `FUN_004aefb7` : [sonde #39](https://github.com/rakmahefa/aoe-rea/actions/runs/38740603626) ([artefact 11976087652](https://github.com/rakmahefa/aoe-rea/actions/runs/38740603626/artifacts/11976087652)) ; dossier `FUN_004aeee8` : [sonde #40](https://github.com/rakmahefa/aoe-rea/actions/runs/38742083079) ([artefact 11977520029](https://github.com/rakmahefa/aoe-rea/actions/runs/38742083079/artifacts/11977520029)) ; dossier `FUN_0058e2c3` : [sonde #41](https://github.com/rakmahefa/aoe-rea/actions/runs/38743002770) ([artefact 11976439859](https://github.com/rakmahefa/aoe-rea/actions/runs/38743002770/artifacts/11976439859)) ; dossier d'insertion dans le tas `FUN_004afb4c` : [sonde #42](https://github.com/rakmahefa/aoe-rea/actions/runs/38743994938) ([artefact 11978560249](https://github.com/rakmahefa/aoe-rea/actions/runs/38743994938/artifacts/11978560249)) ; dossier de son appelant `FUN_004ae7b1` terminé : [probe #43](https://github.com/rakmahefa/aoe-rea/actions/runs/38745133893) ([artefact 11978346441](https://github.com/rakmahefa/aoe-rea/actions/runs/38745133893/artifacts/11978346441)) ; dossier de mise à jour du tas `FUN_004b1e94` : [probe #44](https://github.com/rakmahefa/aoe-rea/actions/runs/38772710258) ([artefact 11991884059](https://github.com/rakmahefa/aoe-rea/actions/runs/38772710258/artifacts/11991884059)) ; dossier de l'autre appelant `FUN_008caa04` : [probe #45](https://github.com/rakmahefa/aoe-rea/actions/runs/38774292963) ([artefact 11993540489](https://github.com/rakmahefa/aoe-rea/actions/runs/38774292963/artifacts/11993540489)) ; dossier d'insertion dans `DAT_00cafb9c` : [probe #46](https://github.com/rakmahefa/aoe-rea/actions/runs/38775891857) ([artefact 11994206385](https://github.com/rakmahefa/aoe-rea/actions/runs/38775891857/artifacts/11994206385)) ; dossier de recherche par coordonnées `FUN_004ae797` : [probe #47](https://github.com/rakmahefa/aoe-rea/actions/runs/38782180985) ([artefact 11996292779](https://github.com/rakmahefa/aoe-rea/actions/runs/38782180985/artifacts/11996292779)) ; dossier pool d'entrées `FUN_004adea4` : [probe #48](https://github.com/rakmahefa/aoe-rea/actions/runs/38783723125) ([artefact 11996853539](https://github.com/rakmahefa/aoe-rea/actions/runs/38783723125/artifacts/11996853539)) ; boucle de callbacks `FUN_00401fa0` : [probe #49](https://github.com/rakmahefa/aoe-rea/actions/runs/38785347582) ([artefact 11998191528](https://github.com/rakmahefa/aoe-rea/actions/runs/38785347582/artifacts/11998191528)) ; saut indirect `JMP EAX` à `0x401fd6` : [probe #50](https://github.com/rakmahefa/aoe-rea/actions/runs/38852450383) ([artefact 12025552949](https://github.com/rakmahefa/aoe-rea/actions/runs/38852450383/artifacts/12025552949)) ; entrée callback `MOV EAX,ECX` à `0x8ca934` : [probe #52](https://github.com/rakmahefa/aoe-rea/actions/runs/38853201623) ([artefact 12025469262](https://github.com/rakmahefa/aoe-rea/actions/runs/38853201623/artifacts/12025469262)) ; continuation `XOR ECX,ECX` à `0x8ca936` : [probe #53](https://github.com/rakmahefa/aoe-rea/actions/runs/38853803910) ([artefact 12026795710](https://github.com/rakmahefa/aoe-rea/actions/runs/38853803910/artifacts/12026795710)) ; écriture `MOV [EAX+0x2c],ECX` à `0x8ca938` : [probe #54](https://github.com/rakmahefa/aoe-rea/actions/runs/38854422589) ([artefact 12026542570](https://github.com/rakmahefa/aoe-rea/actions/runs/38854422589/artifacts/12026542570)) ; tentative dossier fonction `0x8ca934` refusée car aucune procédure Ghidra n'existe : [probe #55](https://github.com/rakmahefa/aoe-rea/actions/runs/38854789080) ([artefact 12026372536](https://github.com/rakmahefa/aoe-rea/actions/runs/38854789080/artifacts/12026372536)) ; écriture du lien avant `MOV [EAX+0x28],ECX` à `0x8ca93b` : [probe #56](https://github.com/rakmahefa/aoe-rea/actions/runs/38855936196) ([artefact 12027357090](https://github.com/rakmahefa/aoe-rea/actions/runs/38855936196/artifacts/12027357090)) ; retour du callback `RET` à `0x8ca93e` : [probe #57](https://github.com/rakmahefa/aoe-rea/actions/runs/38856897665) ([artefact 12026774512](https://github.com/rakmahefa/aoe-rea/actions/runs/38856897665/artifacts/12026774512)) ; sondes de continuation appelante : #58 à `0x401fc8` ([run 38923177848, artefact 12055028788](https://github.com/rakmahefa/aoe-rea/actions/runs/38923177848/artifacts/12055028788)) et #59 à `0x401fca` ([run 39012977596, artefact 12094140406](https://github.com/rakmahefa/aoe-rea/actions/runs/39012977596/artifacts/12094140406)) ; prochaine cible `0x401fcd`.

## 1. But du projet

Le projet vise à étudier Age of Empires III à l’aide de REA et Ghidra, puis à reconstruire progressivement les comportements nécessaires dans du code maintenable afin de parvenir, à terme, à un véritable exécutable Linux natif (ELF). Le but n’est pas de se limiter à Wine/Proton, à un lanceur ou à des rapports de décompilation.

**État réel : recherche statique précoce.** Aucun code source original complet n’a été récupéré, aucun port natif complet n’a été construit et aucun exécutable ELF du jeu n’est disponible à ce stade. Les noms `FUN_...` sont générés par l’analyse ; le pseudocode est une interprétation de Ghidra, pas le code original.

## 2. État vérifié du dépôt

- Dépôt GitHub : https://github.com/rakmahefa/aoe-rea
- Branche principale : `main`
- Commit `main` vérifié : `4dd1e638cb53e77375c4b1061e5f290a6ea73af0` (fusion de la PR #16, qui suit le commit `489abee57d8677f7a9cbe7a18bcd074f36fe3717`). Vérifier de nouveau le commit avant toute nouvelle branche.
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
| [#28](https://github.com/rakmahefa/aoe-rea/actions/runs/38437864410) | `xref_address=0x8827cc` | Succès. `xrefs.json` retourne une seule référence à `0x88960a`, l'instruction de la routine d'enregistrement qui pousse le pointeur de callback avant l'appel à `FUN_00624f52`. Le xref confirme l'enregistrement, mais ne révèle pas le corps du callback ; prochaine étape : inspecter l'instruction à `0x8827cc` directement. |
| [#29](https://github.com/rakmahefa/aoe-rea/actions/runs/38448930654) | `instruction_address=0x8827cc` | Succès. La nouvelle inspection décode 5 octets (`a1 34 62 c6 00`) en `MOV EAX,[0x00c66234]`, une lecture de donnée/global, sans procédure englobante récupérée (`procedure=null`). Le flux est `FALL_THROUGH`. Étape suivante : inspecter l’instruction à `0x8827d1`, puis continuer selon le flux de contrôle observé. |
| [#30](https://github.com/rakmahefa/aoe-rea/actions/runs/38452908507) | `instruction_address=0x8827d1` | Succès. Six octets (`8b 88 3c 01 00 00`) se décodent en `MOV ECX,dword ptr [EAX + 0x13c]`, flux `FALL_THROUGH`, `procedure=null`. Artifact `11841443159`. Les sondes ultérieures sont documentées à la section 5. |

### Détail de référence — run #29

Le [run #29](https://github.com/rakmahefa/aoe-rea/actions/runs/38448930654) s'est terminé avec succès le 13 octobre 2026.

- Input effectif : `instruction_address=0x8827cc`; `function_selector`, `search_query` et `xref_address` vides.
- Artifact : `rea-analysis` (run ID `38448930654`, artifact ID `11839108635`).
- Binaire : `retro/exe et dll/age3y.exe`.
- SHA-256 : `b1a1dab7264d2db72e8f8ae1df1e419eecc223b40db00c9d1013a3bc77611d9d`.
- Commit analysé : `813677b565d1e26535c5908cc194e421603afe90`.
- REA `6.4.0`, Ghidra `12.1.4`.
- Le step `Inspect native instruction address` a réussi ; analyse de fonction et xrefs ont été sautées.
- `instruction.json` : `operation=inspect_native_instruction`, `parameters.address=0x8827cc`, `status=decoded`, `confidence=observed`, `procedure=null`.
- Octets observés : `a1 34 62 c6 00`, longueur 5.
- Désassemblage : `MOV EAX,[0x00c66234]`.
- Flux : `FALL_THROUGH`, non conditionnel, aucune destination directe.
- Référence : accès de lecture `0x8827cc → 0x00c66234`; la signification du champ global est inconnue.
- Limite signalée par REA/Ghidra : les tokens opérandes n'exposent pas les rôles d'adressage mémoire plus détaillés ni le contexte de mode par instruction.

Interprétation prudente : l'adresse callback correspond bien à des octets que Ghidra décode comme une instruction x86, mais elle n'est pas associée à une procédure identifiée. L'instruction lit une adresse absolue globale et laisse le flux continuer. Ce fait seul ne permet pas de savoir si le chargement prépare la suite d'un wrapper, saute ensuite via un appel indirect, ou appartient à un corps que Ghidra n'a pas délimité comme fonction.

Comme la longueur décodée est 5 octets et le flux est fall-through, l'adresse adjacente suivante est `0x8827d1`. L'inspection instruction par instruction devra reconstruire assez de séquence pour identifier les opérations suivantes et un éventuel saut/appel/retour. L'adresse du callback reste une étiquette de code, pas encore une entrée de procédure Ghidra reconnue.

## 5. État actuel de `kbCanPath2` et prochaine étape

### Séquence native observée

Toutes les adresses d'instruction ci-dessous décodent dans le binaire de référence avec Ghidra 12.1.4. Pour les instructions du callback, REA rapporte toujours `procedure=null`; elles ne prouvent donc pas encore la frontière d'une procédure complète.

| Adresse | Instruction et flux | Run / artifact |
|---|---|---|
| `0x8827cc` | `a1 34 62 c6 00` — `MOV EAX,[0x00c66234]`, 5 octets, `FALL_THROUGH` | [#29](https://github.com/rakmahefa/aoe-rea/actions/runs/38448930654), [11839108635](https://github.com/rakmahefa/aoe-rea/actions/runs/38448930654/artifacts/11839108635) |
| `0x8827d1` | `8b 88 3c 01 00 00` — `MOV ECX,[EAX+0x13c]`, 6 octets, `FALL_THROUGH` | [#30](https://github.com/rakmahefa/aoe-rea/actions/runs/38452908507), [11841443159](https://github.com/rakmahefa/aoe-rea/actions/runs/38452908507/artifacts/11841443159) |
| `0x8827d7` | `TEST ECX,ECX`, 2 octets | [probe](https://github.com/rakmahefa/aoe-rea/actions/runs/38505129056), [11868005187](https://github.com/rakmahefa/aoe-rea/actions/runs/38505129056/artifacts/11868005187) |
| `0x8827d9` | `JZ 0x8827f5`, saut conditionnel, 2 octets | [probe](https://github.com/rakmahefa/aoe-rea/actions/runs/38505701574), [11867433197](https://github.com/rakmahefa/aoe-rea/actions/runs/38505701574/artifacts/11867433197) |
| `0x8827db` | `MOV EDX,[0x00c66664]`, 6 octets | [probe](https://github.com/rakmahefa/aoe-rea/actions/runs/38506248967), [11868017112](https://github.com/rakmahefa/aoe-rea/actions/runs/38506248967/artifacts/11868017112) |
| `0x8827e1` | `PUSH EDX`, 1 octet | [probe](https://github.com/rakmahefa/aoe-rea/actions/runs/38506676784), [11868386272](https://github.com/rakmahefa/aoe-rea/actions/runs/38506676784/artifacts/11868386272) |
| `0x8827e2` | `CALL 0x44cb21`, 5 octets | [probe](https://github.com/rakmahefa/aoe-rea/actions/runs/38507195067), [11868985480](https://github.com/rakmahefa/aoe-rea/actions/runs/38507195067/artifacts/11868985480) |
| `0x8827e7` | `TEST EAX,EAX`, 2 octets | [probe](https://github.com/rakmahefa/aoe-rea/actions/runs/38508299938), [11868907012](https://github.com/rakmahefa/aoe-rea/actions/runs/38508299938/artifacts/11868907012) |
| `0x8827e9` | `JZ 0x8827f5`, saut conditionnel, 2 octets | [probe](https://github.com/rakmahefa/aoe-rea/actions/runs/38508675506), [11869745563](https://github.com/rakmahefa/aoe-rea/actions/runs/38508675506/artifacts/11869745563) |
| `0x8827eb` | `MOV EAX,[EAX+0x80]`, 6 octets, `FALL_THROUGH` | [probe](https://github.com/rakmahefa/aoe-rea/actions/runs/38512045239), [11870287872](https://github.com/rakmahefa/aoe-rea/actions/runs/38512045239/artifacts/11870287872) |
| `0x8827f1` | `TEST EAX,EAX`, 2 octets, `FALL_THROUGH` | [probe](https://github.com/rakmahefa/aoe-rea/actions/runs/38512425597), [11870802007](https://github.com/rakmahefa/aoe-rea/actions/runs/38512425597/artifacts/11870802007) |
| `0x8827f3` | `JNZ 0x8827f8`, 2 octets, saut conditionnel direct | [probe](https://github.com/rakmahefa/aoe-rea/actions/runs/38513028245), [11870374493](https://github.com/rakmahefa/aoe-rea/actions/runs/38513028245/artifacts/11870374493) |
| `0x8827f5` | `XOR AL,AL`, 2 octets | [probe](https://github.com/rakmahefa/aoe-rea/actions/runs/38508468586), [11868359993](https://github.com/rakmahefa/aoe-rea/actions/runs/38508468586/artifacts/11868359993) |
| `0x8827f7` | `RET`, 1 octet, `RETURN` | [probe](https://github.com/rakmahefa/aoe-rea/actions/runs/38511605181), [11870545584](https://github.com/rakmahefa/aoe-rea/actions/runs/38511605181/artifacts/11870545584) |
| `0x8827f8` | `MOV EDX,[ESP+0xc]`, 4 octets, `FALL_THROUGH`, `procedure=null` | [run #14](https://github.com/rakmahefa/aoe-rea/actions/runs/38513505693), [11870019274](https://github.com/rakmahefa/aoe-rea/actions/runs/38513505693/artifacts/11870019274) |
| `0x8827fc` | `PUSH 0x799782`, 5 octets, `FALL_THROUGH`, référence `DATA` vers `0x799782` | [run #15](https://github.com/rakmahefa/aoe-rea/actions/runs/38526015005), [11875972173](https://github.com/rakmahefa/aoe-rea/actions/runs/38526015005/artifacts/11875972173) |
| `0x882801` | `PUSH 0x0`, 2 octets, `FALL_THROUGH`, `procedure=null` | [run #16](https://github.com/rakmahefa/aoe-rea/actions/runs/38526782966), [11876875242](https://github.com/rakmahefa/aoe-rea/actions/runs/38526782966/artifacts/11876875242) |
| `0x882803` | `PUSH 0x0`, 2 octets, `FALL_THROUGH`, `procedure=null` | [run #17](https://github.com/rakmahefa/aoe-rea/actions/runs/38527580929), [11876802096](https://github.com/rakmahefa/aoe-rea/actions/runs/38527580929/artifacts/11876802096) |
| `0x882805` | `PUSH 0x0`, 2 octets, `FALL_THROUGH`, `procedure=null` | [run #18](https://github.com/rakmahefa/aoe-rea/actions/runs/38528517211), [11877336853](https://github.com/rakmahefa/aoe-rea/actions/runs/38528517211/artifacts/11877336853) |
| `0x882807` | `PUSH 0x0`, 2 octets, `FALL_THROUGH`, `procedure=null` | [run #19](https://github.com/rakmahefa/aoe-rea/actions/runs/38529441143), [11878120336](https://github.com/rakmahefa/aoe-rea/actions/runs/38529441143/artifacts/11878120336) |
| `0x882809` | `PUSH 0x0`, 2 octets, `FALL_THROUGH`, `procedure=null` | [run #20](https://github.com/rakmahefa/aoe-rea/actions/runs/38530554944), [11878127349](https://github.com/rakmahefa/aoe-rea/actions/runs/38530554944/artifacts/11878127349) |
| `0x88280b` | `PUSH 0x0`, 2 octets, `FALL_THROUGH`, `procedure=null` | [run #21](https://github.com/rakmahefa/aoe-rea/actions/runs/38535073544), [11880091082](https://github.com/rakmahefa/aoe-rea/actions/runs/38535073544/artifacts/11880091082) |
| `0x88280d` | `8d 4c 24 2c` — `LEA ECX,[ESP+0x2c]`, 4 octets, `FALL_THROUGH`, `procedure=null` | [run #22](https://github.com/rakmahefa/aoe-rea/actions/runs/38536133294), [11881235066](https://github.com/rakmahefa/aoe-rea/actions/runs/38536133294/artifacts/11881235066) |
| `0x882811` | `51` — `PUSH ECX`, 1 octet, `FALL_THROUGH`, `procedure=null` | [run #23](https://github.com/rakmahefa/aoe-rea/actions/runs/38543440912), [11884165751](https://github.com/rakmahefa/aoe-rea/actions/runs/38543440912/artifacts/11884165751) |
| `0x882812` | `8b 4c 24 28` — `MOV ECX,dword ptr [ESP+0x28]`, 4 octets, `FALL_THROUGH`, `procedure=null` | [run #24](https://github.com/rakmahefa/aoe-rea/actions/runs/38592966677), [11909780246](https://github.com/rakmahefa/aoe-rea/actions/runs/38592966677/artifacts/11909780246) |
| `0x882816` | `52` — `PUSH EDX`, 1 octet, `FALL_THROUGH`, `procedure=null` | [run #25](https://github.com/rakmahefa/aoe-rea/actions/runs/38593942037), [11908194310](https://github.com/rakmahefa/aoe-rea/actions/runs/38593942037/artifacts/11908194310) |
| `0x882817` | `8b 54 24 28` — `MOV EDX,dword ptr [ESP+0x28]`, 4 octets, `FALL_THROUGH`, `procedure=null` | [run #26](https://github.com/rakmahefa/aoe-rea/actions/runs/38682182138), [11947964421](https://github.com/rakmahefa/aoe-rea/actions/runs/38682182138/artifacts/11947964421) |
| `0x88281b` | `51` — `PUSH ECX`, 1 octet, `FALL_THROUGH`, `procedure=null` | [run #27](https://github.com/rakmahefa/aoe-rea/actions/runs/38684233397), [11948769728](https://github.com/rakmahefa/aoe-rea/actions/runs/38684233397/artifacts/11948769728) |
| `0x88281c` | `52` — `PUSH EDX`, 1 octet, `FALL_THROUGH`, `procedure=null` | [run #28](https://github.com/rakmahefa/aoe-rea/actions/runs/38686269488), [11950941183](https://github.com/rakmahefa/aoe-rea/actions/runs/38686269488/artifacts/11950941183) |
| `0x88281d` | `8b c8` — `MOV ECX,EAX`, 2 octets, `FALL_THROUGH`, `procedure=null` | [sonde séquentielle #29; Actions run ID 38691004803](https://github.com/rakmahefa/aoe-rea/actions/runs/38691004803), [11952515685](https://github.com/rakmahefa/aoe-rea/actions/runs/38691004803/artifacts/11952515685) |
| `0x88281f` | `e8 57 ed fe ff` — `CALL 0x0087157b`, 5 octets, appel direct inconditionnel, `procedure=null` | [Sonde ponctuelle #30; Actions run ID 38731342538](https://github.com/rakmahefa/aoe-rea/actions/runs/38731342538), [11970986662](https://github.com/rakmahefa/aoe-rea/actions/runs/38731342538/artifacts/11970986662) |
| `0x87157b` | `8b 44 24 20` — `MOV EAX,dword ptr [ESP+0x20]`, 4 octets, `FALL_THROUGH`, `procedure=0x87157b` | [Sonde ponctuelle #31; Actions run ID 38732373199](https://github.com/rakmahefa/aoe-rea/actions/runs/38732373199), [11971133081](https://github.com/rakmahefa/aoe-rea/actions/runs/38732373199/artifacts/11971133081) |

### Helper appelé

Le `CALL` à `0x8827e2` vise `FUN_0044cb21`. Son dossier REA/Ghidra ([run](https://github.com/rakmahefa/aoe-rea/actions/runs/38507674474), [artifact 11868089731](https://github.com/rakmahefa/aoe-rea/actions/runs/38507674474/artifacts/11868089731)) indique que la fonction vérifie que son argument entier est non négatif et inférieur à `*(ECX+0x5c)`. Si l'index est valide, elle lit un dword depuis le tableau pointé par `ECX+0x58`; sinon elle renvoie zéro. Le corps Ghidra est non contigu : `0x44cb21–0x44cb3e` et `0x4649e1–0x4649e5`. Au site d'appel, `EDX` est poussé en argument après avoir été chargé depuis `0x00c66664`; `ECX` conserve la valeur chargée depuis `[EAX+0x13c]`.

### Dossier de fonction — `FUN_0087157b` (sonde ponctuelle #32)

Preuve : [run #32, ID 38733263497](https://github.com/rakmahefa/aoe-rea/actions/runs/38733263497) ; [artefact 11970339116](https://github.com/rakmahefa/aoe-rea/actions/runs/38733263497/artifacts/11970339116).

- Ghidra identifie une procédure continue de `0x87157b` à `0x871808` inclus (654 octets). Les types du pseudocode sont des déductions par défaut de faible confiance ; conserver les noms `param_N` tant que les sites d'appel ne permettent pas mieux.
- Le caller à `0x88281f` prépare 11 arguments sur la pile et `ECX`. Les chemins de retour de la procédure utilisent `RET 0x2c` (44 octets), cohérent avec 11 arguments de pile de quatre octets. Cela établit la mécanique d'appel, pas le sens métier des paramètres.
- Le pseudocode traite `param_1` et `param_2` comme des pointeurs vers des flottants et calcule `sqrt((param_2[0]-param_1[0])² + (param_2[2]-param_1[2])²)`. Si le pointeur optionnel `param_4` désigne un seuil supérieur à cette distance, la fonction renvoie tôt une valeur vraie apparente.
- La chaîne `tempKBPath` est référencée à `0x00c14068`. La fonction récupère cette entrée via `FUN_0086f5d3` et `FUN_0086d3c5`, puis appelle `FUN_00799898`. En cas de succès, elle peut écrire l'identifiant retourné via `param_8` ; en cas d'échec, elle appelle `FUN_00871539` avant un retour faux apparent (`AL=0`).
- Autres références d'appel entrantes observées : `0x7400f5`, `0x7448e4`, `0x744c65` et `0x7450cd`. Cette procédure n'est donc pas utilisée exclusivement par le callback `kbCanPath2`.

**Hypothèse fortement étayée, mais pas un nom original récupéré :** compte tenu de la description enregistrée de `kbCanPath2` comme vérification de chemin booléenne, des contrôles de distance/position et de la requête `tempKBPath`, ce corps est fortement compatible avec une méthode de vérification de chemin. Les sens exacts des paramètres, le type d'objet et le rôle précis de `FUN_00799898` restent à déterminer. La sonde ponctuelle #33 ([run ID 38734503232](https://github.com/rakmahefa/aoe-rea/actions/runs/38734503232)) analyse maintenant `FUN_00799898`.

### Dossier helper — `FUN_00799898` (sonde ponctuelle #33)

Preuve : [run #33, ID 38734503232](https://github.com/rakmahefa/aoe-rea/actions/runs/38734503232) ; [artefact 11972660987](https://github.com/rakmahefa/aoe-rea/actions/runs/38734503232/artifacts/11972660987).

- Ghidra identifie une procédure continue de `0x799898` à `0x799938` inclus (161 octets). Les types des neuf `param_N` sont des déductions par défaut de faible confiance.
- La fonction appelle `FUN_00798492` pour `param_2` et `param_3`; si l'une des résolutions renvoie zéro, la fonction retourne zéro.
- Elle lit un entier signé sur 16 bits à l'offset `+0xac` de chaque objet résolu, puis délègue à `FUN_00798815` en lui transmettant `param_1`, les deux champs extraits, `param_4` et `param_5` à `param_9`.
- Si `FUN_00798815` renvoie une valeur non nulle et que l'entier à `param_4 + 8` est positif, elle appelle `FUN_004dfcfb(0, param_2)` puis `FUN_004dfcfb(longueur - 1, param_3)`, et retourne un. Sinon, elle retourne zéro.
- Ghidra indique deux appelants : `FUN_0087157b` à `0x87157b` et `FUN_008722c4` à `0x8722c4`.

**Interprétation encore prudente :** cette fonction résout deux objets, extrait des champs/identifiants courts, délègue la décision principale et touche conditionnellement les première et dernière entrées d'un objet qui contient une longueur. Le sens métier de ces objets, du champ `param_4 + 8` et de `FUN_004dfcfb` n'est pas établi. La sonde #34 ([run ID 38735602782](https://github.com/rakmahefa/aoe-rea/actions/runs/38735602782)) analyse maintenant `FUN_00798815`, helper directement appelé.

### Dossier helper central — `FUN_00798815` (sonde ponctuelle #34)

Preuve : [run #34, ID 38735602782](https://github.com/rakmahefa/aoe-rea/actions/runs/38735602782) ; [artefact 11974515991](https://github.com/rakmahefa/aoe-rea/actions/runs/38735602782/artifacts/11974515991).

- Ghidra identifie une procédure continue de 766 octets, de `0x798815` à `0x798b12` inclus. Les noms/types sémantiques des paramètres restent hypothétiques.
- La fonction contrôle `param_2` et `param_3` contre une collection reçue dans `ECX` (compte à `+8`, table de pointeurs à `+4`) et retourne zéro si l'un des indices est hors limites ou désigne une entrée nulle.
- Elle peut remettre à zéro l'entier à `param_4 + 8`, puis parcourt des candidats obtenus via `FUN_004af0c9` / `FUN_004aefb7`. Elle suit une mesure flottante via `FUN_00423897` et compare une autre valeur à `2.0`; noms et unités non établis.
- Pour chaque candidat, elle appelle `FUN_00798492`, parcourt ses entrées selon le compte à l'offset `+0x4c`, mappe chaque entrée via `FUN_00795987` puis la table `ECX+4`, et applique au besoin le filtre indirect `param_5`.
- Le traitement lit des valeurs de type vecteur via `FUN_006f2237` / `FUN_004237e5`, ajuste un flottant selon des drapeaux, utilise `FUN_0044cb21` et `FUN_00795aa3`, puis passe des valeurs construites à `FUN_008caa04`.
- En fin de parcours, elle teste le candidat retenu et `param_8`/le champ 16 bits à `+0xac`, parcourt un lien à `+0x24` avec `FUN_004a5f76`, appelle éventuellement `FUN_004a5ddd`, puis retourne avec `RET 0x24` (36 octets, cohérent avec neuf arguments de pile de quatre octets).
- Autres appelants observés : `0x753f2e`, `0x86d51e`, `0x86d596`, `0x871809`, `0x873d85` et `0x87e7f8`, en plus de `FUN_00799898`.

**Hypothèse :** l'itération des candidats, les mesures vectorielles et le filtre indirect sont compatibles avec une routine de recherche/validation utilisée dans la chaîne `tempKBPath`. Les rôles précis des objets, les unités, la collection et la signification métier du retour restent inconnus. La sonde #35 ([run ID 38736569975](https://github.com/rakmahefa/aoe-rea/actions/runs/38736569975)) analyse le résolveur `FUN_00798492` utilisé par cette routine.

### Dossier résolveur — `FUN_00798492` (sonde ponctuelle #35)

Preuve : [run #35, ID 38736569975](https://github.com/rakmahefa/aoe-rea/actions/runs/38736569975) ; [artefact 11974527446](https://github.com/rakmahefa/aoe-rea/actions/runs/38736569975/artifacts/11974527446).

- Ghidra identifie une procédure continue de 217 octets, de `0x798492` à `0x79856a` inclus.
- Le pseudocode traite l'entrée comme un pointeur vers un vecteur flottant et utilise les composantes `[0]` et `[2]`. Il retourne zéro si la table spatiale à `ECX+0xb4` est absente ou si une coordonnée est inférieure à environ zéro (`-1e-6`).
- Il divise les coordonnées par l'échelle flottante à `ECX+0xac` et les convertit en coordonnées de grille entières, contrôlées par les dimensions aux offsets `ECX+0xa4` et `ECX+0xa8`.
- Il indexe un tableau de cellules à `ECX+0xb4` avec un pas de six octets par cellule, lit un indice signé sur 16 bits, le vérifie par rapport au compte d'objets à `ECX+8`, puis renvoie le pointeur de la table `ECX+4` si l'indice est valide. Cellule/indice invalide : retour zéro.
- Parmi les appelants listés par Ghidra figurent `FUN_00798815` (`0x798815`), `FUN_00799898` (`0x799898`) et `FUN_00799939` (`0x799939`); ce résolveur est partagé au-delà de la chaîne du callback.

**Interprétation appuyée par la structure du code :** cela ressemble à une conversion coordonnées → cellule de grille → pointeur d'objet. L'identité métier de la grille, la signification de l'entrée 16 bits, l'unité de l'échelle et le type des objets restent inconnus.

### Dossier de l'itérateur — `FUN_004af0c9` (sonde ponctuelle #36)

Preuve : [run #36, ID 38737601357](https://github.com/rakmahefa/aoe-rea/actions/runs/38737601357) ; [artefact 11973429389](https://github.com/rakmahefa/aoe-rea/actions/runs/38737601357/artifacts/11973429389).

- Ghidra rapporte un corps non contigu de 149 octets, réparti en trois plages : `0x4af0c9–0x4af11f`, `0x4cfdd5–0x4cfe0b` et `0x4d5cec–0x4d5cf2`. Se limiter au bloc d'entrée manquerait la boucle de comparaison et le retour faux.
- La fonction appelle `FUN_004aefe9` en lui passant une zone de sortie, puis consomme les valeurs de cette zone comme indice entier de table et clé flottante.
- Elle lit une entrée depuis la table globale `DAT_00cafb9c + indice*4`. Si l'entrée contient un lien à l'offset `+0x28`, elle suit la chaîne et compare `ABS(*(float*)(nœud+0x14) + *(float*)(nœud+0x18) + *(float*)(nœud+0x1c) - clé)` à `0.0001`.
- Si elle trouve une correspondance (ou si le premier nœud n'a pas de lien), elle appelle `FUN_004af120(indice, nœud, &DAT_00cafb9c)`, remet à zéro les champs `+0x2c` et `+0x28` du nœud, puis renvoie le pointeur du nœud. Si la chaîne se termine sans correspondance, elle appelle `FUN_00678a72`; une entrée initiale absente passe aussi par ce helper.
- Appelants connus : `FUN_004ae98b` et `FUN_00798815` (`0x7988d3`).

**Interprétation non résolue :** le corps semble sélectionner/consommer une entrée de table globale et d'une chaîne liée à l'aide d'une clé flottante. Le sens métier de la clé, des trois champs flottants et des champs remis à zéro reste inconnu. Le dossier #37 ([Actions run ID 38739802167](https://github.com/rakmahefa/aoe-rea/actions/runs/38739802167), artefact [11975426935](https://github.com/rakmahefa/aoe-rea/actions/runs/38739802167/artifacts/11975426935)) montre que `FUN_004aefe9` a la forme d'une extraction du minimum d'un tas, mais la sémantique de la priorité reste inconnue. Le run #38 ([Actions run ID 38740230871](https://github.com/rakmahefa/aoe-rea/actions/runs/38740230871), artefact [11975947354](https://github.com/rakmahefa/aoe-rea/actions/runs/38740230871/artifacts/11975947354)) établit que `FUN_004af120` retire un nœud d'une liste doublement chaînée. Le run #39 ([Actions run ID 38740603626](https://github.com/rakmahefa/aoe-rea/actions/runs/38740603626), artefact [11976087652](https://github.com/rakmahefa/aoe-rea/actions/runs/38740603626/artifacts/11976087652)) établit que `FUN_004aefb7` insère un nœud à la fin d'un compartiment de `DAT_00cafba8` sélectionné par un hachage tronqué à 11 bits. Le dossier #40 ([run ID 38742083079](https://github.com/rakmahefa/aoe-rea/actions/runs/38742083079), artefact [11977520029](https://github.com/rakmahefa/aoe-rea/actions/runs/38742083079/artifacts/11977520029)) décrit `FUN_004aeee8` comme un mélangeur de trois valeurs de 32 bits avec addition, soustraction, XOR et décalages; `FUN_004aefb7` masque sa sortie à 11 bits pour choisir un compartiment. Le dossier #41 ([Actions run ID 38743002770](https://github.com/rakmahefa/aoe-rea/actions/runs/38743002770), artefact [11976439859](https://github.com/rakmahefa/aoe-rea/actions/runs/38743002770/artifacts/11976439859)) établit que `FUN_0058e2c3` maintient un tableau dynamique d'éléments de 8 octets, avec pointeur à `+0`, taille logique à `+4` et capacité à `+8`. Le dossier #42 ([Actions run ID 38743994938](https://github.com/rakmahefa/aoe-rea/actions/runs/38743994938), artefact [11978560249](https://github.com/rakmahefa/aoe-rea/actions/runs/38743994938/artifacts/11978560249)) établit que `FUN_004afb4c` insère une paire de 8 octets dans le tas et la remonte selon sa clé flottante. Quand la structure est vide, le code initialise une sentinelle `0xff7fffff` / `0xffffffff` à l'indice zéro; les éléments réels commencent à l'indice un. Le run #43 ([Actions run ID 38745133893](https://github.com/rakmahefa/aoe-rea/actions/runs/38745133893), artefact [11978346441](https://github.com/rakmahefa/aoe-rea/actions/runs/38745133893/artifacts/11978346441)) a terminé l'analyse de `FUN_004ae7b1`; ses constatations sont consignées ci-dessous.

### Dossier du producteur de clé — `FUN_004aefe9` (sonde ponctuelle #37)

Preuve : [run #37, ID 38739802167](https://github.com/rakmahefa/aoe-rea/actions/runs/38739802167) ; [artefact 11975426935](https://github.com/rakmahefa/aoe-rea/actions/runs/38739802167/artifacts/11975426935).

- Ghidra rapporte un corps non contigu de 241 octets réparti sur `0x4aefe9–0x4af0c8`, `0x4aff67–0x4aff6e` et `0x4d5ce3–0x4d5ceb`.
- La fonction renvoie une valeur faux apparente (`AL=0`) lorsque le compte global `DAT_00cafbb8` est inférieur à deux. Sinon, elle copie la première paire stockée à `DAT_00cafbb4 + 8` / `+0xc` vers la zone de sortie du caller, déplace la dernière paire à la racine et décrémente le compte.
- Elle fait descendre ce remplacement dans un tableau de paires de 8 octets, compare le premier champ comme flottant et remonte un enfant lorsque la clé du remplacement est supérieure. Elle réécrit la paire à sa place, appelle `FUN_0058e2c3(compte-1, 0)`, puis renvoie une valeur vraie apparente (`AL=1`).
- Le sens métier du second DWORD, celui de la file globale, les unités de la clé flottante et le rôle de `FUN_0058e2c3` restent inconnus.

**Interprétation, confiance moyenne :** la structure ressemble à une extraction du minimum d'une file de priorité min (retour de la racine, remplacement par le dernier élément, puis rétablissement de l'ordre du tas). C'est une inférence algorithmique, pas le nom original retrouvé ni une preuve de ce que la file priorise. Les runs #38 (https://github.com/rakmahefa/aoe-rea/actions/runs/38740230871) et #39 (https://github.com/rakmahefa/aoe-rea/actions/runs/38740603626) examinent deux helpers voisins de cette gestion des candidats.

### Helper de retrait de nœud — `FUN_004af120` (sonde ponctuelle #38)

Preuve : [run #38, ID 38740230871](https://github.com/rakmahefa/aoe-rea/actions/runs/38740230871) ; [artefact 11975947354](https://github.com/rakmahefa/aoe-rea/actions/runs/38740230871/artifacts/11975947354).

- Ghidra rapporte un corps non contigu de 164 octets, réparti sur `0x4af120–0x4af160`, `0x4cfe0c–0x4cfe21`, `0x4ee766–0x4ee796` et `0x678947–0x678962`.
- La fonction utilise un indice dans la table de têtes de listes pointée par `*param_3`, puis recherche `param_2` dans la chaîne doublement chaînée. Le champ `+0x28` est utilisé comme pointeur `suivant`, et `+0x2c` comme pointeur `précédent`.
- Si le nœud retiré est la tête, la table est mise à jour vers le nœud suivant et le pointeur précédent de celui-ci est effacé. Sinon, les liens voisins sont reconnectés. Dans les chemins de suppression réussie, `+0x28` et `+0x2c` du nœud cible sont remis à zéro.
- Appelants indiqués par Ghidra : `FUN_004af0c9`, `FUN_00678a5f` et `FUN_008caa04`.

**Interprétation :** le rôle générique de suppression dans une liste doublement chaînée est fortement établi. Le type métier des nœuds et de la table reste inconnu.

### Insertion dans la chaîne candidate hachée — `FUN_004aefb7` (sonde ponctuelle #39)

Preuve : [run #39, ID 38740603626](https://github.com/rakmahefa/aoe-rea/actions/runs/38740603626) ; [artefact 11976087652](https://github.com/rakmahefa/aoe-rea/actions/runs/38740603626/artifacts/11976087652).

- Ghidra rapporte un corps non contigu de 92 octets réparti sur `0x4aefb7–0x4aefe8`, `0x4cfe22–0x4cfe3c` et `0x678a50–0x678a5e`.
- La fonction appelle `FUN_004aeee8` avec trois valeurs dérivées de `*param_1`, `param_1[2]` et `*(ECX+0x18)`, masque le hachage obtenu par `0x7ff`, puis choisit un compartiment dans la table globale `DAT_00cafba8` (2 048 compartiments possibles).
- Si le compartiment est vide, il devient la tête de la liste. Sinon, la fonction suit les pointeurs `+0x28` jusqu'à la fin, ajoute le nœud, écrit l'ancien dernier nœud dans le champ précédent `+0x2c` du nouvel élément et met son pointeur suivant `+0x28` à zéro.
- Appelants connus : `FUN_004ae98b` et `FUN_00798815`.

**Interprétation :** comportement compatible avec une insertion dans une table de hachage à chaînage séparé. Le sens métier de la clé hachée et sa relation avec les autres tables globales ne sont pas établis. La sonde #40 ([run ID 38742083079](https://github.com/rakmahefa/aoe-rea/actions/runs/38742083079), artefact [11977520029](https://github.com/rakmahefa/aoe-rea/actions/runs/38742083079/artifacts/11977520029)) a récupéré le hacheur de 32 bits documenté ci-dessus; la sonde #41 (https://github.com/rakmahefa/aoe-rea/actions/runs/38743002770) analyse `FUN_0058e2c3`.

### Hacheur de clés candidates — `FUN_004aeee8` (sonde ponctuelle #40)

Preuve : [run #40, ID 38742083079](https://github.com/rakmahefa/aoe-rea/actions/runs/38742083079) ; [artefact 11977520029](https://github.com/rakmahefa/aoe-rea/actions/runs/38742083079/artifacts/11977520029).

- Ghidra identifie un corps contigu de 207 octets, de `0x4aeee8` à `0x4aefb6`.
- La fonction reçoit trois valeurs de 32 bits, les mélange avec des opérations répétées d'addition/soustraction/XOR et des décalages variables (comptes observés : 13, 8, 12, 16, 5, 3, 10 et 15), puis renvoie un résultat de 32 bits.
- L'appelant `FUN_004aefb7` masque ce résultat par `0x7ff` pour sélectionner un des 2 048 compartiments de `DAT_00cafba8`. Autres appelants indiqués par Ghidra : `FUN_004ae7b1` et `FUN_008caa04`.
- Le sens métier des trois valeurs d'entrée et le nom de l'algorithme original ne sont pas récupérés. Le choix de compartiment est observé, mais pas le sens métier des collisions ni des objets stockés dans cette table.

**Interprétation :** `FUN_004aeee8` est un mélangeur/hacheur déterministe de 32 bits utilisé pour le choix d'un compartiment par au moins un appelant. La sonde #41 ([run ID 38743002770](https://github.com/rakmahefa/aoe-rea/actions/runs/38743002770)) examine `FUN_0058e2c3`, appelée après l'extraction de tas observée au run #37.

### Helper de tableau dynamique — `FUN_0058e2c3` (sonde ponctuelle #41)

Preuve : [run #41, ID 38743002770](https://github.com/rakmahefa/aoe-rea/actions/runs/38743002770) ; [artefact 11976439859](https://github.com/rakmahefa/aoe-rea/actions/runs/38743002770/artifacts/11976439859).

- Ghidra rapporte un corps non contigu de 296 octets réparti sur `0x58e2c3–0x58e2eb`, `0x58e7b5–0x58e84c` et `0x64c75c–0x64c7c2`.
- La fonction manipule une structure de type tableau dynamique adressée par `ECX` : pointeur de données à `+0`, taille logique à `+4`, capacité à `+8`. La taille allouée vaut `capacité * 8`, donc les éléments font 8 octets.
- Avec le second argument optionnel à zéro, la fonction met à jour directement la taille logique si la capacité suffit ; si une taille plus grande est demandée, elle augmente la capacité par doublement jusqu'à la taille nécessaire et alloue/réalloue le stockage. Un indicateur non nul force une voie de réinitialisation/reconstruction. Les échecs d'allocation passent par des helpers d'erreur/exception.
- Dans le site d'appel du run #37, `ECX` pointe vers `DAT_00cafbb4` et `FUN_004aefe9` appelle `FUN_0058e2c3(nouvelle_taille, 0)` après l'extraction d'une paire racine. L'appel met donc à jour la taille logique du tableau après le retrait.

**Interprétation :** le run #41 établit que `DAT_00cafbb4` est un tableau dynamique d'éléments de 8 octets et que l'extraction apparente du tas réduit sa taille logique. Combiné au réordonnancement descendant selon une clé flottante dans `FUN_004aefe9`, cela renforce l'hypothèse d'une extraction du minimum. Le sens métier et les unités de la clé restent inconnus. Le run #42 (https://github.com/rakmahefa/aoe-rea/actions/runs/38743994938) analyse `FUN_004afb4c`, candidat naturel pour le chemin d'insertion complémentaire ; son corps doit encore le confirmer.

### Insertion dans le tas min — `FUN_004afb4c` (sonde ponctuelle #42)

Preuve : [run #42, ID 38743994938](https://github.com/rakmahefa/aoe-rea/actions/runs/38743994938) ; [artefact 11978560249](https://github.com/rakmahefa/aoe-rea/actions/runs/38743994938/artifacts/11978560249).

- Ghidra rapporte un corps non contigu de 241 octets, réparti sur `0x4afb4c–0x4afc08` et `0x4b00ce–0x4b0101`.
- La fonction développe le tableau dynamique à `DAT_00cafbb4` via `FUN_0058e2c3`, écrit une paire de deux DWORDs à un indice, puis la fait remonter tant que le premier DWORD interprété comme flottant est inférieur ou égal à la clé du parent.
- Lorsque le tableau est vide, elle tente d'insérer à l'indice zéro une sentinelle de premier DWORD `0xff7fffff` (flottant IEEE-754 fini négatif maximal) et de second DWORD `0xffffffff`; le premier élément réel commence ensuite à l'indice un. Pendant l'insertion normale, les paires parentes sont déplacées vers le bas jusqu'à ce que la nouvelle clé soit supérieure à celle du parent, puis la nouvelle paire est placée dans l'emplacement final.
- Cette opération est cohérente avec un tas min indexé à partir de 1, utilisant l'indice zéro comme sentinelle pour arrêter la remontée. `FUN_004aefe9` (run #37) fournit le chemin complémentaire d'extraction de la racine; `FUN_0058e2c3` (run #41) gère la taille/capacité du tableau.
- Appelants listés par Ghidra : `FUN_004ae7b1` et `FUN_008caa04`. Le run #43 ([ID 38745133893](https://github.com/rakmahefa/aoe-rea/actions/runs/38745133893), artefact [11978346441](https://github.com/rakmahefa/aoe-rea/actions/runs/38745133893/artifacts/11978346441)) a terminé l'analyse de `FUN_004ae7b1`; son dossier ci-dessous documente la construction de la paire et son usage du tas.

**Interprétation solidement étayée au niveau algorithmique :** insertion dans un tas min à clé flottante, avec sentinelle à l'indice zéro. Le sens métier de la clé et du second DWORD reste inconnu.

### Dossier producteur de priorité — `FUN_004ae7b1` (sonde ponctuelle #43)

Preuve : [run #43, ID 38745133893](https://github.com/rakmahefa/aoe-rea/actions/runs/38745133893) ; [artefact 11978346441](https://github.com/rakmahefa/aoe-rea/actions/runs/38745133893/artifacts/11978346441).

- Ghidra rapporte un corps total de 583 octets réparti sur cinq plages non contiguës : `0x4ab9bf–0x4ab9d5`, `0x4ae7b1–0x4ae98a`, `0x4aff40–0x4aff5d`, `0x4b1e7a–0x4b1e93` et `0x4b1fd1–0x4b1fee`. Ne pas lire les plages disjointes comme une séquence linéaire continue.
- La fonction appelle `FUN_004aeee8` avec les composantes `param_1[0]`, `param_1[2]` et une valeur à `ECX+0x18`, masque le résultat par `0x7ff`, puis appelle `FUN_004ae797` pour rechercher un élément à cet indice dans `DAT_00cafb9c`. Si rien n'est trouvé, elle consulte séparément `DAT_00cafba8` avec le même indice.
- Quand `param_2` est non nul, le premier coût local correspond à la distance euclidienne dans le plan X/Z entre `param_1` et `param_2`, additionnée à `param_2[5]`. Cette valeur est écrite dans le champ du nœud `+0x14` (`pfVar6[5]`). La fonction calcule ensuite une deuxième distance X/Z entre `param_1` et les coordonnées lues à `ECX+0x0c` / `ECX+0x14`, la stocke dans `+0x18` (`pfVar6[6]`) et l'ajoute au premier coût.
- Pour un nouveau nœud, la fonction relie l'entrée à la chaîne du compartiment de `DAT_00cafb9c` à l'aide des champs `+0x28` / `+0x2c`, puis appelle `FUN_004afb4c(&local_10)`. Le layout Ghidra place le flottant `local_10` immédiatement avant `local_c` (DWORD suivant), et le pseudocode assigne `local_c = uVar5`, l'indice masqué du compartiment. Le couple transmis au tas est donc compatible avec `[score flottant combiné, indice de compartiment]`; ce lien de données ne signifie pas que le tas et la table de hachage sont la même structure.
- Dans la branche où un nœud existe déjà dans `DAT_00cafb9c`, le code conserve la valeur combinée précédente `pfVar6[7] + pfVar6[6] + pfVar6[5]`, met à jour les champs du nœud, puis appelle `FUN_004b1e94` avec l'indice, l'ancienne valeur combinée et la nouvelle valeur. La branche de la table secondaire peut appeler `FUN_00678a5f`; leurs sémantiques restent à examiner.

**Hypothèse algorithmique fortement étayée, mais non prouvée au niveau métier :** le score du tas a la forme *coût accumulé + distance euclidienne restante*, compatible avec une priorité de frontière de type A*. Le contexte des routines de chemin renforce cette piste, mais ni le nom original, ni les unités, ni l'interprétation exacte des champs, ni l'algorithme de recherche complet ne sont confirmés. Ne pas renommer définitivement cette routine en A*.

**Prochaine cible recommandée après le run #44 :** analyser `FUN_008caa04`, le second appelant de `FUN_004b1e94` et de `FUN_004afb4c`, afin de comprendre l'autre chemin d'utilisation du tas. `FUN_00678a5f` reste une cible secondaire pour la table `DAT_00cafba8`. Garder la piste géométrie/obstruction/occupation des runs #20–23 séparée.

### Dossier de mise à jour de priorité — `FUN_004b1e94` (sonde ponctuelle #44)

Preuve : [run #44, ID 38772710258](https://github.com/rakmahefa/aoe-rea/actions/runs/38772710258) ; [artefact 11991884059](https://github.com/rakmahefa/aoe-rea/actions/runs/38772710258/artifacts/11991884059).

- Ghidra identifie un corps total de 817 octets réparti sur six plages non contiguës : `0x4b1e94–0x4b1fd0`, `0x4b1fef–0x4b1ff3`, `0x4b1ff7–0x4b210a`, `0x4b22db–0x4b2356`, `0x4b23d7–0x4b240b` et `0x4b73f6–0x4b741f`.
- La fonction parcourt les paires de 8 octets de `DAT_00cafbb4`. Elle recherche une paire dont le second DWORD égale la clé entière fournie par l'appelant, puis vérifie que sa priorité flottante correspond à l'ancienne valeur avec une tolérance que Ghidra décompile comme `0.0001` (l'assembleur lit le flottant à `DAT_00ba175c`).
- Lorsque la paire correspond, elle remplace le premier DWORD par la nouvelle priorité et conserve le second DWORD. Puis elle remonte la paire dans le tas tant que la nouvelle priorité est inférieure ou égale à celle du parent. Le corps observé n'insère ni ne retire de paire et ne met pas à jour la longueur logique du tableau.
- Le site d'appel de `FUN_004ae7b1` fournit la clé/indice et les anciennes/nouvelles valeurs combinées. Les types de paramètres proposés par Ghidra sont peu fiables ; la séquence d'appel et le flux des valeurs sont plus sûrs que la signature déduite.
- Si la clé et l'ancienne priorité ne correspondent pas comme prévu, le flux atteint les helpers courts `FUN_00678963`, `FUN_0067896c` ou `FUN_00678975`. Leur sémantique exacte et les raisons des appels marqués terminaux par Ghidra restent inconnues.
- Appelants listés par Ghidra : `FUN_004ae7b1` et `FUN_008caa04`.

**Interprétation forte au niveau algorithmique :** il s'agit d'une mise à jour en place de la priorité, suivie d'une réparation ascendante du tas, compatible avec une opération de type *decrease-key*. Dans `FUN_004ae7b1`, la garde environnante rejette un candidat moins avantageux avant d'atteindre cette mise à jour, ce qui renforce cette lecture. La signification métier exacte et les unités des deux DWORD restent inconnues.

**Rappel chronologique :** le run #45, décrit juste après, a examiné l'autre appelant `FUN_008caa04`.

### Dossier du second appelant du tas — `FUN_008caa04` (sonde ponctuelle #45)

Preuve : [run #45, ID 38774292963](https://github.com/rakmahefa/aoe-rea/actions/runs/38774292963) ; [artefact 11993540489](https://github.com/rakmahefa/aoe-rea/actions/runs/38774292963/artifacts/11993540489).

- Ghidra identifie une procédure contiguë de 459 octets, de `0x8caa04` à `0x8cabce`. Son appelant est `FUN_00798815` à `0x798815`.
- Comme `FUN_004ae7b1`, elle calcule un indice via `FUN_004aeee8` puis `& 0x7ff`, et consulte `DAT_00cafb9c` avant `DAT_00cafba8`. Les tables et la mémoire du tas restent des structures distinctes.
- Si la table principale contient un candidat, elle conserve l'ancien score combiné `+0x14 + +0x18 + +0x1c`, actualise les champs du nœud, recalcule une priorité flottante, puis appelle `FUN_004b1e94` avec la clé de compartiment et les priorités ancienne/nouvelle.
- Si seul `DAT_00cafba8` contient un candidat compatible avec la garde de score, la fonction retire le nœud avec `FUN_004af120`, le réutilise, et suit un chemin de promotion vers `DAT_00cafb9c` et le tas. Si aucun candidat réutilisable n'est trouvé, elle obtient/initialise un nœud via `FUN_004adea4`.
- Le chemin nouveau/promu appelle `FUN_004aded1` pour l'entrée dans `DAT_00cafb9c`, puis `FUN_004afb4c` pour insérer la paire score/clé dans le tas min. Dans un mode, `FUN_004237e5` calcule une valeur géométrique à préciser.
- La procédure écrit plusieurs champs de `+0x00` à `+0x1c` et réinitialise d'autres champs. Le sens métier complet des champs n'est pas résolu.

**Interprétation :** ces opérations sont compatibles avec la réutilisation/la promotion de candidats entre deux états stockés par table, avec un tas min pour la priorité. Une piste de recherche de chemin est plausible, mais les noms « open set » et « closed set » ne sont pas établis.

**Prochaine cible recommandée :** `FUN_004aded1`, appelée lorsque `FUN_008caa04` ajoute un candidat à `DAT_00cafb9c`. La comparer à l'insertion en chaîne déjà observée pour `DAT_00cafba8` sans fusionner les identités des deux tables.

### Dossier d'insertion dans la table principale — `FUN_004aded1` (sonde ponctuelle #46)

Preuve : [run #46, ID 38775891857](https://github.com/rakmahefa/aoe-rea/actions/runs/38775891857) ; [artefact 11994206385](https://github.com/rakmahefa/aoe-rea/actions/runs/38775891857/artifacts/11994206385).

- Ghidra rapporte un corps de 78 octets réparti sur trois plages : `0x4aded1–0x4adef1`, `0x4b2368–0x4b2385` et `0x5004bd–0x5004cb`. Les segments disjoints ne doivent pas être lus comme un bloc linéaire.
- Le pseudocode lit la tête du compartiment depuis `*param_3 + param_1*4`. Si le compartiment est vide, il écrit `param_2` comme nouvelle tête et retourne.
- Si le compartiment n'est pas vide, il suit les pointeurs suivants `+0x28` jusqu'à la fin de la chaîne, met le champ `+0x28` de la queue à `param_2`, écrit l'ancien nœud de queue dans le champ précédent `+0x2c` du nouveau nœud et efface le pointeur suivant `+0x28` du nouveau nœud.
- Ghidra ne rapporte qu'un appelant direct, `FUN_008caa04`, à l'adresse d'appel `0x8cabb2`. Le helper ne calcule pas le hash : l'appelant fournit l'indice de compartiment et le pointeur de la table/tableau de têtes.
- Sur la branche compartiment vide, le helper n'initialise pas explicitement les liens du nœud inséré. Ne pas supposer qu'il efface toujours ces champs : l'initialisation peut dépendre de l'appelant ou de l'état antérieur du nœud.
- La forme ressemble à l'insertion dans la table distincte `DAT_00cafba8` effectuée par `FUN_004aefb7` (run #39), mais les deux tables doivent rester séparées faute de preuve sur leur rôle métier.

**Interprétation :** ajout confirmé en queue d'une chaîne de compartiment en parcourant des pointeurs `next`, avec un lien `previous` renseigné lors d'un ajout non vide. Le sens métier de la table et des champs reste inconnu.

**Prochaine cible à l'issue du run #46 :** `FUN_004ae797`, le helper de recherche en compartiment. Le résultat de sa sonde est décrit dans le dossier #47 ci-dessous.

### Dossier de recherche d'un candidat par coordonnées — `FUN_004ae797` (sonde ponctuelle #47)

Preuve : [run #47, ID 38782180985](https://github.com/rakmahefa/aoe-rea/actions/runs/38782180985) ; [artefact 11996292779](https://github.com/rakmahefa/aoe-rea/actions/runs/38782180985/artifacts/11996292779).

- Ghidra identifie 127 octets de corps répartis sur trois plages non contiguës : `0x4ae797–0x4ae7b0`, `0x4afeec–0x4aff3f` et `0x4b2357–0x4b2367`. Les plages disjointes forment un ensemble d'adresses et non un bloc linéaire.
- La fonction reçoit un indice de compartiment entier, un pointeur vers un tuple de flottants et un pointeur vers un descripteur de table. Elle lit la tête dans `*param_3 + param_1*4`; une tête nulle entraîne un retour nul immédiat.
- Elle compare les composantes flottantes `[0]` et `[2]` du nœud et de la requête. Tant que l'une des différences absolues est supérieure ou égale à `1e-6`, elle suit le pointeur suivant du nœud à l'offset `+0x28`. Elle renvoie le nœud si les deux coordonnées correspondent ; la fin de la chaîne renvoie nul.
- Ghidra répertorie deux appelants : `FUN_004ae7b1` aux sites `0x4ae827` et `0x4ae843`, ainsi que `FUN_008caa04` aux sites `0x8caa68` et `0x8caa9d`. Les deux appelants utilisent le helper pour chercher d'abord dans `DAT_00cafb9c`, puis dans `DAT_00cafba8` si nécessaire.

**Interprétation structurelle fortement étayée :** chaque table est recherchée par un indice de compartiment préalablement calculé, puis par égalité des coordonnées X/Z avec une tolérance absolue de `1e-6` dans une chaîne liée. Cela suggère des nœuds associés à des positions. Ce n'est pas une preuve des noms métier des tables, de la raison des deux structures ni du sens de la troisième composante fournie au calcul de hachage.

**Repère chronologique après le run #47 :** la prochaine cible choisie était `FUN_004adea4`; son analyse et les étapes suivantes sont consignées dans les sections #48–50 ci-dessous.

### Dossier de l'allocateur de pool de candidats — `FUN_004adea4` (sonde ponctuelle #48)

Preuve : [run #48, ID 38783723125](https://github.com/rakmahefa/aoe-rea/actions/runs/38783723125) ; [artefact 11996853539](https://github.com/rakmahefa/aoe-rea/actions/runs/38783723125/artifacts/11996853539).

- Ghidra rapporte 254 octets de corps dans deux plages non contiguës : `0x4adea4–0x4aded0` et `0x67897f–0x678a4f`. Les zones disjointes ne forment pas une séquence linéaire.
- L'objet référencé par `ECX` contient un compteur d'entrées libres dans `in_ECX[5]` et un tableau de pointeurs libres à `in_ECX[4]`. Si ce compteur est positif, la fonction renvoie le dernier pointeur libre puis demande une réduction du compte via `FUN_00401113(count-1, 0)`.
- S'il ne reste aucune entrée libre, elle prend la taille de lot `*in_ECX`, la fixe à 100 si elle est inférieure à un, puis alloue `taille_du_lot * 0x34` octets via `FUN_00401398`. Une allocation échouée retourne zéro.
- Le bloc est transmis à `FUN_00401fa0(base, 0x34, taille_du_lot, &LAB_008ca934)`. La fonction enregistre ensuite le bloc et empile les pointeurs vers les éléments à pas fixe de `0x34` dans le stockage des objets libres ; elle renvoie le pointeur du premier élément. Les tableaux de suivi utilisent aussi `FUN_00401113`.
- Ghidra liste comme appelants `FUN_004ae7b1`, `FUN_004b004e` et `FUN_008caa04`. Dans ce dernier, l'appelant remet ensuite à zéro 13 DWORDs avant d'initialiser un candidat. Cela concorde avec une réserve de mémoire réutilisable, mais ne prouve pas que le pool construit entièrement un objet métier.

**Interprétation fortement étayée au niveau de la gestion mémoire :** allocateur de pool pour des enregistrements de taille fixe `0x34` octets, réutilisant d'abord les pointeurs libres puis allouant des lots de 100 par défaut. La disposition complète de son état, le rôle de `LAB_008ca934` et le nom original de ce mécanisme restent inconnus.

**Résultat des runs #49–57 :** `FUN_00401fa0` parcourt les records à pas `0x34`, puis `0x401fd6` exécute `JMP EAX` vers `LAB_008ca934`. Les runs #52–56 décodent `MOV EAX,ECX`, `XOR ECX,ECX`, puis deux stores zéro aux champs `[EAX+0x2c]` et `[EAX+0x28]`, compatibles avec l'effacement des liens arrière et avant. Le run #57 décode `0x8ca93e: RET` (octet `c3`, un octet, flux retour), ce qui termine le chemin du callback observé. La prochaine cible est la continuation appelante `0x401fc8`; la frontière de procédure et le rôle métier restent inconnus.

### Dossier de la boucle de callbacks à pas fixe — `FUN_00401fa0` (sonde #49)

Preuve : [run #49, ID 38785347582](https://github.com/rakmahefa/aoe-rea/actions/runs/38785347582) ; [artefact 11998191528](https://github.com/rakmahefa/aoe-rea/actions/runs/38785347582/artifacts/11998191528).

- Ghidra identifie un corps contigu de 54 octets, de `0x401fa0` à `0x401fd5`.
- La signature pseudocode exposée par Ghidra déclare trois arguments, mais le code lit un quatrième argument à `[ESP+0x10]` à l'entrée (après ajustements de pile dans le prologue) et termine par `RET 0x10`. Le prototype déduit par Ghidra est incomplet : le code consomme quatre arguments de pile.
- Le compte est lu depuis `[ESP+0x0c]` à l'entrée. Si le compte est positif, la fonction boucle exactement ce nombre de fois. À chaque tour, elle place l'adresse de l'élément courant dans `ECX`, charge le quatrième argument dans `EAX`, appelle `0x401fd6`, puis avance l'adresse de l'élément courant du pas transmis en deuxième argument.
- En contexte, `FUN_004adea4` appelle cette routine avec la base du bloc, le pas `0x34`, le compte du lot et `LAB_008ca934`. Le flux de données est compatible avec une boucle générique de callback pour des enregistrements à pas fixe : adresse du record dans `ECX` et cible de callback transportée dans `EAX`.
- Au run #49, le dossier fonctionnel identifiait un helper de deux octets sans exposer ses octets natifs. La sonde instruction #50 a ensuite décodé cette adresse en `JMP EAX`.

**Interprétation :** le pool délègue une opération à chaque record au moyen d'un pointeur de callback, plutôt que d'initialiser directement tous les champs dans `FUN_00401fa0`. Le rôle exact de `LAB_008ca934` reste inconnu.

**Résultat du run #50 :** `0x401fd6` contient `FF E0`, décodé `JMP EAX`. Le helper effectue un saut indirect vers le callback transmis dans `EAX`, avec l'adresse du record courant dans `ECX`. **Prochaine cible :** inspecter les instructions à `LAB_008ca934` (`0x8ca934`).

### Dossier du transfert indirect vers le callback — `0x401fd6` (sonde #50)

Preuve : [run #50, ID 38852450383](https://github.com/rakmahefa/aoe-rea/actions/runs/38852450383) ; [artefact 12025552949](https://github.com/rakmahefa/aoe-rea/actions/runs/38852450383/artifacts/12025552949).

- La sonde native décode les octets `ff e0` à `0x401fd6` en `JMP EAX`, longueur deux, flux de saut calculé et aucune destination directe.
- Cela confirme le flux de données du run #49 : `FUN_00401fa0` charge le quatrième argument de pile dans `EAX`, place l'adresse du record courant dans `ECX`, puis appelle `0x401fd6`. Le helper de deux octets saute immédiatement vers la cible contenue dans `EAX`, de sorte que le callback s'exécute avec l'adresse du record courant dans `ECX`.
- Comme il s'agit d'un saut final (*tail jump*), le retour normal du callback revient à l'adresse de retour poussée par `CALL 0x401fd6` à `0x401fc3`, donc à la continuation `0x401fc8`.
- L'instruction ne code aucune destination directe : le callee dépend de la valeur transmise à l'exécution. Sur le chemin observé dans `FUN_004adea4`, cette valeur est le label `LAB_008ca934`.
- Un dossier fonctionnel distinct pour `FUN_00401fd6` dans le [run #51](https://github.com/rakmahefa/aoe-rea/actions/runs/38852714545) ([artefact 12025049050](https://github.com/rakmahefa/aoe-rea/actions/runs/38852714545/artifacts/12025049050)) avertit « Could not recover jumptable » et génère un pseudocode d'appel indirect suivi d'un retour. Ne pas prendre ce retour synthétique pour un flot machine : les octets natifs `ff e0` du run #50 et le type de flot confirment `JMP EAX`.

**Interprétation confirmée au niveau du flot de contrôle :** `FUN_00401fa0` itère sur le bloc et distribue un appel de callback pour chaque élément par saut indirect final. Le comportement des champs reste inconnu tant que le corps du callback n'a pas été tracé.

**Résultat du run #54 :** à `0x8ca938`, les octets `89 48 2c` décodent `MOV dword ptr [EAX+0x2c],ECX` (3 octets, `FALL_THROUGH`, `procedure=null`). Après `MOV EAX,ECX` à `0x8ca934` et `XOR ECX,ECX` à `0x8ca936`, cela écrit zéro à `+0x2c` du record. D'autres routines de listes utilisent ce décalage comme lien arrière, interprétation structurelle plausible. **Prochaine cible :** inspecter `0x8ca93b`.

### Dossier de l'entrée callback — `0x8ca934` (sonde #52)

Preuve : [run #52, ID 38853201623](https://github.com/rakmahefa/aoe-rea/actions/runs/38853201623) ; [artefact 12025469262](https://github.com/rakmahefa/aoe-rea/actions/runs/38853201623/artifacts/12025469262).

- La sonde native décode les octets `8b c1` à `0x8ca934` en `MOV EAX,ECX`, longueur deux octets, `FALL_THROUGH`, avec `procedure=null`.
- Dans le contexte établi par les runs #49–50, `ECX` porte l'adresse du record courant au transfert dans le callback. Cette instruction copie ce pointeur dans `EAX`; elle ne prouve pas l'initialisation d'un champ ni la sémantique métier du record.
- Ghidra ne reconnaît pas `0x8ca934` comme entrée de procédure dans cette sonde. Le traiter comme label/bloc de code tant qu'une analyse de corps plus large n'en établit pas la frontière.

**État chronologique au run #52 :** l'adresse suivante était `0x8ca936`; la séquence a depuis été décodée jusqu'à `0x8ca93a` par les runs #53–54. La cible actuelle est `0x8ca93b`.

### Dossier de la continuation du callback — `0x8ca936` (sonde #53)

Preuve : [run #53, ID 38853803910](https://github.com/rakmahefa/aoe-rea/actions/runs/38853803910) ; [artefact 12026795710](https://github.com/rakmahefa/aoe-rea/actions/runs/38853803910/artifacts/12026795710).

- La sonde native décode les octets `33 c9` à `0x8ca936` en `XOR ECX,ECX`, longueur deux, `FALL_THROUGH`, avec `procedure=null`.
- L'instruction précédente observée au run #52 est `MOV EAX,ECX` à `0x8ca934`. La paire d'instructions copie donc le pointeur du record dans `EAX`, puis efface le registre `ECX`. C'est un constat de flux de registres, pas la preuve qu'un champ métier du record est remis à zéro.
- Ghidra ne reconnaît pas encore de frontière de procédure sur ces deux adresses. Continuer séquentiellement jusqu'à ce qu'un saut, appel, retour ou une limite de procédure décodé fournisse une preuve plus forte.

**Prochaine cible après le run #53 :** `0x8ca938`, ensuite décodée au run #54. Les runs #56–57 ont poursuivi jusqu'au `RET` à `0x8ca93e` ; reprendre dans le bloc appelant à `0x401fc8` plutôt que de continuer linéairement après le retour.

### Dossier de la continuation du callback — écriture du lien arrière à `0x8ca938` (sonde #54)

Preuve : [run #54, ID 38854422589](https://github.com/rakmahefa/aoe-rea/actions/runs/38854422589) ; [artefact 12026542570](https://github.com/rakmahefa/aoe-rea/actions/runs/38854422589/artifacts/12026542570).

- La sonde native décode les octets `89 48 2c` à `0x8ca938` en `MOV dword ptr [EAX + 0x2c],ECX`, longueur trois octets, `FALL_THROUGH`, avec `procedure=null`.
- En combinant les runs #52–54, la séquence observée est `MOV EAX,ECX` à `0x8ca934`, `XOR ECX,ECX` à `0x8ca936`, puis écriture de `ECX` dans `[EAX+0x2c]` à `0x8ca938`. Le flux de registres étaye la conclusion qu'un zéro est écrit à l'offset `+0x2c` du record désigné par le pointeur copié dans `EAX`.
- Les sondes antérieures de gestion de listes associent l'offset `+0x2c` à un lien précédent/arrière. L'instruction est donc compatible avec l'effacement de ce lien lors de l'initialisation d'un record neuf. Cette comparaison structurelle reste une interprétation ; le rôle métier complet du callback n'est pas prouvé.
- Ghidra renvoie toujours `procedure=null` à cette adresse. Ne pas conclure que le callback constitue déjà une procédure indépendante identifiée.
- La tentative de dossier au niveau fonction depuis `0x8ca934` a échoué au run #55 ([Actions run ID 38854789080](https://github.com/rakmahefa/aoe-rea/actions/runs/38854789080), artefact [12026372536](https://github.com/rakmahefa/aoe-rea/actions/runs/38854789080/artifacts/12026372536)) avec `invalid_request`: `No procedure exists at the requested address: 0x8ca934`. Aucun corps de fonction n'a été produit; la frontière du callback reste donc non reconnue.

**État chronologique après le run #54 :** la cible `0x8ca93b` a été décodée au run #56, puis `0x8ca93e` s'est révélé être un `RET` au run #57. La prochaine cible utile est `0x401fc8`, dans le chemin appelant.

### Dossier de la continuation du callback — écriture du lien avant à `0x8ca93b` (sonde #56)

Preuve : [run #56, ID 38855936196](https://github.com/rakmahefa/aoe-rea/actions/runs/38855936196) ; [artefact 12027357090](https://github.com/rakmahefa/aoe-rea/actions/runs/38855936196/artifacts/12027357090).

- La sonde native décode les octets `89 48 28` à `0x8ca93b` en `MOV dword ptr [EAX + 0x28],ECX`, longueur trois octets, `FALL_THROUGH`, avec `procedure=null`.
- En combinant les runs #52–56, la séquence copie le pointeur du record de `ECX` vers `EAX`, efface `ECX`, puis écrit zéro à `[EAX+0x2c]` à `0x8ca938` et à `[EAX+0x28]` à `0x8ca93b`.
- Les routines de listes antérieurement sondées utilisent `+0x28` comme lien avant/suivant et `+0x2c` comme lien arrière/précédent. Les deux stores sont donc compatibles avec le nettoyage des deux liens d'un record détaché ou neuf. Cela reste une hypothèse structurelle; le but complet du callback n'est pas prouvé.
- Le run #55 ([Actions run ID 38854789080](https://github.com/rakmahefa/aoe-rea/actions/runs/38854789080), artefact [12026372536](https://github.com/rakmahefa/aoe-rea/actions/runs/38854789080/artifacts/12026372536)) n'a pas récupéré de corps de fonction : `rea function 0x8ca934` renvoie `No procedure exists at the requested address`. Les sondes séquentielles restent la base de preuve, avec `procedure=null`.

**Résultat de la sonde #57 :** [run #57](https://github.com/rakmahefa/aoe-rea/actions/runs/38856897665), [artefact 12026774512](https://github.com/rakmahefa/aoe-rea/actions/runs/38856897665/artifacts/12026774512).

### Dossier du retour du callback — `0x8ca93e` (sonde #57)

Preuve : [run #57, ID 38856897665](https://github.com/rakmahefa/aoe-rea/actions/runs/38856897665) ; [artefact 12026774512](https://github.com/rakmahefa/aoe-rea/actions/runs/38856897665/artifacts/12026774512).

- La sonde native décode l'octet `c3` à `0x8ca93e` en `RET`, longueur un octet, flux de retour, avec `procedure=null`.
- Le chemin observé du callback se termine donc après la copie du pointeur, l'effacement de `ECX` et les deux stores zéro aux offsets `+0x2c` et `+0x28`.
- Associé au `JMP EAX` de `0x401fd6` (#50) et à l'appel du thunk en `0x401fc3`, un retour normal est compatible avec une reprise à `0x401fc8`. Cela établit le flot de contrôle attendu, sans identifier la fonction métier du callback.
- Ne pas continuer à décoder séquentiellement après `RET` comme si ces octets appartenaient au même chemin d'exécution. **Prochaine cible :** inspecter `0x401fc8`, continuation appelante.

### Caller continuation after callback — `0x401fc8` (probe #58)

Evidence: [Actions run #58, ID 38923177848](https://github.com/rakmahefa/aoe-rea/actions/runs/38923177848); [artifact 12055028788](https://github.com/rakmahefa/aoe-rea/actions/runs/38923177848/artifacts/12055028788).

- The native instruction probe decodes bytes `03 f5` at `0x401fc8` as `ADD ESI,EBP`, length 2, `FALL_THROUGH`, with `procedure=0x401fa0`.
- The instruction itself proves only a register addition. The function dossier for `FUN_00401fa0` in probe #49 shows that `ESI` holds the current record address and `EBP` holds the second argument; `FUN_004adea4` calls this loop with stride `0x34`. In combination, this is strong evidence that the caller advances the current record pointer by the record stride after the callback returns.
- The target executable is `retro/exe et dll/age3y.exe`, SHA-256 `b1a1dab7264d2db72e8f8ae1df1e419eecc223b40db00c9d1013a3bc77611d9d`; the artifact records REA 6.4.0 and Ghidra 12.1.4.
- Ghidra identifies the enclosing procedure as `FUN_00401fa0`; this differs from the callback label at `0x8ca934`, for which prior probes report `procedure=null`.

**Next target at the time of probe #58:** `0x401fca`, the next sequential instruction.

### Loop-counter decrement — `0x401fca` (probe #59)

Evidence: [Actions run #59, ID 39012977596](https://github.com/rakmahefa/aoe-rea/actions/runs/39012977596); [artifact 12094140406](https://github.com/rakmahefa/aoe-rea/actions/runs/39012977596/artifacts/12094140406).

- The native probe decodes bytes `83 ef 01` at `0x401fca` as `SUB EDI,0x1`, length 3, `FALL_THROUGH`, with `procedure=0x401fa0`.
- The complete function dossier from probe #49 shows `EDI` is the loop counter initialized from the requested count. Probe #59 directly confirms that the counter is decremented once after the record pointer advances; it does not itself establish the following branch.
- The function-level assembly in probe #49 already reports `0x401fcd: JNZ 0x00401fbf`. That decode makes a loop-back to the record-processing block consistent with the observed count-decrement sequence; a one-address probe at `0x401fcd` is the next confirmation step.
- Together with #50 and #52–57, the observed control-flow chain is: `CALL 0x401fd6` at `0x401fc3` → thunk `JMP EAX` → callback returns at `0x8ca93e` → caller resumes at `0x401fc8` → advances `ESI` by `EBP` → decrements `EDI`. This does not establish the original source-level signature or broader business meaning of the callback.

### Faits vs hypothèses

- **Fait observé :** les deux sauts conditionnels à `0x8827d9` et `0x8827e9` ciblent `0x8827f5`. La destination exécute `XOR AL,AL`, puis `RET` à `0x8827f7`. Ce chemin efface explicitement l'octet bas de retour `AL` avant `RET`. C'est cohérent avec un résultat booléen faux, mais ne prouve pas que le registre 32 bits `EAX` entier vaut zéro.
- **Fait observé :** si `ECX` est nul, le premier `JZ` prend ce chemin qui met `AL` à zéro avant le retour. Sinon, le code appelle le helper avec la valeur lue à `0x00c66664`, teste `EAX`, puis prend le même chemin `AL=0; RET` si le résultat est nul.
- **Fait observé :** si le résultat du helper est non nul, le flux tombe à `0x8827eb`, où `MOV EAX,[EAX+0x80]` est décodé. Le `TEST EAX,EAX` à `0x8827f1` est suivi de `JNZ 0x8827f8` à `0x8827f3`. Si `EAX` est nul, le flux séquentiel tombe dans le bloc `AL=0; RET` à `0x8827f5–0x8827f7`; sinon le saut mène à `0x8827f8`. Cette adresse décode `8b 54 24 0c` en `MOV EDX,dword ptr [ESP+0xc]` (4 octets, `FALL_THROUGH`, `procedure=null`). Cela lit un dword depuis la pile ; l'argument ou la variable représentée n'est pas établi. La cible séquentielle est `0x8827fc`. Cette adresse décode `68 82 97 79 00` en `PUSH 0x799782` (5 octets, `FALL_THROUGH`), avec une référence de type `DATA` vers `0x799782`. Le type et le rôle de cette adresse ne sont pas établis. À `0x882801`, bytes `6a 00` décodent `PUSH 0x0` (2 octets, `FALL_THROUGH`, `procedure=null`), et l'adresse suivante est `0x882803`.
- **Hypothèse limitée :** `FUN_0044cb21` ressemble à un accessor de collection indexé avec contrôle de bornes. Ni la signification de cette collection, ni celles des globaux `0x00c66234` et `0x00c66664`, ni le rôle des offsets `+0x13c` et `+0x80` ne sont connus.
- La piste géométrie/obstruction/occupation des runs #20–23 reste indépendante jusqu'à preuve de lien avec cette logique.

**Prochaine action :** sonder `0x401fcd` pour confirmer directement `JNZ 0x00401fbf`, déjà présent dans le dossier de fonction #49. Si le saut est confirmé, poursuivre dans la cible `0x401fbf` en tenant compte de la boucle sur les enregistrements. Continuer à séparer les faits décodés des interprétations, à citer les artefacts, à garder la piste géométrie des runs #20–23 indépendante et à travailler par branche + PR.

## 6. Règles de travail pour la prochaine session

- Utiliser les capacités GitHub connectées pour inspecter le dépôt et Actions directement ; ne pas supposer que l’utilisateur doit recopier manuellement tous les résultats.
- Vérifier le dernier run à chaque reprise. L’historique ci-dessus est un instantané daté, et non une affirmation sur des exécutions futures.
- Pour les changements dans le dépôt, travailler sur une branche dédiée et ouvrir une pull request plutôt que de modifier `main` directement.
- Ajouter des notes de preuve : adresse, run/artifact, chaînes, imports, appels, interprétation et niveau de confiance.
- Séparer explicitement les faits observés des hypothèses. Ne pas présenter du pseudocode Ghidra comme code source original récupéré.
- Ne pas promettre ou prétendre qu’un port Linux natif existe tant qu’un ELF compilé et son comportement n’ont pas été validés.
- Respecter les droits d’utilisation. Ne pas publier des exécutables, DLL ou ressources propriétaires du jeu dans des releases sans autorisation ; préférer du code reconstruit, des instructions reproductibles et des fichiers fournis légalement par l’utilisateur.

## 7. Message de démarrage à copier dans une nouvelle session

> Nous poursuivons https://github.com/rakmahefa/aoe-rea. `main` a été vérifié au commit `4dd1e638cb53e77375c4b1061e5f290a6ea73af0` après fusion de la PR #16. Le binaire de référence est `retro/exe et dll/age3y.exe` (SHA-256 `b1a1dab7264d2db72e8f8ae1df1e419eecc223b40db00c9d1013a3bc77611d9d`). Les sondes #58 et #59 (runs [38923177848](https://github.com/rakmahefa/aoe-rea/actions/runs/38923177848), artefact [12055028788](https://github.com/rakmahefa/aoe-rea/actions/runs/38923177848/artifacts/12055028788) ; run [39012977596](https://github.com/rakmahefa/aoe-rea/actions/runs/39012977596), artefact [12094140406](https://github.com/rakmahefa/aoe-rea/actions/runs/39012977596/artifacts/12094140406)) décodent `0x401fc8` en `ADD ESI,EBP` et `0x401fca` en `SUB EDI,0x1`, dans `FUN_00401fa0`. Le dossier #49 indique ensuite `0x401fcd: JNZ 0x00401fbf` ; prochaine sonde : `0x401fcd`. Les résultats confirment le flot de la boucle d'initialisation à pas fixe, pas la sémantique métier complète du callback. Séparer faits et hypothèses, citer chaque run/artefact, ne pas confondre les tables `DAT_00cafb9c`, `DAT_00cafba8` et `DAT_00cafbb4`, garder la piste géométrie des runs #20–23 indépendante et travailler par branche + PR.