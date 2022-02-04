# SNA-AH-NLU-Labeling-Cross-Platforms
<b>Natural Language Understanding, Processing, and Sentiment Testing across social media platforms on Amber Heard data using Scientific Methods - <i>NLU/NLP engines, monitoring, classifications, training.</i></b>

<b><i>Classifying Texts and Accounts in Case Study</b></i> - 
<br>Automatic programs label texts for multiclassifier categories of support, defense, offense, defense_against and label supporters/offenders accounts around her environment to show help or harm to her.</b>
<br>-> Threat analysis, negative texts, and specific word filtering related to the disinformation operations is applied in further analysis. Wordclouds show patterns across-platforms.

#### <b>Data and Analysis of Twitter, Reddit, Instagram, YouTube, Change.org, Facebook</b>
- <b>Support and Defense Data is included, as well as Compliments, Love Data for training NLU - including 5.9K of 12.4K labeled training</b>
<br>-> 10K NLG created Supportive Compliments of her from Semiosis is included for comparison of labeled texts vs articulate compliments from <a href="https://github.com/mullikine/positive-nlg-compliments">AI</a>. Compare density and prompt-based similarities.
<br> -> In context of domestic abuse and coercive control, it's important to show what is supportive and positive in relationships through support, defense, compliments, and love texts. <i>The adversiarial framework of operations or tactic strategy is further a layer. </i>
- Monitoring and Dashboards included
- Instagram threat analysis includes both <a href="https://myvocabulary.com/word-list/crime-vocabulary">Crime</a> | <a href="https://myvocabulary.com/word-list/human-trafficking-vocabulary">Human Trafficking</a> words analysis with NLU testing
- Testing data is flooded with harms 
- <b>High volumes apply:</b> With the monitoring NLU, there were 122K auto-labeled tweets by June 2021 and over tens of thousands of accounts labeled from one monitoring account. Increase of harmful volume increases risks and amounts affect her wellbeing.
<br><i>-> Correlate meaning to quantifications</i>

<i><b>Labels are:</b> support, defense, offense, defense_against (focused on victim - target of operations)</i>

<b>Demo Videos:</b> 
<br><a href="https://www.youtube.com/watch?v=2_bgfNKQI_w">Demo Video Monitoring Twitter Bot 1 - 2021-05-20</a>
<br><a href="https://www.youtube.com/watch?v=HHTUsL-TR08">Demo Video Monitoring Twitter Bot 2 - 2021-05-20</a>
<br><a href="https://www.youtube.com/watch?v=t4bBtGPF000">Video Demo Monitoring Twitter (Backend) - 2021-03-26</a>
<br><a href="https://www.youtube.com/watch?v=xkrJbJr4TlU">NLP Engine version 1 result</a>


<b>Monitoring is easier than responding with NLG</b> - Hence, 'liking-only-bots' are easier to create, and there are many of them in the operations against Amber Heard. They sometimes do classification mistakes, creating preliminary precedence for gamification analysis of them and reverse engineering.

<i>Data used in NLU Testing Analysis is in /Testing Data folder</i>
<br>Dashboard files show of using program to run the monitoring bot. Monitoring js files are included.
- Papers are provided under Guides to NLU and "Studying Technologies" in Background - Preliminary Effects folder. E.g., Argumentation research and Logic.
<br>Similar to <a href="https://www.chess.com/article/view/chess-tactics">Chess-Tactics</a>, however, in dynamic context of coercive control or warfare-operations. Our goal is to mitigate the operations.
- We've provided some data on AH's NLU to a Data Science anti-harassment start up understanding gender dynamics. Please contact us if you need more data.

### <b>Natural Language Understanding:</b>
- A BERT File under config shows <a href="https://github.com/google-research/bert">BERT</a> for Amber Heard NLP training
- There are Dashboard code files in Javascript. The requirements are Reactjs, Javascript, and Django languages
- Package examples and how to train NLU is included - e.g., <a href="https://www.nltk.org/">nltk_data</a>
- Supporters and Offenders are marked by the numbers of tweets using the NLU classifications
- There are monitoring pages, showing how the crawler monitors while classifying and storing the texts in a database

There is an NLU dashboard tester using the api for the trained NLU.
<br>The API uses Postman.
<br><b>Pre-Processing Bot code to extract text from images and testing the results with a video is added.</b>

#### <b>Requirements of NluEngine:</b>
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

Version NLU Trained on Data from: Twitter, Facebook, Change.org primarily with some YouTube and Reddit. 
1. First example (old nlpengine) is 2 classifications only of love or hate - quickly seen as not accurate and to move to an offense, defense, support strategy with multiclassification 
2. Second example, more accurate for nlp engine is <b>multiclassifier</b> - support, defense, offense, defense_against (focused on victim - target of operations) - trained on 12.4K texts 
<br><i>Supporters both support and defend. Offenders offend and defense_against. 
<br>Support is completely focused on uplifting her, while defense includes constructive words to defend and support her. Offense is purely harmful towards her while defense_against includes support of her adversary.</i> 
<br>-> <i>Accounts are labeled by the NLP and number of texts classified for, against, or neutral. Label texts 0-1 for percentages to create training with patterns.</i>

<b>- This is under Natural Language Understanding, deeper than NLP and using Artificial Intelligence training on a GPU</b>

<i>A further development would be Multi-Agent Modeling and creating Simulations with 'Action-Trees' of perpetrators and victim, supporters and offenders.</i>
