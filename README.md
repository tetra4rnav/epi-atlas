# epi-atlas

Anthropic公式MCP Python SDKを使った、最小構成のMCPサーバーです。

## 仕様

- Transport: `stdio`
- Tool: `get_study_design`
- 引数: `research_question: str`
- 返り値: `"This is a test response"`（固定）

## セットアップ

```bash
python -m venv .venv
```

Windows (PowerShell):

```bash
.venv\Scripts\Activate.ps1
```

依存関係をインストール:

```bash
pip install -r requirements.txt
```

## サーバー起動（stdio）

```bash
python server.py
```

## Claude Desktop への登録

Claude Desktop の設定ファイル（`claude_desktop_config.json`）に、以下のように追記します。

Windows例:

```json
{
  "mcpServers": {
    "epi-atlas": {
      "command": "python",
      "args": ["C:/Users/jh1cid/Dev/epi-atlas/server.py"]
    }
  }
}
```

仮想環境のPythonを使う場合は、`command` を `.venv` のPython実行ファイルに変更してください。

## Confounders KBについて

`confounders.json` は preliminary です。PubMed MCP と組み合わせてリアルタイムの文献根拠を取得することを推奨します。
