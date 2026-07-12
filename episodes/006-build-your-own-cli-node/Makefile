# Episode 006 — Node CLI
.PHONY: setup run test

setup:
	@# No third-party deps, but wire up npm if it's available.
	@command -v npm >/dev/null 2>&1 && npm install --silent || echo "(npm not found — this episode needs none anyway)"

run:
	@printf "the quick brown fox\njumps over\n" | node src/cli.js

test:
	@node tests/cli.test.js

clean:
	rm -rf node_modules
