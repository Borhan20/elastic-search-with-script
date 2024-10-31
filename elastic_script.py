from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Index name
index_name = "test1"

# Example data
data = [
    {"id": 1, "text": "The sun slowly set behind the mountains, casting a golden glow across the landscape. The air was crisp and cool, a gentle breeze rustling through the leaves of the trees. Birds chirped in the distance, their melodic songs filling the air. As I walked along the winding path, I couldn't help but marvel at the beauty of nature surrounding me. The scent of wildflowers wafted through the air, intoxicating and refreshing. It was a moment of tranquility, a moment to escape from the chaos of everyday life and immerse myself in the serenity of the natural world."},
    {"id": 2, "text": "The bustling city streets were filled with the sound of car horns and chatter. People hurried past, their faces lost in a sea of anonymity. Skyscrapers towered above, their reflective glass windows shimmering in the sunlight. The aroma of street food filled the air, mingling with the scent of exhaust fumes. Neon signs flashed with vibrant colors, advertising the latest products and services. It was a city that never slept, a constant whirlwind of activity and excitement. Amidst the chaos, I navigated through the crowds, searching for moments of connection and inspiration."},
    {"id": 3, "text": "The waves crashed against the shore, each one a powerful force of nature. The sand beneath my feet shifted with every step, as if it was alive. Seagulls soared overhead, their calls echoing through the salty air. The ocean stretched out before me, its vastness both awe-inspiring and humbling. I closed my eyes and listened to the symphony of the sea, the rhythm of the waves lulling me into a state of tranquility. It was a place of solace, a place where the worries of the world melted away and all that remained was the beauty of the natural world."},
    {"id": 4, "text": "The old bookstore was a treasure trove of knowledge and stories. Rows upon rows of bookshelves lined the walls, each one filled with books of every genre and era. The scent of aged paper and ink filled the air, creating an atmosphere of nostalgia and adventure. As I perused the shelves, my fingers lightly grazing the spines of the books, I felt a sense of wonder and curiosity. Each book held the potential to transport me to another world, to introduce me to new ideas and perspectives. It was a sanctuary for the avid reader, a place where imagination flourished and stories came to life."}
]

# Create Elasticsearch index and mapping
if not es.indices.exists(index=index_name):
    es_index = {
        "mappings": {
            "properties": {
                "text": {"type": "text"},
                # "embedding": {"type": "dense_vector", "dims": 768}
            }
        }
    }
    es.indices.create(index=index_name, body=es_index, ignore=[400])

# Upload documents to Elasticsearch with text embeddings
model = SentenceTransformer('quora-distilbert-multilingual')

for doc in data:
    # Calculate text embeddings using the SentenceTransformer model
    embedding = model.encode(doc["text"], show_progress_bar=False)

    # Create document with text and embedding
    document = {
        "text": doc["text"],
        # "embedding": embedding.tolist()
    }

    # Index the document in Elasticsearch
    es.index(index=index_name, id=doc["id"], body=document)


# # Perform text embedding using SentenceTransformer
# model = SentenceTransformer('quora-distilbert-multilingual')
# embedding = model.encode("sun", show_progress_bar=False)

# # Build the Elasticsearch script query
# script_query = {
#     "script_score": {
#         "query": {"match_all": {}},
#         "script": {
#             "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
#             "params": {"query_vector": embedding.tolist()}
#         }
#     }
# }

# # Execute the search query
# search_results = es.search(index="test1", body={"query": script_query})

# # Process and return the search results
# results = search_results["hits"]["hits"]
    