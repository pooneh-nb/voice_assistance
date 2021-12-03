'use strict';

import * as readline from 'node:readline';
import * as fsPromises from 'fs/promises';
import {stdin, stdout} from 'process';
import puppeteer from 'puppeteer-extra';
import StealthPlugin from 'puppeteer-extra-plugin-stealth';
import AdblockerPlugin from 'puppeteer-extra-plugin-adblocker';

(async () => {
  puppeteer.use(StealthPlugin());
  puppeteer.use(AdblockerPlugin({ blockTrackers: true }))

  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setViewport({width: 1080, height: 1920});

  const rl = readline.createInterface({input: stdin, output: stdout});

  const departmentInfo = [{
    name: 'Alexa Skills',
    ids: ['n/13727921011'],
  }];

  for (let i=0; i<departmentInfo.length; i++) {
    const currentIds = departmentInfo[i].ids;

    const url = new URL("https://www.amazon.com/s?i=alexa-skills&s=featured-rank");
    url.searchParams.set("rh", currentIds.join(",").replaceAll('/', ':'));

    console.log(`Visiting ${url} ...`);

    while (true) {
      try {
        await page.goto(url);
      } catch (error) {
        console.error(error);
        continue;
      }

      if (null === await page.$('#captchacharacters')) {
        break;
      } else {
        await page.screenshot({ path: 'page.png' });

        const answer = await new Promise(resolve => {
          rl.question('Captcha: ', resolve);
        });

        await page.type('#captchacharacters', answer);
        await page.click('button[type=submit]');
        await page.waitForTimeout(2000);
      }
    }

    if (await page.evaluate(() => document.body.textContent.includes('Try checking your spelling'))) {
      console.log("Something went wrong!!!");
    }

    const departments = await page.$$eval('#departments>ul>li', (l) => l.map(e => ({
      name: e.textContent.trim(),
      id: e.id,
    })));

    departmentInfo[i].nPages = await page.$$eval('ul.a-pagination>li',
      l => Math.max(1, ...l.map(e => parseInt(e.textContent) || 0)));

    for (let d of departments) {
      if (currentIds.includes(d.id)) continue;

      departmentInfo.push({
        name: d.name,
        ids: currentIds.concat([d.id]),
      });
    }

    await new Promise(resolve => setTimeout(resolve, 2000));
  }

  await fsPromises.writeFile('departments.json', JSON.stringify(departmentInfo));

  await browser.close();
  rl.close();
})();
