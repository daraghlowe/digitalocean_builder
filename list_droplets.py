import digitalocean
import argparse
import sys

def get_file_contents(filename):
    """ Given a filename,
        return the contents of that file
    """
    try:
        with open(filename, 'r') as f:
            # It's assumed our file contains a single line,
            # with our API key
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)

secrets_file = 'keys'
api_key = get_file_contents(secrets_file)

def list_droplets():
    manager = digitalocean.Manager(token=api_key)
    # Pulls a list of all droplet objects
    droplets_list = manager.get_all_droplets()
    # Extract information from Droplet object
    for droplet in droplets_list:
    	droplet_tags = droplet.tags
    	droplet_id = droplet.id
    	droplet_created_at = droplet.created_at
    	droplet_status = droplet.status
    	droplet_region = droplet.region["name"]

    	print(droplet)

    	# print("Droplet tags: {}".format(droplet_tags))
    	# print("Droplet ID: {}".format(droplet_id))
    	# print("Droplet was created at: {}".format(droplet_created_at))
    	# print("Droplet status: {}".format(droplet_status))
    	# print("Droplet region: {}".format(droplet_region))


list_droplets()