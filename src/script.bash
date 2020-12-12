#!/bin/bash

POLI=1
AUTH=1


gnome-terminal --title="Server"  -- python3 server.py 

for i in $(seq 1 $END); do 
	gnome-terminal --title="Politician $i" -- python3 politician.py;
done

for i in $(seq 1 $END); do 
	gnome-terminal --title="Author $i"  -- python3 author.py
done
