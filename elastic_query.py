from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import json
from datetime import datetime
# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")
# Perform text embedding using SentenceTransformer
model = SentenceTransformer('quora-distilbert-multilingual')
embedding = model.encode("sun", show_progress_bar=False)

# Build the Elasticsearch script query
# script_query = {
#     "script_score": {
#         "query": {"match_all": {}},
#         "script": {
#             "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
#             "params": {"query_vector": embedding.tolist()}
#         }
#     }
# }
# script_query ={
#     "query_string": {
#         "query": "su",
#         "default_field": "text",
#         "fuzziness": "AUTO"
#     }
# }

script_query ={
       "multi_match": {
            "query": "sun",
            "fields": ["text", "id"],  # List of fields to search across
            "fuzziness": "AUTO",  # Automatically determine fuzziness level
            "type": "most_fields",  # Score based on matches across multiple fields
            "minimum_should_match": "70%"  # Set the minimum level of match required
        }
}            


# Execute the search query
search_results = es.search(index="test1", body={"query": script_query})

# Process and return the search results
results = search_results["hits"]["hits"]

def make_jsonable(data):
    if isinstance(data, list):
        return [make_jsonable(item) for item in data]
    elif isinstance(data, dict):
        return {key: make_jsonable(value) for key, value in data.items()}
    elif isinstance(data, datetime):
        return data.isoformat()  # Convert datetime to ISO format string
    else:
        return data  # Return as-is if already JSON serializable

# Apply the function to the results
jsonable_results = make_jsonable(results)

# Convert to a JSON-formatted string
json_string = json.dumps(jsonable_results, indent=2)
print(json_string)