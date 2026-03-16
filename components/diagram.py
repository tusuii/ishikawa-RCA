import math
import streamlit as st
import streamlit.components.v1 as components
from utils.state import CATEGORIES, CATEGORY_COLORS, get_all_causes

# ── Canvas constants ───────────────────────────────────────────────────────────
W          = 1200
H          = 560
SPINE_Y    = H // 2
SPINE_X1   = 60
SPINE_X2   = W - 180
HEAD_X     = W - 30
BONE_ANGLE = 38   # degrees from spine
BONE_LEN   = 150  # main rib length
SUB_LEN    = 52   # sub-bone (cause) length
MAX_CAUSES = 6    # max causes rendered per category


# ── Helpers ───────────────────────────────────────────────────────────────────

def _trunc(s: str, n: int) -> str:
    return s[:n] + "…" if len(s) > n else s


def _hex_alpha(hex_color: str, alpha: float) -> str:
    """Convert #rrggbb + alpha to rgba(r,g,b,a)."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


# ── SVG builder ───────────────────────────────────────────────────────────────

def _build_svg(causes: dict, effect: str) -> str:
    parts: list[str] = []
    rad = math.radians(BONE_ANGLE)

    # ── defs ────────────────────────────────────────────────────────────────
    parts.append(f"""
<defs>
  <marker id="arr" markerWidth="9" markerHeight="6"
          refX="9" refY="3" orient="auto">
    <polygon points="0 0, 9 3, 0 6" fill="#58a6ff"/>
  </marker>
  <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="4" result="blur"/>
    <feMerge>
      <feMergeNode in="blur"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>
  <filter id="glow-soft" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="2" result="blur"/>
    <feMerge>
      <feMergeNode in="blur"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>
  <linearGradient id="spine-grad" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%"   stop-color="#1f6feb" stop-opacity="0.6"/>
    <stop offset="100%" stop-color="#58a6ff"/>
  </linearGradient>
</defs>""")

    # ── background ──────────────────────────────────────────────────────────
    parts.append(f'<rect width="{W}" height="{H}" fill="#0d1117" rx="0"/>')

    # subtle dot grid
    for gx in range(0, W, 48):
        for gy in range(0, H, 48):
            parts.append(f'<circle cx="{gx}" cy="{gy}" r="0.8" fill="#1c2128"/>')

    # ── spine ───────────────────────────────────────────────────────────────
    parts.append(
        f'<line x1="{SPINE_X1}" y1="{SPINE_Y}" x2="{SPINE_X2}" y2="{SPINE_Y}" '
        f'stroke="url(#spine-grad)" stroke-width="3" marker-end="url(#arr)"/>'
    )

    # ── fish head ───────────────────────────────────────────────────────────
    hw, hh = 155, 56
    hx = SPINE_X2 + 8
    hy = SPINE_Y - hh // 2
    parts.append(
        f'<rect x="{hx}" y="{hy}" width="{hw}" height="{hh}" rx="8" '
        f'fill="#0d1f3c" stroke="#58a6ff" stroke-width="1.8" filter="url(#glow)"/>'
    )
    # effect text — wrap into two lines if long
    eff = effect or "Production Incident"
    line1 = _trunc(eff, 18)
    line2 = _trunc(eff[18:], 18) if len(eff) > 18 else ""
    cx = hx + hw // 2
    if line2:
        parts.append(
            f'<text x="{cx}" y="{SPINE_Y - 6}" fill="#e6edf3" '
            f'font-size="10.5" font-weight="700" font-family="monospace" '
            f'text-anchor="middle">{line1}</text>'
        )
        parts.append(
            f'<text x="{cx}" y="{SPINE_Y + 9}" fill="#e6edf3" '
            f'font-size="10.5" font-weight="700" font-family="monospace" '
            f'text-anchor="middle">{line2}</text>'
        )
    else:
        parts.append(
            f'<text x="{cx}" y="{SPINE_Y + 4}" fill="#e6edf3" '
            f'font-size="11" font-weight="700" font-family="monospace" '
            f'text-anchor="middle">{line1}</text>'
        )

    # ── bones ───────────────────────────────────────────────────────────────
    # 6 categories → 3 top (even indices) + 3 bottom (odd indices)
    top_cats = CATEGORIES[0::2]   # People, Tools/Tech, Measurement
    bot_cats = CATEGORIES[1::2]   # Process, Environment, Materials/Data

    n = len(top_cats)
    usable = SPINE_X2 - SPINE_X1
    x_positions = [
        SPINE_X1 + usable * (i + 1) / (n + 1)
        for i in range(n)
    ]

    for i, (top_cat, bot_cat) in enumerate(zip(top_cats, bot_cats)):
        bx = x_positions[i]

        for cat, direction in [(top_cat, -1), (bot_cat, +1)]:
            color = CATEGORY_COLORS[cat]
            color_dim = _hex_alpha(color, 0.55)

            end_x = bx - BONE_LEN * math.cos(rad)
            end_y = SPINE_Y + direction * BONE_LEN * math.sin(rad)

            # Rib bone
            parts.append(
                f'<line x1="{bx:.1f}" y1="{SPINE_Y}" '
                f'x2="{end_x:.1f}" y2="{end_y:.1f}" '
                f'stroke="{color}" stroke-width="2.2" '
                f'filter="url(#glow-soft)"/>'
            )

            # Joint dot at spine
            parts.append(
                f'<circle cx="{bx:.1f}" cy="{SPINE_Y}" r="4" '
                f'fill="{color}" opacity="0.9"/>'
            )

            # Category label
            label_y = end_y - 12 if direction == -1 else end_y + 20
            parts.append(
                f'<text x="{end_x:.1f}" y="{label_y:.1f}" fill="{color}" '
                f'font-size="11" font-weight="700" font-family="monospace" '
                f'text-anchor="middle">{cat}</text>'
            )

            # ── sub-bones (causes) ──────────────────────────────────────────
            cat_causes = causes.get(cat, [])[:MAX_CAUSES]
            n_causes = len(cat_causes)

            for j, cause in enumerate(cat_causes):
                t = (j + 1) / (n_causes + 1)
                # Point along rib
                px = bx + (end_x - bx) * t
                py = SPINE_Y + (end_y - SPINE_Y) * t

                # Sub-bone direction: roughly perpendicular toward spine
                sx = px + SUB_LEN * math.cos(rad) * 0.65
                sy = py - direction * SUB_LEN * 0.75

                parts.append(
                    f'<line x1="{px:.1f}" y1="{py:.1f}" '
                    f'x2="{sx:.1f}" y2="{sy:.1f}" '
                    f'stroke="{color_dim}" stroke-width="1.3" '
                    f'stroke-dasharray="3 2"/>'
                )

                # Tiny dot at the cause end
                parts.append(
                    f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="2" '
                    f'fill="{color}" opacity="0.7"/>'
                )

                # Cause text
                txt_x = sx + (4 if sx > px else -4)
                txt_anchor = "start" if sx > px else "end"
                txt_y = sy - 4 if direction == -1 else sy + 12
                parts.append(
                    f'<text x="{txt_x:.1f}" y="{txt_y:.1f}" '
                    f'fill="#c9d1d9" font-size="9" font-family="monospace" '
                    f'text-anchor="{txt_anchor}">'
                    f'{_trunc(cause, 24)}</text>'
                )

    # ── title bar ───────────────────────────────────────────────────────────
    parts.append(
        f'<text x="12" y="20" fill="#58a6ff" font-size="11" '
        f'font-weight="700" font-family="monospace" opacity="0.7">'
        f'ISHIKAWA  ·  ROOT CAUSE ANALYSIS</text>'
    )

    inner = "\n".join(parts)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {W} {H}" '
        f'width="100%" height="auto" '
        f'style="display:block;">'
        f'{inner}'
        f'</svg>'
    )


# ── Streamlit renderer ────────────────────────────────────────────────────────

def render_fishbone_svg():
    st.markdown("### 🎯 Live Fishbone Diagram")

    causes = get_all_causes()
    effect = st.session_state.incident.get("effect", "Production Incident")
    total  = sum(len(v) for v in causes.values())

    if total == 0:
        st.info("⬅️ Add causes in the form to render the fishbone diagram.")

    svg = _build_svg(causes, effect)

    components.html(
        f"""<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background:#0d1117;">
  <div style="background:#0d1117;border:1px solid #21262d;
              border-radius:8px;padding:10px 10px 6px;overflow:hidden;">
    {svg}
  </div>
</body>
</html>""",
        height=500,
        scrolling=False,
    )

    st.download_button(
        label="⬇️ Export SVG",
        data=svg.encode("utf-8"),
        file_name="fishbone_rca.svg",
        mime="image/svg+xml",
        use_container_width=True,
    )
