# Choix de design pour l'implémentation

## Pourquoi passer par la pile Internet

Le cadre du projet, réaliser une ville portuaire intelligente (VPI), implique un WAN d'appareils interconnectés sur un
réseau métropolitain. La pile Internet est une pile de protocoles prouvée pour ce genre d'application. On y retrouve
plusieurs solutions bien adaptées au genre de communications que l'on veut réaliser comme décrit dans le reste de
ce document.

Même si l'on choisissait d'accepter que notre projet est un modèle réduit d'une VPI, nous avons cru comprendre que les
*drivers* *Bluetooth* étaient problématiques sur les *Jetsons*. Nous avons donc supposé que le *Bluetooth* était à
éviter. De toute manière, la nature du protocole *Bluetooth* ne convient pas à notre application. On a plusieurs
appareils qui communiquent avec une quantité inconnue d'appareils aussi inconnue. À notre connaissance, la capacité
*broadcast* du *Bluetooth* conviendrait peut-être **si l'on n'avait pas de problèmes de drivers** et si l'on supposait
que notre produit ne sera jamais implémenté dans un WAN métropolitain.

Puisque la quantité de données à transmettre est **minuscule** (1 octet d'identifiant, 1 octet de charge utile
disponible sur la balance), un protocole comme LoRa aurait amplement suffit. LoRa supporte un débit et une portée
amplement suffisante. Cependant, les implémentations au-delà de la couche physique imposent des topologies différentes
de la nôtre. Sans compter les modifications à apporter à notre topologie, les réseaux LoRa supposent un ensemble de
nœuds fiables et *well behaved*.

Dans un cadre de routage de cargaison sur une base collaborative (plutôt que compétitive), un WAN LoRa aurait eu
beaucoup de sens. En effet, les distances supportées sont raisonnables et la consommation énergétique réduite est
intéressante pour des appareils qui doivent opérer de manière autonome sur une batterie.

Malheureusement, nos stations de base ne supportent pas le protocole. Nous croyons donc que les protocoles typiques
de la pile Internet sont un choix plus judicieux pour notre protocole de réseautique.

## Protocole à la couche liaison

À la couche liaison, la décision n'est pas trop difficile. Les *Jetsons* ainsi que les stations de base sont déjà
connectées sur un LAN WiFi. Le LAN WiFi simulera le WAN métropolitain où plusieurs appareils seraient interconnectés
dans un domaine de routage quelconque.

## Protocole réseau

Pour le protocole réseau, nous proposons des groupes IP *multicast*. Les groupes multicast sont parfaitement adaptés
à notre domaine d'application.

Plutôt que de transmettre des données à une interface en particulier en passant par une adresse *unicast*, les sous
systèmes grue transmetterons leurs données à une adresse *multicast*. Tous les abonnés au groupe *multicast* recevront
alors les données.

Pour s'abonner à un groupe *multicast* sur un LAN, un protocole comme IGMP peut être utilisé avec IPv4. Pour IPv6,
la spec inclus déjà la composante MLD.

Dans tous les cas, nous n'aurons pas besoin d'explicitement utiliser aucun de ces protocoles. Des APIs dans plusieurs
langages (basés sur le *socket api*) permettent de se joindre à un groupe à l'aide de quelques appels de fonction
depuis votre langage de programmation préféré.

Le *multicast* IP est idéal puisque les données seront transmises à une adresse MAC *multicast* à la couche liaison !
Les interfaces WiFi seront configurés pour écouter les trames destinées à cette adresse de groupe et feront suivre les
datagrammes aux couches supérieures de la pile réseau.

*Multicast* nous permet donc de minimiser le traffic sur le réseau tout en minimisant la configuration nécessaire pour
transmettre aux sous systèmes voiture.

Du point de vue des sous systèmes grue, la transmission est identique à tout autre envoi de datagramme IP. Seule
l'adresse de destination est changée pour une adresse de groupe prédéterminée.

Pour les sous systèmes véhicule, il suffit de s'abonner au groupe *multicast* lors de l'initialisation du système. Les
datagrammes IP seront démultiplexés jusqu'à la couche transport sur le port préalablement choisi. Il suffit alors de
se connecter sur le port et d'écouter les messages des autres équipes.

Puisque les adresse *multicast* utilisées ne dépendent pas du préfixe réseau, la topologie est portable. Aucune
configuration ne sera nécessaire si le préfixe réseau de la VPI change.

### v4 ou v6

Bien que l'implémentation Python supporte présentement les deux protocoles, nous croyons que l'utilisation d'IPv6
serait bien plus simple.

Contrairement à IPv4, IPv6 permet aux hôtes sur un réseau local d'autoconfigurer des adresses *link-local*. Nous
n'aurions donc pas besoin de configurer statiquement des adresses pour chacun de nos sous systèmes. La topologie serait
aussi super portable puisque les adresses sont auto assignées et ne dépendent du préfixe réseau.

## Protocole de transport

Pour le protocole de transport, la décision est assez facile. Nous n'avons pas besoin de la fiabilité que nous fournit
TCP puisqu'un paquet est seulement pertinent pour la seconde suivant sa transmission.

En plus, la fiabilité de transmission comme fournie par TCP est assez difficile à implémenter sur IP *multicast*. En
effet, les sous systèmes grue n'auront aucune idée d'à qui les messages transmits sont envoyés. Implémenter un système
d'*acknowledgements* sur *multicast* est donc ardu[^1].

[^1]: Mais pas impossible. Voir https://datatracker.ietf.org/doc/html/rfc3208.

De toute manière, le coût de la fiabilité de transmission n'en vaut pas ses avantages pour nos systèmes. Un paquet
perdu sur le réseau sera tout simplement remplacé par de l'information plus à jour à la seconde suivante. L'ordre
des paquets est important, mais peut être assuré en ajoutant simplement un numéro de séquence au niveau du protocole
applicatif.

## Protocole applicatif

Pour le protocole applicatif, nous avons assumé la taille des données suivantes :

- ID d'équipe : 1 octet d'entier non signé (équipe 0 à 255).
- Charges disponibles : 1 octet d'entier non signé (0 à 255 charges disponibles).
- Numéro de séquence : 4 octets d'entier non signé. Ici, 4 octets est une quantité de données immense pour les requis
  du projet. En effet, pour le numéro de séquence, il faut simplement que sa taille maximale soit au moins aussi grande
  que le nombre maximal d'autres paquets pouvant être transmis avant que le paquet n'arrive à destination. Puisque nous
  transmettons à chaque seconde, les paquets auront $2^{32} = 4294967296$ secondes pour arriver à destination. Aucun TTL
  sur notre réseau ne pourrait permettre un tel délais.

Un autre problème considéré lors de la création du protocole applicatif est celui de l'authenticité des données. Qu'est
ce qui empêche une équipe de transmettre qu'une autre grue que la sienne n'a aucune charge présente sur la balance ?
Rien du tout.

Pour mitiger ce problème, nous proposons la signature électronique des champs suivants :

- ID d'équipe
- Charges disponibles
- Numéro de séquence

La signature électronique proposée est basée sur l'algorithme [Curve25519](https://en.wikipedia.org/wiki/Curve25519).
L'algorithme est rapide[^2], robuste et prouvé. C'est l'algorithme qui supporte toute la sécurité sur Internet depuis
TLS1.3[^3].

[^2]: Signature en 87548 cycles et validation en 273364 cycles d'horloge sur un CPU Intel moderne.
[^3]: Voir https://datatracker.ietf.org/doc/html/rfc8446

Chaque équipe GEL-GIF devra générer une paire de clés publique et privée. La clé privée sera utilisée par les sous
systèmes grue pour signer les messages avant de les transmettre. La clée publique sera distribuée aux équipes de GLO
afin que l'authenticité des messages puisse être validée à la réception.

Le *payload* UDP est donc modifié pour contenir les champs supplémentaires suivants :

- Longueur de la signature : 4 octets d'entier non signé (**obligatoire**)
- Signature : longueur variable (optionnel)

Le choix d'un champ longueur obligatoire permet une certaine flexibilité quant à la signature. Une équipe ne désirant
pas signer son message peut tout simplement mettre ce champ à 0 pour avertir les sous systèmes grue que le message
n'est pas signé.

Le champ longueur nous permettra aussi de changer l'algorithme de signature si nécessaire.

Finalement, le champ signature est optionnel. Si la longueur de signature est mise à 0, ce champ peut être laissé
vide.