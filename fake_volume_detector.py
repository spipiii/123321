
def detect_fake_volume(volume, price):

    if volume <= 0:
        return True

    if price <= 0:
        return True

    # simple heuristic
    if volume > 1_000_000_000:
        return True

    return False
