import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import matplotlib.pyplot as plt
import numpy as np
import time

st.set_page_config(page_title="Next Token Visualizer", layout="wide")

# -------------------------------------------------------
# Cached loader
# -------------------------------------------------------
@st.cache_resource
def load_model():
    tok = AutoTokenizer.from_pretrained("distilgpt2")
    tok.pad_token = tok.eos_token
    tok.padding_side = "left"
    model = AutoModelForCausalLM.from_pretrained("distilgpt2")
    model.config.pad_token_id = model.config.eos_token_id
    return tok, model

tok, model = load_model()

# -------------------------------------------------------
# Sidebar controls
# -------------------------------------------------------
st.sidebar.header("Decoding Settings")
decode_mode = st.sidebar.selectbox(
    "Decoding mode",
    ["Greedy", "Sampling"],
    help="Greedy: picks the single most likely next token.\nSampling: draws from probability distribution for diversity."
)
temperature = st.sidebar.slider(
    "Temperature", 0.1, 2.0, 0.8, 0.05,
    help="Controls randomness. Lower = deterministic, Higher = more creative."
)
top_p = st.sidebar.slider(
    "Top-p (nucleus)", 0.1, 1.0, 0.9, 0.05,
    help="Keeps smallest set of tokens whose cumulative probability ≤ p.\nHigher = more random."
)
top_k = st.sidebar.slider(
    "Top-k", 0, 100, 50, 1,
    help="Considers only the top-k most probable tokens during sampling.\n0 disables it."
)
sleep_time = st.sidebar.slider(
    "Delay between tokens (s)", 0.0, 1.0, 0.3, 0.05,
    help="Pause time between tokens when displaying generation."
)
max_new = st.sidebar.slider(
    "Max new tokens", 1, 60, 20,
    help="Maximum number of tokens to generate."
)

# -------------------------------------------------------
# Main UI
# -------------------------------------------------------
st.title("Next-Token Visualizer — distilgpt2")
st.markdown(
    "Visualize **tokenization**, **token IDs**, **next-token probabilities**, "
    "and **step-by-step generation** in GPT-style models."
)

text = st.text_input("Prompt", "The future of AI is").strip()
cols = st.columns(2)

# -------------------------------------------------------
# Tokenization grid
# -------------------------------------------------------
if text:
    tokens = tok.tokenize(text)
    ids = tok.encode(text)
    display_tokens = [t.replace("Ġ", "␣") for t in tokens]
    color_palette = ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#0081AF",
                     "#4392F1", "#BDBDBD", "#5EAAA8", "#E36414", "#4E8098"]

    html = "<div style='display:flex; flex-wrap:wrap; gap:6px;'>"
    for i, (t, idx) in enumerate(zip(display_tokens, ids)):
        color = color_palette[i % len(color_palette)]
        html += (
            f"<div style='background:{color}; color:white; padding:8px 10px; "
            f"border-radius:8px; font-family:monospace; font-size:16px;'>"
            f"{t}<br><span style='font-size:12px; color:#e0e0e0;'>{idx}</span></div>"
        )
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)
    st.code(f"Input IDs: {ids}", language="python")

# -------------------------------------------------------
# Column 1: next-token probabilities
# -------------------------------------------------------
with cols[0]:
    st.subheader("Top-10 Next-Token Probabilities")
    if st.button("Show next-token probabilities") and text:
        inputs = tok(text, return_tensors="pt", padding=True)
        with torch.no_grad():
            logits = model(**inputs).logits
        probs = torch.softmax(logits[0, -1], dim=-1)
        topk = torch.topk(probs, 10)
        words = [tok.decode(i) for i in topk.indices]
        vals = topk.values.detach().cpu().numpy()

        plt.rcParams.update({"font.size": 12, "figure.dpi": 150})
        fig, ax = plt.subplots(figsize=(5, 4), dpi=150)
        ax.barh(words[::-1], vals[::-1], color="#2E86AB")
        ax.set_xlabel("Probability")
        ax.set_title("Top-10 Next-Token Probabilities")
        ax.grid(alpha=0.3, linestyle="--")
        plt.tight_layout()
        st.pyplot(fig)

# -------------------------------------------------------
# Column 2: step-by-step generation
# -------------------------------------------------------
with cols[1]:
    st.subheader("Step-By-Step Generation")
    if st.button("Generate step-by-step") and text:
        st.write(f"Decoding: {decode_mode}")
        input_ids = tok.encode(text, return_tensors="pt")
        generated_text = text
        placeholder = st.empty()

        for _ in range(max_new):
            with torch.no_grad():
                logits = model(input_ids).logits[:, -1, :]

            if decode_mode == "Greedy":
                next_token = torch.argmax(logits, dim=-1)
            else:
                logits = logits / temperature
                probs = torch.softmax(logits, dim=-1)
                if top_k > 0:
                    probs, idxs = torch.topk(probs, k=top_k)
                    next_token_rel = torch.multinomial(probs, 1)
                    next_token = idxs[0, next_token_rel]       
                else:
                    next_token = torch.multinomial(probs, 1)

            next_str = tok.decode(next_token.item())
            generated_text += next_str
            placeholder.text(generated_text)
            next_token = next_token.view(1, -1) 
            input_ids = torch.cat([input_ids, next_token], dim=1)
            if next_str.strip() in [".", "!", "?", "\n"]:
                break
            time.sleep(sleep_time)

st.markdown("---")
