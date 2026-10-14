# Passation de session — projet aoe-rea

**Mise à jour : 14 octobre 2026**  
**Dépôt :** https://github.com/rakmahefa/aoe-rea  
**Dernière analyse principale vérifiée :** [REA binary analysis #30](https://github.com/rakmahefa/aoe-rea/actions/runs/38452908507) ; dernière sonde ciblée terminée : [instruction `0x8827f8`](https://github.com/rakmahefa/aoe-rea/actions/runs/38513505693)

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

### Helper appelé

Le `CALL` à `0x8827e2` vise `FUN_0044cb21`. Son dossier REA/Ghidra ([run](https://github.com/rakmahefa/aoe-rea/actions/runs/38507674474), [artifact 11868089731](https://github.com/rakmahefa/aoe-rea/actions/runs/38507674474/artifacts/11868089731)) indique que la fonction vérifie que son argument entier est non négatif et inférieur à `*(ECX+0x5c)`. Si l'index est valide, elle lit un dword depuis le tableau pointé par `ECX+0x58`; sinon elle renvoie zéro. Le corps Ghidra est non contigu : `0x44cb21–0x44cb3e` et `0x4649e1–0x4649e5`. Au site d'appel, `EDX` est poussé en argument après avoir été chargé depuis `0x00c66664`; `ECX` conserve la valeur chargée depuis `[EAX+0x13c]`.

### Faits vs hypothèses

- **Fait observé :** les deux sauts conditionnels à `0x8827d9` et `0x8827e9` ciblent `0x8827f5`. La destination exécute `XOR AL,AL`, puis `RET` à `0x8827f7`. Ce chemin efface explicitement l'octet bas de retour `AL` avant `RET`. C'est cohérent avec un résultat booléen faux, mais ne prouve pas que le registre 32 bits `EAX` entier vaut zéro.
- **Fait observé :** si `ECX` est nul, le premier `JZ` prend ce chemin qui met `AL` à zéro avant le retour. Sinon, le code appelle le helper avec la valeur lue à `0x00c66664`, teste `EAX`, puis prend le même chemin `AL=0; RET` si le résultat est nul.
- **Fait observé :** si le résultat du helper est non nul, le flux tombe à `0x8827eb`, où `MOV EAX,[EAX+0x80]` est décodé. Le `TEST EAX,EAX` à `0x8827f1` est suivi de `JNZ 0x8827f8` à `0x8827f3`. Si `EAX` est nul, le flux séquentiel tombe dans le bloc `AL=0; RET` à `0x8827f5–0x8827f7`; sinon le saut mène à `0x8827f8`. Cette adresse décode `8b 54 24 0c` en `MOV EDX,dword ptr [ESP+0xc]` (4 octets, `FALL_THROUGH`, `procedure=null`). Cela lit un dword depuis la pile ; l'argument ou la variable représentée n'est pas établi. La cible séquentielle est `0x8827fc`.
- **Hypothèse limitée :** `FUN_0044cb21` ressemble à un accessor de collection indexé avec contrôle de bornes. Ni la signification de cette collection, ni celles des globaux `0x00c66234` et `0x00c66664`, ni le rôle des offsets `+0x13c` et `+0x80` ne sont connus.
- La piste géométrie/obstruction/occupation des runs #20–23 reste indépendante jusqu'à preuve de lien avec cette logique.

**Prochaine action :** inspecter `0x8827fc`, après les 4 octets de l'instruction à `0x8827f8`. Le [run #15](https://github.com/rakmahefa/aoe-rea/actions/runs/38526015005) est actuellement en cours pour cette adresse. Continuer selon la longueur et le flux réellement décodés ; suivre les cibles de saut/appel et ne pas supposer une séquence linéaire. Ne pas utiliser `function_selector=0x8827cc` tant que l'entrée d'une vraie procédure n'est pas confirmée.

## 6. Règles de travail pour la prochaine session

- Utiliser les capacités GitHub connectées pour inspecter le dépôt et Actions directement ; ne pas supposer que l’utilisateur doit recopier manuellement tous les résultats.
- Vérifier le dernier run à chaque reprise. L’historique ci-dessus est un instantané daté, et non une affirmation sur des exécutions futures.
- Pour les changements dans le dépôt, travailler sur une branche dédiée et ouvrir une pull request plutôt que de modifier `main` directement.
- Ajouter des notes de preuve : adresse, run/artifact, chaînes, imports, appels, interprétation et niveau de confiance.
- Séparer explicitement les faits observés des hypothèses. Ne pas présenter du pseudocode Ghidra comme code source original récupéré.
- Ne pas promettre ou prétendre qu’un port Linux natif existe tant qu’un ELF compilé et son comportement n’ont pas été validés.
- Respecter les droits d’utilisation. Ne pas publier des exécutables, DLL ou ressources propriétaires du jeu dans des releases sans autorisation ; préférer du code reconstruit, des instructions reproductibles et des fichiers fournis légalement par l’utilisateur.

## 7. Message de démarrage à copier dans une nouvelle session

> Nous poursuivons https://github.com/rakmahefa/aoe-rea. La PR #11 est fusionnée. Run #30 a décodé `0x8827d1` comme `MOV ECX,[EAX+0x13c]`. Les sondes ciblées ont établi `TEST ECX,ECX; JZ 0x8827f5`, puis un `CALL 0x44cb21` avec argument issu de `[0x00c66664]`. Le helper `FUN_0044cb21` fait un accès indexé borné via les offsets `ECX+0x58` et `ECX+0x5c` (signification métier inconnue). Après `TEST EAX,EAX; JZ 0x8827f5`, le bloc `0x8827f5: XOR AL,AL; 0x8827f7: RET` donne le chemin de retour avec `AL=0` (sans établir la valeur des 24 bits supérieurs de `EAX`). Le chemin non nul continue à `0x8827eb: MOV EAX,[EAX+0x80]` ; prochaine cible `0x8827f8`. Procedure du callback toujours non résolue; garder faits et hypothèses séparés, liens run/artifact, piste géométrie des runs #20–23 distincte, changements via branche + PR.
