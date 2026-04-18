#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import csv
from pathlib import Path
from typing import Dict, List
from urllib.parse import urlparse

from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scrape the latest visible posts from an X account and write them to CSV."
    )
    parser.add_argument(
        "--account-url",
        default="https://x.com/DCPoliceDept",
        help="Full X account URL to scrape.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Number of posts to capture. Default: 20",
    )
    parser.add_argument(
        "--output-file",
        default="dcpolicedept_last_20_posts.csv",
        help="CSV output path. Default: dcpolicedept_last_20_posts.csv",
    )
    parser.add_argument(
        "--headful",
        action="store_true",
        help="Run the browser with a visible window. Useful if X challenges headless traffic.",
    )
    parser.add_argument(
        "--timeout-ms",
        type=int,
        default=45000,
        help="Per-page timeout in milliseconds. Default: 45000",
    )
    return parser.parse_args()


def extract_screen_name(account_url: str) -> str:
    parsed = urlparse(account_url)
    parts = [part for part in parsed.path.split("/") if part]
    if not parts:
        raise ValueError(f"Could not determine screen name from URL: {account_url}")
    return parts[0].lstrip("@")


async def collect_posts(account_url: str, limit: int, headful: bool, timeout_ms: int) -> List[Dict[str, str]]:
    target_screen_name = extract_screen_name(account_url).lower()

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=not headful,
            args=[
                "--disable-blink-features=AutomationControlled",
            ],
        )
        context = await browser.new_context(
            locale="en-US",
            timezone_id="America/New_York",
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1440, "height": 1600},
        )
        page = await context.new_page()
        page.set_default_timeout(timeout_ms)

        await page.goto(account_url, wait_until="domcontentloaded")

        try:
            await page.wait_for_selector("article[data-testid='tweet']", timeout=15000)
        except PlaywrightTimeoutError:
            await browser.close()
            raise RuntimeError(
                "X did not render any tweet articles. Retry with --headful and, if prompted, complete any login or bot check."
            )

        posts_by_id: Dict[str, Dict[str, str]] = {}
        stale_rounds = 0
        last_seen_count = 0

        while len(posts_by_id) < limit and stale_rounds < 6:
            extracted = await page.evaluate(
                """(targetScreenName) => {
                    const toAbsoluteUrl = (value) => {
                        if (!value) return "";
                        try {
                            return new URL(value, window.location.origin).toString();
                        } catch {
                            return "";
                        }
                    };

                    const normalizeText = (article) => {
                        const textNode = article.querySelector('[data-testid="tweetText"]');
                        if (!textNode) return "";
                        return Array.from(textNode.querySelectorAll('span'))
                            .map((node) => node.textContent || "")
                            .join("")
                            .replace(/\\s+/g, " ")
                            .trim();
                    };

                    const articles = Array.from(document.querySelectorAll('article[data-testid="tweet"]'));
                    return articles.map((article) => {
                        const statusLink = article.querySelector('a[href*="/status/"]');
                        const href = statusLink ? toAbsoluteUrl(statusLink.getAttribute('href')) : "";
                        const pathname = href ? new URL(href).pathname : "";
                        const match = pathname.match(/^\\/([^/]+)\\/status\\/(\\d+)/);
                        if (!match) return null;

                        const screenName = match[1].toLowerCase();
                        const postId = match[2];
                        if (screenName !== targetScreenName.toLowerCase()) return null;

                        const timestampNode = article.querySelector("time");
                        const replyContext = article.innerText.includes("Replying to");
                        const pinned = article.innerText.includes("Pinned");

                        return {
                            post_id: postId,
                            screen_name: match[1],
                            url: href,
                            posted_at: timestampNode ? timestampNode.getAttribute("datetime") || "" : "",
                            text: normalizeText(article),
                            is_reply: replyContext ? "yes" : "no",
                            is_pinned: pinned ? "yes" : "no",
                        };
                    }).filter(Boolean);
                }""",
                target_screen_name,
            )

            for post in extracted:
                if post["is_pinned"] == "yes":
                    continue
                posts_by_id.setdefault(post["post_id"], post)

            if len(posts_by_id) == last_seen_count:
                stale_rounds += 1
            else:
                stale_rounds = 0
                last_seen_count = len(posts_by_id)

            await page.mouse.wheel(0, 2200)
            await page.wait_for_timeout(1400)

        await browser.close()

    posts = sorted(posts_by_id.values(), key=lambda item: item["posted_at"], reverse=True)
    if not posts:
        raise RuntimeError("No posts were extracted from the account timeline.")
    return posts[:limit]


def write_csv(output_file: Path, posts: List[Dict[str, str]]) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "post_id",
        "screen_name",
        "posted_at",
        "url",
        "text",
        "is_reply",
    ]
    with output_file.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for post in posts:
            writer.writerow({key: post.get(key, "") for key in fieldnames})


async def async_main() -> int:
    args = parse_args()
    posts = await collect_posts(
        account_url=args.account_url,
        limit=max(args.limit, 1),
        headful=args.headful,
        timeout_ms=args.timeout_ms,
    )
    write_csv(Path(args.output_file), posts)
    print(f"Wrote {len(posts)} posts to {args.output_file}")
    return 0


def main() -> int:
    try:
        return asyncio.run(async_main())
    except KeyboardInterrupt:
        return 130
    except Exception as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
