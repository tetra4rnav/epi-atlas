# epi-atlas: Concept Sheet
**Version**: 0.1 (Draft)  
**Date**: 2026-04-29  
**Author**: Matt Sakamaki  
**Status**: Living document — to be updated as development progresses

---

## 1. Background and Motivation

### 1.1 Problem Statement

Epidemiological research requires a series of methodological decisions before any analysis can begin: selecting an appropriate study design, identifying suitable data sources, operationalizing exposures and outcomes, and anticipating major sources of confounding and bias. This process is time-consuming, requires substantial domain expertise, and is rarely supported by integrated tooling.

Existing resources are fragmented:
- Study design guidance exists in textbooks and guidelines (e.g., STROBE, JBI) but is not queryable
- Data catalogs (e.g., data.gov, healthdata.gov) list datasets but do not map them to research questions
- General-purpose LLMs (e.g., ChatGPT, Claude) can discuss epidemiology but hallucinate variable names and dataset-specific details
- No tool integrates study design recommendation, dataset discovery, and confounder identification in a single workflow

### 1.2 Target Users

- MPH students and epidemiology trainees
- Public health researchers at academic institutions
- Global health practitioners designing studies in resource-limited settings
- Eventually: wider public health community (US-first, expanding to Japan and globally)

### 1.3 Gap in the Literature

A review of existing tools confirms no integrated solution exists that:
1. Accepts a free-text research question (RQ)
2. Recommends appropriate study designs with rationale
3. Identifies relevant datasets with variable-level detail
4. Surfaces major confounders with literature-based justification

This gap has been acknowledged in the epidemiological literature. AI tools relevant to epidemiological study support remain scarce, and tools that validate study design or dataset selection are not yet widely available (cf. automated-epidemiology, Springer Current Epidemiology Reports 2025).

---

## 2. Tool Design

### 2.1 Core Functionality

Given a free-text research question, epi-atlas currently returns structured catalogs (not server-side recommendations):

1. **Study design catalog** — full `designs.json` with description, strengths, limitations, and when to use
2. **Dataset catalog** — full `datasets.json` with access information, unit of analysis, and key domains
3. **Confounder catalog** — full `confounders.json` (preliminary seeds with review metadata)

### 2.2 Design Philosophy

**Transparency over automation**  
epi-atlas does not make decisions for the researcher. It surfaces structured information and reasoning support, leaving methodological judgment to the user. All outputs are labeled with their evidence status (e.g., `kb_status: "preliminary"`).

**Evidence-based knowledge base**  
The knowledge base (KB) is designed to be justified by peer-reviewed literature. In the current phase, confounder seed entries reflect textbook-level consensus. Full evidence mapping will follow a Scoping Review methodology (see Section 5).

**Separation of concerns**  
The server returns structured KB content. Reasoning and synthesis are performed by the LLM (Claude) on the client side. This separation:
- Avoids hallucination of variable names and dataset details
- Keeps server-side logic minimal and auditable
- Allows the KB to be updated independently of the server logic

**Community maintainability**  
The KB is stored as plain JSON in a public GitHub repository. Contributions require cited evidence (DOI). Non-engineers (e.g., epidemiologists) can contribute by editing JSON files and submitting pull requests.

---

## 3. Architecture

### 3.1 Overview

epi-atlas is implemented as a **Model Context Protocol (MCP) server** — a lightweight extension to Claude Desktop and compatible AI agents.

```
User (Claude Desktop)
  │
  ├── epi-atlas MCP Server (this project)
  │     └── Returns structured KB content (designs, datasets, confounders)
  │
  └── Data Commons MCP Server (Google, hosted)
        └── Returns aggregated statistical variables for area-level data
```

The two MCP servers operate in parallel. Claude integrates their outputs.

### 3.2 epi-atlas MCP Server

- **Language**: Python
- **Framework**: Anthropic MCP Python SDK (`mcp`)
- **Transport**: stdio (local process)
- **Distribution**: local Python script execution (`python server.py`) via Claude Desktop MCP registration

**Tools exposed:**

| Tool | Input | Output |
|---|---|---|
| `get_study_design` | `research_question: str` | Full `designs.json` content + RQ |
| `get_dataset_candidates` | `research_question: str` | Full `datasets.json` content + RQ |
| `get_confounders` | `research_question: str` | `kb_status` + full `confounders.json` content + RQ |

### 3.3 Knowledge Base

Stored as versioned JSON files under `knowledge-base/`:

```
knowledge-base/
├── designs.json         # Study design catalog
├── datasets.json        # Dataset catalog (US-first)
└── confounders.json     # Confounder catalog by domain
```

Each file is human-editable and PR-reviewable.

### 3.4 Current Local Operation (README-aligned)

- Create a virtual environment and install dependencies from `requirements.txt`
- Start MCP server in stdio mode with `python server.py`
- Register in Claude Desktop via `claude_desktop_config.json`:
  - `command`: `python`
  - `args`: path to `server.py`
- `confounders.json` is explicitly preliminary; users should combine with PubMed MCP for real-time evidence lookup
### 3.5 External Integration

**Google Data Commons MCP** (parallel, not called by epi-atlas directly):
- Provides 200,000+ statistical variables from CDC, World Bank, US Census, and others
- Suited for area-level / ecological study designs
- Complements epi-atlas's individual-level dataset guidance (e.g., NHANES)

**PubMed MCP** (parallel):
- Used to retrieve real-time literature evidence for confounder justification
- Addresses the limitation that hardcoded confounder lists cannot be geographically or culturally exhaustive

---

## 4. Knowledge Base Design Decisions

### 4.1 Why Static JSON (not a database)

- Zero infrastructure cost: no server, no database, no authentication
- GitHub serves as the CMS: versioned, diffable, PR-reviewable
- Non-engineers can contribute by editing JSON
- Suitable for data that changes on the order of months to years (dataset access policies, study design consensus)

**Acknowledged limitation**: Static KB requires manual update when dataset policies change. Mitigation: `last_verified` field in each entry; GitHub Actions to check URL liveness weekly.

### 4.2 Why LLM Reasoning (not keyword matching)

Early prototyping used keyword matching to map RQs to designs and datasets. This was replaced because:
- Epidemiological concepts have too many synonyms ("diabetes" / "glycemic control" / "HbA1c" / "insulin resistance")
- Keyword lists cannot be exhaustively maintained
- LLMs handle semantic equivalence natively

Current approach: server returns full KB content; Claude performs reasoning. This is auditable (KB content is visible) and avoids the false precision of scoring algorithms.

### 4.3 Why Python (not TypeScript)

The primary contributor base is expected to be epidemiologists and public health researchers, for whom Python is the dominant programming environment (alongside R). Python was chosen to lower the barrier to contribution for the target community.

---

## 5. Evidence Strategy for the Knowledge Base

### 5.1 Current Status

`confounders.json` entries are currently labeled `kb_status: "preliminary"` with `review_method: "pending_scoping_review"` and `last_verified` metadata. Seed confounders reflect textbook-level consensus (e.g., Rothman, Szklo & Nieto). No systematic search has been conducted.

### 5.2 Planned Methodology: Scoping Review

To justify KB content for academic publication, a Scoping Review will be conducted following:
- **JBI methodology for scoping reviews** (Peters et al.)
- **PRISMA-ScR** (Tricco et al., 2018, *Annals of Internal Medicine*)

Scope: For each disease/exposure domain in `confounders.json`, identify the set of confounders most commonly adjusted for in observational epidemiological studies, as reported in systematic reviews and large cohort studies.

**Protocol pre-registration**: OSF (Open Science Framework) — planned post-Capstone (August 2026)

### 5.3 Handling Incompleteness

Entries missing literature support are retained with `kb_status: "preliminary"` and `references: []`. Users are informed via:
- README disclaimer
- `get_confounders` tool response (`kb_status`)
- Recommendation to cross-reference PubMed MCP for real-time literature

This approach follows the precedent of Wikipedia and systematic review databases: transparency about what is and is not known is preferable to false completeness.

### 5.4 Geographic and Cultural Diversity

Hardcoded confounders cannot reflect geographic or cultural variation (e.g., diet-disease relationships differ across populations). Mitigation:
- PubMed MCP integration for real-time, context-specific literature retrieval
- Future KB expansion to include region-specific entries (US, Japan, global)
- Community contributions from domain experts in different regions

---

## 6. Relation to Existing Tools

| Tool | Overlap | Difference |
|---|---|---|
| CDC NHANES Variable Search | Dataset-specific variable lookup | No RQ input, no design recommendation |
| nhanesA (R package) | NHANES data retrieval | No AI integration, no design guidance |
| Google Data Commons MCP | Statistical variable access | Area-level only, no study design support |
| ChatGPT / Claude (general) | Study design discussion | No structured KB, hallucination risk for variable names |
| OHDSI Atlas | Observational study cohort definition | Clinical data only, no general epi support |

epi-atlas occupies a distinct niche: **integrated, evidence-anchored, LLM-augmented research design support for public health researchers**.

---

## 7. Publication Strategy

### 7.1 Intended Contribution

A methods/tool paper describing:
1. The design and architecture of epi-atlas
2. The KB construction methodology (Scoping Review)
3. A validation study assessing tool usefulness among MPH students / epidemiologists

### 7.2 Target Journals (preliminary)

- *Journal of Medical Internet Research* (JMIR) — digital health tools
- *JAMIA* — medical informatics / tool development
- *International Journal of Epidemiology* — epidemiological methods
- *PLOS ONE* — open access, methods papers

### 7.3 Timeline

| Phase | Target |
|---|---|
| Prototype development | April–May 2026 |
| Scoping Review protocol + OSF pre-registration | September 2026 |
| KB evidence population | October–December 2026 |
| Validation study (user study at JHU) | Early 2027 |
| Manuscript submission | Mid 2027 |

---

## 8. Open Questions and Known Limitations

```
- KB coverage is US-centric in Phase 1; Japan (e-Stat) and global expansion planned
- NHANES individual-level variable catalog: manual curation needed (API-based update planned)
- Confounder KB is preliminary; Scoping Review pending
- No formal validation of tool accuracy or usefulness yet conducted
- MCP ecosystem is nascent; long-term compatibility with Claude Desktop not guaranteed
- Geographic and cultural variation in confounders not yet addressed
- PECO/PICO output format: identified as desirable feature, not yet implemented
- README "仕様" section still reflects an early prototype and should be synchronized with current 3-tool implementation
```

---

## 9. Repository

**GitHub**: https://github.com/tetra4rnav/epi-atlas  
**License**: MIT  
**Language**: Python  
**Distribution**: pip / uv  

---

*This document is a living research note. It will be updated to reflect architectural decisions, KB methodology refinements, and publication planning as the project develops.*
