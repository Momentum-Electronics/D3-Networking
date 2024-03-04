# D3-Networking

Réseautique dans notre ville portuaire intelligente

## À propos

Nous sommes *Momentum Electronics* et voici notre proposition d'implémentation pour la réseautique dans notre
ville portuaire intelligente.

L'implémentation est basée sur *IP Multicast* et permet aux sous systèmes grue de communiquer l'information sur la
charge utile disponible à tous les sous systèmes véhicule en même temps ! Le protocole implémente aussi une forme
de signature électronique afin de permettre au sous systèmes véhicule de valider l'authenticité des messages reçus.
Vous pouvez vous informer sur l'implémentation dans la [`documentation/`](./docs) fournie par l'équipe.

## Implémentation

Une implémentation en Python est fournie pour vous permettre de rapidement commencer à tester le protocole. D'autres
implémentations, notamment celle d'un serveur pour l'ESP-32, seront ajoutées au courant de la session.

Les implémentations sont contenues dans le répertoire [`implementations/`](./implementations).

L'implémentation Python consiste en des utilitaires pour créer un client et un serveur respectant la *spec* décrite
sous [`docs/specs.md`](./docs/spec.md). Un exemple d'une paire de client/serveur sur IPv6 y est inclu.

L'implémentation Python vient aussi avec une interface sur la ligne de commande pour générer une paire de clés pour
la signature numérique. Voir le document [`setup.md`](./docs/setup.md) pour plus d'information sur l'utilisation de
cette interface.

## Contribuer

Nous sommes ouverts à vos contributions. Nous croyons qu'une implémentation unifiée comme celle-ci assure une meilleure
compatibilité entre nos interfaces.

Voir le document [`CONTRIBUTING.md`](./CONTRIBUTING.md) pour plus d'information sur comment contribuer au projet.