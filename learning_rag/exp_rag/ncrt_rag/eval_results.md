(ncrt-rag) PS C:\Users\vempa\learnning_rag\exp_rag\ncrt_rag> uv run ncrt.py
C:\Users\vempa\learnning_rag\exp_rag\ncrt_rag\ncrt.py:1: DeprecationWarning: `langchain-community` is being sunset and is no longer actively maintained. See https://github.com/langchain-ai/langchain-community/issues/674 for details and migration guidance toward standalone integration packages.
  from langchain_community.document_loaders import PyPDFLoader
158
{'producer': 'Adobe Acrobat (64-bit) 26.1.21367', 'creator': 'Adobe Acrobat (64-bit) 26.1.21367', 'creationdate': '2026-04-07T17:14:35+05:30', 'moddate': '2026-04-07T17:14:43+05:30', 'title': '', 'source': './knowledge/ncrt_book.pdf', 'total_pages': 40, 'page': 0, 'page_label': '1'}
<langchain_chroma.vectorstores.Chroma object at 0x000001D8978262A0>
==================================================
2.1 Simple Expressions
You may have seen mathematical phrases like 13 + 2, 20 – 4, 12 × 5, and 
18 ÷ 3. Such phrases are called arithmetic expressions. 
Every arithmetic expression has a value which is the number it 
evaluates to. For example, the value of the expression 13 + 2 is 15. This 
expression can be read as ‘13 plus 2’ or ‘the sum of 13 and 2’.
We use the equality sign ‘=’ to denote the relationship between an 
arithmetic expression and its value. For example:
13 + 2 = 15.
{'page': 0, 'page_label': '1', 'creator': 'Adobe Acrobat (64-bit) 26.1.21367', 'producer': 'Adobe Acrobat (64-bit) 26.1.21367', 'total_pages': 40, 'title': '', 'source': './knowledge/ncrt_book.pdf', 'creationdate': '2026-04-07T17:14:35+05:30', 'moddate': '2026-04-07T17:14:43+05:30'}
==================================================
Arithmetic Expressions
45
 
Expression Engineer!
Using three 3’s along with the four operations (addition, subtraction, 
multiplication, and division) and brackets as needed we can create 
several expressions. For example, (3 + 3)/3 = 2, 3 + 3 – 3 = 3, 3 × 
3 + 3 = 12, and so on.
Using four 4’s, create expressions to get all values from 1 to 20.
Using the numbers 1, 2, 3, 4, and 5 exactly once in any order get 
as many values as possible between  – 10 and +10.
{'creationdate': '2026-04-07T17:14:35+05:30', 'page_label': '22', 'moddate': '2026-04-07T17:14:43+05:30', 'creator': 'Adobe Acrobat (64-bit) 26.1.21367', 'page': 21, 'source': './knowledge/ncrt_book.pdf', 'total_pages': 40, 'producer': 'Adobe Acrobat (64-bit) 26.1.21367', 'title': ''}
==================================================
Arithmetic Expressions
29
Expression Expression as the sum of its terms Terms
13 – 2 + 6 13 – 2+ 6+ 13, – 2, 6
5 + 6 × 3 5 6 × 3+
4 + 15 – 9 + +
23 – 2 × 4 + 16 + +
28 + 19 – 8 + +
Now we will see how terms are used to determine the order of 
operations to find the value of an expression. 
We will start with expressions having only additions (with all the 
subtractions suitably converted into additions).
Does changing the order in which the terms are added give different 
values?
{'page_label': '6', 'title': '', 'producer': 'Adobe Acrobat (64-bit) 26.1.21367', 'moddate': '2026-04-07T17:14:43+05:30', 'creator': 'Adobe Acrobat (64-bit) 26.1.21367', 'total_pages': 40, 'page': 5, 'source': './knowledge/ncrt_book.pdf', 'creationdate': '2026-04-07T17:14:35+05:30'}
==================================================
Arithmetic Expressions
27
Without knowing the context behind this expression, Purna found 
the value of this expression to be 140. He added 30 and 5 first, to get 35, 
and then multiplied 35 by 4 to get 140.
Mallesh found the value of this expression to be 50. He multiplied 5 
and 4 first to get 20 and added 20 to 30 to get 50. 
In this case, Mallesh is right. But why did Purna get it wrong? 
Just looking at the expression 30 + 5 × 4, it is not clear whether we
{'page_label': '4', 'source': './knowledge/ncrt_book.pdf', 'creationdate': '2026-04-07T17:14:35+05:30', 'page': 3, 'creator': 'Adobe Acrobat (64-bit) 26.1.21367', 'total_pages': 40, 'title': '', 'moddate': '2026-04-07T17:14:43+05:30', 'producer': 'Adobe Acrobat (64-bit) 26.1.21367'}
✨ You're running DeepEval's latest Faithfulness Metric! (using gemini-2.5-flash, strict=False, async_mode=True)...

╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ 🚀 DeepEval Evaluation Results                                                                                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ ✅ test_case_0 (Passed 1 metrics)                                                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Aggregate Metrics                                                                                                                                        │
│                                                                                                                                                          │
│  Metric                         ┃ Average Score                    ┃ Pass Rate                                                          ┃ Total          │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━ │
│  Faithfulness                   │ 1.00                             │ 100.00% | passed=1 | failed=0                                      │ 1              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯


⚠ WARNING: No hyperparameters logged.
» Log hyperparameters to attribute prompts and models to your test runs.

================================================================================


✓ Evaluation completed 🎉! (time taken: 33.39s | token cost: None)
» Test Results (1 total tests):
   » Pass Rate: 100.0% | Passed: 1 | Failed: 0

 ================================================================================ 

» Want to share evals with your team, or a place for your test cases to live? ❤️ 🏡
  » Run 'deepeval view' to analyze and save testing results on Confident AI.


✨ You're running DeepEval's latest Answer Relevancy Metric! (using gemini-2.5-flash, strict=False, async_mode=True)...

╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ 🚀 DeepEval Evaluation Results                                                                                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ ✅ test_case_0 (Passed 1 metrics)                                                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Aggregate Metrics                                                                                                                                        │
│                                                                                                                                                          │
│  Metric                               ┃ Average Score                  ┃ Pass Rate                                                       ┃ Total         │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━ │
│  Answer Relevancy                     │ 1.00                           │ 100.00% | passed=1 | failed=0                                   │ 1             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯


⚠ WARNING: No hyperparameters logged.
» Log hyperparameters to attribute prompts and models to your test runs.

================================================================================


✓ Evaluation completed 🎉! (time taken: 15.75s | token cost: None)
» Test Results (1 total tests):
   » Pass Rate: 100.0% | Passed: 1 | Failed: 0

 ================================================================================ 

» Want to share evals with your team, or a place for your test cases to live? ❤️ 🏡
  » Run 'deepeval view' to analyze and save testing results on Confident AI.


✨ You're running DeepEval's latest Contextual Precision Metric! (using gemini-2.5-flash, strict=False, async_mode=True)...

╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ 🚀 DeepEval Evaluation Results                                                                                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ ✅ test_case_0 (Passed 1 metrics)                                                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Aggregate Metrics                                                                                                                                        │
│                                                                                                                                                          │
│  Metric                                     ┃ Average Score                ┃ Pass Rate                                                    ┃ Total        │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━ │
│  Contextual Precision                       │ 1.00                         │ 100.00% | passed=1 | failed=0                                │ 1            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯


⚠ WARNING: No hyperparameters logged.
» Log hyperparameters to attribute prompts and models to your test runs.

================================================================================


✓ Evaluation completed 🎉! (time taken: 36.47s | token cost: None)
» Test Results (1 total tests):
   » Pass Rate: 100.0% | Passed: 1 | Failed: 0

 ================================================================================ 

» Want to share evals with your team, or a place for your test cases to live? ❤️ 🏡
  » Run 'deepeval view' to analyze and save testing results on Confident AI.


✨ You're running DeepEval's latest Contextual Recall Metric! (using gemini-2.5-flash, strict=False, async_mode=True)...

╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ 🚀 DeepEval Evaluation Results                                                                                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ ✅ test_case_0 (Passed 1 metrics)                                                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Aggregate Metrics                                                                                                                                        │
│                                                                                                                                                          │
│  Metric                                 ┃ Average Score                 ┃ Pass Rate                                                      ┃ Total         │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━ │
│  Contextual Recall                      │ 1.00                          │ 100.00% | passed=1 | failed=0                                  │ 1             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯


⚠ WARNING: No hyperparameters logged.
» Log hyperparameters to attribute prompts and models to your test runs.

================================================================================


✓ Evaluation completed 🎉! (time taken: 10.54s | token cost: None)
» Test Results (1 total tests):
   » Pass Rate: 100.0% | Passed: 1 | Failed: 0

 ================================================================================ 

» Want to share evals with your team, or a place for your test cases to live? ❤️ 🏡
  » Run 'deepeval view' to analyze and save testing results on Confident AI.


✨ You're running DeepEval's latest Contextual Relevancy Metric! (using gemini-2.5-flash, strict=False, async_mode=True)...

╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ 🚀 DeepEval Evaluation Results                                                                                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ ✅ test_case_0 (Passed 1 metrics)                                                                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Aggregate Metrics                                                                                                                                        │
│                                                                                                                                                          │
│  Metric                                     ┃ Average Score                ┃ Pass Rate                                                    ┃ Total        │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━ │
│  Contextual Relevancy                       │ 0.50                         │ 100.00% | passed=1 | failed=0                                │ 1            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯


⚠ WARNING: No hyperparameters logged.
» Log hyperparameters to attribute prompts and models to your test runs.

================================================================================


✓ Evaluation completed 🎉! (time taken: 49.36s | token cost: None)
» Test Results (1 total tests):
   » Pass Rate: 100.0% | Passed: 1 | Failed: 0

 ================================================================================ 

» Want to share evals with your team, or a place for your test cases to live? ❤️ 🏡
  » Run 'deepeval view' to analyze and save testing results on Confident AI.


(ncrt-rag) PS C:\Users\vempa\learnning_rag\exp_rag\ncrt_rag> 