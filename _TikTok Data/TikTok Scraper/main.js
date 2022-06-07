const TikTokScraper = require('./build');

// import TikTokScraper from 'tiktok-scraper'

// Hashtag feed
(async () => {
    try {
        const posts = await TikTokScraper.hashtag('HASHTAG', {
            number: 100,
            sessionList: ['sid_tt=58ba9e34431774703d3c34e60d584475;']
        });
        console.log(posts);
    } catch (error) {
        console.log(error);
    }
})();