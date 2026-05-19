CSS_VERSION = "8"


def theme_colors(request):
    if not request.user.is_authenticated:
        return {}
    colors = request.session.get('theme_colors', {})
    defaults = {
        'bg_primary': '#1a1a2e',
        'bg_secondary': '#16213e',
        'text_primary': '#e0e0e0',
        'text_secondary': '#a0a0a0',
        'accent_color': '#0f3460',
        'accent_hover': '#1a4a8a',
        'sidebar_bg': '#0f3460',
        'card_bg': '#1e2a4a',
        'border_color': '#2a3a5c',
        'success_color': '#28a745',
        'danger_color': '#dc3545',
        'warning_color': '#ffc107',
    }
    for key in defaults:
        if key not in colors:
            colors[key] = defaults[key]
    return {'theme': colors, 'css_version': CSS_VERSION}
