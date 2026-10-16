#!/usr/bin/env python3
"""Publish a post to a VK community wall via the official API (no third-party deps).

Usage:
  python3 vk_post.py --group-id -12345678 --text-file draft.txt [--photo img.jpg] [--publish-after 1700000000]
  python3 vk_post.py --screen-name nord21vek --text-file draft.txt   # resolves num id via groups.getById

Token is read from the environment variable VK_TOKEN and never printed.
"""
import argparse
import json
import mimetypes
import os
import sys
import urllib.parse
import urllib.request

API = "https://api.vk.com/method/"
VERSION = "5.199"


def api(method, token, **params):
    params = {k: v for k, v in params.items() if v is not None}
    params.update({"access_token": token, "v": VERSION})
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(API + method, data=data)
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.loads(resp.read().decode())
    if "error" in body:
        sys.exit(f"VK API error {body['error'].get('error_code')}: {body['error'].get('error_msg')}")
    return body["response"]


def upload_photo(token, group_id, path):
    """Upload an image for a wall post of the community. Returns attachment string."""
    gid = abs(int(group_id))
    server = api("photos.getWallUploadServer", token, group_id=gid)
    boundary = "----vkupload"
    fname = os.path.basename(path)
    ctype = mimetypes.guess_type(path)[0] or "image/jpeg"
    with open(path, "rb") as fh:
        content = fh.read()
    body = (
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"photo\"; filename=\"{fname}\"\r\n"
        f"Content-Type: {ctype}\r\n\r\n".encode()
        + content
        + f"\r\n--{boundary}--\r\n".encode()
    )
    req = urllib.request.Request(
        server["upload_url"], data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        up = json.loads(resp.read().decode())
    saved = api(
        "photos.saveWallPhoto", token, group_id=gid,
        photo=up["photo"], server=up["server"], hash=up["hash"],
    )
    p = saved[0]
    return f"photo{p['owner_id']}_{p['id']}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--group-id", help="e.g. -12345678 or 12345678")
    ap.add_argument("--screen-name", help="community short address (e.g. nord21vek); num id resolved via groups.getById")
    ap.add_argument("--text-file", required=True, help="path to UTF-8 file with final post text")
    ap.add_argument("--photo", help="optional local image path")
    ap.add_argument("--publish-after", type=int, help="unixtime for delayed publishing")
    args = ap.parse_args()

    token = os.environ.get("VK_TOKEN")
    if not token:
        sys.exit("VK_TOKEN environment variable is not set.")

    if args.group_id is None and args.screen_name is None:
        sys.exit("Provide either --group-id or --screen-name.")
    if args.group_id is not None:
        gid = int(args.group_id)
    else:
        info = api("groups.getById", token, group_id=args.screen_name)
        gid = -int(info["groups"][0]["id"])
        print(f"Resolved @{args.screen_name} -> group id {gid}")
    if gid > 0:
        gid = -gid  # communities are negative ids

    with open(args.text_file, encoding="utf-8") as fh:
        text = fh.read().strip()
    if not text:
        sys.exit("Post text is empty.")

    attachments = upload_photo(token, gid, args.photo) if args.photo else None

    result = api(
        "wall.post", token,
        group_id=gid, message=text, attachments=attachments,
        from_group=1, publish_date=args.publish_after,
    )
    print(json.dumps({
        "post_id": result["post_id"],
        "url": f"https://vk.com/wall{gid}_{result['post_id']}",
        "delayed": bool(args.publish_after),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
