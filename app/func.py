import hashlib
import random


def generate_dna_sequence(id: str, region: str, age: int, seed: int) -> str:
    # Set the seed for reproducibility
    combined_seed = f"{id}-{region}-{age}-{seed}"
    hash_value = int(hashlib.sha256(combined_seed.encode()).hexdigest(), 16)
    random.seed(hash_value)

    # Define the DNA alphabet
    dna_chars = ['A', 'T', 'G', 'C']

    # Generate a random DNA sequence of length between 100 and 150
    sequence_length = random.randint(100, 150)
    dna_sequence = ''.join(random.choices(dna_chars, k=sequence_length))

    return dna_sequence
