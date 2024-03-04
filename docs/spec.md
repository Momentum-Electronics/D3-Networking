# Description de la *spec*

## Protocole réseau

Pour le protocole réseau, les adresses *multicast* suivantes sont utilisées

| Protocole | Adresse         |
|-----------|-----------------|
| IPv4      | `224.0.0.25/24` |
| IPv6      | `ff12::e01/16`  |

## Protocole de transport

Le port UDP utilisé est `36868`

## Protocole applicatif

Voici le format des messages à transmettre :

```

+---------1---------2-------------6-------------10----------------// up to 508 bytes
| Team ID | Charges | Seq. number | Sig. length | Signature       // 
+---------+---------+0------------+-------------+-----------------//

```

À noter que les dimensions sont en octets.

### Description des champs

#### `Team ID`

Identifiant de l'équipe comme un entier non signé sur un octet.

#### `Charges`

Nombre de charges disponibles sur la balance comme un entier non signé sur un octet.

#### `Seq. number`

Numéro de séquence du paquet. Entier non signé sur 32 bits stocké LSByte-first.

Utilisé pour valider que les paquets reçus sont à jour.

#### `Sig. length`

Longueur de la signature électronique. Entier non signé sur 32 bits stocké LSByte-first.

#### `Signature`

Signature électronique de longueur variable.

> [!NOTE]
> Si la longueur de la signature est de 64 octets, le type de signature est assumé comme Ed25519.
> Si la longueur de la signature est 0, le champ signature ne sera pas traité, et ce, peu importe son contenu.
