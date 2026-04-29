import json
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("epi-atlas")

KNOWLEDGE_BASE_DIR = Path(__file__).parent / "knowledge-base"
DESIGNS_PATH = KNOWLEDGE_BASE_DIR / "designs.json"
DATASETS_PATH = KNOWLEDGE_BASE_DIR / "datasets.json"

with DESIGNS_PATH.open("r", encoding="utf-8") as f:
    DESIGNS = json.load(f)
with DATASETS_PATH.open("r", encoding="utf-8") as f:
    DATASETS = json.load(f)

@mcp.tool()
def get_study_design(research_question: str) -> dict:
    return {
        "research_question": research_question,
        "designs": DESIGNS,
    }


@mcp.tool()
def get_dataset_candidates(research_question: str) -> dict:
    return {
        "research_question": research_question,
        "datasets": DATASETS,
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
