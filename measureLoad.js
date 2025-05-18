const puppeteer = require('puppeteer');

async function measureLoad(url) {
const browser = await puppeteer.launch({
  executablePath: '/snap/bin/chromium',
  args: ['--no-sandbox', '--disable-setuid-sandbox'],
});

  const page = await browser.newPage();

  const response = await page.goto(url, { waitUntil: 'load' });

  // Get performance timing metrics from the page
  const perfTiming = JSON.parse(
    await page.evaluate(() => JSON.stringify(window.performance.timing))
  );

  await browser.close();

  // Calculate metrics
  const navigationStart = perfTiming.navigationStart;
  const responseStart = perfTiming.responseStart;
  const domContentLoadedEventEnd = perfTiming.domContentLoadedEventEnd;
  const loadEventEnd = perfTiming.loadEventEnd;
  const requestStart = perfTiming.requestStart;
  const responseEnd = perfTiming.responseEnd;

  const ttfb = responseStart - navigationStart;
  const domContentLoaded = domContentLoadedEventEnd - navigationStart;
  const loadTime = loadEventEnd - navigationStart;
  const totalRequestDuration = responseEnd - requestStart;

  console.log(`TTFB: ${ttfb} ms`);
  console.log(`DOMContentLoaded: ${domContentLoaded} ms`);
  console.log(`Load event end: ${loadTime} ms`);
  console.log(`Total request duration: ${totalRequestDuration} ms`);
}

const url = process.argv[2];
if (!url) {
  console.error('Please provide a URL as argument');
  process.exit(1);
}

measureLoad(url);
