# 第6回 解答

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前：glossary_search_glossary
- STEP 2 の [tool call]：glossary_search_glossary({'query': '3レベル'})
- STEP 3 の [tool call]：fetch_fetch({'url': 'https://modelcontextprotocol.io/'})
- STEP 4 の [tool call]：aws_aws___search_documentation({'topics': ['general'], 'search_phrase': 'Amazon S3 バージョニング 概要'})
 aws_aws___search_documentation({'topics': ['general'], 'search_phrase': 'Using versioning in S3 buckets'})
- 気づき・疑問：STEP 2 に比べて、STEP 4 は入力のトークン数がとても多かった。ツールが増えたからなのか、検索結果が長かったからなのかが気になった。

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：基礎
- やったこと：app/mcp_server.py に server.tool()(tools.get_lecture_summary) を1行書き足した。
- 結果：list-tools でツールが7個から8個になり、glossary_get_lecture_summary が増えた。「第2回では何を学びますか？」と聞くと glossary_get_lecture_summary({'lecture': 2}) が呼ばれ、第2回（ファインチューニングとLoRA）の内容を答えた。
- 気づき・疑問：サーバー側に1行足すだけで、エージェントを変えなくても新しいツールが使えた。
