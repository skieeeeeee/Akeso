import { chromium } from "playwright";
const { TOKEN, OUT } = process.env;
const SITE = "https://akeso-zeta.vercel.app";
const browser = await chromium.launch({ channel: "chrome" });
const ctx = await browser.newContext({ viewport: { width: 900, height: 1200 }, permissions: ["microphone"] });
const page = await ctx.newPage();
await page.goto(`${SITE}/login`, { waitUntil: "domcontentloaded" });
await page.evaluate((t) => {
  localStorage.setItem("medikiosk.token", t);
  localStorage.setItem("medikiosk.language", "en");
}, TOKEN);

for (const [name, url] of [
  ["medical history", "/onboarding/medical-profile"],
  ["personal details", "/onboarding/personal"],
  ["AYUSH notes", "/ayush"],
  ["records", "/records"],
]) {
  await page.goto(SITE + url);
  await page.waitForLoadState("networkidle");
  await page.waitForTimeout(2000);
  const info = await page.evaluate(() => {
    const skip = ["file","hidden","radio","checkbox","submit","button"];
    const fields = [...document.querySelectorAll("input, textarea")]
      .filter((el) => !skip.includes((el.getAttribute("type") || "text").toLowerCase()))
      .map((el) => (el.tagName === "TEXTAREA" ? "textarea" : el.getAttribute("type") || "text"));
    const mics = [...document.querySelectorAll("button")]
      .filter((b) => /speak instead/i.test(b.textContent || "")).length;
    return { fields, mics, path: location.pathname };
  });
  const text = info.fields.filter((f) => f === "text" || f === "textarea").length;
  console.log(`  ${name.padEnd(18)} ${info.path.padEnd(30)} text=${text} mics=${info.mics} ${text === info.mics && text > 0 ? "LIVE" : "not deployed"}`);
  if (OUT) await page.screenshot({ path: `${OUT}/live-${name.replace(/\W+/g,"_")}.png`, fullPage: true });
}
await browser.close();
