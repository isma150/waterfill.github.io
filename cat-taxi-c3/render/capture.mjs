// Renders each sprite spec through the harness API on black and white backgrounds.
import { chromium } from "playwright-core";
import fs from "node:fs";
import path from "node:path";
const dir = path.dirname(new URL(import.meta.url).pathname);
const specs = JSON.parse(fs.readFileSync(path.join(dir, "specs.json"), "utf8"));
const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell", args: ["--no-sandbox", "--allow-file-access-from-files"] });
const page = await browser.newPage({ viewport: { width: 420, height: 746 }, deviceScaleFactor: 1 });
const errors = [];
page.on("pageerror", e => errors.push(String(e)));
await page.goto("file://" + path.join(dir, "harness.html"));
await page.waitForFunction(() => window.__api && window.__api.canvas);
for (const s of specs) {
  const passes = s.mode === "opaque" ? ["000000"] : ["000000", "ffffff"];
  for (const bg of passes) {
    const url = await page.evaluate(({ code, bg }) => {
      const api = window.__api, c = api.ctx;
      c.setTransform(1, 0, 0, 1, 0, 0); c.globalAlpha = 1; c.fillStyle = "#" + bg; c.fillRect(0, 0, 420, 746);
      new Function("api", code)(api);
      return api.canvas.toDataURL("image/png");
    }, { code: s.code, bg });
    fs.writeFileSync(path.join(dir, "raw", `${s.name}_${bg}.png`), Buffer.from(url.split(",")[1], "base64"));
  }
}
await browser.close();
console.log(JSON.stringify({ captured: specs.length, pageErrors: errors.slice(0, 5) }));
