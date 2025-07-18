# Changelog

## [0.2.6] - 2025-07-18
### Added
- CLI command `get-context` to print recent memory entries
- Test coverage for the new CLI command
- Documentation updates for context retrieval

### Changed
- Version bumped to 0.2.6

## [0.2.5] - 2025-07-18
### Added
- `ConvoGraph.refresh()` to keep memory in sync across agents
- `ConvoGraph.context()` now reloads data before filtering
- Test ensuring context reflects updates from other instances

### Changed
- Version bumped to 0.2.5

## [0.2.4] - 2025-07-17
### Added
- `ConvoGraph.context()` method to fetch recent interactions
- `Agent.get_context()` convenience wrapper
- `LOG_FILE` environment variable for configurable logging path
- Documentation updates covering context retrieval and log configuration

### Changed
- Improved logging initialization message

