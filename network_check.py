
def networks_compatible(networks_a, networks_b):

    for n in networks_a:
        if n in networks_b:
            return True

    return False
