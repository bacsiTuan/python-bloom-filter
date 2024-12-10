import redis
import mmh3
import math


class RedisBloomFilter:
    """
    Redis-backed Bloom Filter using murmur3 hash function.
    """

    def __init__(self, redis_client, redis_key, items_count, fp_prob):
        """
        Initialize Redis-based Bloom Filter.

        :param redis_client: Redis connection object
        :param redis_key: Key in Redis to store the bit array
        :param items_count: Number of items expected to be stored in bloom filter
        :param fp_prob: Desired false positive probability
        """
        self.redis_client = redis_client
        self.redis_key = redis_key

        # False Positive probability
        self.fp_prob = fp_prob

        # Calculate size of the bit array
        self.size = self.get_size(items_count, fp_prob)

        # Calculate number of hash functions
        self.hash_count = self.get_hash_count(self.size, items_count)

    def add(self, item):
        """
        Add an item to the Bloom Filter.
        """
        for i in range(self.hash_count):
            # Generate hash and calculate the bit index
            digest = mmh3.hash(item, i) % self.size
            # Set the corresponding bit in Redis
            self.redis_client.setbit(self.redis_key, digest, 1)

    def check(self, item):
        """
        Check if an item might be in the Bloom Filter.
        """
        for i in range(self.hash_count):
            # Generate hash and calculate the bit index
            digest = mmh3.hash(item, i) % self.size
            # Check if the corresponding bit is set in Redis
            if self.redis_client.getbit(self.redis_key, digest) == 0:
                return False  # Definitely not in the set
        return True  # Might be in the set

    @classmethod
    def get_size(cls, n, p):
        """
        Return the size of bit array(m) to used using
        following formula
        m = -(n * lg(p)) / (lg(2)^2)
        n : int
            number of items expected to be stored in filter
        p : float
            False Positive probability in decimal
        """
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)

    @classmethod
    def get_hash_count(cls, m, n):
        """
        Return the hash function(k) to be used with following formula
        k = (m/n) * lg(2)

        m : int
            size of bit array
        n : int
            number of items expected to be stored in filter
        """
        k = (m / n) * math.log(2)
        return int(k)
