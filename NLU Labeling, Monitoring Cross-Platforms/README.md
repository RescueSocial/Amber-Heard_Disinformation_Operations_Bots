# SNA-AH-NLU-Labeling-Cross-Platforms
Natural Language Understanding, Processing, and Sentiment Testing across social media platforms on Amber Heard data using Scientific Methods. <br><b>NLU engines, monitoring, classifications, training.</b>

- Twitter, Reddit. Instagram, YouTube, Change.org, Facebook
- Mainy Support and Defense Data included, Compliments, Love Data for training NLU - including 5.9K of 12.4K labeled files
- Monitoring and Dashboards included
- Instagram threat analysis includes Both Crime | Human Trafficking words analysis
- Testing data is flooded with harms 

<i>Data used in NLU Testing Analysis is in /Testing Data folder</i>
<br>Dashboard files show of using programs to run the monitoring bot. Monitoring js files are included.

<b>Natural Language Understanding:</b>
- A BERT File under config shows BERT for Amber Heard NLP training
- There are Dashboard code files in Javascript. The requirements are Reactjs, Javascript, and Django languages
- Package examples and how to train NLU is included - e.g., <a href="https://www.nltk.org/">nltk_data</a>
- Supporters and Offenders are marked by the numbers of tweets using the NLU classifications
- There are monitoring pages, showing how the crawler monitors while classifying and storing the texts in a database

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
3. Second example, more accurate for nlp engine is multiclassifier - support, defense, offense, defense_against (focused on victim - target of operations) - trained on 12.4K texts

<b>Monitoring is easier than responding with NLG,</b> hence, 'like-bots' are easier to create, and there are many of them. They sometimes do classification mistakes, creating preliminary precedence for gamification analysis of them and reverse engineering.
<br>In context of domestic abuse, it's important to show what is supportive and positive in relationships through support, defense, compliments, and love texts.
- This is under Natural Language Understanding, deeper than NLP and using Artificial Intelligence training on a GPU
