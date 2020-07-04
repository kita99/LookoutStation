export function SET_OVERVIEW_STATISTICS (state, payload) {
  state.assetCount = payload.asset_count
  state.vulnerabilityCount = payload.vulnerability_count
  state.openPortCount = payload.open_port_count
  state.feedCount = payload.feed_count
  state.cpeCount = payload.cpe_count
  state.cveCount = payload.cve_count
}
