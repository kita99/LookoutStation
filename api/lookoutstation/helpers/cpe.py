from lookoutstation.models import CPE

CPE_MATCH = 'standard:version:part:vendor:product:version:update:edition:language:sw_edition:target_sw:target_hw:other'

def __parse(matches, cve_name):
    parsed = []

    keys = CPE_MATCH.split(':')

    for match in matches:
        expanded = dict(zip(keys, values.split(':')))

        parsed.append(CPE(
            cve_name=cve_name,
            part=expanded['part'],
            vendor=expanded['vendor'],
            product=expanded['product'],
            version=expanded['version'],
            update=expanded['update'],
            edition=expanded['edition']
        ))

    return parsed


def find_and_parse(nodes, cve_name, parse=True):
    matches = []

    if len(nodes) == 0:
        return false

    for node in nodes:
        if 'cpe_match' in node:
            if 'cpe23Uri' in node['cpe_match']:
                matches.append(node['cpe_match'])

        if 'children' in node:
            sub_matches = find_and_parse(nodes['children'], cve_name, False)
            matches.append(sub_matches)

    if not parse:
        return matches

    return __parse(matches)
