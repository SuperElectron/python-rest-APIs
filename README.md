# Udemy Coursework
- python rest APIs with Flask, Docker, MongoDB, and AWS DevOps


## Random Docker Functions
- A handful of docker CLI functions that are extremely helpful when working. \
```console
*Stop all containers and remove network
$ docker-compose down
*Remove all volumes
$ docker volume prune
*Remove all stopped containers/images
$ docker system prune -a

*Show all runnning containers
$ docker ps
*view logs from a specific container
$ docker logs <id> 
*Show all running and stopped containers
$ docker ps -a 
*Remove all stopped networks
$ docker network prune
*delete all volumes and images
$ docker rm $(docker ps -aq) && docker rmi $(docker images -q)
```