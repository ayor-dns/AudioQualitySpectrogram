

# Générateur de spectrogrammes

Ce script permet de générer des spectrogrammes à partir de fichiers audio contenus dans un dossier. Les spectrogrammes sont sauvegardés sous forme d'images dans un dossier de destination spécifié.

## Prérequis

- **Python 3.9+** doit être installé sur votre machine.
- Les dépendances du projet doivent être installées. Pour cela, utilisez la commande suivante :
  ```bash
  pip install -r requirements.txt
  ```

## Utilisation

Le script est conçu pour être exécuté en ligne de commande. Voici les options disponibles :

### Commande de base

```bash
python script.py <source> [-d <destination>] [-w <workers>]
```

### Arguments

1. **`source`** (obligatoire) :
   - Chemin vers le dossier contenant les fichiers audio à traiter.
   - Tous les fichiers avec les extensions `.mp3`, `.flac` et `.wav` seront pris en compte.
   - Exemple : 
     ```bash
     python script.py /path/to/audio/files
     ```

2. **`-d` ou `--destination`** (optionnel) :
   - Chemin où les images de spectrogrammes seront enregistrées.
   - Si non spécifié, les résultats seront sauvegardés dans un dossier nommé `Spectrogrambox_result` situé à côté du dossier source.
   - Exemple :
     ```bash
     python script.py /path/to/audio/files -d /path/to/save/results
     ```

3. **`-w` ou `--workers`** (optionnel) :
   - Nombre de cœurs CPU à utiliser pour paralléliser le traitement.
   - Par défaut, le script utilise tous les cœurs disponibles moins un.
   - Exemple :
     ```bash
     python script.py /path/to/audio/files -w 4
     ```

### Exemple complet

Générer des spectrogrammes pour les fichiers dans `/audio/files` et les enregistrer dans `/results`, en utilisant 4 processus :

```bash
python script.py /audio/files -d /results -w 4
```

## Résultats

Chaque fichier audio traité génère une image au format `.png`. Les spectrogrammes sont sauvegardés avec le même nom que le fichier audio original, mais avec l'extension `.png`. Si un fichier a déjà été traité, il sera ignoré pour éviter de recalculer les spectrogrammes.

## Compatibilité

Ce script est compatible avec :
- Windows
- macOS
- Linux

---
