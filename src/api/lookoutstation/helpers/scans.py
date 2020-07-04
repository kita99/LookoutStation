def __assign_values(port):
    result = {
        'range_start': port['id'],
        'protocol': port['protocol'],
        'state': port['state']['state'],
        'reason': port['state']['reason'],
        'service_name': port['service']['name'],
        'service_version': port['service']['version']
    }

    return result


def compact(host):
    """
        Takes in an a list of ports and attempts to compact them into port ranges
        when certain conditions are met
    """
    result = []

    for i, port in enumerate(host['ports']):
        if len(result) == 0:
            result.append({})
            result[-1] = __assign_values(port)

            continue

        if (
            result[-1]['protocol'] != port['protocol'] or
            result[-1]['state'] != port['state']['state'] or
            result[-1]['reason'] != port['state']['reason'] or
            result[-1]['service_name'] != port['service']['name']
        ):
            result[-1]['range_end'] = host['ports'][i - 1]['id']

            result.append({})
            result[-1] = __assign_values(port)

    return result
