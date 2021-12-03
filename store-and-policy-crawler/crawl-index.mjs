'use strict';

import _ from 'lodash';
import * as path from 'path';
import * as readline from 'node:readline';
import * as fsPromises from 'fs/promises';
import {stdin, stdout} from 'process';
import puppeteer from 'puppeteer-extra';
import StealthPlugin from 'puppeteer-extra-plugin-stealth';
import AdblockerPlugin from 'puppeteer-extra-plugin-adblocker';

async function gotoAmazonPage(page, url, rl) {
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
}

(async () => {
  const departmentInfo = await fsPromises.readFile('departments.json').then(JSON.parse);
  const leafDepartments = [];

  for (let i = departmentInfo.length - 1; i >= 0; --i) {
    const d1 = departmentInfo[i];

    if (leafDepartments.some(d2 => (_.last(d1.ids) == _.last(d2.ids) || d1.ids.every((e, i) => e == d2.ids[i])))) {
      continue;
    }

    d1.s = "date-desc-rank"
    leafDepartments.push({...d1});

    if (d1.nPages >= 400) {
      d1.name += " (R)";
      d1.s = "date-asc-rank";
      leafDepartments.push({...d1});
    }
  }

  puppeteer.use(StealthPlugin());
  puppeteer.use(AdblockerPlugin({ blockTrackers: true }))

  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setViewport({width: 1080, height: 1920});

  const rl = readline.createInterface({input: stdin, output: stdout});

  for (let d of leafDepartments) {
    const outDir = path.join("index", _.last(d.ids).replaceAll("/", ":") + " " + d.name);
    await fsPromises.mkdir(outDir, {recursive: true});

    let lastPage = await fsPromises.readdir(outDir).then((l) => Math.max(0, ...l.map(x => parseInt(x) || 0)));

    const url = new URL("https://www.amazon.com/s?i=alexa-skills");
    url.searchParams.set("s", d.s);
    url.searchParams.set("rh", d.ids.join(",").replaceAll('/', ':'));

    for (let i = lastPage + 1; i <= d.nPages; ++i) {
      console.log("%s [%d/%d]", d.name, i, d.nPages);
      url.searchParams.set("page", i);
      console.log(`Visiting ${url} ...`);
      await gotoAmazonPage(page, url, rl);

      const cdp = await page.target().createCDPSession();
      const { data } = await cdp.send('Page.captureSnapshot', { format: 'mhtml' });
      await fsPromises.writeFile(path.join(outDir, `${i}`.padStart(3, '0') + '.mhtml'), data);

      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }

  await browser.close();
  rl.close();
})();
