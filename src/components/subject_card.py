import streamlit as st 

def subject_card(name, code, section, stats=None, footer_callback=None):
    # Build stats HTML
    stats_html = ""
    if stats:
        stats_items = ""
        for icon, label, value in stats:
            stats_items += f'<div style="background:rgba(235,69,158,0.08);padding:8px 16px;border-radius:12px;font-size:0.85rem;font-weight:600;color:#c4b5fd;display:flex;align-items:center;gap:6px;"><span style="font-size:1.1rem;">{icon}</span><b style="color:#f1f5f9;">{value}</b> {label}</div>'
        stats_html = f'<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:16px;">{stats_items}</div>'

    html = f'''<div style="background:linear-gradient(135deg,rgba(88,101,242,0.12) 0%,rgba(235,69,158,0.08) 100%);border:1px solid rgba(88,101,242,0.25);border-left:5px solid #EB459E;padding:24px 28px;border-radius:16px;margin-bottom:20px;">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;">
        <div>
            <h3 style="margin:0 0 8px 0;color:#f1f5f9;font-size:1.4rem;font-weight:700;letter-spacing:-0.01em;">{name}</h3>
            <p style="color:#94a3b8;margin:0;font-size:0.9rem;display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
                <span style="background:rgba(88,101,242,0.2);color:#a5b4fc;padding:3px 10px;border-radius:6px;font-weight:600;font-size:0.82rem;letter-spacing:0.02em;">{code}</span>
                <span style="color:#475569;">•</span>
                <span>Section: <b style="color:#c4b5fd;">{section}</b></span>
            </p>
        </div>
    </div>
    {stats_html}
</div>'''
    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()