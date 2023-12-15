""" Duplicate skills detector. """

import pandas as pd
import pickle

from ddat.pipeline.models.semantic_similarity.pre_trained.sentence_similarity import compute_sentence_similarity

# Module name.
MODULE_NAME = 'Duplicate Skills Detector'

# Input parsed objects.
INPUT_SKILLS_FILE_PATH = 'parsed/skills.pkl'

# Output file relative path and name.
OUTPUT_RANKED_SKILLS_FILE_PATH = 'models/semantic_similarity/skills_semantic_similarity.xlsx'

# Skill levels.
SKILL_LEVELS = ['Awareness', 'Working', 'Practitioner', 'Expert']


def run(base_working_dir):
    """ Run this pipeline module.

    Args:
        base_working_dir (string): Path to the base working directory.

    """

    # Load the parsed Skill objects from file.
    skills = load_skills(base_working_dir)

    # Flatten skill properties into descriptive sentences.
    skill_sentences = generate_skill_sentences(skills)
    skill_names = skill_sentences[0]

    # Compare and rank skill name and description sentences.
    skill_name_description_sentences = skill_sentences[1]
    skill_name_description_sentences_ranked = compare_rank_skill_name_description_sentences(
        skill_name_description_sentences)

    # Compare and rank skill name, description and skill level sentences.
    skill_name_description_skill_level_sentences = skill_sentences[2]
    skill_name_description_skill_level_sentences_ranked = compare_rank_skill_name_description_skill_level_sentences(
        skill_name_description_skill_level_sentences)

    # Generate a dataframe of ranked skill name and description sentences.
    skill_name_description_sentences_ranked_df = generate_skill_sentences_similarity_dataframe(
        skill_sentences=skill_name_description_sentences,
        ranked_skill_sentences=skill_name_description_sentences_ranked,
        skill_names=skill_names)

    # Generate a dataframe of ranked skill name, description and skill level sentences.
    skill_name_description_skill_level_sentences_ranked_df = generate_skill_sentences_similarity_dataframe(
        skill_sentences=skill_name_description_skill_level_sentences,
        ranked_skill_sentences=skill_name_description_skill_level_sentences_ranked,
        skill_names=skill_names)

    # Write the ranked skill sentence dataframes to file.
    write_skill_sentences_similarity_dataframes_to_file(
        base_working_dir, skill_name_description_sentences_ranked_df,
        skill_name_description_skill_level_sentences_ranked_df)


def load_skills(base_working_dir):
    """ Load the list of parsed Skill objects from file.

    Args:
        base_working_dir (string): Path to the base working directory.

    Returns:
        List of skill objects.

    """

    with open(f'{base_working_dir}/{INPUT_SKILLS_FILE_PATH}', 'rb') as f:
        skills = pickle.load(f)
    return skills


def generate_skill_sentences(skills):
    """ Flatten skill properties into descriptive sentences.

    Args:
        skills (List): List of skill objects.

    Returns:
        Tuple of dictionaries containing descriptive sentences for each skill.

    """

    skill_names = {}
    skill_names_descriptions = {}
    skill_names_descriptions_skill_levels = {}
    for skill in skills:

        # Generate a dictionary of skill names only.
        skill_names[skill.anchor_id] = skill.name

        # Generate a dictionary of skill names concatenated with skill descriptions.
        if skill.description:
            skill_names_descriptions[skill.anchor_id] = f'{skill.name} - {skill.description}'

        # Generate a dictionary of skill names concatenated with skill descriptions and skill levels.
        sentence = skill.name
        if skill.description:
            sentence = f'{sentence} - {skill.description}'
        for skill_level in SKILL_LEVELS:
            if skill_level in skill.skill_levels:
                for skill_level_description in skill.skill_levels[skill_level]:
                    sentence = f'{sentence}; {skill_level_description}'
        skill_names_descriptions_skill_levels[skill.anchor_id] = sentence

    return skill_names, skill_names_descriptions, skill_names_descriptions_skill_levels


def compare_rank_skill_name_description_sentences(skill_name_description_sentences):
    """ Compare and rank the similarity between skill name and description sentences.

    Args:
        skill_name_description_sentences (Dict): Skill name and description sentences.

    Returns:
        Pairwise list of skill sentences ranked by their cosine similarity score.

    """

    return compute_skill_sentences_similarity(skill_name_description_sentences)


def compare_rank_skill_name_description_skill_level_sentences(skill_name_description_skill_level_sentences):
    """ Compare and rank the similarity between skill name, description and skill level sentences.

    Args:
        skill_name_description_skill_level_sentences (Dict): Skill name, description and skill level sentences.

    Returns:
        Pairwise list of skill sentences ranked by their cosine similarity score.

    """

    return compute_skill_sentences_similarity(skill_name_description_skill_level_sentences)


def compute_skill_sentences_similarity(skill_sentences_dict):
    """ Compute the similarity between given skill sentences.

    Args:
        skill_sentences_dict (Dict): Dictionary of skill sentences

    Returns:
        Pairwise list of skill sentences ranked by their cosine similarity score.
    """

    # Generate a single list of sentences.
    skill_sentences = []
    for skill_sentence in skill_sentences_dict.values():
        skill_sentences.append(skill_sentence)

    # Generate a pairwise list of skill sentences ranked by their cosine similarity score.
    return compute_sentence_similarity(skill_sentences)


def generate_skill_sentences_similarity_dataframe(skill_sentences, ranked_skill_sentences, skill_names):
    """ Generate a dataframe from a given tuple of ranked skill sentences.

    Args:
        skill_sentences (Dict): Skill sentences.
        ranked_skill_sentences (List): Ranked list of skill sentences.
        skill_names (Dict): Mapping between skill anchor ID and skill name

    Returns:
        Dataframe of ranked skill sentences
    """

    # Add skill names to each pairwise combination.
    augmented_ranked_pairs = []
    skill_sentences_keys = list(skill_sentences.keys())
    skill_sentences_values = list(skill_sentences.values())
    for ranked_pair in ranked_skill_sentences:
        skill_1_anchor_id = skill_sentences_keys[skill_sentences_values.index(ranked_pair[0])]
        skill_2_anchor_id = skill_sentences_keys[skill_sentences_values.index(ranked_pair[1])]
        augmented_ranked_pairs.append((
            skill_names[skill_1_anchor_id], ranked_pair[0],
            skill_names[skill_2_anchor_id], ranked_pair[1],
            ranked_pair[2]))

    # Generate and return a dataframe of ranked skill sentences.
    ranked_skill_sentences_df = pd.DataFrame(
        augmented_ranked_pairs,
        columns=['skill_1_name', 'skill_1_sentence', 'skill_2_name', 'skill_2_sentence', 'similarity_score'])
    return ranked_skill_sentences_df


def write_skill_sentences_similarity_dataframes_to_file(
        base_working_dir, skill_name_description_sentences_ranked_df,
        skill_name_description_skill_level_sentences_ranked_df):
    """ Write the ranked skill sentence dataframes to file.

    Args:
        base_working_dir (string): Path to the base working directory.
        skill_name_description_sentences_ranked_df: Ranked skill name and description sentences.
        skill_name_description_skill_level_sentences_ranked_df: Ranked skill name, description and skill levels.

    """

    with pd.ExcelWriter(f'{base_working_dir}/{OUTPUT_RANKED_SKILLS_FILE_PATH}') as writer:
        skill_name_description_sentences_ranked_df.to_excel(
            writer, sheet_name="Names Descriptions", header=True, index=False)
        skill_name_description_skill_level_sentences_ranked_df.to_excel(
            writer, sheet_name="Names Descriptions Skill Levels", header=True, index=False)
