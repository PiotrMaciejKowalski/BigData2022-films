# TODO: Tets, checks, exceptions
def cosine_similarity(vec1, vec2):
    return float(vec1.dot(vec2) / (vec1.norm(2) * vec2.norm(2)))
