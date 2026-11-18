// Stampa un HTML in PDF con Chromium (Playwright), con piè di pagina «titolo · pagina n di N».
// Uso: node stampa.js <file.html> <file.pdf> "<titolo per il piè di pagina>"
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const [html, pdf, titolo = ''] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(html), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  const piede = `
    <div style="font-family: Inter, sans-serif; font-size: 7.5pt; color: #8a93a5; width: 100%;
                padding: 0 16mm; display: flex; justify-content: space-between;">
      <span>${titolo.replace(/</g, '&lt;')}</span>
      <span><span class="pageNumber"></span> / <span class="totalPages"></span></span>
    </div>`;
  await page.pdf({
    path: pdf, format: 'A4', printBackground: true, preferCSSPageSize: true,
    displayHeaderFooter: true, headerTemplate: '<div></div>', footerTemplate: piede,
  });
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
