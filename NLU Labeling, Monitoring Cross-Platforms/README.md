# SNA-AH-NLU-Labeling-Cross-Platforms
Natural Language Understanding, Processing, and Sentiment Testing across social media platforms on AH data using Scientific Methods

- Twitter, Reddit. Instagram, YouTube, Change.org, Facebook
<br><b>NLU engines, monitoring, classifications, training.</b>

<i>Data used in NLU Testing Analysis is in /Testing Data folder</i>
Dashboard files show of using programs to run the monitoring bot. Monitoring js files are included.

<b>Natural Language Understanding:</b>
- A BERT File under config shows BERT for Amber Heard NLP training
- There are Dashboard code files in Javascript. The requirements are Reactjs, javascript, and Django languages
- Package examples and how to train NLU is included
- Supporters and Offenders are marked by the numbers of tweets using the NLU classifications

There is an NLU dashboard tester using the api for the trained NLU.

<b>Requirements of NluEngine:</b>
- pytorch-lightning >= 0.9.0
- torch >= 1.7.0
- transformers >= 3.2.0
- kaggle >= 1.5.8
- pandas >= 1.1.2
- scikit-learn >= 0.23.2
- datasets >= 1.0.2
- tqdm == 4.41.0
- sentencepiece >= 0.1.94
- 2nd Requirements file included

Version NLU Trained on Data from: Twitter, Facebook, Change.org primarily with some YouTube and Reddit
1. First example (old nlpengine) is 2 classifications only of love or hate - quickly seen as not accurate and to move to an offense, defense, support strategy
2. Second example, more accurate for nlp engine is multiclassifier - support, offense, defense, defense_against (focused on victim - target of operations)
- This is under Natural Language Understanding, deeper than NLP and using artificial intelligence training on a GPU
