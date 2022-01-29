const puppeteer = require("puppeteer-extra");
const ua = require("random-useragent");
const randomUseragent = require('random-useragent');
const StealthPlugin = require('puppeteer-extra-plugin-stealth')
const striptags = require("striptags");
const fs = require("fs");

url = "https://lihkg.com/profile/81150";

puppeteer.use(StealthPlugin());

(async () => {
    const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36';
    
    async function createPage (browser, url, callback) {

        //Randomize User agent or Set a valid one
        const userAgent = randomUseragent.getRandom();
        const UA = userAgent || USER_AGENT;
        const page = await browser.newPage();

        //Randomize viewport size
        await page.setViewport({
            width: 1920 + Math.floor(Math.random() * 100),
            height: 3000 + Math.floor(Math.random() * 100),
            deviceScaleFactor: 1,
            hasTouch: false,
            isLandscape: false,
            isMobile: false,
        });

        await page.setUserAgent(UA);
        await page.setJavaScriptEnabled(true);
        await page.setDefaultNavigationTimeout(0);

        //Skip images/styles/fonts loading for performance
        await page.setRequestInterception(true);
        page.on('request', (req) => {
            if(req.resourceType() == 'stylesheet' || req.resourceType() == 'font' || req.resourceType() == 'image'){
                req.abort();
            } else {
                req.continue();
            }
        });

        page.on('response', callback);

        await page.evaluateOnNewDocument(() => {
            // Pass webdriver check
            Object.defineProperty(navigator, 'webdriver', {
                get: () => false,
            });
        });

        await page.evaluateOnNewDocument(() => {
            // Pass chrome check
            window.chrome = {
                runtime: {},
                // etc.
            };
        });

        await page.evaluateOnNewDocument(() => {
            //Pass notifications check
            const originalQuery = window.navigator.permissions.query;
            return window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
        });

        await page.evaluateOnNewDocument(() => {
            // Overwrite the `plugins` property to use a custom getter.
            Object.defineProperty(navigator, 'plugins', {
                // This just needs to have `length > 0` for the current test,
                // but we could mock the plugins too if necessary.
                get: () => [1, 2, 3, 4, 5],
            });
        });

        await page.evaluateOnNewDocument(() => {
            // Overwrite the `languages` property to use a custom getter.
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
        });

        await page.goto(url, { waitUntil: 'networkidle2',timeout: 0 } );
        return page;
    }

    const browser = await puppeteer.launch({
        headless: true,
    });

    const page = await createPage(browser, "https://lihkg.com/profile/81150");

    const all_thread_links = await page.evaluate(() => {
        return [...document.querySelectorAll("._2A_7bGY9QAXcGu1neEYDJB")].map(e => e.href);
    });

    let total = [];
    let sentiment = [];

    for (let thread_link of all_thread_links) {
        const page = await createPage(browser, thread_link, async (response) => {
            try {
                if (new RegExp("https://lihkg.com/api_v2/thread/\\d{1,7}/page/\\d{1,3}(order=reply_time)?").test(response.url())) {
                    const data = (await response.json()).response;
                    total.push({
                        id: data.thread_id,
                        title: data.title,
                        content:  striptags(data.item_data.length ? data.item_data[0].msg : ""),
                        source_name: "麵咪媽",
                        keywords: ["麵咪媽"],
                        source_url: "https://lihkg.com/profile/81150",
                        created_at: new Date(data.create_time * 1000).toISOString(),
                        updated_at: new Date(data.create_time * 1000).toISOString(),
                    });
                    const score = ((data.like_count) / (data.like_count + data.dislike_count)) * 2 - 1;
                    sentiment.push({
                        id: data.thread_id,
                        score,
                        is_positive: score > 0,
                    });
                    fs.writeFileSync("./result.json", JSON.stringify(total, null ,4));
                    fs.writeFileSync("./sentiment.json", JSON.stringify(sentiment, null ,4));
                }
            } catch (e) {
                console.log("error occurred");
                console.log(e);
            }
        });

        await page.waitForTimeout(3000);
    }

    await browser.close();
})()