do not do this lol

```
python create_droplet.py -l k8s
[<Droplet: blah>, <Droplet: blah>, <Droplet: blah>]
Creating your droplet!
```

# digitalocean_builder
Build things on digital ocean using a build script


# Current abilities
- Creates digital ocean droplets
- Automatically names droplets based on count of exiting droplets - eg. if web-1 exists, build web-2
- Allows selection of region
- Has an argeparser interface

# To Do
- Delete droplets
- Track who whodunnit
- ~~List existing droplets~~ - list by tag
- Replace hard coded information with dynamic input 
- Create more comprehensive tags and droplet naming
- Faciliate restarting the droplets
- Faciliate editing droplets eg. size

# Off In The Future
- Build clustered environments
