""" Sentence similarity. """

from sentence_transformers import SentenceTransformer, util

# Pre-trained model
MODEL = SentenceTransformer('all-MiniLM-L6-v2')


def compute_sentence_similarity(sentences):
    """ Compute the similarity between a given list of sentences.

    Args:
        sentences (List): List of sentences

    Returns:
        Pairwise list of sentences ranked by their cosine similarity score.

    """

    # Encode all sentences.
    embeddings = MODEL.encode(sentences)

    # Compute cosine similarity between all pairs.
    cosine_similarity = util.cos_sim(embeddings, embeddings)

    # Add all pairs to a list with their cosine similarity score.
    pairwise_sentence_combinations = []
    for i in range(len(cosine_similarity) - 1):
        for j in range(i + 1, len(cosine_similarity)):
            pairwise_sentence_combinations.append([cosine_similarity[i][j], i, j])

    # Sort the pairwise list by the highest cosine similarity score.
    pairwise_sentence_combinations = sorted(pairwise_sentence_combinations, key=lambda x: x[0], reverse=True)

    # Return a ranked list of tuples with each tuple containing each pair and their cosine similarity score.
    ranked_pairs = []
    for score, i, j in pairwise_sentence_combinations:
        ranked_pairs.append((sentences[i], sentences[j], float('%.5f' % cosine_similarity[i][j])))
    return ranked_pairs
