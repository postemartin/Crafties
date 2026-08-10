#!/usr/bin/env python3
"""Team Crafties Pattern Image Toolkit.

Local CLI for choosing image-generation presets, rendering consistent prompts,
calling FAL.ai directly when a key is available, and making deterministic SVG
pattern diagrams when exact craft instructions matter more than AI imagery.

No third-party Python packages are required.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "scripts" / "pattern-image-presets.json"
HERMES_ENV = Path.home() / ".hermes" / ".env"
LOCAL_ENV = ROOT / ".env"
VALID_ASPECTS = {"landscape", "square", "portrait"}


class ToolkitError(RuntimeError):
    """User-facing toolkit error."""


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = value.replace("é", "e").replace("è", "e").replace("ê", "e")
    value = value.replace("à", "a").replace("ç", "c").replace("ï", "i")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "crafties-image"


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def load_config() -> dict[str, Any]:
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ToolkitError(f"missing config: {CONFIG_PATH}") from exc
    except json.JSONDecodeError as exc:
        raise ToolkitError(f"invalid JSON in {CONFIG_PATH}: {exc}") from exc


def output_root(config: dict[str, Any]) -> Path:
    return ROOT / config.get("output_root", ".crafties-toolkit")


def get_preset(config: dict[str, Any], name: str) -> dict[str, Any]:
    presets = config.get("presets", {})
    if name not in presets:
        choices = ", ".join(sorted(presets))
        raise ToolkitError(f"unknown preset '{name}'. Available presets: {choices}")
    preset = dict(presets[name])
    preset["name"] = name
    return preset


def render_prompt(preset: dict[str, Any], title: str, craft: str, details: str) -> str:
    template = preset.get("prompt_template")
    if not template:
        raise ToolkitError(f"preset '{preset['name']}' does not define a prompt_template")
    prompt = template.format(
        title=title.strip(),
        craft=(craft or "general craft").strip(),
        details=(details or "clear beginner-friendly finished pattern asset").strip(),
    )
    # Shared guardrail: pattern images should not pretend a physically tested
    # object exists unless the user supplied a real sample photo.
    return " ".join(prompt.split())


def request_json(url: str, *, method: str = "GET", payload: dict[str, Any] | None = None, headers: dict[str, str] | None = None, timeout: int = 90) -> dict[str, Any]:
    body = None
    request_headers = {"User-Agent": "TeamCraftiesPatternToolkit/1.0"}
    if headers:
        request_headers.update(headers)
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        request_headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=request_headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            text = response.read().decode("utf-8")
            return json.loads(text)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:600]
        raise ToolkitError(f"HTTP {exc.code} from {url}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise ToolkitError(f"network error calling {url}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ToolkitError(f"non-JSON response from {url}: {exc}") from exc


def fal_payload(preset: dict[str, Any], prompt: str, aspect_ratio: str, seed: int | None) -> dict[str, Any]:
    aspect = aspect_ratio or preset.get("aspect_ratio", "square")
    if aspect not in VALID_ASPECTS:
        raise ToolkitError(f"aspect must be one of {sorted(VALID_ASPECTS)}, got '{aspect}'")
    payload = dict(preset.get("defaults", {}))
    size_key = preset.get("size_parameter")
    if size_key:
        sizes = preset.get("sizes", {})
        payload[size_key] = sizes.get(aspect, sizes.get("square", "square_hd"))
    payload["prompt"] = prompt
    if seed is not None:
        payload["seed"] = seed
    # Drop None values to avoid model-specific schema errors.
    return {key: value for key, value in payload.items() if value is not None}


def submit_fal(model: str, payload: dict[str, Any], timeout: int) -> dict[str, Any]:
    fal_key = os.environ.get("FAL_KEY")
    if not fal_key:
        raise ToolkitError("FAL_KEY is missing. Add it to ~/.hermes/.env or export it before running generate.")
    headers = {"Authorization": f"Key {fal_key}"}
    submit_url = f"https://queue.fal.run/{model}"
    submitted = request_json(submit_url, method="POST", payload=payload, headers=headers, timeout=timeout)

    if "images" in submitted or "image" in submitted:
        return submitted

    status_url = submitted.get("status_url")
    response_url = submitted.get("response_url") or submitted.get("result_url")
    if not status_url and not response_url:
        raise ToolkitError(f"FAL response did not include status/result URLs: {submitted}")

    deadline = time.time() + timeout
    last_status = "submitted"
    while time.time() < deadline:
        if status_url:
            status = request_json(status_url, headers=headers, timeout=min(30, timeout), method="GET")
            last_status = str(status.get("status", last_status))
            response_url = status.get("response_url") or status.get("result_url") or response_url
            if last_status.upper() in {"COMPLETED", "DONE"} and response_url:
                return request_json(response_url, headers=headers, timeout=min(90, timeout), method="GET")
            if last_status.upper() in {"FAILED", "ERROR"}:
                raise ToolkitError(f"FAL generation failed: {status}")
        elif response_url:
            return request_json(response_url, headers=headers, timeout=min(90, timeout), method="GET")
        time.sleep(2)

    raise ToolkitError(f"timed out waiting for FAL result; last status: {last_status}")


def first_image_url(result: dict[str, Any]) -> str:
    images = result.get("images")
    if isinstance(images, list) and images:
        first = images[0]
        if isinstance(first, dict) and first.get("url"):
            return first["url"]
        if isinstance(first, str):
            return first
    image = result.get("image")
    if isinstance(image, dict) and image.get("url"):
        return image["url"]
    if isinstance(image, str):
        return image
    raise ToolkitError(f"could not find image URL in FAL result keys: {sorted(result.keys())}")


def download_file(url: str, destination: Path, timeout: int = 120) -> int:
    destination.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "TeamCraftiesPatternToolkit/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = response.read()
    except urllib.error.URLError as exc:
        raise ToolkitError(f"failed to download generated image: {exc}") from exc
    if len(data) < 5000:
        preview = data[:500].decode("utf-8", "replace")
        raise ToolkitError(f"downloaded response is too small to be an image ({len(data)} bytes): {preview}")
    destination.write_bytes(data)
    return len(data)


def pollinations_url(prompt: str, preset: dict[str, Any], aspect_ratio: str, seed: int | None) -> str:
    aspect = aspect_ratio or preset.get("aspect_ratio", "square")
    if aspect not in VALID_ASPECTS:
        raise ToolkitError(f"aspect must be one of {sorted(VALID_ASPECTS)}, got '{aspect}'")
    width, height = preset.get("sizes", {}).get(aspect, [1024, 1024])
    params = {
        "width": str(width),
        "height": str(height),
        "nologo": "true",
        "private": "true",
        "enhance": "true",
    }
    if seed is not None:
        params["seed"] = str(seed)
    encoded_prompt = urllib.parse.quote(prompt)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?{urllib.parse.urlencode(params)}"


def write_sidecar(destination: Path, metadata: dict[str, Any]) -> Path:
    sidecar = destination.with_suffix(destination.suffix + ".json")
    sidecar.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    return sidecar


def command_list(args: argparse.Namespace) -> None:
    config = load_config()
    print("Team Crafties Pattern Image Toolkit presets:\n")
    for name, preset in config.get("presets", {}).items():
        model = preset.get("model", "local")
        print(f"- {name}")
        print(f"  {preset.get('label', '')}")
        print(f"  model: {model}")
        print(f"  best for: {preset.get('best_for', '')}\n")


def command_prompt(args: argparse.Namespace) -> None:
    config = load_config()
    preset = get_preset(config, args.preset)
    print(render_prompt(preset, args.title, args.craft, args.details))


def command_check(args: argparse.Namespace) -> None:
    load_dotenv(HERMES_ENV)
    load_dotenv(LOCAL_ENV)
    config = load_config()
    out = output_root(config)
    out.mkdir(parents=True, exist_ok=True)
    presets = config.get("presets", {})
    fal_presets = [name for name, preset in presets.items() if preset.get("kind") == "fal-image"]
    missing = [name for name in fal_presets if not presets[name].get("model")]
    if missing:
        raise ToolkitError(f"FAL presets missing model: {', '.join(missing)}")
    print(f"OK config: {CONFIG_PATH.relative_to(ROOT)}")
    print(f"OK presets: {len(presets)} ({', '.join(sorted(presets))})")
    print(f"OK output root: {out.relative_to(ROOT)}")
    if os.environ.get("FAL_KEY"):
        print("OK FAL_KEY: present (value hidden)")
    else:
        print("WARN FAL_KEY: missing; prompt/diagram modes still work, generate mode will not")
    print("OK no extra Python packages required")


def command_generate(args: argparse.Namespace) -> None:
    load_dotenv(HERMES_ENV)
    load_dotenv(LOCAL_ENV)
    config = load_config()
    preset = get_preset(config, args.preset)
    if preset.get("kind") == "local-svg-diagram":
        make_diagram(args, config)
        return
    if preset.get("kind") == "local-cover-svg":
        make_cover(args, config)
        return
    prompt = render_prompt(preset, args.title, args.craft, args.details)
    aspect = args.aspect or preset.get("aspect_ratio", "square")

    if preset.get("kind") == "pollinations-image":
        url = pollinations_url(prompt, preset, aspect, args.seed)
        if args.dry_run:
            print(json.dumps({"model": preset.get("model"), "url": url, "prompt": prompt}, indent=2))
            return
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = args.output or f"{slugify(args.title)}-{args.preset}-{stamp}.jpg"
        destination = output_root(config) / "images" / filename
        size = download_file(url, destination, timeout=args.timeout)
        sidecar = write_sidecar(destination, {
            "title": args.title,
            "craft": args.craft,
            "details": args.details,
            "preset": args.preset,
            "model": preset.get("model"),
            "aspect_ratio": aspect,
            "prompt": prompt,
            "generated_at": stamp,
            "image": str(destination.relative_to(ROOT)),
            "note": "Free Pollinations draft fallback; review before publishing.",
        })
        print(f"generated: {destination.relative_to(ROOT)} ({size:,} bytes)")
        print(f"metadata:  {sidecar.relative_to(ROOT)}")
        return

    if preset.get("kind") != "fal-image":
        raise ToolkitError(f"preset '{args.preset}' is not an image preset")
    payload = fal_payload(preset, prompt, aspect, args.seed)
    if args.dry_run:
        print(json.dumps({"model": preset["model"], "payload": payload}, indent=2))
        return

    result = submit_fal(preset["model"], payload, args.timeout)
    image_url = first_image_url(result)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = args.output or f"{slugify(args.title)}-{args.preset}-{stamp}.png"
    destination = output_root(config) / "images" / filename
    size = download_file(image_url, destination)
    sidecar = write_sidecar(destination, {
        "title": args.title,
        "craft": args.craft,
        "details": args.details,
        "preset": args.preset,
        "model": preset["model"],
        "aspect_ratio": aspect,
        "prompt": prompt,
        "payload": {key: value for key, value in payload.items() if key != "prompt"},
        "generated_at": stamp,
        "image": str(destination.relative_to(ROOT)),
    })
    print(f"generated: {destination.relative_to(ROOT)} ({size:,} bytes)")
    print(f"metadata:  {sidecar.relative_to(ROOT)}")


def parse_component(value: str) -> tuple[str, str]:
    if ":" in value:
        label, detail = value.split(":", 1)
    elif "|" in value:
        label, detail = value.split("|", 1)
    else:
        label, detail = value, ""
    return label.strip(), detail.strip()


def wrap_words(text: str, limit: int, max_lines: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) > limit and current:
            lines.append(current)
            current = word
            if len(lines) >= max_lines:
                break
        else:
            current = candidate
    if current and len(lines) < max_lines:
        lines.append(current)
    if len(lines) == max_lines and words:
        original = " ".join(words)
        if len(" ".join(lines)) < len(original):
            lines[-1] = lines[-1].rstrip(".,;: ") + "…"
    return lines or [""]


def make_cover(args: argparse.Namespace, config: dict[str, Any] | None = None) -> None:
    config = config or load_config()
    title_lines = wrap_words(args.title, 18, 3)
    detail_lines = wrap_words(args.details or args.craft or "Beginner-friendly craft pattern", 38, 3)
    title_svg = "\n".join(
        f'<text x="600" y="{330 + i * 82}" text-anchor="middle" font-size="70" font-weight="950" fill="#2f164f">{html.escape(line)}</text>'
        for i, line in enumerate(title_lines)
    )
    detail_svg = "\n".join(
        f'<text x="600" y="{620 + i * 36}" text-anchor="middle" font-size="28" font-weight="750" fill="#6f4e99">{html.escape(line)}</text>'
        for i, line in enumerate(detail_lines)
    )
    craft_label = html.escape((args.craft or "Craft pattern").title())
    safe_title = html.escape(args.title)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1200" role="img" aria-labelledby="title desc">
<title id="title">{safe_title} Team Crafties cover</title>
<desc id="desc">A clean local Team Crafties pattern cover for {safe_title}.</desc>
<defs>
  <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#fffaf2"/><stop offset=".48" stop-color="#f1e7ff"/><stop offset="1" stop-color="#ddfbf7"/></linearGradient>
  <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="24" stdDeviation="20" flood-color="#5b2da0" flood-opacity=".16"/></filter>
  <style><![CDATA[text {{ font-family: Inter, Avenir Next, Arial, sans-serif; }}]]></style>
</defs>
<rect width="1200" height="1200" fill="#fffaf2"/>
<rect width="1200" height="1200" rx="84" fill="url(#bg)"/>
<circle cx="170" cy="190" r="92" fill="#34d6c3" opacity=".32"/>
<circle cx="1040" cy="220" r="130" fill="#ff8ec7" opacity=".24"/>
<circle cx="1020" cy="970" r="112" fill="#fff2a8" opacity=".58"/>
<circle cx="170" cy="1010" r="116" fill="#b894ff" opacity=".28"/>
<rect x="118" y="128" width="964" height="944" rx="76" fill="#fffefb" opacity=".92" filter="url(#shadow)"/>
<path d="M238 234h724" stroke="#efe0ff" stroke-width="12" stroke-linecap="round"/>
<path d="M238 958h724" stroke="#ddfbf7" stroke-width="18" stroke-linecap="round"/>
<rect x="378" y="178" width="444" height="66" rx="33" fill="#5b2da0"/>
<text x="600" y="222" text-anchor="middle" font-size="28" font-weight="900" fill="#fff">TEAM CRAFTIES</text>
<rect x="436" y="760" width="328" height="58" rx="29" fill="#fff2a8" stroke="#5b2da0" stroke-width="5"/>
<text x="600" y="799" text-anchor="middle" font-size="26" font-weight="900" fill="#2f164f">{craft_label}</text>
{title_svg}
{detail_svg}
<g transform="translate(500 850)">
  <circle cx="100" cy="72" r="48" fill="#b894ff" stroke="#5b2da0" stroke-width="8"/>
  <ellipse cx="77" cy="76" rx="12" ry="9" fill="#2f164f"/><ellipse cx="123" cy="76" rx="12" ry="9" fill="#2f164f"/>
  <path d="M81 99c15 13 38 13 53 0" fill="none" stroke="#2f164f" stroke-width="7" stroke-linecap="round"/>
  <path d="M143 31c22-30 58-19 62 9-25-7-43 4-62-9z" fill="#34d6c3" stroke="#5b2da0" stroke-width="6"/>
  <circle cx="191" cy="29" r="10" fill="#fff2a8" stroke="#5b2da0" stroke-width="4"/>
</g>
<text x="600" y="1030" text-anchor="middle" font-size="24" font-weight="800" fill="#6f4e99">Free pattern • warm handmade steps • beginner friendly</text>
</svg>
'''
    filename = args.output or f"{slugify(args.title)}-local-cover.svg"
    destination = output_root(config) / "covers" / filename
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(svg, encoding="utf-8")
    print(f"cover: {destination.relative_to(ROOT)}")


def make_diagram(args: argparse.Namespace, config: dict[str, Any] | None = None) -> None:
    config = config or load_config()
    components = [parse_component(value) for value in (args.component or [])]
    if not components:
        components = [
            ("1", "Main piece / first round"),
            ("2", "Add small pieces"),
            ("3", "Assemble and finish"),
        ]
    width, height = 1200, 760
    card_w, card_h = 320, 170
    gap = 48
    cols = min(3, max(1, len(components)))
    start_x = (width - (cols * card_w + (cols - 1) * gap)) // 2
    rows = (len(components) + cols - 1) // cols
    start_y = 190 if rows == 1 else 155
    palette = ["#f1e7ff", "#ddfbf7", "#fff4be", "#ffe0ef", "#eadfff"]
    cards = []
    arrows = []
    for idx, (label, detail) in enumerate(components):
        row, col = divmod(idx, cols)
        x = start_x + col * (card_w + gap)
        y = start_y + row * (card_h + 64)
        color = palette[idx % len(palette)]
        num = idx + 1
        cards.append(f'''
  <g class="step-card">
    <rect x="{x}" y="{y}" width="{card_w}" height="{card_h}" rx="34" fill="{color}" stroke="#5b2da0" stroke-width="5"/>
    <circle cx="{x+42}" cy="{y+42}" r="25" fill="#5b2da0"/>
    <text x="{x+42}" y="{y+51}" text-anchor="middle" font-size="28" fill="#fff" font-weight="800">{num}</text>
    <text x="{x+84}" y="{y+48}" font-size="27" fill="#2f164f" font-weight="800">{html.escape(label[:24])}</text>
    <foreignObject x="{x+30}" y="{y+76}" width="{card_w-60}" height="{card_h-98}">
      <div xmlns="http://www.w3.org/1999/xhtml" class="detail">{html.escape(detail)}</div>
    </foreignObject>
  </g>''')
        if idx < len(components) - 1:
            nrow, ncol = divmod(idx + 1, cols)
            if nrow == row:
                x1, y1 = x + card_w + 8, y + card_h / 2
                x2, y2 = x + card_w + gap - 8, y + card_h / 2
            else:
                x1, y1 = x + card_w / 2, y + card_h + 10
                x2, y2 = start_x + ncol * (card_w + gap) + card_w / 2, y + card_h + 54
            arrows.append(f'<path d="M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}" stroke="#5b2da0" stroke-width="8" stroke-linecap="round" marker-end="url(#arrow)"/>')
    safe_title = html.escape(args.title)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{safe_title} Team Crafties pattern diagram</title>
<desc id="desc">A clean Team Crafties assembly or stitch helper diagram for {safe_title}.</desc>
<defs>
  <marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 Z" fill="#5b2da0"/></marker>
  <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#fffaf2"/><stop offset="1" stop-color="#efe5ff"/></linearGradient>
  <style><![CDATA[
    text {{ font-family: Inter, Arial, sans-serif; }}
    .detail {{ font: 700 20px/1.25 Inter, Arial, sans-serif; color: #3b235e; overflow-wrap: break-word; }}
  ]]></style>
</defs>
<rect width="{width}" height="{height}" fill="#fffaf2"/>
<rect width="{width}" height="{height}" rx="56" fill="url(#bg)"/>
<circle cx="100" cy="90" r="42" fill="#34d6c3" opacity=".45"/>
<circle cx="1090" cy="120" r="52" fill="#ff8ec7" opacity=".35"/>
<text x="600" y="92" text-anchor="middle" font-size="48" font-weight="900" fill="#2f164f">{safe_title}</text>
<text x="600" y="136" text-anchor="middle" font-size="24" font-weight="700" fill="#6f4e99">Team Crafties pattern helper • exact labels, no AI guessing</text>
{''.join(arrows)}
{''.join(cards)}
<text x="600" y="710" text-anchor="middle" font-size="22" font-weight="800" fill="#6f4e99">Use diagrams for stitch counts, assembly order, and printable clarity.</text>
</svg>
'''
    filename = args.output or f"{slugify(args.title)}-assembly-diagram.svg"
    destination = output_root(config) / "diagrams" / filename
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(svg, encoding="utf-8")
    print(f"diagram: {destination.relative_to(ROOT)}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Team Crafties pattern image and diagram toolkit")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="List available presets")
    p_list.set_defaults(func=command_list)

    p_check = sub.add_parser("check", help="Validate local config and credential availability")
    p_check.set_defaults(func=command_check)

    p_prompt = sub.add_parser("prompt", help="Render the exact prompt for a preset")
    p_prompt.add_argument("--preset", required=True)
    p_prompt.add_argument("--title", required=True)
    p_prompt.add_argument("--craft", default="general craft")
    p_prompt.add_argument("--details", default="")
    p_prompt.set_defaults(func=command_prompt)

    p_generate = sub.add_parser("generate", help="Generate an image through FAL or a local SVG diagram preset")
    p_generate.add_argument("--preset", required=True)
    p_generate.add_argument("--title", required=True)
    p_generate.add_argument("--craft", default="general craft")
    p_generate.add_argument("--details", default="")
    p_generate.add_argument("--aspect", choices=sorted(VALID_ASPECTS))
    p_generate.add_argument("--seed", type=int)
    p_generate.add_argument("--timeout", type=int, default=180)
    p_generate.add_argument("--output", help="Output filename inside .crafties-toolkit/images or diagrams")
    p_generate.add_argument("--dry-run", action="store_true", help="Print model payload without calling FAL")
    p_generate.add_argument("--component", action="append", help="For assembly-diagram-svg: 'Label: detail' (repeatable)")
    p_generate.set_defaults(func=command_generate)

    p_diagram = sub.add_parser("diagram", help="Create a deterministic SVG assembly/stitch helper")
    p_diagram.add_argument("--title", required=True)
    p_diagram.add_argument("--component", action="append", help="'Label: detail' (repeatable)")
    p_diagram.add_argument("--output")
    p_diagram.set_defaults(func=lambda args: make_diagram(args))
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
        return 0
    except ToolkitError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
