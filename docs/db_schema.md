![Database Schema](http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/Lyghtur/kbp/master/docs/uml/database_schema.puml)\
## Table of content
- [Entities](#entities)
  - [Users](#users)
  - [Tasks](#tasks)
  - [Files](#files)
# Entities
## Users
| Column | Type | Description |
|-|-|-|
| **id** | uuid PK ||
## Tasks
| Column | Type | Description |
|-|-|-|
| **id** | uuid PK ||
| name | Text | Task title |
## Files
| Column | Type | Description |
|-|-|-|
| **id** | uuid PK||
| path | varchar(256) | location at the file storage |
| task_id | uuid FK || 
*[main](../README.md)*