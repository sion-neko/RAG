import asyncio
import sys

import httpx
from bs4 import BeautifulSoup


async def scrape(url: str) -> str:
    async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
        response = await client.get(url)
        response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # 不要な要素を削除
    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()

    # テキスト抽出
    text = soup.get_text(separator="\n")

    # 前後の空白を削除
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


if __name__ == "__main__":
    result = asyncio.run(scrape("https://www.google.com"))
    print(result[:3000])
    print(f"\n--- 合計 {len(result)} 文字取得 ---")
