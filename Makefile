.PHONY: check test

# Validate every card and tool against schema/, then run the fixture self-test.
check:
	python3 scripts/check.py
	python3 scripts/check.py --self-test

test: check
