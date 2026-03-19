import plotly.graph_objects as go


def build_sankey() -> go.Figure:
    # Updated data from the application tracker.
    raw_links = [
        ("Total Applications", "Ghosted/Rejected", 107),
        ("Total Applications", "Interview", 6),
        ("Total Applications", "OA (Online Assessment)", 3),
        ("Interview", "Offer", 2),
        ("Interview", "Ranked", 3),
        ("Interview", "Ghosted/Rejected", 1),
        ("Interview", "Denied Interview", 1),
        ("OA (Online Assessment)", "Interview", 1),
    ]

    # Transform to: Total -> Initial Status -> Final Outcome,
    # while preserving OA -> Interview as a middle step.
    total_apps = sum(v for s, _, v in raw_links if s == "Total Applications")
    initial_ghosted = next(v for s, t, v in raw_links if s == "Total Applications" and t == "Ghosted/Rejected")
    initial_oa = next(v for s, t, v in raw_links if s == "Total Applications" and t == "OA (Online Assessment)")
    initial_interview = next(v for s, t, v in raw_links if s == "Total Applications" and t == "Interview")

    oa_to_interview = next(v for s, t, v in raw_links if s == "OA (Online Assessment)" and t == "Interview")

    interview_offer = next(v for s, t, v in raw_links if s == "Interview" and t == "Offer")
    interview_ranked = next(v for s, t, v in raw_links if s == "Interview" and t == "Ranked")
    interview_rejected = next(v for s, t, v in raw_links if s == "Interview" and t == "Ghosted/Rejected")
    interview_denied = next(v for s, t, v in raw_links if s == "Interview" and t == "Denied Interview")

    interview_total = initial_interview + oa_to_interview
    ghosted_total = initial_ghosted + interview_rejected

    node_keys = [
        "Total Applications",
        "Ghosted/Rejected",
        "OA",
        "Interview",
        "Ranked",
        "Offer",
        "Denied Interview",
    ]
    labels = [
        f"Total Applications ({total_apps})",
        f"Ghosted/Rejected ({ghosted_total})",
        f"OA ({initial_oa})",
        f"Interview ({interview_total})",
        f"Ranked ({interview_ranked})",
        f"Offer ({interview_offer})",
        f"Denied Interview ({interview_denied})",
    ]
    index = {label: i for i, label in enumerate(node_keys)}

    links = [
        ("Total Applications", "Ghosted/Rejected", initial_ghosted),
        ("Total Applications", "OA", initial_oa),
        ("Total Applications", "Interview", initial_interview),
        ("OA", "Interview", oa_to_interview),
        ("Interview", "Offer", interview_offer),
        ("Interview", "Ranked", interview_ranked),
        ("Interview", "Ghosted/Rejected", interview_rejected),
        ("Interview", "Denied Interview", interview_denied),
    ]

    source = [index[s] for s, _, _ in links]
    target = [index[t] for _, t, _ in links]
    value = [v for _, _, v in links]

    link_labels = [
        f"{s} -> {t}: {v}"
        for s, t, v in links
    ]

    green = "#4E9F68"
    red = "#C65555"
    light_gold = "#E1AD01"
    dark_gray = "#333333"
    white = "#FFFFFF"

    green_rgba = "rgba(78, 159, 104, 0.42)"
    red_rgba = "rgba(198, 85, 85, 0.40)"
    light_gold_rgba = "rgba(225, 173, 1, 0.58)"

    node_colors = [
        green,  # Total Applications
        red,    # Ghosted/Rejected
        green,  # OA
        green,  # Interview
        green,  # Ranked
        light_gold,  # Offer
        red,    # Denied Interview
    ]

    link_colors = []
    for s, t, _ in links:
        if t == "Offer":
            link_colors.append(light_gold_rgba)
        elif t in {"Ghosted/Rejected", "Denied Interview"}:
            link_colors.append(red_rgba)
        else:
            link_colors.append(green_rgba)

    fig = go.Figure(
        data=[
            go.Sankey(
                arrangement="snap",
                node=dict(
                    pad=40,
                    thickness=15,
                    line=dict(color=white, width=0),
                    label=labels,
                    color=node_colors,
                    # Position Ghosted/Rejected toward the top so high-volume
                    # rejection flow recedes into the background.
                    x=[0.02, 0.50, 0.28, 0.56, 0.86, 0.86, 0.86],
                    y=[0.46, 0.06, 0.72, 0.78, 0.58, 0.82, 0.24],
                ),
                link=dict(
                    source=source,
                    target=target,
                    value=value,
                    color=link_colors,
                    label=link_labels,
                    line=dict(color="rgba(255,255,255,0)", width=0),
                    hovertemplate="%{label}<extra></extra>",
                ),
            )
        ]
    )

    fig.update_layout(
        title_text=f"Job Application Funnel ({total_apps} Applications)",
        font_size=12,
        font=dict(family="Arial, sans-serif", color=dark_gray),
        paper_bgcolor=white,
        plot_bgcolor=white,
        margin=dict(l=20, r=20, t=60, b=20),
    )

    return fig


if __name__ == "__main__":
    figure = build_sankey()
    figure.show(config={"displayModeBar": False})
