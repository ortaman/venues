# Venues

API to searching venues near of the current location.

## Installation
- Install [docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-repository1) 
and [docker-compose](https://docs.docker.com/compose/install/).

```
In the root directory:
docker-compose up
Go to http://localhost:8000/ and you should see the swagger docs (in devepment).

In another console:
- docker-compose exec web my_app/manage.py migrate
- docker-compose exec web my_app/manage.py createsuperuser

Go to http://localhost:8000/admin
```
