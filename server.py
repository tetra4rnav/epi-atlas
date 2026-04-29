import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("epi-atlas")

KNOWLEDGE_BASE_PATH = Path(__file__).parent / "knowledge-base" / "designs.json"

with KNOWLEDGE_BASE_PATH.open("r", encoding="utf-8") as f:
    DESIGNS = json.load(f)

KEYWORDS_BY_DESIGN = {
    "cross-sectional": [
        "prevalence",
        "snapshot",
        "at one time",
        "single time point",
        "cross-sectional",
    ],
    "cohort": [
        "incidence",
        "follow-up",
        "longitudinal",
        "prospective",
        "retrospective cohort",
        "risk over time",
    ],
    "case-control": [
        "rare disease",
        "rare outcome",
        "odds ratio",
        "cases and controls",
        "case control",
        "case-control",
    ],
    "ecological": [
        "population level",
        "country level",
        "regional",
        "aggregate data",
        "ecological",
        "policy comparison",
    ],
    "RCT": [
        "randomized",
        "randomised",
        "trial",
        "intervention",
        "efficacy",
        "rct",
    ],
    "natural experiment": [
        "policy change",
        "natural experiment",
        "quasi-experimental",
        "difference-in-differences",
        "instrumental variable",
        "exogenous shock",
    ],
}


@mcp.tool()
def get_study_design(research_question: str) -> dict:
    normalized_question = research_question.lower()
    scores = {design: 0 for design in KEYWORDS_BY_DESIGN}

    for design, keywords in KEYWORDS_BY_DESIGN.items():
        for keyword in keywords:
            if keyword in normalized_question:
                scores[design] += 1

    selected_design = max(scores, key=scores.get)

    if scores[selected_design] == 0:
        selected_design = "cross-sectional"

    return {
        "matched_design_key": selected_design,
        "matched_score": scores[selected_design],
        "design": DESIGNS[selected_design],
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
