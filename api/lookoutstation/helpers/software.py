def check_for_match(existing, current):
    for software in existing:
        if software.name == curent['name'] and software.version == current['version']:
            return 'match', software

        if software.name == curent['name'] and software.version != current['version']:
            return 'update', software

    return 'no_match', None
