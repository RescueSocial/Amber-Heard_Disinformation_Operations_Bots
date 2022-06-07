import {hashtag} from '../src';

var fs = require('fs');

let date = new Date()
date.toISOString().split('T')[0]


const offset = date.getTimezoneOffset()
date = new Date(date.getTime() - (offset * 60 * 1000))
let right_date = date.toISOString().split('T')[0]

let hashtags = [
    "amberheard",
    "amberheardisinnocent",
    "justiceforamberheard",
    "istandwithamberheard",
    "teamah",
    "teamamberheard",
    "johnnydeppisguilty",
    "johnnydeppisanabuser",
    "ibelieveamberheard",
    "wearewithyouamberheard",
    "istandwithamberheard",
    "amberheardismera",
    "amberheardismymera",
    "amberismymera",
    "westandwithamberheard",
    "amberhearddomesticabuse",
    "amberheardisasurvivor",
    "amberheardisavictim",
    "boycottfantasticbeasts",
    "johnnydeppisanabuser",
    "johnnydeppisawifebeater",
    "boycottjohnnydepp",
    "johnnydeppisguilty",
    "johnnydepplied",
    "johnnydeppisarapist",
    "amberheardaquaman",
    "amberheardloreal",
    "amberheardmera",
    "amberheardaclu",
    "darvodepp",
    "standwithamberheard",
    "loveamberheard",
    "istandwithamber",

    "johnnydepp",
    "johnnydeppisinnocent",
    "justiceforjohnnydepp",
    "istandbyjohnnydepp",
    "teamjd",
    "teamjohnnydepp",

    "amberheard🤮",
    "amberheard🤢",
    "amberheard🤡",
    "amberheard💩",
    "amberheardslawyersucks",
    "amberheardisguilty",
    "amberheardisanabuser",
    "amberturd",
    "putamberheardinjail",
    "amberpoop",
    "fireamberheard",
    "boycottwarnerbros",
    "boycottwarnerbrothers",
    "boycottloreal",
    "boycottaquaman2",
    "amberheardisagolddigger",
    "amberheardisaliar",
    "amberheardforprison",
    "amberheardforjail",
    "amberheardisafraud",
    "amberhearddidnotdonate",
    "johnnydeppvsamberheard",
    "warnerbrosisoverparty",
    "aclusupportsabusers",
    "recastmera",
    "amberheardisapsycopath",
    "amberhearddeservesprison",
    "amberheardisacriminal",
    "amberhearddoesnotspeakforme",
    "amberheardperjury",
    "amberheardisoverparty",
    "amberheardaquaman",
    "amberheardloreal",
    "aclusupportsabusers",

    "johnnydeppamberheard",
    "amberheardtrial",
    "deppvsheard",
    "johnnydeppvsamberheard",
    "amberheardjohnnydepp",
    "johnnydepptrial",
    "deppvheardtrial",
    "deppheardtrial"
]

var output_dir = '../../TikTokData';

if (!fs.existsSync(output_dir)) {
    fs.mkdirSync(output_dir);
}

output_dir = output_dir.concat("/", right_date)
if (!fs.existsSync(output_dir)) {
    fs.mkdirSync(output_dir);
}

hashtags.forEach(function (element) {

    (async () => {
        try {
            console.log('"'.concat(element.toLowerCase(), '",'))
            await hashtag(element, {
                number: 9999,
                sessionList: ['sid_tt=asdasd13123123123adasda;'],
                filetype: 'all',
                filepath: output_dir,
                timeout: 10000
            });
        } catch (error) {
            console.log(error);
        }

    })();
});


/**
 * Output example
 */
// [
//     {
//         id: '6702952481954991366',
//         text: 'Swimming pool fails w/ @erin_nichole18 #fails #summer #foryou #foryoupage #trending #featureme',
//         createTime: '1560652741',
//         authorId: '6653484314188251142',
//         authorName: 'malorielynn14',
//         authorFollowing: 40,
//         authorFans: 471748,
//         authorHeart: '7678430',
//         authorVideo: 68,
//         authorDigg: 2822,
//         authorVerified: false,
//         authorPrivate: false,
//         authorSignature: '',
//         musicId: '6647277225529838341',
//         musicName: 'See Me Fall (Y2K Remix)',
//         musicAuthor: 'Ro Ransom',
//         musicOriginal: '',
//         imageUrl: 'https://p16-va-default.akamaized.net/obj/tos-maliva-p-0068/a865cf63f422476b86f891237b1755d0',
//         videoUrl:
//             'https://v16.muscdn.com/f7108f69ff74a76471b37af959aaf3af/5e7e5832/video/tos/useast2a/tos-useast2a-ve-0068/dd8d7c6c890f46aeb6f5e08705ea2788/?a=1233&br=8042&bt=4021&cr=0&cs=0&dr=0&ds=3&er=&l=2020032713464701018904915654210E53&lr=tiktok_m&qs=0&rc=M2x5OXJ2eTN0bjMzaDczM0ApN2Q8Nmg7Ozw6N2Q2OTc0NGdgb2g0aGNmai9fLS1eMTZzc2MuNTM2NGIyYWEyYDMxLjM6Yw%3D%3D&vl=&vr=',
//         videoUrlNoWaterMark: 'https://api2.musical.ly/aweme/v1/playwm/?video_id=v09044ae0000bk2qm0ivfsko76kvric0',
//         diggCount: 7196732,
//         shareCount: 293012,
//         playCount: 96225830,
//         commentCount: 82711,
//         downloaded: false,
//         hashtags: [[]],
//     },
// ];
