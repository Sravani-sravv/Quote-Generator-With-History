import streamlit as st
import anthropic
import json
import os
from database import init_db, save_quote, get_all_quotes, delete_quote, toggle_like, clear_all_quotes
from dotenv import load_dotenv

load_dotenv()

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Quote Generator",
    page_icon="💬",
    layout="centered"
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
    .quote-box {
        background: #f8f9fa;
        border-left: 4px solid #4A90D9;
        border-radius: 8px;
        padding: 24px 28px;
        margin: 16px 0;
        font-size: 20px;
        font-style: italic;
        line-height: 1.7;
        color: #1a1a2e;
    }
    .author-text {
        text-align: right;
        font-size: 15px;
        color: #555;
        margin-top: 10px;
        font-weight: 500;
    }
    .history-card {
        background: #fff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }
    .badge {
        background: #e8f0fe;
        color: #1a73e8;
        font-size: 12px;
        padding: 3px 10px;
        border-radius: 99px;
        font-weight: 500;
    }
    .liked-badge {
        background: #fce4ec;
        color: #e91e63;
        font-size: 12px;
        padding: 3px 10px;
        border-radius: 99px;
    }
</style>
""", unsafe_allow_html=True)

# ── DB Init ───────────────────────────────────────────────────
init_db()

# ── Session state ─────────────────────────────────────────────
if "current_quote" not in st.session_state:
    st.session_state.current_quote = None
if "saved" not in st.session_state:
    st.session_state.saved = False

# ── Fetch quote from Anthropic ────────────────────────────────
def fetch_quote(category: str) -> dict:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("❌ ANTHROPIC_API_KEY not found in .env file.")
        return {}

    client = anthropic.Anthropic(api_key=api_key)

    prompt = (
        f"Generate one unique, meaningful {category} quote. "
        "Return ONLY a JSON object with keys: "
        '"text" (the quote), "author" (real person or "Unknown"), "category". '
        "No markdown fences, no explanation."
    )

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(raw)


# ── Header ────────────────────────────────────────────────────
st.title("💬 Quote Generator")
st.caption("AI-powered quotes saved to your personal history database")

# ── Tabs ──────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["✨ Generate", "📚 History"])

# ════════════════════════════════
# TAB 1 — GENERATE
# ════════════════════════════════
with tab1:
    CATEGORIES = [
        "Motivation", "Wisdom", "Stoicism", "Love",
        "Humor", "Science", "Success", "Philosophy"
    ]

    col1, col2 = st.columns([3, 1])
    with col1:
        category = st.selectbox("Select a category", CATEGORIES, label_visibility="collapsed")
    with col2:
        fetch_btn = st.button("🎲 New Quote", use_container_width=True, type="primary")

    # Fetch on button click
    if fetch_btn:
        with st.spinner("Fetching your quote..."):
            quote = fetch_quote(category)
            if quote:
                st.session_state.current_quote = quote
                st.session_state.saved = False

    # Display current quote
    q = st.session_state.current_quote
    if q:
        st.markdown(f"""
        <div class="quote-box">
            "{q.get('text', '')}"
            <div class="author-text">— {q.get('author', 'Unknown')}</div>
        </div>
        """, unsafe_allow_html=True)

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            save_label = "✅ Saved!" if st.session_state.saved else "💾 Save to History"
            if st.button(save_label, use_container_width=True, disabled=st.session_state.saved):
                save_quote(q["text"], q["author"], q["category"])
                st.session_state.saved = True
                st.success("Quote saved to history!")
                st.rerun()

        with col_b:
            if st.button("📋 Copy Quote", use_container_width=True):
                copy_text = f'"{q["text"]}" — {q["author"]}'
                st.code(copy_text, language=None)

        with col_c:
            st.markdown(f'<span class="badge">{q.get("category","")}</span>', unsafe_allow_html=True)

    else:
        st.info("👆 Pick a category and click **New Quote** to get started.")


# ════════════════════════════════
# TAB 2 — HISTORY
# ════════════════════════════════
with tab2:
    quotes = get_all_quotes()

    if not quotes:
        st.info("No quotes saved yet. Go to **Generate** and save some!")
    else:
        # Stats
        total = len(quotes)
        liked = sum(1 for q in quotes if q["liked"])
        cats  = len(set(q["category"] for q in quotes))

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Saved", total)
        c2.metric("Liked", liked)
        c3.metric("Categories", cats)

        st.divider()

        # Filters
        f1, f2 = st.columns(2)
        with f1:
            all_cats = ["All"] + sorted(set(q["category"] for q in quotes))
            cat_filter = st.selectbox("Filter by category", all_cats)
        with f2:
            liked_filter = st.selectbox("Filter by likes", ["All", "Liked only"])

        filtered = quotes
        if cat_filter != "All":
            filtered = [q for q in filtered if q["category"] == cat_filter]
        if liked_filter == "Liked only":
            filtered = [q for q in filtered if q["liked"]]

        st.caption(f"Showing {len(filtered)} of {total} quotes")

        # Clear all button
        if st.button("🗑️ Clear All History", type="secondary"):
            clear_all_quotes()
            st.success("History cleared.")
            st.rerun()

        st.divider()

        # Quote cards
        for q in filtered:
            with st.container():
                st.markdown(f"""
                <div class="history-card">
                    <p style="font-style:italic; font-size:16px; margin-bottom:8px;">"{q['text']}"</p>
                    <p style="color:#555; font-size:13px; margin-bottom:10px;">— {q['author']}</p>
                </div>
                """, unsafe_allow_html=True)

                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.caption(f"🗂 {q['category']}  ·  🕒 {q['saved_at'][:16].replace('T',' ')}")
                with col2:
                    like_label = "❤️ Unlike" if q["liked"] else "🤍 Like"
                    if st.button(like_label, key=f"like_{q['id']}"):
                        toggle_like(q["id"], not q["liked"])
                        st.rerun()
                with col3:
                    if st.button("🗑 Remove", key=f"del_{q['id']}"):
                        delete_quote(q["id"])
                        st.rerun()

                st.markdown("---")
