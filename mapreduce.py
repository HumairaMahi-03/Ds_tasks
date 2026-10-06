import socket

Documents = [
    "This is the first document. It contains some text.",
    "This is the second document. It also contains some text.",
    "This is the third document. It has different text.",
]

def map_task(doc_id, doc_content):
    
    words = doc_content.split()
   
    word_pairs = [(word, 1) for word in words]
    
    return word_pairs

def suffle(all_mapped_pairs, num_workers):
    
    shuffled_data = {}
    
    for pairs in all_mapped_pairs:
        for word, count in pairs:
            shuffled_data.setdefault(word, []).append(count)
            
       

    buckets = {i: [] for i in range(num_workers)}
    for word, counts in shuffled_data.items():
        bucket_index = hash(word) % num_workers
        buckets[bucket_index].append((word, counts))    
    
    return shuffled_data, buckets

def main():
    num_workers = 3
    all_mapped_pairs = []
    
    for doc_id, doc_content in enumerate(Documents):
        mapped_pairs = map_task(doc_id, doc_content)
        all_mapped_pairs.append(mapped_pairs)
    
    shuffled_data, buckets = suffle(all_mapped_pairs, num_workers)
    print("Shuffled Data:", shuffled_data)
    print("Buckets:", buckets)
    print("Shuffled Data:")
    for word, counts in shuffled_data.items():
        print(f"{word}: {counts}")
    
    print("\nBuckets:")
    for bucket_index, bucket_data in buckets.items():
        print(f"Bucket {bucket_index}: {bucket_data}")

main()