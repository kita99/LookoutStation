from lookoutstation.models import CVEImpactMetric

def extract_and_prepare(impact, cve_name):
    impact_metrics = []

    if 'baseMetricV2' in impact:
        metric = impact['baseMetricV2']

        impact_metrics.append(CVEImpactMetric(
            cve_name=cve_name,
            cvss_version=metric['cvssV2']['version'],
            vector_string=metric['cvssV2']['vectorString'],
            attack_vector=metric['cvssV2']['accessVector'],
            attack_complexity=metric['cvssV2']['accessComplexity'],
            confidentiality_impact=metric['cvssV2']['confidentialityImpact'],
            integrity_impact=metric['cvssV2']['integrityImpact'],
            availability_impact=metric['cvssV2']['integrityImpact'],
            base_score=metric['cvssV2']['baseScore'],
            exploitability_score=metric['exploitabilityScore'],
            impact_score=metric['impactScore']
        ))

    if 'baseMetricV3' in impact:
        metric = impact['baseMetricV3']

        impact_metrics.append(CVEImpactMetric(
            cve_name=cve_name,
            cvss_version=metric['cvssV3']['version'],
            vector_string=metric['cvssV3']['vectorString'],
            attack_vector=metric['cvssV3']['attackVector'],
            attack_complexity=metric['cvssV3']['attackComplexity'],
            privileges_required=metric['cvssV3']['privilegesRequired'],
            confidentiality_impact=metric['cvssV3']['confidentialityImpact'],
            integrity_impact=metric['cvssV3']['integrityImpact'],
            availability_impact=metric['cvssV3']['integrityImpact'],
            base_score=metric['cvssV3']['baseScore'],
            base_severity=metric['cvssV3']['baseSeverity'],
            exploitability_score=metric['exploitabilityScore'],
            impact_score=metric['impactScore']
        ))

    return impact_metrics
