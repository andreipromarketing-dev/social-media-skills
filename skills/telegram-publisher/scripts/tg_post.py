#!/usr/bin/env python3
"""Publish a message/photo to a Telegram chat or channel via the Bot API (no deps).

Usage:
  python3 tg_post.py --text-file draft.txt [--photo img.jpg] [--html]

Env: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID. Values are never printed.
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.error
import urllib.request


def call(token, method, fields=None, files=None):
    if files:
        boundary = "----tgupload"
        body = b""
        for k, v in (fields or {}).items():
            body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n").encode()
        for k, (fname, content, ctype) in files.items():
            body += (
                f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"; filename=\"{fname}\"\r\n"
                f"Content-Type: {ctype}\r\n\r\n"
            ).encode() + content + b"\r\n"
        body += f"--{boundary}--\r\n".encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/{method}", data=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )
    else:
        data = urllib.parse.urlencode(fields or {}).encode()
        req = urllib.request.Request(f"https://api.telegram.org/bot{token}/{method}", data=data)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            out = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = json.loads(e.read().decode()).get("description", "")
        except Exception:
            pass
        sys.exit(f"Telegram API error {e.code}: {detail or e.reason}")
    if not out.get("ok"):
        sys.exit(f"Telegram API error: {out.get('description')}")
    return out["result"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text-file", required=True)
    ap.add_argument("--photo")
    ap.add_argument("--html", action="store_true", help="use HTML parse_mode")
    args = ap.parse_args()

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat:
        sys.exit("Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.")

    with open(args.text_file, encoding="utf-8") as fh:
        text = fh.read().strip()
    if not text:
        sys.exit("Message text is empty.")

    fields = {"chat_id": chat}
    if args.html:
        fields["parse_mode"] = "HTML"

    if args.photo:
        if len(text) > 1024:
            sys.exit("Caption exceeds 1024 chars (see platform card telegram.md). Trim or send as separate message.")
        ctype = "image/jpeg"
        if args.photo.lower().endswith(".png"):
            ctype = "image/png"
        with open(args.photo, "rb") as fh:
            content = fh.read()
        fields["caption"] = text
        result = call(token, "sendPhoto", fields, {"photo": (os.path.basename(args.photo), content, ctype)})
    else:
        if len(text) > 4096:
            sys.exit("Message exceeds 4096 chars. Split it or use a Telegraph article.")
        fields["text"] = text
        result = call(token, "sendMessage", fields)

    mid = result["message_id"]
    link = None
    if chat.startswith("@"):
        link = f"https://t.me/{chat[1:]}/{mid}"
    print(json.dumps({"message_id": mid, "url": link, "chat_type": result.get("chat", {}).get("type")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
