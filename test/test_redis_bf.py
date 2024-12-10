from src.redis_bf import RedisBloomFilter
from random import shuffle
import redis

# Connect to Redis
redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)

# Parameters for the Bloom Filter
n = 20  # Number of items to add
p = 0.05  # False positive probability

# Redis key for the Bloom Filter
redis_key = "test_bloom_filter"

# Clear the Redis key before testing
redis_client.delete(redis_key)

# Initialize the Redis-backed Bloom Filter
bloomf = RedisBloomFilter(
    redis_client,
    redis_key,
    n,
    p,
)

print("Size of bit array: {}".format(bloomf.size))
print("False positive Probability: {}".format(p))
print("Number of hash functions: {}".format(bloomf.hash_count))

# Words to be added
word_present = [
    "abound",
    "abounds",
    "abundance",
    "abundant",
    "accessible",
    "bloom",
    "blossom",
    "bolster",
    "bonny",
    "bonus",
    "bonuses",
    "coherent",
    "cohesive",
    "colorful",
    "comely",
    "comfort",
    "gems",
    "generosity",
    "generous",
    "generously",
    "genial",
]

# Words not added
word_absent = [
    "bluff",
    "cheater",
    "hate",
    "war",
    "humanity",
    "racism",
    "hurt",
    "nuke",
    "gloomy",
    "facebook",
    "geeksforgeeks",
    "twitter",
]

# Add words to the Bloom Filter
for item in word_present:
    bloomf.add(item)

# Shuffle words for testing
shuffle(word_present)
shuffle(word_absent)

# Test words
test_words = word_present[:10] + word_absent
shuffle(test_words)

# Check each word and print results
for word in test_words:
    if bloomf.check(word):
        if word in word_absent:
            print("'{}' is a false positive!".format(word))
        else:
            print("'{}' is probably present!".format(word))
    else:
        print("'{}' is definitely not present!".format(word))

# Cleanup Redis key after test
redis_client.delete(redis_key)
