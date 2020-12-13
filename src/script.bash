#!/bin/bash


if [ -z $1 ]; then
	POLI=1
else
	POLI=$1
fi

if [ -z $2 ]; then
	AUTH=1
else
	AUTH=$2
fi

if [ -z $3 ]; then
	PROXY=1234
else
	PROXY=$3
fi

echo  "$POLI $AUTH $PROXY"

#rm proxy
echo "$PROXY" > proxy #un, dos, tres
chmod u+x proxy


gnome-terminal --title="Server"  -- python3 server.py 

for i in $(seq 1 $POLI); do 
	gnome-terminal --title="Politician $i" -- python3 politician.py;
done

for i in $(seq 1 $AUTH); do 
	gnome-terminal --title="Author $i"  -- python3 author.py;
done


