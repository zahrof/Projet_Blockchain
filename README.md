# Projet Blockchain

Le code source de notre projet peut ếtre trouvé à https://github.com/zahrof/Projet_Blockchain.

## Dépendances

Afin de compiler et de lancer le projet vous devez avoir une version de python supérieur ou égal à 3.7.3.

Ainsi que le package python ed25519. Pour l'installer  vous pouvez effectuer la commande: 


```  pip install ed25519 ```

## Protocole 

Nous avons implementé un serveur TCP classique dont les descriptions des requêtes sont les suivante: 
```
talk            : envoi un message à l'ensemble des clients
leave           : un client sort du scrabblos
system          : envoi d'un message system à un client
message         : envoi de message à un client
register        : enregistrement de la clef public d'un client
letters_bag     : envoie d'un sac de lettres à un client
receiveWord     : reception d'un mot
sendWord        : envoi d'un mot à un client
receiveLetter   : reception d'une lettre
sendLetter      : envoi d'une lettre à un client
consensus       : demande d'initiation à un consensus (peut être ignoré)
getVerif        ; demande la vérification d'un bloc
retVerif        : retourne le vote pour l'ajout ou non d'un bloc
kick            : demande d'expulsion d'un utilisateur
initial_block   : bloc initial de la chaîne dont l'auteur est le premier à arriver sur le serveur
```
