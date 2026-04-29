# epi-atlas

Anthropic公式MCP Python SDKを使った、疫学研究向けのMCPサーバーです。  
疫学のResearch Question（RQ）に対して、研究デザイン・データセット・交絡因子の知識ベース情報を返します。

## プロジェクト概要

- 目的: 疫学RQの設計初期で必要な情報を構造化して返す
- 方式: サーバー側は知識ベースJSONを返却し、判断はClaude側で実施
- Transport: `stdio`
- 実装: Python + Anthropic MCP Python SDK（`mcp`）

## 利用可能なツール

> 現在実装されているツールは以下の3つです。

### `get_study_design(research_question: str)`

- 入力: `research_question`（文字列）
- 出力:
  - `research_question`
  - `designs`（`knowledge-base/designs.json` の全内容）

### `get_dataset_candidates(research_question: str)`

- 入力: `research_question`（文字列）
- 出力:
  - `research_question`
  - `datasets`（`knowledge-base/datasets.json` の全内容）

### `get_confounders(research_question: str)`

- 入力: `research_question`（文字列）
- 出力:
  - `research_question`
  - `kb_status`（`preliminary`）
  - `confounders`（`knowledge-base/confounders.json` の全内容）

## セットアップ（uvベース）

### 1) uvのインストール

```bash
pip install uv
```

### 2) 仮想環境の作成

```bash
uv venv
```

Windows (PowerShell):

```bash
.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
source .venv/bin/activate
```

### 3) 依存関係のインストール

```bash
uv pip install -r requirements.txt
```

## サーバー起動（stdio）

```bash
python server.py
```

## Claude Desktopへの登録方法

Claude Desktop の `claude_desktop_config.json` に `mcpServers` 設定を追加します。

### Windows例

```json
{
  "mcpServers": {
    "epi-atlas": {
      "command": "python",
      "args": ["[YOUR_PATH]/epi-atlas/server.py"]
    }
  }
}
```

### Mac例

```json
{
  "mcpServers": {
    "epi-atlas": {
      "command": "python3",
      "args": ["[YOUR_PATH]/epi-atlas/server.py"]
    }
  }
}
```

必要に応じて、`command` に仮想環境のPython実行ファイルを指定してください。

## Knowledge Baseについて

- `knowledge-base/designs.json`: 研究デザイン情報
- `knowledge-base/datasets.json`: データセット情報
- `knowledge-base/confounders.json`: 交絡因子情報
- `confounders.json` は `preliminary` ステータスです
- PubMed MCPと組み合わせて、リアルタイムの文献根拠を取得することを推奨します

## Contributing

- Issue / Pull Request を歓迎します
- 知識ベース更新のPRでは、根拠文献（DOI付き）の提示を必須とします
- `confounders.json` の `references` は、可能な限り査読済み文献で補強してください
