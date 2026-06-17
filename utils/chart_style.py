import matplotlib.pyplot as plt

BG_DARK = '#0D1117'
BG_CARD = '#161B22'
BORDER = '#30363D'
TEXT_PRIMARY = '#E6EDF3'
TEXT_SECONDARY = '#8B949E'
ACCENT_GOLD = '#FFD700'
ACCENT_BLUE = '#58A6FF'
ACCENT_GREEN = '#3FB950'
ACCENT_PURPLE = '#BC8CFF'
ACCENT_RED = '#F85149'
ACCENT_ORANGE = '#F0883E'

def setup_theme():
    plt.rcParams.update({
        'figure.facecolor': BG_DARK,
        'axes.facecolor': BG_DARK,
        'axes.edgecolor': BORDER,
        'axes.labelcolor': TEXT_SECONDARY,
        'text.color': TEXT_PRIMARY,
        'xtick.color': TEXT_SECONDARY,
        'ytick.color': TEXT_SECONDARY,
        'grid.color': '#21262D',
        'grid.linewidth': 0.5,
        'font.size': 11,
        'font.family': 'sans-serif',
    })

def style_chart(ax, title, subtitle=''):
    ax.set_title('')
    ax.text(0, 1.08, title, transform=ax.transAxes, fontsize=18,
            fontweight='bold', color=ACCENT_GOLD, va='bottom')
    if subtitle:
        ax.text(0, 1.025, subtitle, transform=ax.transAxes,
                fontsize=10, color=TEXT_SECONDARY, va='bottom')
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis='y', length=0)
    ax.grid(axis='x', color='#21262D', linewidth=0.5, zorder=1)
    ax.grid(axis='y', visible=False)

def add_insight_box(fig, text):
    props = dict(boxstyle='round,pad=0.8', facecolor=BG_CARD,
                 edgecolor=BORDER, alpha=0.95)
    fig.text(0.05, -0.01, 'INSIGHT:  ' + text, fontsize=9.5,
             color=TEXT_SECONDARY, style='italic', wrap=True,
             bbox=props, transform=fig.transFigure)