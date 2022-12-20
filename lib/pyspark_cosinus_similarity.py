from pyspark.ml.linalg import Vectors, VectorUDT
from pyspark.sql.functions import udf

# Define a function that takes two vectors as input and returns their cosine similarity
def cosineSimilarity(vec1, vec2):
    return float(vec1.dot(vec2) / (vec1.norm(2) * vec2.norm(2)))


    cosine_similarity_udf = udf(cosine_similarity, FloatType())

    # Use the UDF to compute the cosine similarity between the two columns
    df = df.withColumn("similarity", cosine_similarity_udf("col1", "col2"))