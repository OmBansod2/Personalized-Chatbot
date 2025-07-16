# app/utils/chatbot.py

# --- FAQ Retrieval Functions using SentenceTransformers ---
from sentence_transformers import SentenceTransformer, util
from app.models import QAPair

# Load a pretrained Sentence Transformer model (for FAQ retrieval)
qa_model = SentenceTransformer('all-MiniLM-L6-v2')
SIMILARITY_THRESHOLD = 0.3  # Adjust this threshold as needed

def load_qas():
    """
    Load enabled FAQ pairs from the database and compute embeddings.
    Returns: (questions, question_embeddings, qa_mapping)
    """
    qa_entries = QAPair.query.filter_by(is_enabled=True).all()
    questions = [entry.question for entry in qa_entries]
    qa_mapping = {entry.question: entry.answer for entry in qa_entries}
    question_embeddings = qa_model.encode(questions)
    return questions, question_embeddings, qa_mapping

def get_faq_reply(user_input, questions, question_embeddings, qa_mapping):
    """
    Computes cosine similarity between the user input and FAQ embeddings,
    and returns an answer if the best match exceeds the similarity threshold.
    """
    user_embedding = qa_model.encode(user_input)
    similarities = util.cos_sim(user_embedding, question_embeddings)[0]
    best_match_idx = similarities.argmax()
    if similarities[best_match_idx] >= SIMILARITY_THRESHOLD:
        return qa_mapping[questions[best_match_idx]]
    return None

# --- Fallback Conversational Model using DialoGPT ---
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load DialoGPT-small from Hugging Face
dialo_tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
dialo_model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

def get_general_reply(user_input):
    """
    Generate a response using DialoGPT.
    If the generated reply is empty or too generic (or nearly identical to the input),
    return a default message.
    """
    # Encode the input along with the EOS token.
    input_ids = dialo_tokenizer.encode(user_input + dialo_tokenizer.eos_token, return_tensors="pt")
    # Generate a response (single-turn conversation)
    chat_history_ids = dialo_model.generate(input_ids, max_length=100, pad_token_id=dialo_tokenizer.eos_token_id)
    reply = dialo_tokenizer.decode(chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
    if not reply.strip() or reply.strip().lower() == user_input.strip().lower():
        return "Sorry, I don't know."
    return reply

# --- Combined Hybrid Reply Function ---
def get_reply(user_input):
    """
    Hybrid approach:
      1. Attempt to retrieve an FAQ answer using SentenceTransformers.
      2. If no adequate match is found, fall back to generating a general conversational reply.
    """
    questions, question_embeddings, qa_mapping = load_qas()
    faq_reply = get_faq_reply(user_input, questions, question_embeddings, qa_mapping)
    if faq_reply is not None:
        return faq_reply
    else:
        return get_general_reply(user_input)
