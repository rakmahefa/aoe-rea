# Passation de session — projet aoe-rea

**Mise à jour : 12 octobre 2026**  
**Dépôt :** https://github.com/rakmahefa/aoe-rea  
**Dernier run vérifié lors de la rédaction :** [REA binary analysis #14](https://github.com/rakmahefa/aoe-rea/actions/runs/38249737918)

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
3. Renseigner l’entrée facultative `function_selector` avec une adresse (par exemple `0x555de7`) ou un nom de fonction si nécessaire.
4. Lancer le workflow puis attendre son état `success` ou `failure`.
5. Ouvrir le run, télécharger l’artifact `rea-analysis` et inspecter au minimum `metadata.json`, `function-selection.json`, `function.json` et `callees/manifest.json`, puis les dossiers de fonctions qui ont réussi.
6. Avant de conseiller une nouvelle cible, contrôler la dernière exécution réelle dans GitHub Actions : l’utilisateur peut avoir lancé un run plus récent depuis la rédaction de ce document.

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

### Dernier run en détail

Le run #14 s’est terminé avec succès le 12 octobre 2026. Métadonnées relevées dans l’artifact :

- Cible : `0x5562ad` (source manuelle).
- Fichier : `retro/exe et dll/age3y.exe`.
- SHA-256 : `b1a1dab7264d2db72e8f8ae1df1e419eecc223b40db00c9d1013a3bc77611d9d`.
- REA `6.4.0`, Ghidra `12.1.4`.
- Manifest des callees : 4 candidats. `0x4010ca` n’a pas été résolu ; `0x401113`, `0x401398` et `0x4013b0` ont réussi. Ils semblent être des utilitaires de capacité/allocation mémoire et de chaînes, pas le code gameplay.
- Ghidra relève des plages de fonction non contiguës. Ne pas traiter les limites de fonction et les types déduits comme des certitudes.

Le rapport synthétique associé à ce run indiquait `0x555de7` comme prochaine cible utile, car `0x5562ad` lui passe une petite structure composée de plusieurs valeurs XML. Son rôle n’est pas encore établi.

## 5. Prochaine étape conseillée

**Prochaine cible à vérifier : `0x555de7`.**

Cette adresse est une piste de l’analyse du run #14 : la fonction sélectionnée `0x5562ad` lui transmet une petite structure construite à partir de valeurs extraites de XML. Il faut analyser son dossier avant d’affirmer s’il s’agit d’un parseur de tuple/vecteur, d’une conversion, ou d’une autre routine.

Après le prochain run :

1. Vérifier que le run sélectionne bien `0x555de7` et qu’il est terminé.
2. Lire le pseudocode, les appels directs, les chaînes et le manifeste de callees.
3. Classer chaque fonction comme **runtime générique**, **parseur/chargement de ressources**, **plateforme/UI**, **moteur probable** ou **inconnu**, en indiquant les preuves et le niveau de confiance.
4. Ne pas suivre indéfiniment les utilitaires d’allocation/chaînes ou les effets de particules. En parallèle, rechercher des fonctions clairement liées aux entités/unités, à la simulation, au déplacement/pathfinding, aux ressources/économie, à l’IA, à l’ordre du jeu et à la boucle de tick.
5. Constituer un inventaire d’adresses corroborées et des relations de call graph. Un nom de chaîne ou une seule référence est un indice, pas une preuve suffisante.

## 6. Règles de travail pour la prochaine session

- Utiliser les capacités GitHub connectées pour inspecter le dépôt et Actions directement ; ne pas supposer que l’utilisateur doit recopier manuellement tous les résultats.
- Vérifier le dernier run à chaque reprise. L’historique ci-dessus est un instantané daté, et non une affirmation sur des exécutions futures.
- Pour les changements dans le dépôt, travailler sur une branche dédiée et ouvrir une pull request plutôt que de modifier `main` directement.
- Ajouter des notes de preuve : adresse, run/artifact, chaînes, imports, appels, interprétation et niveau de confiance.
- Séparer explicitement les faits observés des hypothèses. Ne pas présenter du pseudocode Ghidra comme code source original récupéré.
- Ne pas promettre ou prétendre qu’un port Linux natif existe tant qu’un ELF compilé et son comportement n’ont pas été validés.
- Respecter les droits d’utilisation. Ne pas publier des exécutables, DLL ou ressources propriétaires du jeu dans des releases sans autorisation ; préférer du code reconstruit, des instructions reproductibles et des fichiers fournis légalement par l’utilisateur.

## 7. Message de démarrage à copier dans une nouvelle session

> Nous poursuivons le projet https://github.com/rakmahefa/aoe-rea. Le but final est de reconstruire suffisamment le comportement d’Age of Empires III pour viser un vrai exécutable Linux natif ; il n’y a pas encore de port natif ni de source originale récupérée. Lis d’abord `README.md` et `docs/SESSION_HANDOFF.md`, puis vérifie sur GitHub Actions si un run plus récent que le #14 existe. Le dernier run documenté est #14, cible `0x5562ad`, qui a identifié un parseur/chargeur de définitions de particules XML (mots-clés `Particle`, `filename`, `timeoff`) et suggère `0x555de7` comme prochaine cible. Analyse les résultats réels avant de poursuivre et utilise les outils GitHub connectés. Ne prends pas les hypothèses pour des faits. Priorise la découverte des systèmes gameplay (unités/entités, simulation, déplacement, économie, IA) au-delà du sous-système de particules. Pour toute modification du dépôt, crée une branche et une PR.
