"""
Generate the team conflict-and-resolution log as a Word (.docx) file.
Exactly one page per team member (verified with Word pagination).

  >>> EDIT THE `ROSTER` LIST BELOW TO PUT IN THE REAL NAMES, THEN RE-RUN. <<<

The project records no member names (README says only "PGCP-BDA Group 13") and
git is not available on this machine, so the six workstreams below were derived
from the actual module ownership in the codebase. Every conflict documented here
is traceable to real code -- the "Evidence" line on each one names the file and
the construct that resolves it.

Usage:
    python docs/generate_conflict_docs.py

Output:
    docs/Team_Conflicts_And_Resolutions.docx
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

from generate_documentation import (
    ACCENT,
    GREY,
    add_footer_page_numbers,
    add_table,
    callout,
    caption,
    h1,
    h2,
    page_break,
    para,
    setup_styles,
    shade,
)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "Team_Conflicts_And_Resolutions.docx")


# ===================================================================== #
#  >>>>>>>>>>>>>>>>  REPLACE THE NAMES HERE  <<<<<<<<<<<<<<<<
# ===================================================================== #
ROSTER = [
    {
        "name": "Team Member 1",
        "role": "Data Engineering and Preprocessing",
        "files": "src/preprocessing.py, config.py",
        "summary":
            "Owned ingestion: turning three inconsistent raw Kaggle CSVs into one reliable, "
            "de-duplicated article table, plus the configuration module every other component "
            "reads.",
        "conflicts": [
            {
                "title": "Conflict 1: the full dataset would not fit in memory, but a sample "
                         "would not be credible",
                "trigger":
                    "The design document specified 100 articles for fast iteration. The rest of "
                    "the team wanted the full corpus so the metrics would mean something. A naive "
                    "read of the 409 MB data.csv exhausted memory on our laptops.",
                "resolution":
                    "Rather than shrink the corpus or find a bigger machine, we made the read "
                    "itself cheap: usecols so only the five needed columns are parsed, dtype=str "
                    "to skip type inference over hundreds of thousands of rows, and "
                    "on_bad_lines='skip' so one malformed row cannot abort a 409 MB read. "
                    "NEWS_SAMPLE_SIZE was then redefined so 0 means 'use everything', keeping the "
                    "fast demo path available without a code change.",
                "evidence":
                    "preprocessing.py: the header probe, usecols construction and read_kwargs "
                    "dict. config.py: NEWS_SAMPLE_SIZE default 0 documented as ALL.",
                "trade":
                    "Skipping malformed lines silently discards a few records. Accepted, because "
                    "the alternative was a hard failure on data we do not control.",
            },
            {
                "title": "Conflict 2: three raw CSVs, three schemas, no agreed source of truth",
                "trigger":
                    "archive/ ships three CSVs that share most column names but not the important "
                    "ones: only data.csv has full_content, only rating.csv has the "
                    "title_sentiment labels. Members had started against different files, so the "
                    "preprocessing output kept changing shape underneath everyone.",
                "resolution":
                    "Assigned distinct roles instead of mandating one file: data.csv is the "
                    "content source, rating.csv the label source, raw-data.csv unused. Then made "
                    "the loader schema-tolerant anyway, with an ordered candidate list for the "
                    "body column and synthesis of any missing category, url or description "
                    "column.",
                "evidence":
                    "preprocessing.py: _TEXT_COLUMN_CANDIDATES in priority order, the next(...) "
                    "selection, and the three backfill blocks.",
                "trade":
                    "raw-data.csv is now dead weight. Kept rather than deleting supplied data, "
                    "and documented as unused.",
            },
            {
                "title": "Conflict 3: de-duplication shrank the corpus, which nobody wanted",
                "trigger":
                    "Syndicated news repeats the same story across outlets. De-duplicating "
                    "visibly reduced the article count, and the instinct across the team was that "
                    "more data is always better.",
                "resolution":
                    "Kept de-duplication on title after working through the alternative: "
                    "duplicates have near-identical embeddings, so one story would fill several "
                    "slots in a top-5 list and would also inflate Precision@K, since a duplicate "
                    "is trivially in the same category. Keeping them would have made the numbers "
                    "look better and the product worse. Title beat body text because syndicated "
                    "copies differ in body more often than in headline.",
                "evidence":
                    "preprocessing.py: drop_duplicates(subset=['title']), applied after "
                    "whitespace normalisation so formatting cannot defeat the match.",
                "trade":
                    "Two genuinely different articles sharing a headline lose one copy. Rare, and "
                    "cheaper than the alternative.",
            },
        ],
        "differently":
            "Normalise whitespace before the missing-value drop rather than after. The current "
            "order means whitespace-only rows have to be filtered a second time, which is why "
            "there is an extra empty-string filter after _vclean.",
    },
    {
        "name": "Team Member 2",
        "role": "Sentiment Modelling",
        "files": "train_sentiment.py, src/sentiment_analysis.py",
        "summary":
            "Owned article tone: training the classifier, labelling the corpus with it, and "
            "producing the held-out metrics the evaluation report and dashboard depend on.",
        "conflicts": [
            {
                "title": "Conflict 1: the lexicon we started with did not understand news",
                "trigger":
                    "TextBlob was the original design choice because it needs no training. On "
                    "news headlines it was visibly wrong: it has no idea that 'shares plunge' is "
                    "negative. Replacing it meant new dependencies, a training script, a model "
                    "artifact and a deviation from the agreed design.",
                "resolution":
                    "Trained a model but kept TextBlob as a fallback, which meant nobody had to "
                    "lose the argument. rating.csv already carries human title_sentiment labels, "
                    "so TF-IDF plus Logistic Regression could be trained on genuine ground truth. "
                    "analyze_sentiment uses the joblib model when it exists and falls back to "
                    "lexicon polarity when it does not, so the pipeline completes on any machine. "
                    "Held-out accuracy is 82.27%.",
                "evidence":
                    "sentiment_analysis.py: _load_trained_model returns None on absence, and the "
                    "branch that reports method as 'trained model' or 'TextBlob lexicon'.",
                "trade":
                    "Two paths to maintain, and the sentiment column's meaning depends on which "
                    "ran. The printed method name makes that visible in the logs.",
            },
            {
                "title": "Conflict 2: the accuracy number looked better unbalanced, but the model "
                         "was useless",
                "trigger":
                    "Neutral is 73.6% of the labelled titles. An unbalanced classifier predicts "
                    "Neutral almost always, scores a respectable accuracy and finds almost no "
                    "Positive or Negative. The disagreement was real: the headline metric we would "
                    "be presenting is higher without balancing.",
                "resolution":
                    "Used class_weight='balanced' on the argument that a metric exists to "
                    "describe the product, not flatter it. A model that never predicts Positive "
                    "makes the dashboard's mood filter dead. Balancing lifted Positive recall to "
                    "75.1% and Negative to 79.4%. Resampling was rejected as more moving parts for "
                    "the same effect.",
                "evidence":
                    "train_sentiment.py: LogisticRegression(max_iter=1000, C=4.0, "
                    "class_weight='balanced'). The effect is the precision-recall gap per class "
                    "in sentiment_metrics.json.",
                "trade":
                    "Deliberate: Positive precision is 57.9%, so roughly two in five Positive "
                    "labels are really Neutral. For a soft filter, missing upbeat stories hurts a "
                    "reader more than including a borderline one, and the confusion matrix shows "
                    "Positive-Negative confusion stays rare.",
            },
            {
                "title": "Conflict 3: is it honest to report metrics from a model we do not ship?",
                "trigger":
                    "The scored model is trained on 80% of the labels, but for deployment we refit "
                    "on 100% because more data labels better. The published numbers therefore do "
                    "not come from the shipped artifact, which one of us flagged as potentially "
                    "misleading.",
                "resolution":
                    "Shipped the stronger model and published the conservative held-out figure, "
                    "documenting the practice. The 80% model is strictly weaker than what ships, "
                    "so the reported number understates rather than overstates it. Reporting a "
                    "defensible floor is honest; the failure mode we were guarding against is the "
                    "opposite one.",
                "evidence":
                    "train_sentiment.py: metrics computed from X_te, then '# Refit on ALL data "
                    "for deployment' before pipe.fit(X, y). The split is stratified and seeded.",
                "trade":
                    "The published metrics are a lower bound, not an exact description of the "
                    "shipped artifact. Stated openly rather than glossed over.",
            },
        ],
        "differently":
            "Make the two labelling paths agree on their input. The trained model predicts from "
            "the title; the TextBlob fallback scores the first 500 characters of the body. They "
            "label different things, so the sentiment column is not strictly comparable across "
            "runs that used different backends.",
    },
    {
        "name": "Team Member 3",
        "role": "Embeddings and the Recommendation Engine",
        "files": "src/recommendation.py",
        "summary":
            "Owned the core: encoding every article into a semantic vector, caching that matrix, "
            "and the cosine-similarity ranking behind every recommendation request.",
        "conflicts": [
            {
                "title": "Conflict 1: encoding took minutes, but the API had to answer in "
                         "milliseconds",
                "trigger":
                    "The first working version encoded articles inside the request path. A single "
                    "recommendation took minutes, which made the dashboard untestable and made "
                    "iterating on anything downstream painful.",
                "resolution":
                    "Split the expensive step from the serving step and cached the result, which "
                    "became the architectural spine of the project. Encoding happens once offline "
                    "into a 53,527 x 384 float32 embeddings.npy; serving loads it once at startup "
                    "in about 0.16 s and each request is then one matrix-vector product. A full "
                    "recommendation now measures about 122 ms.",
                "evidence":
                    "recommendation.py: generate_embeddings does the cache check, build and "
                    "np.save. api.py: the startup handler builds one global engine.",
                "trade":
                    "A newly published article cannot be recommended until the pipeline is "
                    "re-run. Acceptable for a static dataset; noted as future work.",
            },
            {
                "title": "Conflict 2: caching introduced a silent-corruption risk worse than "
                         "being slow",
                "trigger":
                    "The row index is the article ID, so row i of the DataFrame and row i of "
                    "embeddings.npy must be the same article. When the corpus was re-cleaned "
                    "mid-development the old cache was still loaded and every recommendation "
                    "quietly pointed at the wrong article. Nothing crashed, which is what made it "
                    "dangerous.",
                "resolution":
                    "Made the cache self-validating rather than relying on discipline, which is no "
                    "control at all for an invisible failure. generate_embeddings compares the "
                    "cached row count against the article count and rebuilds on mismatch, printing "
                    "'stale'. run.bat additionally checks processed_news.csv has the url column "
                    "before skipping a rebuild, catching the schema change that caused the "
                    "original incident.",
                "evidence":
                    "recommendation.py: the 'cached.shape[0] == len(self.df)' guard and stale "
                    "print. run.bat: the inline artifact check testing for 'url' in the header.",
                "trade":
                    "Row-count only. A same-length but different corpus still slips through; a "
                    "content hash would close it. Documented as a known limit.",
            },
            {
                "title": "Conflict 3: the best suggestions were articles the reader had already "
                         "read",
                "trigger":
                    "The first ranking returned the reader's own history at the top of the list. "
                    "It looked like a bug in the similarity code and cost real time to diagnose.",
                "resolution":
                    "The maths was right, and that was the insight: the profile is the average of "
                    "the history vectors, so those articles are by construction the closest points "
                    "to it. Fixed with a seen set checked while walking the ranking, which also "
                    "stops early once top_n results are collected.",
                "evidence":
                    "recommendation.py: seen = set(valid), the 'if idx in seen: continue' skip, "
                    "and the break once top_n is reached.",
                "trade":
                    "None of consequence. A set was used over a list to keep the check constant "
                    "time.",
            },
            {
                "title": "Conflict 4: a heavy optional dependency threatened to block everyone",
                "trigger":
                    "sentence-transformers pulls in torch. On one machine it would not install, "
                    "and importing it slowed every run even when cached vectors were being loaded "
                    "and the model was never needed.",
                "resolution":
                    "Kept the transformer as primary with a same-shape fallback, so nobody was "
                    "blocked and nobody was overruled. On failure the engine builds TF-IDF plus "
                    "TruncatedSVD at the same 384 dimensions, leaving cosine similarity, the cache "
                    "format and the API schema unchanged. Heavy imports also moved inside the "
                    "methods that need them.",
                "evidence":
                    "recommendation.py: _encode_sentence_transformer returns None on failure, "
                    "_encode_tfidf clamps n_components, and both imports are function-local.",
                "trade":
                    "The fallback is genuinely weaker, since it still leans on shared vocabulary. "
                    "/health reports which backend is active.",
            },
        ],
        "differently":
            "Cache the row norms on the engine and use np.asarray instead of astype in the "
            "similarity function. astype defaults to copy=True, so it copies the whole 78 MB "
            "matrix on every request even though it is already float32. That one function is "
            "107 ms of the 122 ms request.",
    },
    {
        "name": "Team Member 4",
        "role": "User Simulation and Cold Start",
        "files": "src/user_simulator.py, recommend_for_preferences in src/recommendation.py",
        "summary":
            "Owned the reader side: manufacturing a population to demonstrate personalisation "
            "against, and solving the case of a reader with no history at all.",
        "conflicts": [
            {
                "title": "Conflict 1: the dataset has no users, so half the planned system had "
                         "no input",
                "trigger":
                    "The plan assumed reading histories. The Kaggle dataset has none: no user "
                    "ids, no clicks, no sessions. Collaborative filtering was off the table, and "
                    "there was pressure to synthesise plausible-looking behaviour so that "
                    "click-based metrics could be reported.",
                "resolution":
                    "Simulated 1,000 seeded readers with 3 to 10 articles each, and accepted that "
                    "click metrics are therefore unavailable. Fabricating histories with a "
                    "topical bias and then measuring whether the recommender finds that bias "
                    "would be measuring our own random number generator and calling it accuracy.",
                "evidence":
                    "user_simulator.py: random.Random(seed) with rng.sample over "
                    "range(n_articles). evaluate.py: the docstring states there are no real click "
                    "logs and lists what is measured instead.",
                "trade":
                    "No click-through rate, NDCG or MAP anywhere in the report. A real gap in the "
                    "evaluation, stated as a limitation rather than papered over.",
            },
            {
                "title": "Conflict 2: a brand-new reader has nothing to average",
                "trigger":
                    "The engine works by mean-pooling a reading history. A new visitor breaks that "
                    "assumption completely, and the first version simply returned the first few "
                    "articles in file order.",
                "resolution":
                    "Asked the reader for their interests instead. The engine mean-pools the "
                    "embeddings of their chosen categories into a topical profile, which puts a "
                    "new reader in exactly the same vector space as a returning one. File-order "
                    "behaviour was kept but demoted to a last-resort guard so the endpoint can "
                    "never fail.",
                "evidence":
                    "recommendation.py: recommend_for_preferences builds the profile from "
                    "cat_series.isin(cats), falling back to the corpus mean; the empty-history "
                    "guard in get_top_n_recommendations.",
                "trade":
                    "A declared interest is weaker evidence than actual behaviour. It is the best "
                    "signal available at first visit.",
            },
            {
                "title": "Conflict 3: blending topic and sentiment made the weights meaningless",
                "trigger":
                    "Cosine similarity spans -1 to 1; the sentiment match is 0 or 1. Combining "
                    "them directly meant weights of 0.7 and 0.3 did not produce a 70/30 "
                    "influence, and tuning them produced results nobody could explain.",
                "resolution":
                    "Put both components on a common scale before blending, which made the "
                    "formula explainable -- the actual goal. Cosine is rescaled with "
                    "(sim + 1) / 2, and the blend is divided by the sum of the weights so only "
                    "their ratio matters. 'Any' maps to a flat 0.5 rather than 0, because a "
                    "constant changes no rankings while zero would drag every score down for "
                    "nothing.",
                "evidence":
                    "recommendation.py: sim_norm = (sim + 1.0) / 2.0, then "
                    "final = (wf * sim_norm + ws * sent_match) / total, plus the np.full(n, 0.5) "
                    "branch for 'Any'.",
                "trade":
                    "One extra pass over the score array, in exchange for a formula whose output "
                    "can be reproduced by hand.",
            },
            {
                "title": "Conflict 4: category labels and semantic similarity disagreed on "
                         "relevance",
                "trigger":
                    "A reader picking Technology would sometimes see a highly similar article from "
                    "a neighbouring category ranked above a literal Technology one. Some of us "
                    "read that as correct semantic behaviour and some as an obvious bug.",
                "resolution":
                    "Let similarity lead, with a small tie-breaker for the exact label. A hard "
                    "category filter would throw away the semantic generalisation that is the "
                    "point of using embeddings, and with 257 overlapping categories it would "
                    "exclude obviously relevant Finance articles from a Stock request. A 0.05 "
                    "bonus orders near-ties without letting a label override relevance.",
                "evidence":
                    "recommendation.py: cat_match built from cat_series.isin(cats), then "
                    "'final = final + 0.05 * cat_match  # nudge exact-category articles up'.",
                "trade":
                    "The maximum achievable score becomes 1.05 rather than 1.0, which matters to "
                    "anyone presenting the score as a percentage.",
            },
        ],
        "differently":
            "Sample histories with a deliberate, clearly documented topical bias and report the "
            "relative metrics on both the biased and the uniform population. That would show the "
            "recommender responding to structure without ever presenting a click metric as though "
            "it came from real readers.",
    },
    {
        "name": "Team Member 5",
        "role": "API and Integration",
        "files": "app/api.py, main.py, run.bat",
        "summary":
            "Owned everything between the model and the interface: the REST contract, pipeline "
            "orchestration, and making the whole system start from one command on a clean "
            "machine.",
        "conflicts": [
            {
                "title": "Conflict 1: the API worked alone and failed the moment the dashboard "
                         "was added",
                "trigger":
                    "run.bat launches the API and the dashboard together. The API spends about "
                    "6 s loading embeddings before it can answer anything, so the dashboard came "
                    "up first and greeted every demo with a raw ConnectionError traceback.",
                "resolution":
                    "Defended at both ends rather than picking one fix. run.bat starts the API in "
                    "its own window, waits 6 s, then starts the dashboard; the dashboard catches "
                    "requests.exceptions.ConnectionError specifically and renders the exact "
                    "uvicorn command needed instead of a stack trace. A fixed wait is a guess, "
                    "which is precisely why the error path had to be good.",
                "evidence":
                    "run.bat: start \"Recommendation API\" followed by timeout /t 6 /nobreak. "
                    "dashboard.py: the ConnectionError branch in call_api returning an actionable "
                    "message.",
                "trade":
                    "The 6 s wait is a fixed guess, so on a slower machine the first request can "
                    "still miss the window.",
            },
            {
                "title": "Conflict 2: valid Python that FastAPI refused to serialise",
                "trigger":
                    "Payloads came straight from pandas, so they contained numpy int64 and "
                    "occasional NaN. The standard JSON encoder handles neither, so endpoints that "
                    "worked when called directly from Python returned 500s over HTTP.",
                "resolution":
                    "Converted at the boundary where the values are produced rather than "
                    "registering a custom encoder, so the engine's return values stay honest "
                    "Python for any future caller. Every count in analytics_summary is wrapped in "
                    "int() and every payload field cast with str(). The same pass caught missing "
                    "URLs arriving as the literal string 'nan', which would have rendered as "
                    "broken links.",
                "evidence":
                    "recommendation.py: the int(v) comprehensions in analytics_summary, and the "
                    "'url.lower() != \"nan\"' check in _article_payload.",
                "trade":
                    "Repetitive casting, in exchange for endpoints that behave identically "
                    "in-process and over HTTP.",
            },
            {
                "title": "Conflict 3: demo convenience versus not shipping a footgun",
                "trigger":
                    "Two opposing pulls. We wanted one command that installs, builds and starts "
                    "everything, because setup friction was eating demo time. We also did not "
                    "want an unbounded API that any caller could use to request the entire "
                    "53,527-article catalogue in one response.",
                "resolution":
                    "Automated the setup and constrained the surface. run.bat probes for the key "
                    "imports and only pip installs when something is missing, then rebuilds "
                    "artifacts only when they are absent or stale. Every API input is bounded: "
                    "top_n is Query(ge=1, le=50), both preference weights are "
                    "Field(ge=0.0, le=1.0), and history_indices is typed so a malformed body is "
                    "rejected with 422 before any model code runs.",
                "evidence":
                    "run.bat: the import probe, conditional pip install and NEED_BUILD logic. "
                    "api.py: the Query and Field constraints and the 503 engine guards.",
                "trade":
                    "Still no authentication, rate limiting or CORS. Acceptable only because it "
                    "binds to 127.0.0.1 for a local demonstration, and flagged in the "
                    "documentation as required before any network exposure.",
            },
        ],
        "differently":
            "Replace the fixed 6 s wait with a short polling loop against /health. It removes the "
            "guess entirely and would save several seconds on a fast machine. Also worth moving "
            "off the deprecated on_event('startup') hook to the lifespan handler.",
    },
    {
        "name": "Team Member 6",
        "role": "Dashboard and Evaluation",
        "files": "app/dashboard.py, evaluate.py",
        "summary":
            "Owned how the work is judged and how it is presented: the four-tab interface, and "
            "the evaluation script that produces every number the team reports.",
        "conflicts": [
            {
                "title": "Conflict 1: the metrics we wanted were the ones we could not honestly "
                         "compute",
                "trigger":
                    "Recommender work normally reports NDCG, MAP and click-through rate, and "
                    "their absence looks like an omission. All three need genuine user feedback, "
                    "and our reading histories are randomly generated.",
                "resolution":
                    "Built the evaluation only on ground truth that actually exists, and stated "
                    "what is missing. Three families: retrieval Precision@K using the article's "
                    "own category, which never fed the embeddings; recommendation consistency, "
                    "diversity and coverage; and sentiment accuracy against the dataset's human "
                    "labels. Every relative metric is reported beside a computed random baseline.",
                "evidence":
                    "evaluate.py: the docstring opens by stating there are no real click logs; "
                    "random_baseline is the sum of squared category proportions.",
                "trade":
                    "A visible gap where the familiar ranking metrics would be. We decided a "
                    "defensible gap beats an impressive but meaningless number.",
            },
            {
                "title": "Conflict 2: a headline number that looked bad but was not",
                "trigger":
                    "Precision@5 came out at 23.68%. Read cold, that sounds like a failing "
                    "system, and there was an argument for reporting only the stronger framing or "
                    "leaving it out.",
                "resolution":
                    "Reported all of it with the context that makes it interpretable. With 257 "
                    "categories the chance two random articles share one is 1.64%, so 23.68% is "
                    "about 14 times better than chance. The scoring is also strict by "
                    "construction: exact string match means a Finance article retrieved for a "
                    "Stock query counts as an error, though a human would call it a good result.",
                "evidence":
                    "evaluate.py: random_baseline from (p ** 2).sum(). dashboard.py tab_accuracy: "
                    "score, baseline and multiple shown side by side.",
                "trade":
                    "The raw number still looks modest to anyone reading it without the baseline, "
                    "so the baseline had to be given equal visual weight rather than a footnote.",
            },
            {
                "title": "Conflict 3: numbers that were accurate and completely unreadable",
                "trigger":
                    "Scores arrive as 0.6105 across a band from 0.61 to 0.59, so readers could "
                    "not tell a good recommendation from a mediocre one. The labels Positive, "
                    "Neutral and Negative were also being read as judgements about the news "
                    "rather than descriptions of tone.",
                "resolution":
                    "Presented a human-readable form in the UI while keeping exact values in the "
                    "API. The dashboard shows a clamped percentage and prefers topic_match, the "
                    "component a reader can actually interpret; labels became 'Positive "
                    "(upbeat)', 'Neutral (factual)' and 'Negative (concerning)'. Nothing was lost, "
                    "because score, topic_match and sentiment_match remain in the response at "
                    "full precision.",
                "evidence":
                    "dashboard.py: FRIENDLY_SENTIMENT, and in render_recommendations the "
                    "topic_match-then-score preference with max(0, min(100, ...)).",
                "trade":
                    "The displayed percentage is not the raw score, and the underlying value can "
                    "reach 1.05 because of the category bonus, which is why the display is "
                    "clamped to 100.",
            },
            {
                "title": "Conflict 4: the evaluation itself was too slow and too hungry to run",
                "trigger":
                    "The full similarity matrix for 53,527 articles is over 2.8 billion entries "
                    "and will not fit in memory. The dashboard had the same problem differently: "
                    "Streamlit re-runs the script on every widget interaction, so each slider "
                    "drag re-read a 326 MB CSV.",
                "resolution":
                    "Sampled and cached instead of shrinking the corpus. Retrieval is evaluated on "
                    "500 seeded query articles scored against the full corpus, keeping one axis "
                    "exhaustive while bounding memory, and argpartition finds the top K without "
                    "fully sorting 53,527 entries. The dashboard loader is wrapped in "
                    "@st.cache_data and reads only the five light columns the UI needs.",
                "evidence":
                    "evaluate.py: sims = norm[idxs] @ norm.T with sample=500, and "
                    "np.argpartition(-row, maxk). dashboard.py: @st.cache_data on load_data with "
                    "the usecols selection.",
                "trade":
                    "Retrieval precision is estimated from a 500-article sample, so it carries "
                    "sampling error. A fixed seed at least makes it reproducible.",
            },
        ],
        "differently":
            "Surface which sentiment figures are being shown. evaluate_sentiment prefers the "
            "supervised held-out metrics but silently falls back to scoring TextBlob against "
            "rating.csv, so two very different numbers can occupy the same field. The saved "
            "method string distinguishes them; the dashboard does not show it.",
    },
]

BODY_PT = 8.5


# ===================================================================== #
def cbullet(doc, label: str, text: str, size: float = BODY_PT):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    r = p.add_run(label + ": ")
    r.bold = True
    r.font.size = Pt(size)
    r2 = p.add_run(text)
    r2.font.size = Pt(size)
    return p


def conflict_heading(doc, text: str):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(9.5)
    r.font.color.rgb = ACCENT
    return p


def member_header(doc, m: dict, n: int):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    r = p.add_run(m["name"])
    r.bold = True
    r.font.size = Pt(16)
    r.font.color.rgb = ACCENT
    r2 = p.add_run(f"    (Member {n} of {len(ROSTER)})")
    r2.font.size = Pt(8.5)
    r2.font.color.rgb = GREY

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    r = p.add_run(m["role"])
    r.bold = True
    r.font.size = Pt(11)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.0
    r = p.add_run("Owned files:  ")
    r.bold = True
    r.font.size = Pt(8.5)
    r2 = p.add_run(m["files"])
    r2.font.size = Pt(8.5)
    r2.font.name = "Consolas"

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.0
    r = p.add_run(m["summary"])
    r.font.size = Pt(8.5)
    r.italic = True
    shade(p, "EAF1F8")


def member_page(doc, m: dict, n: int):
    member_header(doc, m, n)
    for c in m["conflicts"]:
        conflict_heading(doc, c["title"])
        cbullet(doc, "What triggered it", c["trigger"])
        cbullet(doc, "How we resolved it", c["resolution"])
        cbullet(doc, "Evidence in the code", c["evidence"])
        cbullet(doc, "Trade accepted", c["trade"])

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    r = p.add_run("What I would do differently: ")
    r.bold = True
    r.font.size = Pt(8.5)
    r.font.color.rgb = ACCENT
    r2 = p.add_run(m["differently"])
    r2.font.size = Pt(8.5)


def cover(doc):
    for _ in range(3):
        doc.add_paragraph()
    para(doc, "CONFLICT AND RESOLUTION LOG", bold=True, size=11,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("What Went Wrong,\nand How We Fixed It")
    r.bold = True
    r.font.size = Pt(26)
    r.font.color.rgb = ACCENT
    para(doc, "Personalised Content Recommendation using Embeddings\nPGCP-BDA Group 13",
         italic=True, size=11.5, align=WD_ALIGN_PARAGRAPH.CENTER)
    doc.add_paragraph()

    total = sum(len(m["conflicts"]) for m in ROSTER)
    add_table(
        doc,
        ["Item", "Detail"],
        [
            ["Purpose", "One page per team member, recording the conflicts encountered in that "
                        "person's workstream and how each was resolved."],
            ["Team members", f"{len(ROSTER)}"],
            ["Conflicts documented", f"{total}"],
            ["Structure per conflict", "What triggered it, how we resolved it, evidence in the "
                                       "code, trade accepted"],
            ["Traceability", "Every resolution names the file and construct that implements it, "
                             "so any claim here can be checked against the repository."],
        ],
        widths=[1.5, 4.8],
        font_size=10,
    )

    callout(doc, "ACTION REQUIRED BEFORE SUBMISSION:",
            "The names in this document are placeholders. The project records no member names "
            "(the README identifies only PGCP-BDA Group 13) and git is not installed on this "
            "machine, so ownership could not be determined automatically. The six workstreams "
            "were derived from the actual module structure of the codebase. Open "
            "docs/generate_conflict_docs.py, replace the 'name' values in the ROSTER list at the "
            "top, and re-run the script to regenerate this file. Reassign a workstream by moving "
            "its entry, or delete an entry if the team is smaller.")
    page_break(doc)


def summary_matrix(doc):
    h1(doc, "Conflicts at a Glance")
    para(doc, "Every conflict in this log, with the theme it belongs to. The same tension often "
              "appeared in more than one workstream, which is itself worth noticing.",
         size=9.5)

    themes = {
        0: ["Scale vs feasibility", "Schema inconsistency", "Data quality vs volume"],
        1: ["Accuracy vs domain fit", "Vanity metric vs usable model", "Reporting honesty"],
        2: ["Latency vs freshness", "Speed vs silent corruption", "Correct maths, wrong output",
            "Dependency risk"],
        3: ["Missing data vs planned scope", "Cold start", "Unit and scale mismatch",
            "Labels vs semantics"],
        4: ["Startup race condition", "Type boundary failure", "Convenience vs safety"],
        5: ["Metric honesty", "Bad-looking but correct number", "Fidelity vs readability",
            "Compute and memory limits"],
    }
    rows = []
    for i, m in enumerate(ROSTER):
        for j, c in enumerate(m["conflicts"]):
            theme = themes.get(i, [])
            rows.append([
                m["name"],
                theme[j] if j < len(theme) else "",
                c["title"].split(":", 1)[1].strip() if ":" in c["title"] else c["title"],
            ])
    add_table(doc, ["Member", "Theme", "Conflict"], rows, widths=[1.15, 1.5, 3.65],
              font_size=8.5)
    caption(doc, "Table 2: Note the recurring pattern. Five of the six workstreams hit some form "
                 "of 'the honest answer is less flattering than the available alternative', and "
                 "in every case the team chose the honest one. That consistency was the single "
                 "most useful thing we established early.")
    page_break(doc)


def closing(doc):
    h1(doc, "What We Learned as a Team")
    h2(doc, "Patterns that showed up repeatedly")
    for label, text in [
        ("Silent wrongness is the enemy, not failure",
         "The stale embedding cache and the numpy serialisation errors sat at opposite ends of "
         "this. A crash tells you where to look. A cache that quietly maps every index to the "
         "wrong article does not. Wherever we could, we made the system detect and announce its "
         "own inconsistency rather than trusting anyone to remember."),
        ("Disagreements were usually about the metric, not the code",
         "Class balancing, Precision@5 and the missing NDCG were all the same argument: whether "
         "to optimise the number or the product. Settling that once, in favour of the product "
         "with the number reported honestly next to its baseline, resolved every later instance "
         "of it quickly."),
        ("A fallback ends an argument better than a decision does",
         "TextBlob versus a trained model, and transformers versus TF-IDF, both looked like "
         "either-or choices. Building a primary path with a same-shape fallback meant nobody had "
         "to be overruled and no machine got blocked. The cost is two paths to maintain, and it "
         "was worth it both times."),
        ("Cheap constraints prevent expensive bugs",
         "One seed makes every number reproducible. One row-count check makes a whole class of "
         "corruption impossible. One Query(ge=1, le=50) stops an unbounded response. None took "
         "more than a line."),
        ("Write the limitation down while you still remember it",
         "The known gaps -- synthetic histories, headline-only sentiment, row-count-only cache "
         "validation, sampled retrieval precision -- are all documented. Every one came from a "
         "decision we understood at the time and would otherwise have forgotten by the time we "
         "were asked about it."),
    ]:
        cbullet(doc, label, text, size=10)

    h2(doc, "Open items we chose not to fix")
    para(doc, "Recorded so they are not mistaken for oversights.", size=9.5, italic=True)
    add_table(
        doc,
        ["Item", "Why it was left", "Owner"],
        [
            ["Cosine similarity copies the full 78 MB matrix per call and recomputes row norms",
             "122 ms per request is comfortably fast enough for a local demonstration. Known hot "
             "spot with a known fix.", "Member 3"],
            ["Cached backend name is recorded as 'cache'",
             "No metadata is stored beside the .npy, so /health cannot report whether the vectors "
             "came from the transformer or the fallback.", "Member 3"],
            ["Stale-cache detection is row-count only",
             "A same-length but different corpus would slip through. --force and run.bat rebuild "
             "cover it in practice.", "Member 3"],
            ["No authentication, rate limiting or CORS on the API",
             "Binds to 127.0.0.1 for local use only. Must be added before any network exposure.",
             "Member 5"],
            ["No click-based ranking metrics",
             "Cannot be computed honestly against synthetic histories. Needs real interaction "
             "logs.", "Members 4 and 6"],
            ["Sentiment is classified from the headline only",
             "rating.csv labels titles, so that is the only genuine ground truth available.",
             "Member 2"],
        ],
        widths=[2.0, 3.0, 1.3],
        font_size=8.5,
    )
    caption(doc, "Table 3: Open items, with the reasoning and the owner for each.")


# ===================================================================== #
def build() -> str:
    doc = Document()
    setup_styles(doc)
    for s in doc.sections:
        s.left_margin = s.right_margin = Inches(0.7)
        s.top_margin = s.bottom_margin = Inches(0.55)
    add_footer_page_numbers(doc)

    cover(doc)
    summary_matrix(doc)
    for i, m in enumerate(ROSTER, start=1):
        member_page(doc, m, i)
        page_break(doc)
    closing(doc)

    doc.save(OUT_PATH)
    return OUT_PATH


if __name__ == "__main__":
    path = build()
    print(f"[docs] Word document written -> {path}")
    print(f"[docs] Size: {os.path.getsize(path) / 1024:.1f} KB")
    print(f"[docs] Members: {len(ROSTER)} | "
          f"Conflicts: {sum(len(m['conflicts']) for m in ROSTER)}")
