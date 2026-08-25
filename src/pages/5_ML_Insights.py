import streamlit as st

from ui_utils import (
    setup_page,
    render_sidebar,
    render_header,
    render_footer,
    render_kpi_row,
    render_panel_header,
    load_ml_evaluation,
    load_feature_importance,
    load_model_comparison
)


setup_page("ML Insights", "🤖")
render_sidebar()

render_header(
    "Machine Learning Insights",
    "Model performance, feature importance and comparison"
)

evaluation = load_ml_evaluation()
importance = load_feature_importance()
comparison = load_model_comparison()


# ============================================================
# QUICK STATS FROM THE ML MODEL ROW (if present)
# ============================================================

ml_row = None

if "model" in evaluation.columns:
    matches = evaluation[
        evaluation["model"].astype(str).str.contains(
            "ML|Random Forest|Machine", case=False, na=False
        )
    ]
    if not matches.empty:
        ml_row = matches.iloc[0]

if ml_row is not None:

    def _pct(value):
        try:
            return f"{float(value) * 100:.1f}%"
        except (TypeError, ValueError):
            return "—"

    cards = []

    if "accuracy" in evaluation.columns:
        cards.append({
            "label": "Accuracy",
            "value": _pct(ml_row.get("accuracy")),
            "icon": "🎯",
            "variant": "blue",
        })

    if "precision" in evaluation.columns:
        cards.append({
            "label": "Precision",
            "value": _pct(ml_row.get("precision")),
            "icon": "📐",
            "variant": "success",
        })

    if "recall" in evaluation.columns:
        cards.append({
            "label": "Recall",
            "value": _pct(ml_row.get("recall")),
            "icon": "📡",
            "variant": "warning",
        })

    if "f1_score" in evaluation.columns:
        cards.append({
            "label": "F1 Score",
            "value": _pct(ml_row.get("f1_score")),
            "icon": "⚖️",
            "variant": "blue",
        })

    if cards:
        render_kpi_row(cards)
        st.write("")


# ============================================================
# TABBED CONTENT
# ============================================================

tab_eval, tab_features, tab_compare = st.tabs(
    ["📈 Model Evaluation", "🧬 Feature Importance", "⚖️ Rule-Based vs ML"]
)


with tab_eval:

    render_panel_header(
        "Model Evaluation",
        "Performance metrics for each model in the pipeline",
        icon="📈",
    )

    st.dataframe(
        evaluation,
        hide_index=True,
        width="stretch"
    )


with tab_features:

    render_panel_header(
        "Feature Importance",
        "Which signals the model relies on most",
        icon="🧬",
    )

    if not importance.empty:

        feature_col = importance.columns[0]
        importance_col = importance.columns[1]

        chart_data = importance.set_index(
            feature_col
        )[[importance_col]]

        st.bar_chart(chart_data)

        st.write("")

        st.dataframe(
            importance,
            hide_index=True,
            width="stretch"
        )


with tab_compare:

    render_panel_header(
        "Rule-Based vs ML",
        "Side-by-side comparison across all users",
        icon="⚖️",
    )

    st.dataframe(
        comparison.head(100),
        hide_index=True,
        width="stretch"
    )

render_footer()