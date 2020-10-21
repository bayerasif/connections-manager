# Connections manager
Connections manager is a service which controls connections to a resource.

## Installation

Build the Docker image from the Dockerfile:
```bash
docker build -t connections-manager .
```
Run with mapping of port 7080 in the container to port 7080 on the Docker host:
```bash
docker run -dp 7080:7080 connections-manager
```

## Usage

In order to ask for a resource send a GET request to:

```http request
http://0.0.0.0:7080/
```
On success a resource will be returned in the given format:
```json
{
  "ip": "<resource_ip>",
  "username": "<username>",
  "password": "<password>"
}
```
In order to release a resource send a POST request to:
```http request
http://0.0.0.0:7080/
```
with body in the given format:
```json
{
  "ip": "<resource_ip>"
}
```
On success the same json will be returned.


## Error Handling
In the case of one of the following:

- Any request not in one of the formats defined above
- GET request while all the resources are already taken
- POST request in which a free resource is asked to be released 

'400 Bad Request' HTTP response will be returned.


## Resources Database
On the first run of the service a resource pool database will be created, and will be initialized with 20 random resources.
The resulting behaviour will be that in the case that the service stops and then runs again, the resources will be in the same state (locked or free) as before.
In order to reset the resources data, the db file 
```text
'/resources_pool.db'
```
has to be deleted.
