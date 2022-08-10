import uuid
from typing import Dict, List, Union

from fastapi import FastAPI

from app.shingle_scorer import ShingleScorer

srvurl = ""

app = FastAPI(
    title="simiscore-kshingle ML API",
    descriptions=(
        "ML API to compute similarities jaccard similarities"
        "between sentences based on hashed k-shingle (character n-grams) sets."
    ),
    version="0.1.0",
    openapi_url=f"{srvurl}/openapi.json",
    docs_url=f"{srvurl}/docs",
    redoc_url=f"{srvurl}/redoc",
)
similarity_scorer = ShingleScorer()


@app.get(f"{srvurl}/")
def get_info() -> dict:
    """Returns basic information about the application"""
    return {
        "name": "simiscore-kshingle",
        "version": app.version,
        "datasketch": {
            "k": similarity_scorer.max_k,
            "num_perm": similarity_scorer.num_perm,
        },
        "input-data": {
            "type": "string"
        },
        "output-data": {
            "type": "matrix",
            "metric": "jaccard"
        }
    }


@app.post(f"{srvurl}/similarities/", response_model=Dict[str, list])
async def compute_similarites(
    query_sents: Union[List[str], Dict[uuid.UUID, str]],
) -> Dict[str, list]:
    if isinstance(query_sents, list):
        query_sents = {uuid.uuid4(): sentence for sentence in query_sents}
    return similarity_scorer.compute_similarity_matrix(query_sents)
