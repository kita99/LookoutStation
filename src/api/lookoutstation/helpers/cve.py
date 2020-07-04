def check_for_match(existing, current):
    if not existing:
        return False

    for cve in existing:
        if cve.name == current.name:
            return True

    return False
