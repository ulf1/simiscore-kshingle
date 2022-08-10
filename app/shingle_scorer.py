import uuid
from typing import Dict, Set

import datasketch
import kshingle as ks


class ShingleScorer:
    """Computes similarity scores between senteces based on hashed k-shingles.
    Default k is 3."""

    def __init__(self, max_k=3, num_perm=256):
        self.max_k = max_k
        self.num_perm = num_perm

    def compute_similarity_matrix(
        self, query_sents: Dict[uuid.UUID, str]
    ) -> Dict[str, list]:
        ids = list(query_sents.keys())
        minhash_table = []
        for _, sentence in query_sents.items():
            shingle_set = ks.shingleset_k(sentence, self.max_k)
            minhash = self._minhash_shingle_set(shingle_set)
            minhash_table.append(minhash)
        similarity_matrix = [
            [
                minhash_table[i].jaccard(minhash_table[j])
                for j in range(len(minhash_table))
            ]
            for i in range(len(minhash_table))
        ]

        return {"ids": ids, "matrix": similarity_matrix}

    def _minhash_shingle_set(
        self, shingle_set: Set[str]
    ) -> datasketch.MinHash:
        minhash = datasketch.MinHash(num_perm=self.num_perm)
        for shingle in shingle_set:
            minhash.update(shingle.encode("utf-8"))
        return minhash
