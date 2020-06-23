from lookoutstation.models import CPE

CPE_MATCH = 'standard:version:part:vendor:product:version:update:edition:language:sw_edition:target_sw:target_hw:other'

def __parse(matches, cve_name):
    parsed = []

    keys = CPE_MATCH.split(':')

    for match in matches:
        expanded = dict(zip(keys, match.split(':')))

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
        return matches

    for node in nodes:
        if 'cpe_match' in node:
            if node['cpe_match']:
                for match in node['cpe_match']:
                    if 'cpe23Uri' in match:
                        matches.append(match['cpe23Uri'])

        if 'children' in node:
            matches += find_and_parse(node['children'], cve_name, False)

    if not parse:
        return matches

    return __parse(matches, cve_name)
