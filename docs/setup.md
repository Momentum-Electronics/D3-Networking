# Comment se configurer pour tester l'implémentation

Le code source de l'implémentation Python est disponible sous le répertoire
[`implementations/python`](../implementations/python).

Un fichier `pyproject.toml` est fourni à la racine du projet Python. Il suffit donc d'exécuter la commande

```
pip install .
```

à la racine du projet Python pour installer la librairie ainsi que ses dépendances.

> [!Note]
> Les dépendances pour l'interface sur la ligne de commande ne sont pas installées par défaut. Pour les installer,
> le `.` dans la commande d'installation doit être remplacé par `".[cli]"`.

## Configuration d'un système client

Un exemple de client est disponible [ici](../implementations/python/examples/client_main.py). Il suffit d'exécuter
le script (une fois les dépendances proprement installées) pour démarrer un client.

Par défaut, le client fourni utilise IPv6 et enforce la signature des paquets. Tout paquet non signé est simplement
ignoré.

## Configuration d'un système serveur

Un exemple de serveur est disponible [ici](../implementations/python/examples/server_main.py). Il suffit d'exécuter
le script (une fois les dépendances proprement installées) pour démarrer un serveur.

Par défaut, le serveur fourni utilise IPv6 et signe tous les paquets. La clé de signature est simplement présente en
clair dans le fichier d'implémentation. Cette clé a été utilisée pour générer la clé de validation sauvegardée dans le
fichier [`demo.keys`](../implementations/python/examples/demo.keys). Le client est ainsi capable de valider la signature
des messages transmis par le serveur par défaut.