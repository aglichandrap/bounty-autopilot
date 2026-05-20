from __future__ import annotations

import os

import bounty_volume_expander as expander


MAX_QUERIES_PER_RUN = int(os.environ.get("BOUNTY_VOLUME_MAX_QUERIES", "8"))
QUERY_DELAY_SECONDS = float(os.environ.get("BOUNTY_QUERY_DELAY_SECONDS", "3"))
QUERY_OFFSET = int(os.environ.get("BOUNTY_VOLUME_QUERY_OFFSET", os.environ.get("GITHUB_RUN_NUMBER", "0")) or "0")

_ORIGINAL_LOAD_QUERIES = expander.load_queries
_ORIGINAL_SLEEP = expander.time.sleep


def load_queries() -> list[str]:
    queries = _ORIGINAL_LOAD_QUERIES()
    if not queries:
        return []
    limit = max(1, min(MAX_QUERIES_PER_RUN, len(queries)))
    offset = (QUERY_OFFSET * limit) % len(queries)
    selected = [queries[(offset + index) % len(queries)] for index in range(limit)]
    print(
        f"Lite volume expander using {len(selected)}/{len(queries)} queries "
        f"from offset {offset} with {QUERY_DELAY_SECONDS:g}s delay."
    )
    return selected


def controlled_sleep(_seconds: float) -> None:
    _ORIGINAL_SLEEP(QUERY_DELAY_SECONDS)


expander.load_queries = load_queries
expander.time.sleep = controlled_sleep


if __name__ == "__main__":
    raise SystemExit(expander.main())
