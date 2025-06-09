# BENCHY
> **体感できる**ベンチマーク
>
> 誰もがベンチマークを愛していますが、実際に触って感じるものに勝るものはありません。その中間点で出会えたらどうでしょうか？
> 
> BENCHYの登場です。特定のユースケースにおいて、LLMのパフォーマンス、価格、速度を並べて比較できる、リラックスしたライブベンチマークツールです。
>
> 最新の開発動画は[こちら](https://youtu.be/f8RnRuaxee8)でご覧ください

## プロジェクト構造

このプロジェクトは、フロントエンドとバックエンドが明確に分離されたフルスタックアプリケーションとして構成されています：

```
benchy/
├── client/                 # フロントエンド Vue.js アプリケーション
│   ├── src/               # Vue ソースコード
│   │   ├── apis/          # すべてのリクエスト用APIレイヤー
│   │   ├── components/    # Vue コンポーネント
│   │   ├── pages/         # フロントエンドのアプリページ
│   │   ├── stores/        # フロントエンドの状態とプロンプト
│   │   └── ...           # その他のソースファイル
│   ├── public/            # 静的アセット
│   ├── package.json       # フロントエンドの依存関係
│   ├── vite.config.ts     # Vite 設定
│   ├── uno.config.ts      # UnoCSS 設定
│   └── ...               # その他のフロントエンド設定ファイル
├── server/                # バックエンド Python サーバー
│   ├── modules/           # Python モジュール
│   ├── benchmark_data/    # ベンチマーク設定
│   ├── reports/          # ベンチマーク結果
│   ├── tests/            # Python テスト
│   ├── pyproject.toml    # Python 依存関係
│   ├── server.py         # メインサーバーファイル
│   ├── .env              # サーバー環境変数
│   └── ...               # その他のサーバーファイル
├── ai_docs/              # AI ドキュメント
├── images/               # プロジェクト画像
├── specs/                # プロジェクト仕様
├── trees/                # Git worktrees ディレクトリ
├── .env                  # ルート環境変数
├── start.sh              # 両サービスを起動する便利なスクリプト
└── ...                   # その他のプロジェクトファイル
```

### クイックスタート
```bash
# フロントエンドとバックエンドを一緒に起動
./start.sh
```

これにより以下が起動します：
- フロントエンド開発サーバー：`http://localhost:5173`（または次に利用可能なポート）
- バックエンドAPIサーバー：`http://localhost:8000`

<img src="./images/o3-mini.png" alt="deepseek-r1" style="max-width: 800px;">

<img src="./images/deepseek-r1.png" alt="deepseek-r1" style="max-width: 800px;">

<img src="./images/o1-ai-coding-limit-testing.png" alt="o1-ai-coding-limit-testing" style="max-width: 800px;">

<img src="./images/m4-max-mac-book-pro-benchmarked.png" alt="m4-mac-book-pro" style="max-width: 800px;">

<img src="./images/parallel-function-calling.png" alt="parallel-function-calling" style="max-width: 800px;">

<img src="./images/perf-price-speed-pick-two.png" alt="pick-two" style="max-width: 800px;">

## Benchy マイクロアプリ
- [Thought Bench](https://youtu.be/UgSGtBZnwEo)
  - 目標：複数の推論モデルを並行して比較し、思考プロセスと応答を分析する
  - デフォルトモデル：Anthropic Claude 4.0 Sonnet/Opus、OpenAI o4-mini/o3、Anthropic Claude 3.7 Sonnet、Gemini 2.5 Flash/Pro、Ollama Qwen3/Gemma3/Devstral
  - ウォークスルー動画は[こちら](https://youtu.be/UgSGtBZnwEo)でご覧ください
  - フロントエンド：[client/src/pages/ThoughtBench.vue](client/src/pages/ThoughtBench.vue)
- [Benchyへの大規模AIコーディングアップデート](https://youtu.be/y_ywOVQyafE)
  - ウォークスルー動画は[こちら](https://youtu.be/y_ywOVQyafE)でご覧ください
- [Iso Speed Bench](https://youtu.be/OwUm-4I22QI)
  - 目標：高品質な洞察と反復のための、統一された設定ファイルベースのマルチLLMプロバイダー、はい/いいえ評価ベースのベンチマークを作成する
  - o3-miniの雰囲気チェック、比較、ベンチマーク動画は[こちら](https://youtu.be/K5xs669ANQo)でご覧ください
  - M4開封とベンチマーク動画は[こちら](https://youtu.be/OwUm-4I22QI)でご覧ください
  - フロントエンド：[client/src/pages/IsoSpeedBench.vue](client/src/pages/IsoSpeedBench.vue)
- [長いツール呼び出し](https://youtu.be/ZlljCLhq814)
  - 目標：長いツール呼び出し/関数呼び出しのチェーン（15以上）に最適なLLMとテクニックを理解する
  - ウォークスルー動画は[こちら](https://youtu.be/ZlljCLhq814)でご覧ください
  - フロントエンド：[client/src/pages/AppMultiToolCall.vue](client/src/pages/AppMultiToolCall.vue)
- [マルチオートコンプリート](https://youtu.be/1ObiaSiA8BQ)
  - 目標：[claude 3.5 haiku](https://www.anthropic.com/claude/haiku)とGPT-4oの[予測出力](https://platform.openai.com/docs/guides/predicted-outputs)を既存のモデルと比較して理解する
  - ウォークスルー動画は[こちら](https://youtu.be/1ObiaSiA8BQ)でご覧ください
  - フロントエンド：[client/src/pages/AppMultiAutocomplete.vue](client/src/pages/AppMultiAutocomplete.vue)

## 重要なファイル

### フロントエンド (client/)
- `client/package.json` - フロントエンドの依存関係とスクリプト
- `client/src/stores/*` - すべてのフロントエンド状態とプロンプトを保存
- `client/src/apis/*` - すべてのリクエスト用APIレイヤー
- `client/src/pages/*` - フロントエンドのアプリページ
- `client/src/components/*` - Vue コンポーネント
- `client/vite.config.ts` - Vite ビルド設定
- `client/uno.config.ts` - UnoCSS 設定

### バックエンド (server/)
- `server/server.py` - メインサーバールートとAPIエンドポイント
- `server/pyproject.toml` - Python 依存関係
- `server/modules/llm_models.py` - すべてのLLMモデル定義
- `server/modules/openai_llm.py` - OpenAI 統合
- `server/modules/anthropic_llm.py` - Anthropic 統合
- `server/modules/gemini_llm.py` - Google Gemini 統合
- `server/modules/ollama_llm.py` - Ollama 統合
- `server/modules/deepseek_llm.py` - Deepseek 統合
- `server/benchmark_data/*` - ベンチマーク設定ファイル
- `server/reports/*` - 生成されたベンチマーク結果

### 設定
- `.env` - APIキー用のルート環境変数
- `server/.env` - サーバー固有の環境変数
- `start.sh` - 両サービスを起動する便利なスクリプト
- `.claude/` - Claude Code 設定とコマンド
  - `.claude/settings.local.json` - Claude Code の権限と設定
  - `.claude/commands/prime.md` - プロジェクトコンテキスト用のカスタムClaudeコマンド

## セットアップ

### APIキーとモデルの取得
- [Anthropic](https://docs.anthropic.com/en/api/getting-started)
- [Google Cloud](https://ai.google.dev/gemini-api/docs/api-key)
- [OpenAI](https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key)
- [Deepseek](https://platform.deepseek.com/)
- [Ollama](https://ollama.ai/download)
  - Ollamaをインストール後、必要なモデルをプルします：
  ```bash
  # Llama 3.2 1B モデルをプル
  ollama pull llama3.2:1b
  
  # Llama 3.2 最新版 (3B) モデルをプル
  ollama pull llama3.2:latest
  
  # Qwen2.5 Coder 14B モデルをプル
  ollama pull qwen2.5-coder:14b

  # Deepseek R1 1.5B, 7b, 8b, 14b, 32b, 70b モデルをプル
  ollama pull deepseek-r1:1.5b
  ollama pull deepseek-r1:latest
  ollama pull deepseek-r1:8b
  ollama pull deepseek-r1:14b
  ollama pull deepseek-r1:32b
  ollama pull deepseek-r1:70b

  # mistral-small 3 をプル
  ollama pull mistral-small:latest

  # Phi-4 モデルをプル
  ollama pull phi4:latest

  # Falcon 3 10B モデルをプル
  ollama pull falcon3:10b

  # Qwen 3 14B モデルをプル
  ollama pull qwen3:14b

  # Gemma 3 4B モデルをプル
  ollama pull gemma3:4b

  # Devstral モデルをプル
  ollama pull devstral
  ```

### フロントエンドセットアップ (client/)
```bash
# clientディレクトリに移動
cd client

# bun を使用して依存関係をインストール（推奨）
bun install

# またはnpmを使用
npm install

# またはyarnを使用
yarn install

# 開発サーバーを起動
bun dev  # または npm run dev / yarn dev
```

### バックエンドセットアップ (server/)
```bash
# serverディレクトリに移動
cd server

# uvを使用して仮想環境を作成・有効化
uv sync

# 環境変数を設定
cp ../.env.sample ../.env  # ルート.envファイル
cp .env.sample .env        # サーバー.envファイル

# 両方のファイルですべての.envキーをAPIキーと設定で設定
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
GEMINI_API_KEY=
DEEPSEEK_API_KEY=
FIREWORKS_API_KEY=

# サーバーを起動
uv run python server.py

# テストを実行
uv run pytest (**注意：APIを使用するため料金が発生します**)
```

### 開発ワークフロー
```bash
# 両方のサービスを一度に起動（推奨）
./start.sh

# または別々のターミナルで個別に起動：
# ターミナル1：フロントエンド
cd client && bun dev

# ターミナル2：バックエンド  
cd server && uv run python server.py
```

### Claude Code 統合

このプロジェクトには、開発体験を向上させるClaude Code設定が含まれています：

- **カスタムコマンド**：Claude Codeで`/prime`コマンドを使用してプロジェクトコンテキストを素早く読み込む
- **権限**：一般的な開発タスク（mkdir、mv、ls）用の事前設定された権限
- **プロジェクトコンテキスト**：`.claude/commands/prime.md`ファイルは自動的に主要なプロジェクトファイルを読み込み、ディレクトリ構造を表示します

Claude Codeで使用するには：
1. Claude Codeでプロジェクトを開く
2. `/prime`と入力してプロジェクトコンテキストを読み込む
3. Claudeはコードベース構造と主要ファイルを即座に理解します

## リソース
- https://github.com/simonw/llm?tab=readme-ov-file
- https://github.com/openai/openai-python
- https://platform.openai.com/docs/guides/predicted-outputs
- https://community.openai.com/t/introducing-predicted-outputs/1004502
- https://unocss.dev/integrations/vite
- https://www.npmjs.com/package/vue-codemirror6
- https://vuejs.org/guide/scaling-up/state-management
- https://www.ag-grid.com/vue-data-grid/getting-started/
- https://www.ag-grid.com/vue-data-grid/value-formatters/
- https://llm.datasette.io/en/stable/index.html
- https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/get-token-count
- https://ai.google.dev/gemini-api/docs/tokens?lang=python
- https://ai.google.dev/pricing#1_5flash
- https://ai.google.dev/gemini-api/docs/structured-output?lang=python
- https://platform.openai.com/docs/guides/structured-outputs
- https://docs.anthropic.com/en/docs/build-with-claude/tool-use
- https://ai.google.dev/gemini-api/docs/models/experimental-models
- https://sqlparse.readthedocs.io/en/latest/intro.html
- mlx: https://huggingface.co/mlx-community
- ollama docs: https://github.com/ollama/ollama/blob/main/docs/api.md#examples
- deepseek docs: https://platform.deepseek.com/usage

## マルチエージェント Git Worktree

### なぜ並列で実行するのか

LLMは非決定論的な確率マシンです - 実行するたびに異なる結果が生成されます。

これはバグではなく機能です。これを活用して**複数の未来のバージョン**を見て、**最良の結果を選択**できます。

複数のAIエージェントを別々のgit worktreeで並列実行することで、以下が可能になります：

#### #1
複数の結果を持つ複雑なタスクでのモデル失敗に対するヘッジ（スタートアップやビッグテックはこれを常に行っています）

#### #2
同じ問題に対する異なる視点を得る - 最良の実装を選択

#### #3
エンジニアリング作業を2〜Nのエージェントに分離して委任

### 仕組み

Git worktreeを使用すると、コードベース全体を新しいブランチとディレクトリに複製できます：

```bash
# worktree用のディレクトリを作成
mkdir trees

# UI改善のための3つの並列worktreeを作成
git worktree add -b ui_revamp-1 trees/ui_revamp-1
git worktree add -b ui_revamp-2 trees/ui_revamp-2
git worktree add -b ui_revamp-3 trees/ui_revamp-3

# 各worktreeに環境変数をコピー
cp .env trees/ui_revamp-1/
cp .env trees/ui_revamp-2/
cp .env trees/ui_revamp-3/
```

その後、各worktreeで同じ計画/プロンプトを使用して別々のAIエージェント（Claude Codeなど）を実行します。各エージェントは独立して作業し、異なるバリエーションを生成します。

### このテクニックを使用する時

1. **複数の満足できる結果**：多くのバージョンが受け入れ可能なUI作業に最適
2. **失敗リスクのある複雑なタスク**：1つのエージェントが失敗する可能性がある場合、3つ実行して勝者を選ぶ
3. **明確な計画がある時**：計画がプロンプトです - 詳細な計画により並列実行が可能

### 大きなアイデア

- **非決定論は機能**：異なるバージョンが選択肢を提供
- **計画がプロンプト**：優れた計画 = 優れたプロンプト
- **スケール計算 = スケール影響**：より多くのトークンを使用してより多くの可能性を見る
- **選択とマージ**：最良のバージョンを選択するか、複数から要素を組み合わせる

この高度なテクニックには大量のトークン（実行あたりドル単位）を消費しますが、以下が可能になります：
- 複数のタイムラインで同時に作業
- 同じ問題に対する異なる視点を得る
- 開発速度を劇的に向上
- 文字通り、複数の未来のバージョンを見る

AIモデルが改善されるにつれて、この並列アプローチは大規模にその能力を活用するためにますます強力になります。

## マスターAIコーディング
[Principles of AI Coding](https://agenticengineer.com/principled-ai-coding?y=benchy)でAIを使ったコーディングを学習しましょう

より多くのAIコーディングのヒントとトリックについては、[IndyDevDan YouTubeチャンネル](https://www.youtube.com/@indydevdan)をフォローしてください。