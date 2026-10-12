# Passation de session — projet aoe-rea

**Mise à jour : 12 octobre 2026**  
**Dépôt :** https://github.com/rakmahefa/aoe-rea  
**Dernier run vérifié lors de la rédaction :** [REA binary analysis #18](https://github.com/rakmahefa/aoe-rea/actions/runs/38264819057)

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

### Dernier run en détail — #18

Le [run #18](https://github.com/rakmahefa/aoe-rea/actions/runs/38264819057) s'est terminé avec succès le 12 octobre 2026.

- Input effectif : recherche littérale `unit`, insensible à la casse.
- Binaire : `retro/exe et dll/age3y.exe`.
- SHA-256 : `b1a1dab7264d2db72e8f8ae1df1e419eecc223b40db00c9d1013a3bc77611d9d`.
- Source commit : `47601a91f5a5cf1ff38b34e56fd2245ada0c9801`.
- REA `6.4.0`, Ghidra `12.1.4`.
- L'artifact contient `search.json` et `metadata.json` ; l'étape d'analyse de fonction a été ignorée conformément au mode de recherche seule.

Pistes intéressantes relevées dans `search.json` :

| Adresse de chaîne | Valeur | Interprétation prudente |
|---|---|---|
| `0xc36e20` | `Unit %d (%S) has a non-unit obstruction type %d` | Message de diagnostic relatif à une obstruction d'unité ; candidat pour remonter au code du module unit. |
| `0xc36e8c` | `.\unit.cpp` | Chemin de source intégré au binaire, proche du diagnostic précédent ; indice de provenance, pas source originale récupérée. |
| `0xc19dc0` | Signature/documentation `kbCanPath2` | API de requête de pathfinding exposée à la couche knowledge-base/IA. |
| `0xc19e68` | Signature/documentation `kbCanSimPath` | API de test de chemin de simulation ; l'implémentation n'est pas établie par la chaîne. |
| `0xc1b0c8` | Signature/documentation `kbUnitCount` | API de comptage d'unités par joueur/type/état. |
| `0xc17d40`, `0xc17dd8` | `kbUnitCostPerResource`, `kbCanAffordUnit` | Pistes d'économie/coût et capacité de paiement. |
| `0xbaee38`, `0xc30d30` | `hcUnitMoveToPos`, `trUnitMoveToPoint` | Descriptions de commandes de déplacement accessibles aux scripts. |

La requête a retourné 1 307 chaînes définies correspondantes. Ces adresses désignent les **données de chaînes**. Une partie des résultats provient d'aide de script, d'UI et de ressources. Aucune de ces chaînes ne prouve à elle seule l'algorithme ou la fonction native recherchée.

## 5. Prochaine étape conseillée

**Priorité : suivre les références croisées des données vers le code natif.**

La recherche #18 fournit deux premiers candidats à tester :

1. **`0xc36e20`** — message de diagnostic dans le voisinage de `.\unit.cpp`. Lancer le workflow avec `xref_address=0xc36e20` pour identifier les fonctions qui référencent ce message.
2. **`0xc19dc0`** — documentation de `kbCanPath2`. Lancer ensuite `xref_address=0xc19dc0` pour cartographier son enregistrement et ses usages éventuels.
3. Après chaque run, inspecter `xrefs.json`. Distinguer les références provenant d'une table d'enregistrement, d'une aide/script, d'un appelant natif ou d'un simple accès aux données. Ne pas supposer que le premier xref est l'implémentation.
4. Relancer avec `function_selector` sur une adresse que les xrefs et le contexte montrent comme fonction de code ; lire le pseudocode, l'assembly, les références et callees.
5. Compléter ensuite par les signatures `kbCanSimPath`, `kbUnitCount`, `kbUnitCostPerResource`, `kbCanAffordUnit` et les commandes de déplacement si elles conduisent à un code gameplay corroboré.

Le run #14 demeure une piste de chargement de particules séparée. Ne revenir à `0x555de7` que si une preuve nouvelle le relie à un système de gameplay prioritaire.

Pour chaque résultat, noter l'adresse, le run/artifact, le contexte de l'xref, l'interprétation, le niveau de confiance et les inconnues. Les chaînes et les pseudocodes Ghidra sont des éléments de preuve à évaluer, pas le code source original.

## 6. Règles de travail pour la prochaine session

- Utiliser les capacités GitHub connectées pour inspecter le dépôt et Actions directement ; ne pas supposer que l’utilisateur doit recopier manuellement tous les résultats.
- Vérifier le dernier run à chaque reprise. L’historique ci-dessus est un instantané daté, et non une affirmation sur des exécutions futures.
- Pour les changements dans le dépôt, travailler sur une branche dédiée et ouvrir une pull request plutôt que de modifier `main` directement.
- Ajouter des notes de preuve : adresse, run/artifact, chaînes, imports, appels, interprétation et niveau de confiance.
- Séparer explicitement les faits observés des hypothèses. Ne pas présenter du pseudocode Ghidra comme code source original récupéré.
- Ne pas promettre ou prétendre qu’un port Linux natif existe tant qu’un ELF compilé et son comportement n’ont pas été validés.
- Respecter les droits d’utilisation. Ne pas publier des exécutables, DLL ou ressources propriétaires du jeu dans des releases sans autorisation ; préférer du code reconstruit, des instructions reproductibles et des fichiers fournis légalement par l’utilisateur.

## 7. Message de démarrage à copier dans une nouvelle session

> Nous poursuivons le projet https://github.com/rakmahefa/aoe-rea. Le but final est de reconstruire suffisamment le comportement d’Age of Empires III pour viser un vrai exécutable Linux natif ; aucun port natif ni source originale complète n'a été récupéré. Lis `README.md` et `docs/SESSION_HANDOFF.md`, vérifie le dernier run GitHub Actions, puis examine ses artifacts. Le run #18 a réussi une recherche littérale `unit` et trouvé 1 307 chaînes ; pistes : message unit `0xc36e20`, signature `kbCanPath2` `0xc19dc0`, `kbCanSimPath` `0xc19e68`, `kbUnitCount` `0xc1b0c8`, coûts d'unités et wrappers de déplacement. Ces adresses sont des chaînes, pas des fonctions. La prochaine étape est d'utiliser `xref_address` (PR à fusionner) pour inspecter les références croisées, puis `function_selector` sur une adresse de code corroborée. Utilise les outils GitHub connectés, analyse les résultats réels, sépare faits et hypothèses, priorise unités/entités, simulation, déplacement, économie et IA, et crée une branche + PR pour toute modification.
