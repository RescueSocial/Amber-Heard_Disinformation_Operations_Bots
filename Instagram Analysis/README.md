## SNA-AH-Case-Instagram
Instagram - Social Network Analysis on Amber Heard's Case Example from Data Analysts, Researchers, and Scientists. 
<br>Instagram: 1,751,113 Comments, 193,967 Posts, 717,311 Accounts (Posts made by 36,137 accounts and 681,174 commented)
<br>Analyzing Same Texts, Comments, Posts, Accounts Analysis, Timings, Threat Analysis.

<b>We obtained over 1.7 million comments and over 190,000 posts from Instagram from the #AmberHeard hashtag for mostly 2018-2021.</b>
- The most interesting bot simulation is 'i am inevitable' from May 2019, which can be perceived as a threat.

<b>Overall the texts appear to be more positive towards Amber Heard on Instagram,</b> requiring threat/negative texts analysis as on other platforms. 
<br>We analyze for same texts and <b>delays in peaks against Amber showing lack of correlation with announcements</b>.
- Instagram has features which make using bot accounts very difficult, which explains the far less volume of data against Amber Heard under her hashtag, and explains more of why on Instagram they focused more on her ex-partner. E.g., our researcher had to use 10 proxies with 10 different accounts which would frequently be blocked, unlike Twitter with 1 proxy, 1 IP (never discovered our monitoring bot either), Google, Reddit, and other platforms with far higher volume of bots and API access.
<br><i>- The higher positivity towards Amber Heard under her name on Instagram reflects more of the real-world. </i>

<b>Comments on Instagram per year:</b>
<br>2020 - 711,339 40.6%
<br>2021 - 478,594 27.3%
<br>2019 - 333,197 19%
<br>2018 227,847 13%

### <b>From Data Investigations File:</b>

The most interesting and obvious bot simulation is 'i am inevitable' from May 2019. Most are on May 14 and May 15 2019 or two days.
<br>The accounts appear to be private or deleted/require login.

The peak day of "i am inevitable" comment is 14 May 2019

df_inev.username.value_counts()
<br>ronak.jain15           1
<br>its_rajdeep_m          1
<br>j.a.k.e.t.a.y.l.o.r    1
<br>dhruvv.agrawal         1
<br>melylunac_             1
                      ..
<br>lyfaday                1
<br>karthickhere           1
<br>jamesquinn3630         1
<br>saini_lovers           1
<br>doughboii.2120         1
<br>Name: username, Length: 151, dtype: int64

<b>This text used 136 times by different 136 users in 3 consecutive days</b>

in those dates
<br>2019-05-14 114
<br>2019-05-15 20
<br>2019-05-16 1
<br>2019-05-25 1

<b>Hashtags	Count</b>
<br>#justiceforjohnnydepp	10244
<br>#amberheardisanabuser	2032
<br>#wearewithyoujohnnydepp	805
<br>#amberheardisaliar	776
<br>#amberturd	449
<br>#fireamberheard	349
<br>#fuckthesun	335
<br>#boycottamberheard	324
<br>#ambertheabuser	165
<br>#amberheardisanabuserandliar	144
<br>#jailforamberheard	89
<br>#removeamberheardsfromaquaman2	57

### From Same Texts File:

<b>Top repeated texts on Instagram:</b>

1	{'beautiful'}	19653
<br>2	{'love'}	8451
<br>3	{'nice'}	6130
<br>4	{'justiceforjohnnydepp'}	5663
<br>5	{'wow'}	5466
<br>6	{'gorgeous'}	5410
<br>7	{'linda'}	3603
<br>8	{'sexy'}	3559
<br>9	{'hermosa'}	3223
<br>10	{'amber'}	2855
<br>13	{'yes'}	2660
<br>14	{'amazing'}	2627
<br>15	{'cute'}	2487
<br>16	{'awesome'}	2315
<br>17	{'amo', 'amore'}	2297
<br>18	{'hot'}	2161
<br>19	{'stunning'}	1986
<br>20	{'thank'}	1911
<br>21	{'lovely'}	1880
<br>23	{'good'}	1654
<br>24	{'pretty'}	1643
<br>26	{'cool'}	1465
<br>27	{'sashabarrese', 'avengersinfinitywar', 'capta...	1427
<br>28	{'omg'}	1416
<br>29	{'aquaman'}	1397
<br>30	{'avengersinfinitywar', 'captainamericacivilwa...	1382
<br>31	{'bella'}	1373
<br>32	{'beauty'}	1321
<br>33	{'perfect'}	1299
<br>34	{'red'}	1239
<br>35	{'amberheard'}	1164
<br>36	{'amor'}	1159
<br>37	{'scarlett'}	1148
<br>38	{'thanks'}	1139
<br>39	{'fiyat'}	1133
<br>40	{'like'}	1122
<br>41	{'queen'}	1118
<br>42	{'wonderful'}	1096
<br>43	{'mera'}	1080
<br>45	{'fuck'}	988
<br>46	{'hi'}	970
<br>47	{'preciosa'}	959
<br>48	{'sweet'}	899
<br>49	{'restorethesnyderverse'}	880

<b>Interestingly, the top hashtag against Amber Heard on Instagram shows Peaks in December 2020, close to the time when YouTube was having extreme peaks from the bots on the "Adapt and Survive" video against her as well as other repeated same texts. Yet, the hashtags pro her ex-partner peaked in November 2020. That shows a strange near month-long delay from the announcement via media of the NGN case to post against AH, further supporting false interactions.</b>

#amberheardisanabuser                          432

Name: message, dtype: int64
<br>amberheardisanabuser.dates()
<br>2020-12-18    43
<br>2020-12-29    22
<br>2020-12-19    18
<br>2020-11-09    12
<br>2020-11-08    11
              ..
<br>2020-04-20     1
<br>2020-03-25     1
<br>2020-12-12     1
<br>2021-04-02     1
<br>2021-08-09     1
<br>Name: date, Length: 194, dtype: int64

amberheardisanabuser.date_info()
<br>The commentes were made between 2019-03-13 and  2021-08-18
    <br>  n_comments
year            
2019          10
<br>2020         354
<br>2021         127

message	repeated_times	avg_likes	n_replies
<br>160	#amberheardisanabuser	432	4.030093	34.0
<br>9306	abuser	346	2.294798	21.0

<b>The comments related to justiceforjohnnydepp mostly only show in 2020 and 2021.</b>
<br>The commentes were made between 2018-08-03 and  2021-08-19
    <br>  n_comments
year            
2018           2
<br>2019           7
<br>2020        4219
<br>2021        1435

#justiceforjohnnydepp                          4862

Peak Dates:
<br>2020-11-07    347
<br>2020-11-13    243
<br>2020-11-08    170
<br>2020-12-18    169
<br>2020-11-09    158
             ... 
<br>2020-03-29      1
<br>2020-05-06      1
<br>2020-09-04      1
<br>2020-09-20      1
<br>2020-05-24      1
<br>Name: date, Length: 489, dtype: int64

message	repeated_times	avg_likes	n_replies
<br>297	#justiceforjohnnydepp	4862	8.439325	490.0
<br>2822	justice for johnny depp	168	11.452381	83.0
<br>2804	justice for johnny	141	8.985816	29.0
<br>1464	@johnnydepp #wearewithyoujohnnydepp #amberhear...	124	0.185484	0.0

"The Amplifications in the counts and number of likes on #justiceforjohnnydepp is quite obvious!!"

The text 'abuser' and other negative texts follow the other peaks more.
<br>abuser              346

abuser.dates()
<br>2020-11-12    18
<br>2020-11-11    14
<br>2020-02-20    13
<br>2020-02-09    11
<br>2020-11-15     9
              ..
<br>2021-03-28     1
<br>2020-08-19     1
<br>2020-10-26     1
<br>2020-12-05     1
<br>2021-03-16     1
<br>Name: date, Length: 326, dtype: int64

The commentes were made between 2018-08-01 and  2021-08-27
    <br>  n_comments
year            
2018           4
<br>2019          39
<br>2020         469
<br>2021         179


<b>Most Repeated Comments Containing "Fire Amber"</b>

df.sort_values('repeated_times', ascending=False).head(25)
<br>message	repeated_times	avg_likes	n_replies
<br>162	#fireamberheard	94	2.031915	1.0
<br>42	#boycottamberheard	83	3.445783	2.0
<br>70	#boycottaquaman2	80	20.087500	27.0
<br>2563	https://www.change.org/p/dc-entertainment-remo...	67	1.358209	11.0
<br>2274	everyone who is a fan of amber heard please l...	44	1.727273	63.0
<br>1925	boycott	39	11.025641	5.0
<br>4179	،#justiceforjohnnydepp #amberheardisanabuser ...	32	0.093750	0.0
<br>235	#justiceforjohnnydepp #amberheardisanabuser ...	26	0.576923	1.0
<br>2311	fire her	23	3.739130	2.0
<br>1961	boycott aquaman 2	19	21.052632	23.0
<br>143	#boycottwarnerbros	19	1.894737	0.0
<br>2273	everyone who is a fan and is following her fan...	14	3.000000	8.0
<br>2295	fire amber heard	13	5.538462	3.0
<br>1727	@wewantjusticeforjohnnydepp #johnnydepp #amber...	12	0.083333	0.0
<br>268	#justiceforjohnnydepp #boycottthesun	12	3.333333	2.0
<br>279	#justiceforjohnnydepp #fireamberheard	12	1.500000	0.0
<br>51	#boycottamberheard #justiceforjohnnydepp #ambe...	10	2.100000	1.0
<br>212	#johnnydeppisanangel #johnnydeppisinnocent #ju...	10	8.100000	2.0
<br>2590	https://www.thetimes.co.uk/edition/news/amber-...	10	0.300000	0.0
<br>3450	she should be fired	10	25.500000	15.0
<br>2025	boycott the movie	9	11.000000	0.0
<br>50	#boycottamberheard #justiceforjohnnydepp	9	5.666667	0.0
<br>1940	boycott amber heard	9	10.333333	10.0
<br>137	#boycottthesun	8	1.125000	0.0
<br>213	#johnnydeppisanangel #johnnydeppisinnocent #ju...	8	0.000000	0.0

Top Users Commented with "Fire Amber"
<br>df_fire.username.nunique()
<br>3588

<b>Comments Created in Each Year on Instagram in AH Dataset - Data Investigations file:</b>
<br>year	n_comments
<br>0	2014	4
<br>1	2015	1
<br>2	2016	15
<br>3	2017	116
<br>4	2018	227847
<br>5	2019	333197
<br>6	2020	711339
<br>7	2021	478594

<b>Most Repeated Comments</b> (with emojis)
<br>Same Text Same Date
<br>Deeper Investigations
<br>df_comments.message.value_counts().head(25)
<br>❤️                       16024
<br>😍                        11011
<br>❤️❤️❤️                   10774
<br>😍😍😍                       8664
<br>❤️❤️                      5566
<br>❤️❤️❤️❤️                  5500
<br>🔥🔥🔥                       5298
<br>beautiful                 5187
<br>😍😍😍😍                      5084
<br>😍😍                        5042
<br>❤️❤️❤️❤️❤️                4942
<br>#justiceforjohnnydepp     4862
<br>🔥                         4761
<br>😍😍😍😍😍                     3625
<br>🔥🔥                        2861
<br>🔥🔥🔥🔥                      2798
<br>❤️❤️❤️❤️❤️❤️              2723
<br>🔥🔥🔥🔥🔥                     2111
<br>nice                      2106
<br>2                         2099
<br>😍😍😍😍😍😍                    2075
<br>1                         2043
<br>👍                         1949
<br>😂😂😂                       1874
<br>❤️❤️❤️❤️❤️❤️❤️            1826
<br>Name: message, dtype: int64
