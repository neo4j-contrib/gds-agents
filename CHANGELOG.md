# Changelog - [0.2.0] - yyyy-mm-dd

### New Features
1. Project all (non-string) node properties using the appropriate (integer/float) types.
2. Support personalisation and post-filtering in centrality algorithms.

### Bug Fixes
1. Fix GDS call for path algorithms and clean up returned data format.


### Other Changes
1. Removed minimum_weight_k_spanning_tree since it is write mode only, which may modify the database unexpectedly.