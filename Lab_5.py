import multiprocessing as mp
import os
import time

MAP_TIMEOUT = 2.0

DOCUMENTS = [
    "hello world hello",
    "python is easy",
    "hello python world",
    "map reduce is useful",
    "python is powerful"
]


def flaky_map_task(doc_id, text, attempt):
    pid = os.getpid()

    print(
        f"[MAP worker pid={pid}] "
        f"attempt #{attempt} on doc {doc_id}: {text!r}"
    )

    if doc_id == 1 and attempt == 1:
        print(
            f"[MAP worker pid={pid}] "
            f"!! CRASHING on doc {doc_id}"
        )
        raise RuntimeError("simulated worker crash")

    if doc_id == 3:
        time.sleep(3.0)

    pairs = [(word, 1) for word in text.split()]

    return pairs


def run_map_with_retry(pool, doc_id, text, max_attempts=3):

    for attempt in range(1, max_attempts + 1):

        async_result = pool.apply_async(
            flaky_map_task,
            (doc_id, text, attempt)
        )

        try:
            return async_result.get(timeout=MAP_TIMEOUT)

        except mp.TimeoutError:

            print(
                f"[MASTER] doc {doc_id} "
                f"attempt #{attempt} is a STRAGGLER "
                f"(> {MAP_TIMEOUT}s) "
                f"-- launching a BACKUP copy"
            )

            backup_result = pool.apply_async(
                flaky_map_task,
                (doc_id, text, attempt)
            )

            return backup_result.get()

        except Exception as e:

            print(
                f"[MASTER] doc {doc_id} "
                f"attempt #{attempt} CRASHED ({e}); "
                f"re-executing on a fresh worker"
            )

            continue

    raise RuntimeError(
        f"doc {doc_id} failed after {max_attempts} attempts"
    )


def main():
    print(
        "[MASTER] splitting input into",
        len(DOCUMENTS),
        "map tasks"
    )
    with mp.Pool(processes=4) as pool:

        all_pairs = []

        for doc_id, text in enumerate(DOCUMENTS):
            pairs = run_map_with_retry(
                pool,
                doc_id,
                text
            )
            all_pairs.extend(pairs)

    counts = {}
    for word, c in all_pairs:
        counts[word] = counts.get(word, 0) + c
    print(
        "\n[MASTER] All map tasks eventually succeeded. "
        "FINAL WORD COUNTS:"
    )
    for word, count in sorted(
        counts.items(),
        key=lambda kv: -kv[1]
    ):
        print(f"  {word:12s} {count}")


if __name__ == "__main__":
    mp.freeze_support()
    main()