import asyncio, pathlib
from playwright.async_api import async_playwright
IMG = pathlib.Path(__file__).resolve().parent.parent / "assets/img"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, w, h, bg in [("lclc-badge", 2000, 2000, "transparent"), ("lclc-mark", 512, 512, "transparent"), ("lclc-wordmark", 0, 0, "#05010c")]:
            svg = (IMG / f"{name}.svg").read_text()
            pg = await b.new_page()
            await pg.set_content(f'<html><body style="margin:0;background:{bg}">{svg}</body></html>')
            el = await pg.query_selector("svg")
            if w: await el.evaluate(f"e=>{{e.setAttribute('width',{w});e.setAttribute('height',{h})}}")
            await el.screenshot(path=str(IMG / f"{name}.png"), omit_background=(bg == "transparent"))
            await pg.close()
        await b.close()
asyncio.run(main())
