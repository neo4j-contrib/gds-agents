# Changelog - [0.3.0] - yyyy-mm-dd

### New Features
1. Add a new get_relationship_properties_keys tool.
2. Add targetNode filtering for longest_path.
3. Add support for similarity algorithms.
4. Add relationship directionality used by graph projection as an optional parameter to all appropriate algorithms. This include all algorithms that support both directed and undirected graphs and behave differently.

### Bug Fixes
1. Return node names in several path algorithms that only returned node ids.
2. Fix a bug with loading node properties incorrectly.


### Other Changes

