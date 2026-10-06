import multiprocessing as mp


DOCUMENTS = [
    "cat dog apple",
    "sun moon cat",
    "apple dog tree"
]


# MAP
def map_task(doc_id, text):
    result = []

    for word in text.split():
        length = len(word)
        result.append((length, word))

    return result


# SHUFFLE
def shuffle(all_pairs):
    groups = {}

    for pairs in all_pairs:
        for length, word in pairs:
            groups.setdefault(length, []).append(word)

    return groups


# REDUCE
def reduce_task(item):
    length, words = item

    return length, len(words), words


def main():

    # MAP
    all_mapped = []

    for doc_id, text in enumerate(DOCUMENTS):
        pairs = map_task(doc_id, text)
        all_mapped.append(pairs)

    print("MAP OUTPUT:")
    for pairs in all_mapped:
        print(pairs)


    # SHUFFLE
    shuffled = shuffle(all_mapped)

    print("\nSHUFFLE OUTPUT:")
    for length, words in shuffled.items():
        print(length, "letters:", words)


    # REDUCE
    print("\nREDUCE OUTPUT:")

    for length, words in sorted(shuffled.items()):
        print(
            f"{length} letters -> "
            f"{len(words)} words: {words}"
        )


if __name__ == "__main__":
    main()