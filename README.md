# BusPoint-Server
A server side program to handle routing requests written in Django

## How it works
The server provides REST endpoints to a mobile client, with which it provides the start, and destination stops. 
The server computes the routing stops using Harvesine's formula as a distance weight computer, and returns a list of stops to be passed through.

## Installation
- Clone this repostiory, and enter the root of the project
- Enable a virtual environment by using a tool of your choice i.e. `venv`, `pipenv`, `virtualenv`
- Run  `pip install -r requirements.txt` to fetch the requirements
- Run `./manage.py startserver`

## Limitations
Currently the server works with stops only within the Dodoma region, a scalable soulution is to be implemented soon.
