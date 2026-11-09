# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：
- `--trace` で見えたツール呼び出し（ツール名と引数）：
- 1つの質問での LLM 呼び出し回数（`requests`）：
- 追加したツールと、docstring に書いた説明：

## 宿題

- 取り組んだレベル：基礎
- やったこと：app/agent.pyのINSTRUCTIONSを１箇所変更した。
　回答末尾に関連する回を示す指示を、「共通点」「違い」「復讐のヒント」の3項目で回答する指示に書き換えた。
- 結果：
同じ質問「LoRA と QLoRA の違いは？」を変更前後で実行した。

変更前の回答結果
[model] gemini-3.5-flash-lite
講座の用語集によると、LoRAとQLoRAの違いは以下のとおりです。

* **LoRA**
  事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法です。学習するパラメータが少なく、学習結果（アダプタ）も小さいファイルで保存できます。
* **QLoRA**
  ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法です。これにより、より大きなモデルを小さなGPUで扱うことができるようになります。

関係する回：第2回

--- trace --
[tool call]   search_glossary({'query': 'LoRA'})
[tool call]   search_glossary({'query': 'QLoRA'})
[tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
[tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…
[usage] RunUsage(cost=Decimal('0.0008194'), details={'text_prompt_tokens': 1198}, input_text_tokens=1198, input_tokens=1198, output_tokens=184, requests=2, tool_calls=2)

変更後の回答結果
[model] gemini-3.5-flash-lite
LoRAとQLoRAの違いについて、講座の用語集を基に以下の3つの項目で解説します。

### 共通点
* **目的と手法の根幹**: どちらも事前学習済みのベースモデルの重みを固定したまま、低ランク行列（アダプタ）の追加によって効率的にファインチューニングを行うPEFT（Parameter-Efficient Fine-Tuning）の手法です。
* **学習効率**: 大規模なモデル全体を更新するのではなく一部のパラメータだけを学習するため、計算コストやメモリを大幅に抑えて追加学習を行えます。

### 違い
* **ベースモデルの扱い（量子化）**: LoRAは通常の精度（通常は16ビットなど）のままベースモデルを保持して学習しますが、QLoRAはベースモデルの重みを4ビットなどに量子化（Quantization）してメモリ消費を極限まで抑えます。
* **GPUリソース要件**: QLoRAのほうがより少ないGPUメモリで大きなモデルを扱えるため、限られたハードウェア環境でも大規模モデルのファインチューニングが可能になります。

### 復習のヒント
* 第2回の講義（および演習）では、モデルのサイズやGPUのメモリ容量に応じてどちらの手法を採用すべきか、また4ビット量子化を行った際に出力やメモリにどのような影響があるのかを比較・確認しています。LoRAがどのように低ランク行列で重み更新を近似しているか、用語集の定義もあわせて見直してみましょう。

--- trace ---
[tool call]   search_glossary({'query': 'LoRA'})
[tool call]   search_glossary({'query': 'QLoRA'})
[tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
[tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…
[usage] RunUsage(cost=Decimal('0.0012617'), details={'text_prompt_tokens': 1214}, input_text_tokens=1214, input_tokens=1214, output_tokens=359, requests=2, tool_calls=2)

- 気づき・疑問：
今回の比較で、INSTRUCTIONSの1行を書き換えることで回答の構成が指示に沿って変わることが確認できた。
