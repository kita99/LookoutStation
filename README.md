# LookoutStation

![](https://lookout.network/img/logo-black.335dd7d1.svg)

# Description
[LookoutStation](https://lookoutstation.network/) is a CyberSecurity tool that focus on providing CSIRT teams a complete inventory of each organization assets.

It monitors newly added CVE's (using [NIST](https://www.nist.gov/) feeds) and tries to match them against installed software.

## Requirements

 - Docker and Docker-Compose
 - OSQuery 4.3+

## Running

    git clone ssh://git@gitlab.estig.ipb.pt:4589/a44721/lookoutstation.git
    cd lookoutstation
    docker-compose up --build

Note: **configs/postgres.env** needs to be created. A configuration example is given on **configs/postgres.env.example**
 
## Compatibility
The following Linux distros have been tested and confirmed to be working:
- Ubuntu
- Debian
- Arch Linux

## Languages

 - Python 3
 - Go Lang
 - JavaScript
 - VueJS

## Infrastructure
![Network Infrastructure](https://i.imgur.com/4usjjjr.png)
