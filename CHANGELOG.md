# Changelog - [0.2.0] - yyyy-mm-dd

### New Features
1. Project all (non-string) node properties using the appropriate (integer/float) types.
2. Support personalisation, post-filtering and node name mapping in centrality and community algorithms whenever appropriate.
3. Support post-filtering and node name mapping in community algorithms whenever appropriate.
4. Support orientation parameter in Degree Centrality.

### Bug Fixes
1. Fix GDS calls for path and community algorithms and clean up returned data format.
2. Fix a bug during GDS graph projection that always created bidirectional relationships.

### Other Changes
1. Removed minimum_weight_k_spanning_tree since it is write mode only, which may modify the database unexpectedly.
