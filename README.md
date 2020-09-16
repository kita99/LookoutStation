# LookoutStation

# Description
LookoutStation is a CyberSecurity tool that focus on providing CSIRT teams insight into their assets. It gathers threats from various vulnerability feeds and cross-checks them against the output of automated NMAP scans or metrics provided by the CLI tool. 


## Requirements

 - Docker and Docker-Compose
 - OSQuery 4.3+

## Setup

Start by creating the required environment dotfiles, check the examples given by `.env.example` files

```
   git clone https://github.com/kita99/LookoutStation
   cd lookoutstation
   docker-compose up --build
```
