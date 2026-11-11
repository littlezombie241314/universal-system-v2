#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""阿里云 OSS 静态站点发布器（全宇宙恒等系统）

用法:
  ALIYUN_ACCESS_KEY_ID=xxx ALIYUN_ACCESS_KEY_SECRET=yyy \
  python3 aliyun_deploy.py --dir /tmp/uv2_publish --bucket universal-system --region cn-hangzhou

行为:
  1. 若 bucket 不存在则创建（公共读）
  2. 上传 index.html / sw.js / 其它静态资源
  3. 开启静态网站托管（index.html 为默认首页与 404）
  4. 输出访问地址与校验信息
"""
import argparse
import os
import sys

import hashlib

try:
    import oss2
    from oss2.models import BucketWebsite
except ImportError:
    sys.exit("缺少 oss2，请先执行: pip install --user oss2")

SKIP_DIRS = {"alipay-backend", "node_modules", ".git", "__pycache__"}
SKIP_FILES = {".DS_Store"}


def collect(root):
    items = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name in SKIP_FILES or name.endswith(".zip"):
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            items.append((full, rel))
    return items


def content_type(rel):
    if rel.endswith(".html"):
        return "text/html; charset=utf-8"
    if rel.endswith(".js"):
        return "application/javascript; charset=utf-8"
    if rel.endswith(".css"):
        return "text/css; charset=utf-8"
    if rel.endswith(".json"):
        return "application/json; charset=utf-8"
    if rel.endswith(".svg"):
        return "image/svg+xml"
    if rel.endswith(".png"):
        return "image/png"
    if rel.endswith(".jpg") or rel.endswith(".jpeg"):
        return "image/jpeg"
    if rel.endswith(".webp"):
        return "image/webp"
    if rel.endswith(".ico"):
        return "image/x-icon"
    return "application/octet-stream"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--bucket", default=os.environ.get("ALIYUN_OSS_BUCKET", "universal-system"))
    ap.add_argument("--region", default=os.environ.get("ALIYUN_REGION", "cn-hangzhou"))
    args = ap.parse_args()

    ak_id = os.environ.get("ALIYUN_ACCESS_KEY_ID", "").strip()
    ak_secret = os.environ.get("ALIYUN_ACCESS_KEY_SECRET", "").strip()
    if not ak_id or not ak_secret:
        sys.exit("ALIYUN_CREDENTIALS_MISSING: 需要 ALIYUN_ACCESS_KEY_ID / ALIYUN_ACCESS_KEY_SECRET")

    endpoint = "https://oss-%s.aliyuncs.com" % args.region
    auth = oss2.Auth(ak_id, ak_secret)
    service = oss2.Service(auth, endpoint)
    bucket = oss2.Bucket(auth, endpoint, args.bucket)

    try:
        bucket.get_bucket_info()
        print("[aliyun] bucket 已存在: %s" % args.bucket)
    except oss2.exceptions.NoSuchBucket:
        print("[aliyun] 创建 bucket: %s (%s)" % (args.bucket, args.region))
        bucket.create_bucket(oss2.BUCKET_ACL_PUBLIC_READ)

    # 阿里云新建 bucket 默认开启「阻止公共访问」，会导致匿名访问 403
    try:
        if bucket.get_bucket_public_access_block().block_public_access:
            bucket.put_bucket_public_access_block(block_public_access=False)
            print("[aliyun] 已关闭 阻止公共访问")
        bucket.put_bucket_acl(oss2.BUCKET_ACL_PUBLIC_READ)
    except Exception as exc:
        print("[aliyun] 警告: 公共读配置失败 (%s)" % exc)

    files = collect(args.dir)
    if not files:
        sys.exit("发布目录为空: %s" % args.dir)

    for full, rel in files:
        headers = {
            "Content-Type": content_type(rel),
            "Cache-Control": "no-cache" if rel in ("index.html", "sw.js") else "public, max-age=86400",
        }
        bucket.put_object_from_file(rel, full, headers=headers)
    print("[aliyun] 已上传 %d 个文件" % len(files))

    try:
        bucket.put_bucket_website(BucketWebsite(index_file="index.html", error_file="index.html"))
        print("[aliyun] 静态网站托管已启用")
    except Exception as exc:  # 权限不足时不影响上传结果
        print("[aliyun] 警告: 静态网站托管设置失败 (%s)" % exc)

    site = "https://%s.oss-%s.aliyuncs.com/index.html" % (args.bucket, args.region)
    print("[aliyun] 访问地址: %s" % site)
    with open(os.path.join(args.dir, "index.html"), "rb") as fh:
        print("[aliyun] md5(index.html): %s" % hashlib.md5(fh.read()).hexdigest())


if __name__ == "__main__":
    main()
