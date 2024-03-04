# Contribuer aux implémentations

Nous sommes ouverts à vos contributions.

N'hésitez pas à ouvrir des *Issues* et des *Pull-Requests* avec vos suggestions. L'équipe sera très active sur ce
repo pour le reste de la session.

## Idées

- [ ] Une suite de tests basée sur un système de *containers* pour valider de nouvelles implémentations. Les containers
  devraient être sous un même préfixe réseau afin de tenter de répliquer la configuration réseau fournie dans le cadre
  du projet.
- [ ] Une batterie de tests. Quelques tests unitaires ne feraient pas de mal. Ils seront très utiles lorsque nous
  voudrons accepter des contributions d'autres équipes.
- [ ] Valider la robustesse du client. Le client reçoit et traite des données sur un groupe *multicast*. Il faut
  s'assurer que l'implémentation ne plante pas lorsqu'elle reçoit des messages dans un mauvais format. Sans quoi le
  service réseau des sous systèmes véhicule pourrait planter.

# Contribuer à la spec

La *spec* n'est pas nécessairement coulée dans le béton pour l'instant. Il est encore temps de faire valoir vos opinions
d'équipe sur son implémentation !

Un [forum de discussion](https://github.com/Momentum-Electronics/D3-Networking/discussions) est ouvert sur notre page
Github pour en jaser.