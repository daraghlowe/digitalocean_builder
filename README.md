# digitalocean_builder
Build things on digital ocean using a build script


# Current abilities
- Creates digital ocean droplets
- Automatically names droplets based on count of exiting droplets - eg. if web-1 exists, build web-2
- Allows selection of region
- Has an argeparser interface

# To Do
- Delete droplets
- Track whodunnit
- ~~List existing droplets~~ - list by tag/region/status
- Replace hard coded information with dynamic input 
- Create more comprehensive tags and droplet naming
- Faciliate restarting the droplets
- Faciliate editing droplets eg. size

# Off In The Future
- Build clustered environments


Usage:
---

```
python create_droplet.py -b -r          [build region]
python create_droplet.py -l             [list droplets]
python create_droplet.py -images        [get images]
```


Added `-images` to check for available images. Seeing as it's hardcoded currently we'd need to do it eventually. It picks up on the `api_key` too.
Need to figure out a way of just parsing the information we want from it though & also passing it to `-b` to create the droplet.
