"""
Generate a deep-dive Word document explaining src/recommendation.py.

Line numbers and the signature map are extracted live from the source file with
`ast`, so the document stays correct if the code moves. The performance numbers
were measured on the real 53,527-article corpus (see MEASURED below) and the
behavioural notes in the Observations section were each confirmed by running the
engine, not inferred from reading.

Usage:
    python docs/generate_recommendation_docs.py

Output:
    docs/Recommendation_Engine_Explained.docx
"""
from __future__ import annotations

import ast
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor

from generate_documentation import (  # shared formatting helpers
    ACCENT,
    add_footer_page_numbers,
    add_table,
    bullet,
    callout,
    caption,
    code_block,
    h1,
    h2,
    h3,
    numbered,
    page_break,
    para,
    pct,
    setup_styles,
)

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
SOURCE = os.path.join(PROJECT_ROOT, "src", "recommendation.py")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
OUT_PATH = os.path.join(HERE, "Recommendation_Engine_Explained.docx")

# Timings measured on this machine against the full corpus (Python 3.11, CPU).
MEASURED = {
    "load_cache_s": 0.16,
    "history_rec_s": 0.122,
    "pref_rec_s": 0.224,
    "cosine_call_s": 0.107,
}


# ===================================================================== #
# Live source introspection
# ===================================================================== #
def read_source() -> tuple[str, list[str]]:
    with open(SOURCE, "r", encoding="utf-8") as f:
        text = f.read()
    return text, text.splitlines()


def build_symbol_map(source_text: str) -> dict[str, dict]:
    """name -> {lineno, end_lineno, args, kind} for every function and method."""
    tree = ast.parse(source_text)
    out: dict[str, dict] = {}

    def record(node, name, kind):
        args = [a.arg for a in node.args.args if a.arg != "self"]
        out[name] = {
            "lineno": node.lineno,
            "end_lineno": getattr(node, "end_lineno", node.lineno),
            "lines": getattr(node, "end_lineno", node.lineno) - node.lineno + 1,
            "args": args,
            "kind": kind,
        }

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            record(node, node.name, "module function")
        elif isinstance(node, ast.ClassDef):
            for sub in node.body:
                if isinstance(sub, ast.FunctionDef):
                    record(sub, sub.name, "method")
    return out


def load_facts() -> dict:
    facts = {"emb_rows": 53527, "emb_dim": 384, "articles": 53527}
    try:
        import numpy as np

        emb = np.load(os.path.join(DATA_DIR, "embeddings.npy"), mmap_mode="r")
        facts["emb_rows"], facts["emb_dim"] = int(emb.shape[0]), int(emb.shape[1])
        facts["emb_mb"] = round(os.path.getsize(os.path.join(DATA_DIR, "embeddings.npy"))
                                / (1024 * 1024), 1)
    except Exception:
        facts["emb_mb"] = 78.4
    try:
        report_path = os.path.join(DATA_DIR, "evaluation_report.json")
        with open(report_path, "r", encoding="utf-8") as f:
            facts["report"] = json.load(f)
    except Exception:
        facts["report"] = {}
    return facts


def snippet(lines: list[str], start: int, end: int, dedent: int = 0) -> str:
    """Extract source lines start..end (1-indexed, inclusive) for a code block."""
    chunk = lines[start - 1:end]
    if dedent:
        chunk = [c[dedent:] if len(c) > dedent and c[:dedent].isspace() else c.lstrip()
                 for c in chunk]
    return "\n".join(chunk)


def sig(sym: dict, name: str, arg_names: bool = True) -> str:
    m = sym[name]
    if arg_names:
        return f"{name}({', '.join(m['args'])})"
    return name


def lref(sym: dict, name: str) -> str:
    m = sym[name]
    return f"lines {m['lineno']}-{m['end_lineno']}"


# ===================================================================== #
# Document sections
# ===================================================================== #
def cover(doc, f, sym, lines):
    for _ in range(4):
        doc.add_paragraph()
    para(doc, "MODULE DEEP DIVE", bold=True, size=11,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("src/recommendation.py")
    run.bold = True
    run.font.size = Pt(26)
    run.font.name = "Consolas"
    run.font.color.rgb = ACCENT
    para(doc, "The Recommendation Engine\nHow it works, why it is built this way,\n"
              "and how to explain it",
         italic=True, size=11.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    doc.add_paragraph()

    add_table(
        doc,
        ["Item", "Detail"],
        [
            ["File", "src/recommendation.py"],
            ["Total lines", f"{len(lines)}"],
            ["Public class", "RecommendationEngine"],
            ["Module-level function", "_cosine_similarity_matrix"],
            ["Methods", f"{sum(1 for v in sym.values() if v['kind'] == 'method')}"],
            ["Role in the project", "Pipeline stage 4 (builds embeddings.npy) AND the entire "
                                    "online serving path behind the API"],
            ["Primary backend", "Sentence-Transformer all-MiniLM-L6-v2 "
                                f"({f['emb_dim']}-dimension vectors)"],
            ["Fallback backend", "TF-IDF + TruncatedSVD, same dimension"],
            ["Artifact produced", f"data/embeddings.npy - {f['emb_rows']:,} x {f['emb_dim']} "
                                  f"float32, {f.get('emb_mb', 78.4)} MB"],
            ["Consumed by", "app/api.py, app/dashboard.py (via the API), evaluate.py, main.py"],
            ["Depends on", "numpy, pandas, config; sentence-transformers/torch and scikit-learn "
                           "imported lazily"],
        ],
        widths=[1.7, 4.6],
        font_size=10,
    )
    caption(doc, "Table 1: Module fact sheet. Line counts and the method count are extracted "
                 "from the source with Python's ast module when this document is generated.")
    page_break(doc)


def section_1_big_picture(doc, f, sym):
    h1(doc, "1. What This File Does, In One Paragraph")
    para(doc,
         "recommendation.py answers one question: given what a reader likes, which articles "
         "should we show them? It does this in three moves. First it turns every article into a "
         f"list of {f['emb_dim']} numbers that encodes what the article is about. Second it turns "
         "the reader into a single list of the same shape, by averaging the articles they have "
         "read. Third it measures the angle between the reader's vector and every article vector, "
         "and returns the closest ones. Everything else in the file exists to make those three "
         "moves fast, reliable and reusable.")

    h2(doc, "1.1 Two jobs in one file")
    add_table(
        doc,
        ["Job", "When it runs", "What it costs", "What it produces"],
        [
            ["Build the embeddings",
             "Once, during the offline pipeline (main.py stage 4)",
             "Minutes. A transformer must read all "
             f"{f['emb_rows']:,} articles.",
             f"data/embeddings.npy, a {f['emb_rows']:,} x {f['emb_dim']} float32 matrix"],
            ["Serve recommendations",
             "On every API request",
             f"About {MEASURED['history_rec_s'] * 1000:.0f} ms. Pure NumPy arithmetic on an "
             "already-loaded matrix.",
             "A ranked list of article dictionaries"],
        ],
        widths=[1.3, 1.75, 1.75, 1.5],
    )
    caption(doc, "Table 2: The expensive job runs once and is cached; the cheap job runs "
                 "thousands of times. Understanding this split is the key to understanding the "
                 "whole file.")

    callout(doc, "The single most important idea:",
            "The transformer is never invoked while serving a request. It ran once, its output "
            "was saved to disk, and the API just does matrix arithmetic on that saved output. "
            "This is why a recommendation takes milliseconds instead of seconds.")

    h2(doc, "1.2 Structure at a glance")
    code_block(doc,
        "recommendation.py\n"
        "|\n"
        "+-- _cosine_similarity_matrix(profile, matrix)     <- the maths, one function\n"
        "|\n"
        "+-- class RecommendationEngine\n"
        "    |\n"
        "    +-- __init__                     load light columns, validate paths\n"
        "    |\n"
        "    +-- EMBEDDINGS\n"
        "    |   +-- _corpus                  build 'title. body' strings (lazy read)\n"
        "    |   +-- _encode_sentence_transformer   primary backend\n"
        "    |   +-- _encode_tfidf            fallback backend\n"
        "    |   +-- generate_embeddings      cache / validate / build / save\n"
        "    |   +-- _ensure_embeddings       lazy trigger used by every public method\n"
        "    |\n"
        "    +-- PAYLOAD HELPERS\n"
        "    |   +-- _short_description       trim to 300 chars\n"
        "    |   +-- _article_payload         build one result dictionary\n"
        "    |\n"
        "    +-- RECOMMENDATION\n"
        "    |   +-- get_top_n_recommendations      returning reader (has history)\n"
        "    |   +-- recommend_for_preferences      new reader (no history)\n"
        "    |\n"
        "    +-- ANALYTICS\n"
        "        +-- category_counts\n"
        "        +-- analytics_summary\n")
    caption(doc, "Figure 1: The file is organised in five bands. Private helpers are prefixed "
                 "with an underscore; the four public entry points are generate_embeddings, "
                 "get_top_n_recommendations, recommend_for_preferences and analytics_summary.")


def section_2_map(doc, f, sym):
    h1(doc, "2. Signature Map")
    para(doc, "Every function in the file, in source order, with its exact location. Use this as "
              "the index when walking through the code on screen.", italic=True, size=9.5)

    descriptions = {
        "_cosine_similarity_matrix":
            "Cosine similarity between one profile vector and every row of the embedding matrix.",
        "__init__":
            "Validate the processed CSV exists, load only the light serving columns, "
            "initialise empty embedding state.",
        "_corpus":
            "Build the list of 'title. body' strings to encode. Reads the heavy text column "
            "lazily, only when needed.",
        "_encode_sentence_transformer":
            "Primary backend. Encode the corpus with all-MiniLM-L6-v2. Returns None on any "
            "failure so the caller can fall back.",
        "_encode_tfidf":
            "Fallback backend. TF-IDF then TruncatedSVD down to the same dimension.",
        "generate_embeddings":
            "The cache manager. Load from disk if valid, otherwise build, then save.",
        "_ensure_embeddings":
            "Lazy guard. Called by every method that needs vectors, so the caller never has to "
            "remember to build them.",
        "_short_description":
            "Trim an article description to 300 characters with an ellipsis.",
        "_article_payload":
            "Assemble one result dictionary: title, sentiment, category, url, description.",
        "get_top_n_recommendations":
            "MAIN PATH. Mean-pool a reading history into a profile, rank all articles by cosine "
            "similarity, drop already-read, return top-N.",
        "category_counts":
            "Category name to article count, sorted descending. Feeds the new-user form.",
        "recommend_for_preferences":
            "COLD-START PATH. Score articles by a weighted blend of topical similarity and "
            "sentiment match for a reader with no history.",
        "analytics_summary":
            "Corpus-level aggregates: totals, sentiment mix, top categories, and a "
            "category-by-sentiment cross-tab.",
    }

    def visibility(name: str) -> str:
        if name == "__init__":
            return "constructor"
        return "internal" if name.startswith("_") else "public"

    rows = []
    for name in sorted(sym, key=lambda k: sym[k]["lineno"]):
        m = sym[name]
        rows.append([
            name,
            f"{m['lineno']}-{m['end_lineno']}",
            str(m["lines"]),
            visibility(name),
            descriptions.get(name, ""),
        ])
    add_table(
        doc,
        ["Function", "Lines", "Len", "Visibility", "What it does"],
        rows,
        widths=[1.6, 0.7, 0.4, 0.75, 2.85],
        font_size=8.5,
    )
    caption(doc, "Table 3: Complete signature map, extracted with ast at generation time.")


def section_3_maths(doc, f, sym, lines):
    h1(doc, "3. The Mathematics, Explained Plainly")
    para(doc, "Three ideas carry the whole engine. None of them require advanced maths to "
              "explain, and being able to explain them clearly is most of what a reviewer wants "
              "to hear.")

    h2(doc, "3.1 Idea one: an embedding is a meaning-coordinate")
    para(doc,
         f"An embedding turns text into a point in {f['emb_dim']}-dimensional space. The model "
         "was trained so that texts with similar meaning land close together. That is the whole "
         "trick: once meaning becomes geometry, 'find me similar articles' becomes 'find me "
         "nearby points', and nearby points can be found with arithmetic.")
    para(doc,
         "Why this beats keyword matching: the headlines \"Share market slumps on rate fears\" "
         "and \"Equities tumble as interest worries mount\" have almost no words in common. A "
         "keyword system scores them as unrelated. An embedding model places them close together "
         "because it was trained on meaning, not spelling.")

    h2(doc, "3.2 Idea two: cosine similarity compares direction, not size")
    code_block(doc, snippet(lines, sym["_cosine_similarity_matrix"]["lineno"],
                            sym["_cosine_similarity_matrix"]["end_lineno"]))
    para(doc, f"({lref(sym, '_cosine_similarity_matrix')})", italic=True, size=8.5)
    numbered(doc, "Both inputs are cast to float32 so the arithmetic is done in one consistent, "
                  "memory-light precision.")
    numbered(doc, "p_norm is the length of the profile vector. m_norm is a vector holding the "
                  f"length of each of the {f['emb_rows']:,} article vectors (axis=1 means "
                  "row-wise).")
    numbered(doc, "The tiny 1e-10 added to each norm is a divide-by-zero guard. An all-zero "
                  "vector, which can happen in the TF-IDF fallback for an article of pure "
                  "stop-words, would otherwise produce NaN and poison the entire ranking.")
    numbered(doc, "matrix @ profile is one matrix-vector product: it computes the dot product of "
                  f"the profile against all {f['emb_rows']:,} articles in a single BLAS call.")
    numbered(doc, "Dividing by the product of the lengths converts those dot products into "
                  "cosines, each in the range [-1, 1].")

    add_table(
        doc,
        ["Cosine value", "Geometric meaning", "In this system"],
        [
            ["+1.0", "Vectors point the same way (0 degrees)", "Same topic and framing"],
            ["around +0.6", "Small angle", "Typical top recommendation "
                                           f"(the measured best score was 0.61)"],
            ["0.0", "Perpendicular (90 degrees)", "Unrelated topics"],
            ["-1.0", "Opposite directions (180 degrees)", "Effectively never seen in practice "
                                                          "with sentence embeddings"],
        ],
        widths=[1.1, 2.2, 3.0],
    )
    caption(doc, "Table 4: How to read a cosine score.")

    callout(doc, "Why cosine and not Euclidean distance:",
            "Cosine ignores vector length. A 2,000-word investigation and a 200-word news brief "
            "on the same subject point in the same direction but have different magnitudes. "
            "Euclidean distance would call them dissimilar because one vector is longer; cosine "
            "correctly calls them similar. Length is a proxy for verbosity, not for topic, so we "
            "deliberately discard it.")

    h2(doc, "3.3 Idea three: mean pooling makes a reader look like an article")
    code_block(doc,
        "history = [412, 3987, 20114]                # three articles the reader consumed\n"
        f"vectors = embeddings[history]               # shape (3, {f['emb_dim']})\n"
        f"profile = vectors.mean(axis=0)              # shape ({f['emb_dim']},)\n"
        "\n"
        "# axis=0 means 'average down the columns':\n"
        "#   dimension 0 of the profile = mean of dimension 0 across the 3 articles\n"
        "#   dimension 1 of the profile = mean of dimension 1 across the 3 articles\n"
        "#   ... and so on for all "
        f"{f['emb_dim']} dimensions")
    para(doc,
         "The average of several points is their centre. So the profile is literally the centre "
         "of the reader's interests, expressed in the same coordinate system as the articles. "
         "That last part is what makes it useful: because the profile lives in article space, a "
         "single cosine call can rank the entire catalogue against it.")
    bullet(doc, "Why mean pooling and not something learned: It needs no training, it updates "
                "the instant a reader's history changes, and it costs one averaging operation. "
                "For a content-based recommender it is the standard, and the simplest thing that "
                "genuinely works.")
    bullet(doc, "Its honest weakness: A reader interested in both cricket and monetary policy "
                "gets a profile sitting midway between the two, which may be near neither. "
                "Clustering the history into several profiles would address this; it is listed "
                "in the improvements section.")


def section_4_init(doc, f, sym, lines):
    h1(doc, "4. Walkthrough: Construction")
    h2(doc, f"4.1 __init__ ({lref(sym, '__init__')})")
    code_block(doc, snippet(lines, sym["__init__"]["lineno"], sym["__init__"]["end_lineno"], 4))

    h3(doc, "What happens, step by step")
    numbered(doc, "Defaults for all three arguments come from config.py, so the engine can be "
                  "constructed with no arguments at all. api.py does exactly that: "
                  "RecommendationEngine().")
    numbered(doc, "It checks processed_news.csv exists and, if not, raises FileNotFoundError "
                  "with an actionable message telling the user to run main.py. Failing early "
                  "with a clear instruction beats a confusing pandas error thirty lines later.")
    numbered(doc, "pd.read_csv(processed_path, nrows=0) reads the header row only, to discover "
                  "which columns are actually present.")
    numbered(doc, "It intersects that header with the five light serving columns (title, "
                  "category, url, description, sentiment) and loads only those.")
    numbered(doc, "If a sentiment column is absent it synthesises one filled with 'Neutral', so "
                  "downstream code can always assume the column exists.")
    numbered(doc, "self.embeddings and self.backend are initialised to None. Nothing heavy is "
                  "loaded in the constructor.")

    h3(doc, "The decisions worth explaining")
    bullet(doc, "Why read the header first: The three CSVs in archive/ have different schemas. "
                "Probing the header and taking the intersection means the engine cannot crash "
                "with a 'usecols do not match columns' error on a slightly different file.")
    bullet(doc, "Why exclude the text column: This is the most consequential line in the "
                "constructor. processed_news.csv is 326 MB, and almost all of that is article "
                "bodies. The serving path never displays the body, only the description. "
                "Skipping it keeps the API process small. The body is read exactly once, inside "
                "_corpus, and only when embeddings genuinely have to be rebuilt.")
    bullet(doc, "Why the constructor stays cheap: Loading embeddings here would make every "
                "import slow and would make the class hard to test. Instead, api.py explicitly "
                "calls generate_embeddings() once at startup, and _ensure_embeddings covers "
                "anyone who forgets.")
    bullet(doc, "Why the sentiment default matters: recommend_for_preferences compares "
                "df['sentiment'] against a preferred value. Without the synthesised column that "
                "comparison would raise a KeyError instead of simply matching nothing.")

    callout(doc, "Row index is the article ID:",
            "There is no separate identifier column. An article's position in the DataFrame is "
            "its ID, and the same position in embeddings.npy holds its vector. This is why the "
            "API takes history_indices as plain integers, and it is why the row-count check in "
            "generate_embeddings matters so much: if the two ever fall out of alignment, every "
            "recommendation would silently point at the wrong article.")


def section_5_embeddings(doc, f, sym, lines):
    h1(doc, "5. Walkthrough: Building the Embeddings")
    para(doc, "Four methods cooperate here. generate_embeddings is the coordinator; the other "
              "three do the work.")

    h2(doc, f"5.1 _corpus ({lref(sym, '_corpus')})")
    code_block(doc, snippet(lines, sym["_corpus"]["lineno"], sym["_corpus"]["end_lineno"], 4))
    bullet(doc, "What it builds: One string per article of the form 'Title. Body text...'.")
    bullet(doc, "Why the title is prepended: A headline is the densest summary an article has. "
                "Including it puts high-signal words into the vector rather than relying on the "
                "body alone.")
    bullet(doc, "Why the body column is read here and nowhere else: This is the lazy load "
                "promised in the constructor. The 326 MB read happens only on the rebuild path.")
    bullet(doc, "Why reset_index(drop=True) on both series: pandas aligns on index when you add "
                "two Series. If the indices differed even slightly, the concatenation would "
                "produce NaN rows rather than an error. Resetting both to a clean 0..n-1 range "
                "guarantees positional pairing.")
    bullet(doc, "Why .astype(str): A missing value would otherwise be a float NaN, and adding a "
                "float to a string raises. Casting makes the operation total.")

    h2(doc, f"5.2 _encode_sentence_transformer ({lref(sym, '_encode_sentence_transformer')})")
    code_block(doc, snippet(lines, sym["_encode_sentence_transformer"]["lineno"],
                            sym["_encode_sentence_transformer"]["end_lineno"], 4))
    bullet(doc, "Two separate try blocks, on purpose: The first catches an ImportError, meaning "
                "the library is not installed. The second catches a runtime failure, meaning the "
                "library is present but the model could not be downloaded or loaded. The second "
                "case prints a diagnostic because it is the surprising one; the first is a known "
                "configuration and stays quiet.")
    bullet(doc, "Why the import is inside the function: sentence-transformers pulls in torch, "
                "which is slow and heavy to import. Keeping the import local means a run that "
                "loads cached embeddings never pays that cost. This is measurable: cache loading "
                f"takes about {MEASURED['load_cache_s']:.2f} s in total.")
    bullet(doc, "Why return None instead of raising: None is the signal to the coordinator that "
                "it should try the fallback. An exception would abort the pipeline; None degrades "
                "it.")
    bullet(doc, "batch_size=64: Articles are encoded 64 at a time. Larger batches use the CPU or "
                "GPU more efficiently; too large and memory becomes the constraint. 64 is a safe "
                "middle for a laptop.")
    bullet(doc, "show_progress_bar=True: This is a multi-minute operation. Visible progress is "
                "the difference between a user waiting and a user assuming it has hung.")
    bullet(doc, "Why cast to float32: The model emits float32 already, but the cast makes the "
                "contract explicit and guarantees the saved file is "
                f"{f.get('emb_mb', 78.4)} MB rather than double that.")

    h2(doc, f"5.3 _encode_tfidf ({lref(sym, '_encode_tfidf')})")
    code_block(doc, snippet(lines, sym["_encode_tfidf"]["lineno"],
                            sym["_encode_tfidf"]["end_lineno"], 4))
    para(doc, "The fallback produces vectors of the same shape by a completely different route: "
              "count-based features, then dimensionality reduction.")
    numbered(doc, "TfidfVectorizer turns the corpus into a large sparse matrix where each column "
                  "is a word, weighted so that distinctive words count more than ubiquitous ones.")
    numbered(doc, "max_features=20000 keeps only the 20,000 most frequent terms. Without a cap, "
                  "a corpus this size produces hundreds of thousands of columns and the SVD "
                  "becomes impractical.")
    numbered(doc, "stop_words='english' removes 'the', 'and', 'of' and similar, which carry no "
                  "topical signal.")
    numbered(doc, "TruncatedSVD projects that sparse matrix down to a dense one. This technique "
                  "is Latent Semantic Analysis: the reduced dimensions capture co-occurrence "
                  "patterns, which is a crude approximation of meaning.")
    numbered(doc, "The three-way clamp on dim is a robustness guard. SVD requires n_components "
                  "to be strictly less than both the number of features and the number of "
                  "documents. On the full corpus dim is simply "
                  f"{f['emb_dim']}; on a tiny test run of five articles it collapses safely to a "
                  "valid small number, and max(dim, 2) stops it reaching zero.")
    numbered(doc, "random_state=config.RANDOM_SEED makes the SVD deterministic, so the fallback "
                  "is as reproducible as the primary path.")
    bullet(doc, "Why match the primary dimension exactly: Nothing downstream needs to know which "
                "backend ran. Cosine similarity, mean pooling, the API schema and the cached file "
                "format are all identical either way. The fallback is a drop-in substitute, not "
                "a special case.")
    bullet(doc, "Honest note on quality: TF-IDF plus SVD still relies on shared vocabulary. It "
                "recovers some synonym structure through co-occurrence but is clearly weaker than "
                "the transformer. It exists so the pipeline always completes, not because it is "
                "equivalent.")

    h2(doc, f"5.4 generate_embeddings ({lref(sym, 'generate_embeddings')})")
    code_block(doc, snippet(lines, sym["generate_embeddings"]["lineno"],
                            sym["generate_embeddings"]["end_lineno"], 4))
    h3(doc, "The decision tree")
    code_block(doc,
        "force=True ?  ------------------------ yes --> rebuild\n"
        "     | no\n"
        "cache file exists ? ------------------ no  --> rebuild\n"
        "     | yes\n"
        "cache rows == len(df) ? -------------- no  --> print 'stale', rebuild\n"
        "     | yes\n"
        "     +--> load from disk, backend = 'cache', return\n"
        "\n"
        "rebuild:  _corpus()\n"
        "          -> _encode_sentence_transformer()   (primary)\n"
        "          -> if None: _encode_tfidf()          (fallback)\n"
        "          -> ensure_data_dir(), np.save(), return")
    bullet(doc, "Why the row-count check is essential: The row index is the article ID. If the "
                "corpus is re-cleaned and ends up with a different number of articles, a stale "
                "cache would map every index to the wrong article and produce confident, "
                "completely wrong recommendations. Silent wrongness is worse than a visible "
                "error, so the engine detects the mismatch and rebuilds.")
    bullet(doc, "Why config.ensure_data_dir() before saving: np.save will not create a missing "
                "directory. On a fresh clone this one call is the difference between success and "
                "an IOError.")
    bullet(doc, "Why every branch prints: This runs unattended in the pipeline. The log lines "
                "are how anyone later determines whether vectors were built or loaded, which "
                "backend ran, and what shape resulted.")
    bullet(doc, "Why it returns the array as well as storing it on self: Callers such as main.py "
                "can use the return value directly, while the API relies on the stored state. "
                "Both styles work.")

    h2(doc, f"5.5 _ensure_embeddings ({lref(sym, '_ensure_embeddings')})")
    code_block(doc, snippet(lines, sym["_ensure_embeddings"]["lineno"],
                            sym["_ensure_embeddings"]["end_lineno"], 4))
    para(doc, "Three lines, and they remove an entire class of bug. Every method that needs "
              "vectors calls this first, so no caller can ever operate on None. It also means "
              "the engine is usable straight from a Python prompt without reading the "
              "documentation first.")


def section_6_helpers(doc, f, sym, lines):
    h1(doc, "6. Walkthrough: Result Payload Helpers")
    para(doc, "Both recommendation methods return lists of dictionaries with an identical shape. "
              "These two helpers guarantee that consistency, which is what allows a single "
              "Pydantic response model in api.py to validate both endpoints.")

    h2(doc, f"6.1 _short_description ({lref(sym, '_short_description')})")
    code_block(doc, snippet(lines, sym["_short_description"]["lineno"],
                            sym["_short_description"]["end_lineno"], 4))
    bullet(doc, "Why truncate at 300 characters: The dashboard shows a preview card. An untrimmed "
                "body would break the layout and would bloat every API response.")
    bullet(doc, "Why the ellipsis is conditional: A description of exactly 200 characters is "
                "complete and should not be given a misleading '...'. The suffix appears only "
                "when content was actually cut.")
    bullet(doc, "Why the isinstance check: A missing description arrives from pandas as a float "
                "NaN, not a string. Calling .strip() on that would raise, so the type is checked "
                "before it is trusted.")

    h2(doc, f"6.2 _article_payload ({lref(sym, '_article_payload')})")
    code_block(doc, snippet(lines, sym["_article_payload"]["lineno"],
                            sym["_article_payload"]["end_lineno"], 4))
    bullet(doc, "Single source of truth for result shape: Five keys, always the same, always in "
                "the same order. The scoring methods then add their own extra keys on top.")
    bullet(doc, "Why the url gets special handling: A missing URL read from CSV can become the "
                "literal string 'nan'. Rendering that as a hyperlink gives the reader a broken "
                "link. The check converts it to an empty string, which the dashboard can then "
                "correctly choose not to render.")
    bullet(doc, "Why row.get with defaults rather than row[...]: The constructor only guarantees "
                "title and sentiment. Using .get with 'General' and 'Neutral' defaults means a "
                "CSV without a category column degrades gracefully instead of raising.")
    bullet(doc, "Why everything is cast with str(): The API response model declares these fields "
                "as strings. Casting here means Pydantic never has to reject a numpy or NaN "
                "value at the boundary.")


def section_7_history(doc, f, sym, lines):
    h1(doc, "7. Walkthrough: Recommending to a Returning Reader")
    h2(doc, f"7.1 get_top_n_recommendations ({lref(sym, 'get_top_n_recommendations')})")
    para(doc, "This is the method behind POST /recommend/ and the one to walk through first when "
              "explaining the system.")
    code_block(doc, snippet(lines, sym["get_top_n_recommendations"]["lineno"],
                            sym["get_top_n_recommendations"]["end_lineno"], 4))

    h3(doc, "Step by step")
    numbered(doc, "_ensure_embeddings() guarantees the matrix is loaded.")
    numbered(doc, "The history is filtered to indices that are genuinely integers and genuinely "
                  "in range. A stale bookmark pointing at article 99,999 in a corpus of "
                  f"{f['emb_rows']:,} is dropped rather than raising IndexError.")
    numbered(doc, "If nothing survives the filter, the method returns the first top_n articles "
                  "as a cold-start fallback instead of failing.")
    numbered(doc, "embeddings[valid].mean(axis=0) mean-pools the surviving history into one "
                  "profile vector. Fancy indexing with a list of positions gathers exactly those "
                  "rows.")
    numbered(doc, f"One cosine call scores the profile against all {f['emb_rows']:,} articles.")
    numbered(doc, "np.argsort(-scores) sorts descending. Negating the scores is the idiomatic "
                  "way to get a descending order from a function that only sorts ascending; it "
                  "returns positions, not values, which is exactly what we need since positions "
                  "are article IDs.")
    numbered(doc, "The loop walks that ranking from the top, skipping anything in the seen set, "
                  "and stops as soon as top_n results are collected.")
    numbered(doc, "Each surviving article gets the standard payload plus a score rounded to four "
                  "decimals.")

    h3(doc, "The decisions worth explaining")
    bullet(doc, "Why already-read articles are excluded: An article the reader has consumed is "
                "the single closest point to their own profile, because it is one of the points "
                "the profile was averaged from. Without the seen filter the top results would be "
                "the reader's own history handed back to them.")
    bullet(doc, "Why a set for seen: Membership testing is constant time. Using a list would "
                "make the loop quadratic in history length. Small here, but it is free to do "
                "correctly.")
    bullet(doc, "Why break early instead of building the whole list: The loop stops after top_n "
                "results, so it typically touches only a handful of the "
                f"{f['emb_rows']:,} ranked entries.")
    bullet(doc, "Why round to four decimals: The raw float carries seventeen digits of noise. "
                "Four is more precision than any consumer needs and keeps the JSON compact.")
    bullet(doc, "Why the cold-start branch returns something rather than erroring: This method "
                "sits directly behind an HTTP endpoint. A brand-new reader with an empty history "
                "should see a page of articles, not a 500.")

    h3(doc, "Measured behaviour on the real corpus")
    add_table(
        doc,
        ["Call", "Measured time", "Note"],
        [
            ["Load cached embeddings", f"{MEASURED['load_cache_s']:.2f} s",
             f"{f.get('emb_mb', 78.4)} MB read from disk, once at API startup"],
            ["One cosine similarity call", f"{MEASURED['cosine_call_s'] * 1000:.0f} ms",
             f"Dominates the request. See Observation 3 in Section 11."],
            ["get_top_n_recommendations", f"{MEASURED['history_rec_s'] * 1000:.0f} ms",
             "Full request path: pool, score, sort, build 5 payloads"],
            ["recommend_for_preferences", f"{MEASURED['pref_rec_s'] * 1000:.0f} ms",
             "Higher because it also builds a category mask and a topical profile"],
        ],
        widths=[1.85, 1.1, 3.35],
    )
    caption(doc, "Table 5: Timings measured directly against the "
                 f"{f['emb_rows']:,}-article corpus on the development machine, not estimated.")

    h3(doc, "Worked example")
    code_block(doc,
        "history_indices = [412, 3987, 20114]\n"
        "\n"
        f"valid    = [412, 3987, 20114]                  # all three in range 0..{f['emb_rows'] - 1}\n"
        f"profile  = mean of 3 vectors        -> shape ({f['emb_dim']},)\n"
        f"scores   = cosine(profile, all)     -> shape ({f['emb_rows']},)\n"
        "order    = argsort(-scores)          -> [20114, 412, 8871, 3987, 41002, ...]\n"
        "                                        (the reader's own articles rank highest)\n"
        "seen     = {412, 3987, 20114}\n"
        "\n"
        "walk order, skip seen:\n"
        "  20114 -> skip (seen)\n"
        "  412   -> skip (seen)\n"
        "  8871  -> KEEP, score 0.6105\n"
        "  3987  -> skip (seen)\n"
        "  41002 -> KEEP, score 0.6042\n"
        "  ...   -> until 5 collected, lowest kept score 0.5897")
    para(doc, "The scores in this example are the real values returned by the engine for that "
              "history. Note how tightly they cluster: 0.6105 down to 0.5897 across five results. "
              "That narrow band is normal for sentence embeddings and is exactly why the "
              "dashboard converts the score to a friendly percentage rather than showing readers "
              "the raw number.", italic=True, size=9.5)


def section_8_coldstart(doc, f, sym, lines):
    h1(doc, "8. Walkthrough: Recommending to a Brand-New Reader")
    h2(doc, f"8.1 recommend_for_preferences ({lref(sym, 'recommend_for_preferences')})")
    para(doc,
         "The cold-start problem: a new reader has no history, so there is nothing to mean-pool. "
         "The solution here is to ask them instead. They pick topics and a preferred tone, and "
         "those declarations stand in for behaviour.")
    code_block(doc, snippet(lines, sym["recommend_for_preferences"]["lineno"],
                            sym["recommend_for_preferences"]["end_lineno"], 4))

    h2(doc, "8.2 The scoring formula, decomposed")
    code_block(doc,
        "STEP 1  topical profile\n"
        "        idx      = rows whose category is one of the chosen ones\n"
        "        profile  = embeddings[idx].mean(axis=0)\n"
        "        (if no categories chosen: profile = mean of the WHOLE corpus)\n"
        "\n"
        "STEP 2  topical similarity, rescaled\n"
        "        sim      = cosine(profile, embeddings)        range [-1, 1]\n"
        "        sim_norm = (sim + 1) / 2                      range [ 0, 1]\n"
        "\n"
        "STEP 3  sentiment component\n"
        "        specific mood : sent_match = 1.0 if article sentiment matches else 0.0\n"
        "        'Any'         : sent_match = 0.5 everywhere  (deliberately neutral)\n"
        "\n"
        "STEP 4  weighted blend\n"
        "        final = (wf * sim_norm + ws * sent_match) / (wf + ws)\n"
        "        (if wf + ws == 0: final = sim_norm, i.e. pure topical match)\n"
        "\n"
        "STEP 5  exact-category nudge\n"
        "        final = final + 0.05 * cat_match")

    h3(doc, "Why each step is built that way")
    bullet(doc, "Why sim is rescaled to [0,1]: This is the step people miss when explaining the "
                "formula. Cosine spans [-1, 1] while sent_match is 0 or 1. Blending them on "
                "different scales would mean the weights do not do what they claim: a weight of "
                "0.7 on a quantity that can go negative is not comparable to 0.7 on a quantity "
                "that cannot. Rescaling puts both components on the same footing so the weights "
                "become honest.")
    bullet(doc, "Why dividing by (wf + ws): It normalises the blend so the result stays within "
                "[0, 1] regardless of the absolute size of the weights. Only their ratio "
                "matters, so a caller passing 7 and 3 gets the same ranking as 0.7 and 0.3.")
    bullet(doc, "Why 'Any' maps to a flat 0.5 rather than to zero: A constant adds the same "
                "amount to every article, so it changes no rankings. Zero would also be "
                "rank-neutral but would drag every score down and make the numbers look worse "
                "than they are. 0.5 keeps the scale meaningful. In practice the dashboard also "
                "sends sentiment_weight=0.0 for 'Any', which removes the term entirely.")
    bullet(doc, "Why the 0.05 category bonus, and why it is small: Two articles can be almost "
                "equally similar to the topical profile while only one is literally tagged with "
                "a chosen category. The bonus breaks that tie in favour of the explicit match. "
                "It is kept small on purpose: large enough to order near-ties, too small to "
                "promote a genuinely irrelevant article just because of its label. Semantic "
                "relevance stays in charge.")
    bullet(doc, "Why the bonus is added after normalisation: It means the maximum achievable "
                "score is 1.05, not 1.0. Worth knowing if you ever present the score as a "
                "percentage; the dashboard's conversion should be understood with that ceiling "
                "in mind.")
    bullet(doc, "Why fall back to the corpus mean when no category is chosen: The mean of "
                "everything is the centre of the whole corpus, so similarity to it ranks "
                "articles by how typical they are. It is a bland but safe ordering, and it means "
                "an empty selection returns results rather than an error.")
    bullet(doc, "Why exclude_indices exists: It lets a caller paginate or suppress articles "
                "already shown, without the engine holding any session state.")

    h2(doc, "8.3 A real worked example")
    para(doc, "Requesting categories ['Technology', 'Health'], preferred_sentiment 'Positive', "
              "interest_focus 0.7, sentiment_weight 0.4 returned this as the top result:")
    add_table(
        doc,
        ["Field", "Value", "Where it comes from"],
        [
            ["category", "Technology", "One of the chosen categories, so cat_match = 1"],
            ["topic_match", "0.8469", "sim_norm, the rescaled cosine against the topical profile"],
            ["sentiment_match", "True", "Article sentiment is Positive, so sent_match = 1.0"],
            ["score", "0.9526",
             "(0.7 x 0.8469 + 0.4 x 1.0) / 1.1 + 0.05 x 1 = 0.9026 + 0.05"],
        ],
        widths=[1.2, 1.0, 4.1],
    )
    caption(doc, "Table 6: Actual engine output, with the arithmetic shown. Being able to "
                 "reproduce a score by hand is the clearest possible demonstration that the "
                 "formula is understood.")
    para(doc, "Check the arithmetic: 0.7 x 0.8469 = 0.5928, plus 0.4 x 1.0 = 0.9928, divided by "
              "1.1 = 0.9026, plus the 0.05 category bonus = 0.9526. This matches the returned "
              "score exactly.", italic=True, size=9.5)

    h2(doc, "8.4 The two extra keys this method returns")
    add_table(
        doc,
        ["Key", "Type", "Purpose"],
        [
            ["score", "float", "The final blended ranking value, 0 to 1.05."],
            ["topic_match", "float",
             "The topical component alone. Lets the UI say 'this matched your interests' "
             "separately from the overall rank."],
            ["sentiment_match", "bool or None",
             "True/False when a specific mood was requested; None when 'Any', because the "
             "question does not apply. This is why the API model types it as bool | None."],
        ],
        widths=[1.2, 1.0, 4.1],
    )
    caption(doc, "Table 7: These keys make the recommendation explainable to the reader instead "
                 "of being an opaque number.")


def section_9_analytics(doc, f, sym, lines):
    h1(doc, "9. Walkthrough: Analytics")
    h2(doc, f"9.1 category_counts ({lref(sym, 'category_counts')})")
    code_block(doc, snippet(lines, sym["category_counts"]["lineno"],
                            sym["category_counts"]["end_lineno"], 4))
    bullet(doc, "Serves GET /categories, which populates the new-user interest form.")
    bullet(doc, "Why counts and not just names: The form can show 'Technology (1,720)' so a "
                "reader understands which interests actually have content behind them.")
    bullet(doc, "Why sorted descending: value_counts orders by frequency, so the most useful "
                "options appear first without the UI having to sort.")

    h2(doc, f"9.2 analytics_summary ({lref(sym, 'analytics_summary')})")
    code_block(doc, snippet(lines, sym["analytics_summary"]["lineno"],
                            sym["analytics_summary"]["end_lineno"], 4))
    add_table(
        doc,
        ["Returned key", "Content", "Verified size"],
        [
            ["articles", "Total article count", "53,527"],
            ["categories", "Number of distinct categories", "257"],
            ["sentiment_counts", "Articles per sentiment label", "3 entries"],
            ["category_counts", "Top categories by volume", "20 entries (head(20))"],
            ["sentiment_by_category", "Nested cross-tab of category against sentiment",
             "10 categories (top_k_categories default)"],
        ],
        widths=[1.5, 2.6, 2.2],
    )
    caption(doc, "Table 8: Confirmed by calling analytics_summary() on the live engine.")
    bullet(doc, "Why two different cut-offs: category_counts uses head(20) for the bar chart, "
                "while the cross-tab uses the top 10 to keep a readable grid. A 257-row "
                "cross-tab would be unusable in a dashboard and slow to serialise.")
    bullet(doc, "Why pd.crosstab: It produces the category-by-sentiment grid in one call. Doing "
                "it with nested loops would be slower and far more code.")
    bullet(doc, "Why every value is wrapped in int(): pandas returns numpy int64, which the "
                "standard json encoder cannot serialise. Casting here means the API can return "
                "the dictionary directly. This is a small line that prevents a real "
                "500-level error.")
    bullet(doc, "Why this runs on the server: The aggregation happens once beside the data "
                "rather than in every browser session, which keeps the dashboard responsive.")


def section_10_integration(doc, f, sym):
    h1(doc, "10. How the Rest of the System Uses This File")
    add_table(
        doc,
        ["Caller", "What it calls", "Why"],
        [
            ["main.py", "generate_embeddings(force=...)",
             "Pipeline stage 4. Builds and caches the embedding matrix."],
            ["app/api.py, startup handler",
             "RecommendationEngine() then generate_embeddings()",
             "Creates ONE global engine and loads vectors once, so no request pays the load "
             f"cost. Measured at about {MEASURED['load_cache_s']:.2f} s, once."],
            ["app/api.py, POST /recommend/", "get_top_n_recommendations(history, top_n)",
             "The returning-reader path. top_n is bounded by Query(ge=1, le=50)."],
            ["app/api.py, POST /recommend/preferences", "recommend_for_preferences(...)",
             "The cold-start path. Pydantic constrains both weights to ge=0.0, le=1.0."],
            ["app/api.py, GET /categories", "category_counts()",
             "Populates the new-user interest form."],
            ["app/api.py, GET /stats", "analytics_summary()",
             "Feeds the dashboard Insights tab."],
            ["app/api.py, GET /health", "engine.df, engine.backend",
             "Reports article count and which embedding backend is active."],
            ["evaluate.py", "generate_embeddings(), get_top_n_recommendations()",
             "Computes Precision@K on the vectors and the recommendation quality metrics."],
            ["app/dashboard.py", "Nothing directly. Calls the API over HTTP.",
             "Keeps the UI decoupled from the model. The dashboard sends interest_focus=0.7 and "
             "sentiment_weight=0.4, or 0.0 when the reader picks 'Any'."],
        ],
        widths=[1.75, 1.9, 2.65],
        font_size=8.5,
    )
    caption(doc, "Table 9: Every call site, confirmed by searching the codebase.")

    callout(doc, "Note on the API defaults:",
            "api.py declares sentiment_weight with a default of 0.3, while the dashboard "
            "explicitly sends 0.4. Both are valid; the dashboard simply overrides the default. "
            "Worth knowing so the two numbers are not mistaken for a contradiction.")


def section_11_observations(doc, f, sym):
    h1(doc, "11. Observations, Edge Cases and Possible Improvements")
    para(doc,
         "Each item below was confirmed by running the engine, not by reading alone. None is a "
         "bug that breaks the system today. They are the honest answers to give if a reviewer "
         "pushes on the weak points, and having them ready is far stronger than being surprised "
         "by them.")

    h2(doc, "11.1 Behavioural observations")

    h3(doc, "Observation 1: the cold-start branch omits the score key")
    para(doc,
         "In get_top_n_recommendations, the normal path attaches a score to every payload, but "
         "the empty-history fallback returns bare payloads. Confirmed: the normal path returns "
         "six keys including score, the fallback returns five without it. This does not break "
         "anything, because the API's RecommendationItem declares score as Optional, so it "
         "serialises as null. Worth knowing because any UI that formats the score must handle "
         "its absence.")

    h3(doc, "Observation 2: backend reads 'cache' after a cache load")
    para(doc,
         "When embeddings are loaded from disk, self.backend is set to the string 'cache' rather "
         "than to whichever backend originally produced the file, because no metadata is stored "
         "alongside the .npy. Confirmed by inspecting engine.backend after a cache load. The "
         "practical consequence is that GET /health reports 'cache' and cannot tell you whether "
         "the cached vectors came from the transformer or from the TF-IDF fallback. Saving a "
         "small sidecar JSON with the backend name and model would resolve it.")

    h3(doc, "Observation 3: the cosine call dominates request latency")
    para(doc,
         f"A single cosine call measures about {MEASURED['cosine_call_s'] * 1000:.0f} ms, out of "
         f"a total {MEASURED['history_rec_s'] * 1000:.0f} ms for a full recommendation. Almost "
         "all of the request is that one function. Two reasons, both confirmed: "
         "matrix.astype(np.float32) copies the entire "
         f"{f.get('emb_mb', 78.4)} MB matrix even though it is already float32, because astype "
         "defaults to copy=True; and the per-row norms are recomputed on every call even though "
         "they never change. Using np.asarray instead of astype would skip the copy, and caching "
         "the norms once on the engine would remove the rest. The current speed is perfectly "
         "adequate, so this is an optimisation rather than a fix.")

    h3(doc, "Observation 4: the text fallback in _short_description cannot fire")
    para(doc,
         "_short_description falls back to row.get('text', '') when the description is blank. But "
         "the constructor deliberately excludes text from the loaded columns, so that key is "
         "never present and the fallback always yields an empty string. Confirmed: "
         "'text' is not among the loaded columns. It has no practical impact, because "
         "preprocessing already backfills every description from the article body. Verified: "
         "zero rows in processed_news.csv have an empty description. The line is defensive "
         "residue from before the lazy-loading optimisation.")

    h3(doc, "Observation 5: stale-cache detection is by row count only")
    para(doc,
         "generate_embeddings compares the cached row count against the article count. If the "
         "corpus were re-cleaned in a way that changed the content but happened to keep the same "
         "number of rows, the stale cache would be accepted. A content hash of the titles stored "
         "beside the array would close the gap. In practice --force and run.bat rebuild cover it, "
         "but it is a real limit of the check.")

    h3(doc, "Observation 6: booleans pass the index validity test")
    para(doc,
         "The filter accepts anything matching isinstance(i, (int, np.integer)). In Python bool "
         "is a subclass of int, so True would be accepted and read as index 1. Harmless in "
         "practice, since Pydantic coerces the API payload to real integers before the engine "
         "ever sees it, but it is a genuine quirk of the check.")

    h2(doc, "11.2 Improvements, in order of value")
    for text in [
        "Cache the row norms and drop the redundant copy: Precompute the per-row norms once, and "
        "use np.asarray in place of astype. Straightforward, and it targets the measured hot spot "
        "directly.",
        "Store backend metadata beside the cache: A small JSON with the backend name, model name "
        "and a corpus hash would fix Observations 2 and 5 together.",
        "Replace argsort with argpartition: A full sort orders all "
        f"{f['emb_rows']:,} articles when only the top few are needed. evaluate.py already uses "
        "argpartition for exactly this reason, so the pattern is established in the codebase.",
        "Add an approximate nearest-neighbour index: FAISS or HNSW would keep latency flat as the "
        "corpus grows past a few hundred thousand articles, where a full scan stops being viable.",
        "Support multi-interest profiles: Cluster a reader's history and score against each "
        "cluster, taking the best match. This addresses the averaging weakness described in "
        "Section 3.3, where a reader with two unrelated interests gets a profile near neither.",
        "Add recency weighting: Weight recent history more heavily than old history when pooling, "
        "so the profile tracks a reader's current interests rather than their lifetime average.",
        "Add explicit diversity re-ranking: Maximal marginal relevance would make the "
        "relevance-versus-variety trade a tunable parameter instead of an emergent side effect.",
    ]:
        bullet(doc, text)


def section_12_qa(doc, f, sym):
    h1(doc, "12. Questions You Are Likely To Be Asked")
    para(doc, "Answers short enough to say out loud, specific to this file.", italic=True,
         size=9.5)
    qa = [
        ("Walk me through what happens on one recommendation request.",
         "Load the cached embedding matrix, gather the rows for the reader's history, average "
         "them into one profile vector, take the cosine of that profile against every article in "
         "a single matrix-vector product, sort descending, skip the articles they have already "
         "read, and return the first five with their scores."),
        ("Why is there a separate function for cosine similarity?",
         "Both recommendation methods need identical maths. One function means one place for the "
         "divide-by-zero guard and the float32 casting, so the two paths cannot drift apart."),
        ("What is the 1e-10 for?",
         "A divide-by-zero guard. A zero-length vector, which the TF-IDF fallback can produce "
         "for an article of pure stop-words, would give NaN and corrupt the whole ranking."),
        ("Why cosine rather than Euclidean distance?",
         "Cosine compares direction and ignores length. Article length would otherwise leak into "
         "the score, making a long piece and a short piece on the same subject look dissimilar."),
        ("What does axis=0 mean in the mean call?",
         "Average down the columns. It collapses several article vectors into one vector of the "
         "same width, which is the reader's centre of interest."),
        ("Why exclude articles the reader has already read?",
         "They are the closest points to the profile by construction, since the profile is their "
         "average. Without the filter the top results would be the reader's own history."),
        ("Why cache the embeddings on disk?",
         f"Encoding {f['emb_rows']:,} articles takes minutes. Cached, the whole matrix loads in "
         f"about {MEASURED['load_cache_s']:.2f} s at startup and every request afterwards is "
         "millisecond-scale arithmetic."),
        ("How do you know the cache is not stale?",
         "generate_embeddings compares the cached row count against the article count and "
         "rebuilds on a mismatch. The row index is the article ID, so a mismatch would silently "
         "map every index to the wrong article."),
        ("What happens if sentence-transformers is not installed?",
         f"_encode_sentence_transformer returns None and the engine builds TF-IDF plus SVD "
         f"vectors at the same {f['emb_dim']} dimensions instead. Quality drops, but nothing "
         "downstream changes and the pipeline still completes."),
        ("Why is the text column excluded when loading the CSV?",
         "processed_news.csv is 326 MB and most of it is article bodies that the serving path "
         "never shows. It is read once inside _corpus, only when embeddings must be rebuilt."),
        ("Why is the row index used as the article ID?",
         "Row i of the DataFrame and row i of embeddings.npy are the same article, so a position "
         "is all you need to look up both the vector and the metadata. It also keeps the API "
         "payload trivially simple."),
        ("How does a reader with no history get recommendations?",
         "recommend_for_preferences. They pick categories and a tone; the engine mean-pools the "
         "embeddings of those categories into a topical profile and blends normalised similarity "
         "with a sentiment match."),
        ("Why rescale the cosine to [0,1] in that method?",
         "The sentiment component is 0 or 1 while cosine spans -1 to 1. Blending two different "
         "scales would make the weights meaningless. Rescaling puts them on common ground."),
        ("Why divide by the sum of the weights?",
         "It normalises the blend so only the ratio of the weights matters and the result stays "
         "inside [0, 1]. Passing 7 and 3 gives the same ranking as 0.7 and 0.3."),
        ("What is the 0.05 bonus for?",
         "It breaks near-ties in favour of articles literally tagged with a chosen category. It "
         "is small on purpose so semantic relevance stays in charge, and it means the maximum "
         "score is 1.05."),
        ("Can you reproduce a score by hand?",
         "Yes. For a Technology article with topic_match 0.8469, Positive sentiment, weights 0.7 "
         "and 0.4: (0.7 x 0.8469 + 0.4 x 1.0) / 1.1 = 0.9026, plus 0.05 = 0.9526, which is "
         "exactly what the engine returned."),
        ("Why does sentiment_match come back as None sometimes?",
         "When the reader chose 'Any' there is no preference to match, so the question does not "
         "apply. None is more honest than False, and the API types the field as bool | None."),
        ("What is the slowest part of a request?",
         f"The cosine call, about {MEASURED['cosine_call_s'] * 1000:.0f} ms of the "
         f"{MEASURED['history_rec_s'] * 1000:.0f} ms total. It copies the whole matrix because "
         "astype defaults to copy=True, and it recomputes the row norms every time. Caching the "
         "norms and using np.asarray would fix both."),
        ("What would you improve first?",
         "Cache the row norms and remove the redundant matrix copy. It targets the measured hot "
         "spot, and it is a small, low-risk change."),
        ("Why keep the imports inside the methods?",
         "torch and scikit-learn are heavy. Importing them lazily means a run that loads cached "
         "embeddings never pays for libraries it does not use."),
    ]
    add_table(doc, ["Question", "Answer"], qa, widths=[1.9, 4.4], font_size=8.5)
    caption(doc, "Table 10: Question-and-answer crib sheet for src/recommendation.py.")


def section_13_summary(doc, f, sym, lines):
    h1(doc, "13. Summary")
    para(doc,
         f"recommendation.py is {len(lines)} lines doing two clearly separated jobs. Offline, it "
         f"converts every article into a {f['emb_dim']}-dimension semantic vector and caches the "
         f"result as a {f['emb_rows']:,} x {f['emb_dim']} float32 matrix. Online, it turns a "
         "reader into a vector of the same shape, measures the cosine of that vector against "
         "every article in one matrix-vector product, and returns the nearest few.")
    para(doc,
         "The engineering around that core exists to make it dependable rather than clever. "
         "Column loading is deliberately narrow so a 326 MB CSV does not have to live in the API "
         "process. The cache is validated against the article count because the row index is the "
         "article ID and a silent misalignment would be worse than a crash. Every heavy import is "
         "lazy, and the transformer has a same-shape fallback so a missing optional dependency "
         "degrades quality instead of stopping the pipeline. Both recommendation paths share the "
         "same payload builder, which is what lets one response model validate both endpoints.")
    para(doc,
         "The weak points are known and small. Cosine similarity copies the matrix and recomputes "
         "norms on every call, which is the measured hot spot; the cached backend name is not "
         "recorded; stale detection is by row count rather than content; and one defensive branch "
         "can no longer fire. Each is documented in Section 11 with the fix, and none affects "
         f"correctness today. A recommendation completes in roughly "
         f"{MEASURED['history_rec_s'] * 1000:.0f} ms against the full corpus.")


# ===================================================================== #
def build() -> str:
    source_text, lines = read_source()
    sym = build_symbol_map(source_text)
    f = load_facts()

    doc = Document()
    setup_styles(doc)
    for s in doc.sections:
        s.left_margin = s.right_margin = Inches(0.8)
        s.top_margin = s.bottom_margin = Inches(0.7)
    add_footer_page_numbers(doc)

    cover(doc, f, sym, lines)
    section_1_big_picture(doc, f, sym)
    page_break(doc)
    section_2_map(doc, f, sym)
    page_break(doc)
    section_3_maths(doc, f, sym, lines)
    page_break(doc)
    section_4_init(doc, f, sym, lines)
    page_break(doc)
    section_5_embeddings(doc, f, sym, lines)
    page_break(doc)
    section_6_helpers(doc, f, sym, lines)
    page_break(doc)
    section_7_history(doc, f, sym, lines)
    page_break(doc)
    section_8_coldstart(doc, f, sym, lines)
    page_break(doc)
    section_9_analytics(doc, f, sym, lines)
    page_break(doc)
    section_10_integration(doc, f, sym)
    page_break(doc)
    section_11_observations(doc, f, sym)
    page_break(doc)
    section_12_qa(doc, f, sym)
    section_13_summary(doc, f, sym, lines)

    doc.save(OUT_PATH)
    return OUT_PATH


if __name__ == "__main__":
    path = build()
    print(f"[docs] Word document written -> {path}")
    print(f"[docs] Size: {os.path.getsize(path) / 1024:.1f} KB")
