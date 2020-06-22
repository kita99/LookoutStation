package responses

type CVEFeed struct {
	CVEDataType         string `json:"CVE_data_type"`
	CVEDataFormat       string `json:"CVE_data_format"`
	CVEDataVersion      string `json:"CVE_data_version"`
	CVEDataNumberOfCVEs string `json:"CVE_data_numberOfCVEs"`
	CVEDataTimestamp    string `json:"CVE_data_timestamp"`
    CVEItems            []CVE  `json:"CVE_Items" diff:"CVE_Items"`
}

type CVE struct {
    DataType    string `json:"data_type" diff:"data_type"`
    DataFormat  string `json:"data_format" diff:"data_format"`
    DataVersion string `json:"data_version" diff:"data_version"`
    CVEDataMeta struct {
        ID       string `json:"ID" diff:"ID"`
        ASSIGNER string `json:"ASSIGNER" diff:"ASSIGNER"`
    } `json:"CVE_data_meta" diff:"CVE_data_meta"`
    Problemtype struct {
        ProblemtypeData []struct {
            Description []struct {
                Lang  string `json:"lang" diff:"lang"`
                Value string `json:"value" diff:"value"`
            } `json:"description" diff:"description"`
        } `json:"problemtype_data" diff:"problemtype_data"`
    } `json:"problemtype" diff:"problemtype"`
    References struct {
        ReferenceData []struct {
            URL       string   `json:"url" diff:"url"`
            Name      string   `json:"name" diff:"name"`
            Refsource string   `json:"refsource" diff:"refsource"`
            Tags      []string `json:"tags" diff:"tags"`
        } `json:"reference_data" diff:"reference_data"`
    } `json:"references" diff:"references"`
    Description struct {
        DescriptionData []struct {
            Lang  string `json:"lang" diff:"lang"`
            Value string `json:"value" diff:"value"`
        } `json:"description_data" diff:"description_data"`
    } `json:"description" diff:"description"`
} `json:"cve" diff:"cve"`
Configurations struct {
    CVEDataVersion string `json:"CVE_data_version" diff:"CVE_data_version"`
    Nodes          []struct {
        Operator string `json:"operator" diff:"operator"`
        CpeMatch []struct {
            Vulnerable bool   `json:"vulnerable" diff:"vulnerable"`
            Cpe23URI   string `json:"cpe23Uri" diff:"cpe23Uri"`
        } `json:"cpe_match" diff:"cpe_match"`
    } `json:"nodes" diff:"nodes"`
} `json:"configurations" diff:"configurations"`
Impact struct {
    BaseMetricV2 struct {
        CvssV2 struct {
            Version               string  `json:"version" diff:"version"`
            VectorString          string  `json:"vectorString" diff:"vectorString"`
            AccessVector          string  `json:"accessVector" diff:"accessVector"`
            AccessComplexity      string  `json:"accessComplexity" diff:"accessComplexity"`
            Authentication        string  `json:"authentication" diff:"authentication"`
            ConfidentialityImpact string  `json:"confidentialityImpact" diff:"confidentialityImpact"`
            IntegrityImpact       string  `json:"integrityImpact" diff:"integrityImpact"`
            AvailabilityImpact    string  `json:"availabilityImpact" diff:"availabilityImpact"`
            BaseScore             float64 `json:"baseScore" diff:"baseScore"`
        } `json:"cvssV2" diff:"cvssV2"`
        Severity                string  `json:"severity" diff:"severity"`
        ExploitabilityScore     float64 `json:"exploitabilityScore" diff:"exploitabilityScore"`
        ImpactScore             float64 `json:"impactScore" diff:"impactScore"`
        AcInsufInfo             bool    `json:"acInsufInfo" diff:"acInsufInfo"`
        ObtainAllPrivilege      bool    `json:"obtainAllPrivilege" diff:"obtainAllPrivilege"`
        ObtainUserPrivilege     bool    `json:"obtainUserPrivilege" diff:"obtainUserPrivilege"`
        ObtainOtherPrivilege    bool    `json:"obtainOtherPrivilege" diff:"obtainOtherPrivilege"`
        UserInteractionRequired bool    `json:"userInteractionRequired" diff:"userInteractionRequired"`
    } `json:"baseMetricV2" diff:"baseMetricV2"`
    BaseMetricV3 struct {
        CvssV3 struct {
            Version               string  `json:"version"`
            VectorString          string  `json:"vectorString"`
            AttackVector          string  `json:"attackVector"`
            AttackComplexity      string  `json:"attackComplexity"`
            PrivilegesRequired    string  `json:"privilegesRequired"`
            UserInteraction       string  `json:"userInteraction"`
            Scope                 string  `json:"scope"`
            ConfidentialityImpact string  `json:"confidentialityImpact"`
            IntegrityImpact       string  `json:"integrityImpact"`
            AvailabilityImpact    string  `json:"availabilityImpact"`
            BaseScore             float64 `json:"baseScore"`
            BaseSeverity          string  `json:"baseSeverity"`
        } `json:"cvssV3"`
        ExploitabilityScore float64 `json:"exploitabilityScore"`
        ImpactScore         float64 `json:"impactScore"`
    } `json:"baseMetricV3"`
} `json:"impact" diff:"impact"`
PublishedDate    string `json:"publishedDate"`
LastModifiedDate string `json:"lastModifiedDate"`
}
