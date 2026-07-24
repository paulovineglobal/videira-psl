#!/usr/bin/env python3
"""Busca clipes de b-roll gratuitos na API do Pexels.

Uso:
    python3 pexels_broll.py "termo de busca" [--per-page 5] [--orientation landscape|portrait|square] [--min-duration 5] [--max-duration 60] [--download DIR]

A chave da API é lida da variável de ambiente PEXELS_API_KEY.
Saída: JSON com os clipes encontrados (link da página, URL de download em HD, duração, autor).
"""

import argparse
import json
import os
import ssl
import sys
import urllib.parse
import urllib.request

API_URL = "https://api.pexels.com/videos/search"


def build_context():
    ca_bundle = os.environ.get("SSL_CERT_FILE") or "/root/.ccr/ca-bundle.crt"
    if os.path.exists(ca_bundle):
        return ssl.create_default_context(cafile=ca_bundle)
    return ssl.create_default_context()


def search(query, per_page, orientation, locale):
    key = os.environ.get("PEXELS_API_KEY")
    if not key:
        sys.exit("ERRO: defina a variável de ambiente PEXELS_API_KEY")

    params = {"query": query, "per_page": per_page}
    if orientation:
        params["orientation"] = orientation
    if locale:
        params["locale"] = locale

    req = urllib.request.Request(
        f"{API_URL}?{urllib.parse.urlencode(params)}",
        headers={"Authorization": key},
    )
    with urllib.request.urlopen(req, context=build_context(), timeout=30) as resp:
        return json.load(resp)


def best_file(video, target_height=1080):
    files = video.get("video_files", [])
    hd = [f for f in files if (f.get("height") or 0) >= target_height]
    pool = hd or files
    return min(pool, key=lambda f: abs((f.get("height") or 0) - target_height), default=None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--per-page", type=int, default=5)
    ap.add_argument("--orientation", choices=["landscape", "portrait", "square"], default=None)
    ap.add_argument("--locale", default=None, help="ex.: pt-BR")
    ap.add_argument("--min-duration", type=int, default=0)
    ap.add_argument("--max-duration", type=int, default=10**6)
    ap.add_argument("--download", metavar="DIR", default=None)
    args = ap.parse_args()

    data = search(args.query, args.per_page, args.orientation, args.locale)
    results = []
    for v in data.get("videos", []):
        if not (args.min_duration <= v.get("duration", 0) <= args.max_duration):
            continue
        f = best_file(v)
        if not f:
            continue
        results.append(
            {
                "id": v["id"],
                "pagina": v["url"],
                "duracao_seg": v["duration"],
                "resolucao": f"{f.get('width')}x{f.get('height')}",
                "download": f["link"],
                "autor": v.get("user", {}).get("name"),
                "preview_imagem": v.get("image"),
            }
        )

    if args.download:
        os.makedirs(args.download, exist_ok=True)
        for r in results:
            dest = os.path.join(args.download, f"broll_{r['id']}.mp4")
            urllib.request.urlretrieve(r["download"], dest)
            r["arquivo_local"] = dest

    json.dump({"query": args.query, "total": len(results), "clipes": results}, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
