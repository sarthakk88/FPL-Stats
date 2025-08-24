import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
from config import team_order, player_orders

def reorder_columns(df, order):
    """Reorder columns. Extra columns appended at end."""
    actual = [col for col in order if col in df.columns]
    rest = [col for col in df.columns if col not in actual]
    return df[actual + rest]

# Page configuration
st.set_page_config(
    page_title="FPL Statistics Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Team shirt configurations
shirt = {
    'LIV': 'https://resources.premierleague.com/premierleague/photo/2018/01/31/d46d02f3-6ef5-4d59-9b78-ef1efd0877d4/ZqLnngek.png',
    'ARS': 'https://resources.premierleague.com/premierleague/photo/2018/01/31/6179608c-4245-4fb9-a9bd-c38721e0c62e/ccPBfVAM.png',
    'NEW': 'https://resources.premierleague.com/premierleague/photo/2018/01/31/efd535e0-574a-423f-b3df-6083bf23f6f0/LFhoSfpV.png',
    'MCI': 'https://resources.premierleague.com/premierleague/photo/2018/01/31/cf8eb725-af7f-4dee-a8af-2acafcdaeb5a/XrxExIPn.png',
    'TOT': 'https://resources.premierleague.com/premierleague/photo/2018/01/31/0ccf1ec6-bbcc-4275-b5d0-8aab85f44c8f/LkwecygZ.png',
    'MUN': 'https://resources.premierleague.com/premierleague/photo/2018/01/31/279c9b39-a25e-4667-b336-8c74ae8c89b4/VVfyUSET.png',
    'EVE': 'https://resources.premierleague.com/premierleague/photo/2018/01/31/c97bde1c-1314-438d-b829-826ac9236b33/kcXAMuAN.png',
    'CHE': 'https://resources.premierleague.com/premierleague/photo/2018/01/31/84edc231-e6e8-4705-a9e6-91e09f93faee/zmrvxhOe.png',
    'CPL': 'https://resources.premierleague.com/premierleague/photo/2018/01/31/284249d1-c028-4496-8326-e7e0b86c2775/kJVLAgWE.png',
    'BRI': 'https://resources.premierleague.com/photos/2020/09/16/fce4c413-157d-4ac8-8721-4000d7d877b1/BHA_HK_516_2020_21.png?width=235&height=310',
    'IPS': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_40-66.webp',
    'BOU': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_91-66.webp',
    'BRE': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_94-66.webp',
    'WOL': 'https://resources.premierleague.com/premierleague/photo/2018/01/31/47cdb4b8-f4f3-4762-af43-15fa1bfe2ce3/fcCQTeYw.png',
    'AVL': 'https://resources.premierleague.com/premierleague/photo/2018/01/31/3a23312a-529b-45f2-aa66-e499bbd66baa/hwgrFXdl.png',
    'FUL': 'https://resources.premierleague.com/premierleague/photo/2018/01/31/ada45e57-b6a1-4364-9193-0c5e7802a8e8/pIDWybRn.png',
    'NOT': 'https://resources.premierleague.com/premierleague/photo/2018/01/31/e8d81ea9-cc54-4231-94b4-f25a83b64ac0/jFkUzjbn.png',
    'LEI': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_13-66.webp',
    'WHM': 'https://resources.premierleague.com/premierleague/photo/2018/01/31/cb5c2b2a-a716-40d6-a754-28c6bd6caea2/VaiXHZwX.png',
    'SOU': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_20-66.webp',
    'BUR': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_90-66.webp', 
    'LEE': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_2-66.webp', 
    'SUN': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_56-66.webp',

}

gk_shirt = {
    'LIV': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_14_1-66.webp',
    'ARS': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_3_1-66.webp',
    'NEW': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_4_1-66.webp',
    'MCI': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_43_1-66.webp',
    'TOT': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_6_1-66.webp',
    'MUN': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_1_1-66.webp',
    'EVE': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_11_1-66.webp',
    'CHE': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_8_1-66.webp',
    'CPL': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_31_1-66.webp',
    'BRI': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_36_1-66.webp',
    'IPS': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_40_1-66.webp',
    'BOU': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_91_1-66.webp',
    'BRE': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_94_1-66.webp',
    'WOL': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_39_1-66.webp',
    'AVL': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_7_1-66.webp',
    'FUL': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_54_1-66.webp',
    'NOT': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_17_1-66.webp',
    'LEI': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_13_1-66.webp',
    'WHM': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_21_1-66.webp',
    'SOU': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_20_1-66.webp',
    'BUR': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_90_1-66.webp',
    'LEE': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_2_1-66.webp', 
    'SUN': 'https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_56_1-66.webp',
}

# Modern Dark Theme CSS using the provided design system
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        /* Primitive Color Tokens */
        --color-white: rgba(255, 255, 255, 1);
        --color-black: rgba(0, 0, 0, 1);
        --color-cream-50: rgba(252, 252, 249, 1);
        --color-cream-100: rgba(255, 255, 253, 1);
        --color-gray-200: rgba(245, 245, 245, 1);
        --color-gray-300: rgba(167, 169, 169, 1);
        --color-gray-400: rgba(119, 124, 124, 1);
        --color-slate-500: rgba(98, 108, 113, 1);
        --color-brown-600: rgba(94, 82, 64, 1);
        --color-charcoal-700: rgba(31, 33, 33, 1);
        --color-charcoal-800: rgba(38, 40, 40, 1);
        --color-slate-900: rgba(19, 52, 59, 1);
        --color-teal-300: rgba(50, 184, 198, 1);
        --color-teal-400: rgba(45, 166, 178, 1);
        --color-teal-500: rgba(33, 128, 141, 1);
        --color-teal-600: rgba(29, 116, 128, 1);
        --color-teal-700: rgba(26, 104, 115, 1);
        --color-teal-800: rgba(41, 150, 161, 1);
        --color-red-400: rgba(255, 84, 89, 1);
        --color-red-500: rgba(192, 21, 47, 1);
        --color-orange-400: rgba(230, 129, 97, 1);
        --color-orange-500: rgba(168, 75, 47, 1);

        /* RGB versions for opacity control */
        --color-brown-600-rgb: 94, 82, 64;
        --color-teal-500-rgb: 33, 128, 141;
        --color-slate-900-rgb: 19, 52, 59;
        --color-slate-500-rgb: 98, 108, 113;
        --color-red-500-rgb: 192, 21, 47;
        --color-red-400-rgb: 255, 84, 89;
        --color-orange-500-rgb: 168, 75, 47;
        --color-orange-400-rgb: 230, 129, 97;
        --color-gray-400-rgb: 119, 124, 124;
        --color-teal-300-rgb: 50, 184, 198;
        --color-gray-300-rgb: 167, 169, 169;
        --color-gray-200-rgb: 245, 245, 245;

        /* Background color tokens (Light Mode) */
        --color-bg-1: rgba(59, 130, 246, 0.08);
        --color-bg-2: rgba(245, 158, 11, 0.08);
        --color-bg-3: rgba(34, 197, 94, 0.08);
        --color-bg-4: rgba(239, 68, 68, 0.08);
        --color-bg-5: rgba(147, 51, 234, 0.08);
        --color-bg-6: rgba(249, 115, 22, 0.08);
        --color-bg-7: rgba(236, 72, 153, 0.08);
        --color-bg-8: rgba(6, 182, 212, 0.08);

        /* Semantic Color Tokens (Light Mode) */
        --color-background: var(--color-cream-50);
        --color-surface: var(--color-cream-100);
        --color-text: var(--color-slate-900);
        --color-text-secondary: var(--color-slate-500);
        --color-primary: var(--color-teal-500);
        --color-primary-hover: var(--color-teal-600);
        --color-primary-active: var(--color-teal-700);
        --color-secondary: rgba(var(--color-brown-600-rgb), 0.12);
        --color-secondary-hover: rgba(var(--color-brown-600-rgb), 0.2);
        --color-secondary-active: rgba(var(--color-brown-600-rgb), 0.25);
        --color-border: rgba(var(--color-brown-600-rgb), 0.2);
        --color-btn-primary-text: var(--color-cream-50);
        --color-card-border: rgba(var(--color-brown-600-rgb), 0.12);
        --color-card-border-inner: rgba(var(--color-brown-600-rgb), 0.12);
        --color-error: var(--color-red-500);
        --color-success: var(--color-teal-500);
        --color-warning: var(--color-orange-500);
        --color-info: var(--color-slate-500);
        --color-focus-ring: rgba(var(--color-teal-500-rgb), 0.4);
        --color-select-caret: rgba(var(--color-slate-900-rgb), 0.8);

        /* Typography */
        --font-family-base: "FKGroteskNeue", "Geist", "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        --font-family-mono: "Berkeley Mono", ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        --font-size-xs: 11px;
        --font-size-sm: 12px;
        --font-size-base: 14px;
        --font-size-md: 14px;
        --font-size-lg: 16px;
        --font-size-xl: 18px;
        --font-size-2xl: 20px;
        --font-size-3xl: 24px;
        --font-size-4xl: 30px;

        /* Spacing */
        --space-4: 4px;
        --space-6: 6px;
        --space-8: 8px;
        --space-10: 10px;
        --space-12: 12px;
        --space-16: 16px;
        --space-20: 20px;
        --space-24: 24px;
        --space-32: 32px;

        /* Border Radius */
        --radius-sm: 6px;
        --radius-base: 8px;
        --radius-md: 10px;
        --radius-lg: 12px;
        --radius-full: 9999px;

        /* Shadows */
        --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.02);
        --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.02);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.04), 0 2px 4px -1px rgba(0, 0, 0, 0.02);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.04), 0 4px 6px -2px rgba(0, 0, 0, 0.02);

        /* Animation */
        --duration-fast: 150ms;
        --duration-normal: 250ms;
        --ease-standard: cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Dark mode colors - Auto detect system preference */
    @media (prefers-color-scheme: dark) {
        :root {
            /* Background color tokens (Dark Mode) */
            --color-bg-1: rgba(29, 78, 216, 0.15);
            --color-bg-2: rgba(180, 83, 9, 0.15);
            --color-bg-3: rgba(21, 128, 61, 0.15);
            --color-bg-4: rgba(185, 28, 28, 0.15);
            --color-bg-5: rgba(107, 33, 168, 0.15);
            --color-bg-6: rgba(194, 65, 12, 0.15);
            --color-bg-7: rgba(190, 24, 93, 0.15);
            --color-bg-8: rgba(8, 145, 178, 0.15);
            
            /* Semantic Color Tokens (Dark Mode) */
            --color-background: var(--color-charcoal-700);
            --color-surface: var(--color-charcoal-800);
            --color-text: var(--color-gray-200);
            --color-text-secondary: rgba(var(--color-gray-300-rgb), 0.7);
            --color-text-muted: rgba(var(--color-gray-400-rgb), 0.6);
            --color-primary: var(--color-teal-300);
            --color-primary-hover: var(--color-teal-400);
            --color-primary-active: var(--color-teal-800);
            --color-secondary: rgba(var(--color-gray-400-rgb), 0.15);
            --color-secondary-hover: rgba(var(--color-gray-400-rgb), 0.25);
            --color-secondary-active: rgba(var(--color-gray-400-rgb), 0.3);
            --color-border: rgba(var(--color-gray-400-rgb), 0.3);
            --color-error: var(--color-red-400);
            --color-success: var(--color-teal-300);
            --color-warning: var(--color-orange-400);
            --color-info: var(--color-gray-300);
            --color-focus-ring: rgba(var(--color-teal-300-rgb), 0.4);
            --color-btn-primary-text: var(--color-slate-900);
            --color-card-border: rgba(var(--color-gray-400-rgb), 0.2);
            --color-card-border-inner: rgba(var(--color-gray-400-rgb), 0.15);
            --color-select-caret: rgba(var(--color-gray-200-rgb), 0.8);

            /* Updated shadows for dark theme */
            --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.4), 0 1px 2px rgba(0, 0, 0, 0.3);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -1px rgba(0, 0, 0, 0.3);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -2px rgba(0, 0, 0, 0.4);
        }
    }

    /* Global Application Styles */
    .stApp {
        font-family: var(--font-family-base);
        background: var(--color-background);
        color: var(--color-text);
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container adjustments */
    .main .block-container {
        padding-top: var(--space-20);
        padding-bottom: var(--space-32);
        max-width: 95%;
        background: var(--color-background);
    }
    
    /* Header styling - Fixed for visibility */
    .main-header {
        color: var(--color-primary) !important;
        font-size: var(--font-size-4xl) !important;
        font-weight: 600 !important;
        text-align: center;
        margin-bottom: var(--space-32) !important;
        letter-spacing: -0.01em;
        line-height: 1.1;
        text-shadow: 0 0 20px rgba(50, 184, 198, 0.60), 0 0 40px rgba(50, 184, 198, 0.35);
    }
    
    /* Section headers */
    .section-header {
        color: var(--color-text) !important;
        font-size: var(--font-size-2xl) !important;
        font-weight: 550 !important;
        margin: var(--space-24) 0 var(--space-16) 0 !important;
        position: relative;
        padding-left: var(--space-16);
    }
    
    .section-header:before {
        content: '';
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 4px;
        height: 1.5rem;
        background: linear-gradient(135deg, var(--color-primary), var(--color-teal-400));
        border-radius: var(--radius-sm);
    }
    
    /* Tab navigation styling */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--color-surface);
        border-radius: var(--radius-lg);
        padding: var(--space-8);
        box-shadow: var(--shadow-md);
        border: 1px solid var(--color-card-border);
        gap: var(--space-8);
    }
    
    .stTabs [data-baseweb="tab-list"] button {
        background: transparent;
        border-radius: var(--radius-base);
        padding: var(--space-12) var(--space-24);
        border: none;
        font-weight: 500;
        font-size: var(--font-size-base);
        transition: all var(--duration-normal) var(--ease-standard);
        color: var(--color-text-secondary) !important;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background: var(--color-primary);
        color: var(--color-charcoal-700) !important;
        box-shadow: var(--shadow-sm);
        transform: translateY(-1px);
    }
    
    .stTabs [data-baseweb="tab-list"] button:hover:not([aria-selected="true"]) {
        background: var(--color-secondary);
        color: var(--color-text) !important;
        transform: translateY(-1px);
    }
    
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        color: inherit !important;
        margin: 0 !important;
    }
    
    /* Stats container */
    .stats-container {
        background: var(--color-surface);
        border-radius: var(--radius-lg);
        padding: var(--space-24);
        box-shadow: var(--shadow-md);
        border: 1px solid var(--color-card-border);
        margin: var(--space-16) 0;
        position: relative;
    }
    
    .stats-container:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--color-primary), var(--color-teal-400));
        border-radius: var(--radius-lg) var(--radius-lg) 0 0;
    }
    
    /* Stat items */
    .stat-item {
        background: rgba(var(--color-gray-400-rgb), 0.1);
        padding: var(--space-20) var(--space-16);
        border-radius: var(--radius-lg);
        text-align: center;
        transition: all var(--duration-normal) var(--ease-standard);
        border: 1px solid var(--color-card-border);
        position: relative;
        overflow: hidden;
    }
    
    .stat-item:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
        border-color: var(--color-primary);
        background: rgba(var(--color-teal-300-rgb), 0.1);
    }
    
    .stat-value {
        font-size: var(--font-size-2xl);
        font-weight: 600;
        color: var(--color-primary);
        display: block;
        margin-bottom: var(--space-8);
    }
    
    .stat-label {
        font-size: var(--font-size-sm);
        color: var(--color-text-secondary);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Form controls */
    .stSelectbox > div > div > div {
        background: var(--color-surface) !important;
        border: 2px solid var(--color-border) !important;
        border-radius: var(--radius-lg) !important;
        color: var(--color-text) !important;
        transition: all var(--duration-normal) var(--ease-standard);
        box-shadow: var(--shadow-sm);
    }
    
    .stSelectbox > div > div > div:hover {
        border-color: var(--color-primary) !important;
        box-shadow: 0 0 0 3px var(--color-focus-ring);
    }
    
    .stTextInput > div > div > input {
        background: var(--color-surface) !important;
        border: 2px solid var(--color-border) !important;
        border-radius: var(--radius-lg) !important;
        color: var(--color-text) !important;
        transition: all var(--duration-normal) var(--ease-standard);
        box-shadow: var(--shadow-sm);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--color-primary) !important;
        box-shadow: 0 0 0 3px var(--color-focus-ring) !important;
        outline: none !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: var(--color-text-muted) !important;
    }
    
    /* DataFrames */
    .modern-table {
        background: var(--color-surface);
        border-radius: var(--radius-lg);
        overflow: hidden;
        box-shadow: var(--shadow-lg);
        border: 1px solid var(--color-card-border);
        margin: var(--space-16) 0;
    }
    
    .stDataFrame {
        background: var(--color-surface);
        border-radius: var(--radius-lg);
        overflow: hidden;
        box-shadow: var(--shadow-lg);
        border: 1px solid var(--color-card-border);
    }
    
    .stDataFrame > div {
        border-radius: var(--radius-lg);
        background: var(--color-surface) !important;
    }
    
    .stDataFrame table {
        background: var(--color-surface) !important;
        color: var(--color-text) !important;
    }
    
    .stDataFrame th {
        background: rgba(var(--color-gray-400-rgb), 0.15) !important;
        color: var(--color-text) !important;
        border-color: var(--color-border) !important;
        font-weight: 550;
    }
    
    .stDataFrame td {
        background: var(--color-surface) !important;
        color: var(--color-text) !important;
        border-color: var(--color-border) !important;
    }
    
    /* Plotly charts */
    .js-plotly-plot {
        background: var(--color-surface) !important;
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-md);
        border: 1px solid var(--color-card-border);
        overflow: hidden;
    }
    
    /* Alert styling */
    .stAlert {
        background: var(--color-surface) !important;
        color: var(--color-text) !important;
        border-radius: var(--radius-lg);
        border-left: 4px solid var(--color-warning);
        box-shadow: var(--shadow-sm);
        border-color: var(--color-card-border) !important;
    }
    
    .stAlert > div {
        color: var(--color-text) !important;
    }
    
    /* Performance indicators */
    .performance-high { 
        color: var(--color-success) !important; 
        font-weight: 550; 
    }
    .performance-medium { 
        color: var(--color-warning) !important; 
        font-weight: 550; 
    }
    .performance-low { 
        color: var(--color-error) !important; 
        font-weight: 550; 
    }
    
    /* Markdown content */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: var(--color-text) !important;
        font-weight: 550 !important;
    }
    
    .stMarkdown p {
        color: var(--color-text) !important;
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-color: var(--color-primary) transparent transparent transparent !important;
    }
    
    /* Footer */
    .footer-text {
        color: var(--color-text-muted) !important;
        text-align: center;
        padding: var(--space-24) 0 var(--space-16) 0;
        border-top: 1px solid var(--color-border);
        margin-top: var(--space-32);
        font-size: var(--font-size-sm);
    }
    
    /* Team Optimizer specific styles */
    .pitch {
        background: url(https://fantasy.premierleague.com/static/media/pitch-default.dab51b01.svg);
        background-position: center top;
        background-size: 100%;
        background-repeat: no-repeat;
        padding: var(--space-32) var(--space-16);
        border-radius: var(--radius-lg);
        background-color: var(--color-surface);
        border: 1px solid var(--color-card-border);
        box-shadow: var(--shadow-md);
        margin: var(--space-16) 0;
    }
    
    .row {
        text-align: center;
        margin: var(--space-16) 0;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;
        gap: var(--space-8);
    }
    
    .subrow {
        text-align: center;
        background-color: rgba(var(--color-gray-400-rgb), 0.1);
        padding: var(--space-16);
        border-radius: var(--radius-base);
        margin: var(--space-16) 0;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;
        gap: var(--space-8);
    }
    
    .playercard {
        font-family: var(--font-family-base);
        text-align: center;
        margin: var(--space-4);
        display: inline-block;
        font-size: var(--font-size-sm);
        font-weight: 500;
        background: var(--color-surface);
        border-radius: var(--radius-base);
        padding: var(--space-8);
        border: 1px solid var(--color-card-border);
        transition: all var(--duration-fast) var(--ease-standard);
        min-width: 80px;
    }
    
    .playercard:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
        border-color: var(--color-primary);
    }
    
    .playercard > img {
        width: 60px;
        height: auto;
        border-radius: var(--radius-sm);
    }
    
    .pname {
        background: var(--color-primary);
        text-align: center;
        color: var(--color-charcoal-700);
        font-weight: 600;
        padding: var(--space-6) var(--space-8);
        border-radius: var(--radius-sm);
        margin: var(--space-4) 0;
        font-size: var(--font-size-xs);
    }
    
    .pteam {
        background: var(--color-success);
        text-align: center;
        color: var(--color-charcoal-700);
        font-weight: 500;
        padding: var(--space-4) var(--space-8);
        border-radius: var(--radius-sm);
        font-size: var(--font-size-xs);
    }
    
    /* Multiselect styling */
    .stMultiSelect > div > div > div {
        background: var(--color-surface) !important;
        border: 2px solid var(--color-border) !important;
        border-radius: var(--radius-lg) !important;
        color: var(--color-text) !important;
    }
    
    .stMultiSelect [data-baseweb="tag"] {
        background: var(--color-primary) !important;
        color: var(--color-charcoal-700) !important;
        border-radius: var(--radius-sm) !important;
        font-weight: 500 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: var(--color-primary) !important;
        color: var(--color-charcoal-700) !important;
        border: none !important;
        border-radius: var(--radius-base) !important;
        padding: var(--space-12) var(--space-24) !important;
        font-weight: 500 !important;
        transition: all var(--duration-normal) var(--ease-standard) !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    .stButton > button:hover {
        background: var(--color-primary-hover) !important;
        transform: translateY(-1px) !important;
        box-shadow: var(--shadow-md) !important;
    }
    
    /* Checkbox styling */
    .stCheckbox > label {
        color: var(--color-text) !important;
        font-weight: 500 !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: var(--color-surface) !important;
        color: var(--color-text) !important;
        border: 1px solid var(--color-card-border) !important;
        border-radius: var(--radius-base) !important;
        font-weight: 500 !important;
    }
    
    .streamlit-expanderContent {
        background: var(--color-surface) !important;
        border: 1px solid var(--color-card-border) !important;
        border-radius: 0 0 var(--radius-base) var(--radius-base) !important;
        border-top: none !important;
    }
    
    /* Team total score styling */
    .total-score {
        background: var(--color-primary);
        color: var(--color-charcoal-700);
        padding: var(--space-16);
        border-radius: var(--radius-lg);
        text-align: center;
        font-size: var(--font-size-xl);
        font-weight: 600;
        margin: var(--space-16) 0;
        box-shadow: var(--shadow-md);
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-header {
            font-size: var(--font-size-3xl) !important;
            margin-bottom: var(--space-24) !important;
        }
        
        .section-header {
            font-size: var(--font-size-xl) !important;
            padding-left: var(--space-12);
        }
        
        .stat-item {
            padding: var(--space-16) var(--space-12);
        }
        
        .stat-value {
            font-size: var(--font-size-xl);
        }
        
        .main .block-container {
            padding-top: var(--space-16);
        }
        
        .playercard {
            min-width: 70px;
            margin: var(--space-2);
        }
        
        .playercard > img {
            width: 50px;
        }
        
        .row, .subrow {
            gap: var(--space-4);
        }
    }
</style>
""", unsafe_allow_html=True)

# Data loading function
@st.cache_data
def load_data():
    """Load all FPL data from CSV files"""
    data_folder = "data"

    # Player data files
    positions = ["attackers", "defenders", "midfielders", "goalkeepers"]
    views = ["all", "home", "away", "last5", "home_last5", "away_last5"]

    player_data = {}
    for position in positions:
        player_data[position] = {}
        for view in views:
            filename = f"{position}_{view}.csv"
            filepath = os.path.join(data_folder, filename)
            if os.path.exists(filepath):
                player_data[position][view] = pd.read_csv(filepath)
            else:
                # Create empty dataframe with expected columns if file doesn't exist
                player_data[position][view] = pd.DataFrame()

    # Team data files
    team_views = ["all_matches", "all_home_matches", "all_away_matches", 
                  "last5_matches", "last5_home_matches", "last5_away_matches"]

    team_data = {}
    for view in team_views:
        filename = f"team_{view}.csv"
        filepath = os.path.join(data_folder, filename)
        if os.path.exists(filepath):
            team_data[view] = pd.read_csv(filepath)
        else:
            team_data[view] = pd.DataFrame()

    return player_data, team_data

# Team optimizer functions
def assert_team(df):
    asserts = {
        'bench_ok': len(df[df.status=='bench'])==4,
        'start_ok' : len(df[df.status=='starting'])==11,
        'teams_ok' : (df.groupby(["Team"]).count().max()[0]<=3),
        'goalies_ok' : len(df[df.Position=='GK'])==2,
        'defs_ok' : len(df[df.Position=="D"])==5,
        'mids_ok' : len(df[df.Position=="M"])==5,
        'fwds_ok' : len(df[df.Position=="F"])==3
    }
    return asserts

def generate_pitch(df, GW):
    pitch = '<div class="pitch">'
    
    # Goalkeeper row
    row = '<div class="row">'
    for k, each in df[df.status=="starting"][df.Position=='GK'].iterrows():
        row += ' '.join([
            '<div class="playercard">',
            '<img src="' + gk_shirt.get(each['Team'], '') + '">',
            '<div class="pname">' + str(each['Player']) + '</div>',
            '<div class="pteam">' + str(each['Team']) + ', ' + str(each[GW]) + '</div>',
            '</div>'
        ])
    row += '</div>'
    pitch += row
    
    # Defenders row
    row = '<div class="row">'
    for k, each in df[df.status=="starting"][df.Position=='D'].iterrows():
        row += ' '.join([
            '<div class="playercard">',
            '<img src="' + shirt.get(each['Team'], '') + '">',
            '<div class="pname">' + str(each['Player']) + '</div>',
            '<div class="pteam">' + str(each['Team']) + ', ' + str(each[GW]) + '</div>',
            '</div>'
        ])
    row += '</div>'
    pitch += row
    
    # Midfielders row
    row = '<div class="row">'
    for k, each in df[df.status=="starting"][df.Position=='M'].iterrows():
        row += ' '.join([
            '<div class="playercard">',
            '<img src="' + shirt.get(each['Team'], '') + '">',
            '<div class="pname">' + str(each['Player']) + '</div>',
            '<div class="pteam">' + str(each['Team']) + ', ' + str(each[GW]) + '</div>',
            '</div>'
        ])
    row += '</div>'
    pitch += row
    
    # Forwards row
    row = '<div class="row">'
    for k, each in df[df.status=="starting"][df.Position=='F'].iterrows():
        row += ' '.join([
            '<div class="playercard">',
            '<img src="' + shirt.get(each['Team'], '') + '">',
            '<div class="pname">' + str(each['Player']) + '</div>',
            '<div class="pteam">' + str(each['Team']) + ', ' + str(each[GW]) + '</div>',
            '</div>'
        ])
    row += '</div>'
    pitch += row
    
    # Bench row
    row = '<div class="subrow">'
    for k, each in df[df.status=="bench"][df.Position=='GK'].sort_values(GW).iterrows():
        row += ' '.join([
            '<div class="playercard">',
            '<img src="' + gk_shirt.get(each['Team'], '') + '">',
            '<div class="pname">' + str(each['Player']) + '</div>',
            '<div class="pteam">' + str(each['Team']) + ', ' + str(each[GW]) + '</div>',
            '</div>'
        ])
    for k, each in df[df.status=="bench"][df.Position!='GK'].sort_values(GW, ascending=[False]).iterrows():
        row += ' '.join([
            '<div class="playercard">',
            '<img src="' + shirt.get(each['Team'], '') + '">',
            '<div class="pname">' + str(each['Player']) + '</div>',
            '<div class="pteam">' + str(each['Team']) + ', ' + str(each[GW]) + '</div>',
            '</div>'
        ])
    row += '</div>'
    pitch += row
    pitch += '</div>'
    return pitch

# Custom function to create performance indicator
def get_performance_class(value, high_threshold, medium_threshold):
    """Return CSS class based on performance value"""
    if value >= high_threshold:
        return "performance-high"
    elif value >= medium_threshold:
        return "performance-medium"
    else:
        return "performance-low"

# Load data
try:
    player_data, team_data = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"Error loading data: {e}")
    data_loaded = False

# Main header
st.markdown('<h1 class="main-header">FPL Statistics Dashboard</h1>', unsafe_allow_html=True)

if not data_loaded:
    st.error("Unable to load FPL data. Please ensure the data files are in the 'data' directory.")
    st.stop()

# Create main tabs
tab1, tab2, tab3, tab4 = st.tabs(["Players", "Teams", "Team Optimizer", 'Player Comparision'])

# Tab 1: Players
with tab1:
    st.markdown('<h2 class="section-header">Player Statistics</h2>', unsafe_allow_html=True)

    # Position tabs
    pos_tab1, pos_tab2, pos_tab3, pos_tab4 = st.tabs(["Goalkeepers", "Defenders", "Midfielders", "Attackers"])

    # Function to render player tab content
    def render_player_tab(position_name, selected_position, tab_key):
        # View selection for players
        view_options = ["all", "home", "away", "last5", "home_last5", "away_last5"]
        view_labels = ["All Matches", "Home Matches", "Away Matches", "Last 5 Matches", "Home Last 5", "Away Last 5"]

        col1, col2 = st.columns([2, 1])
        
        with col1:
            selected_view = st.selectbox(
                "Select Data View",
                view_options,
                format_func=lambda x: dict(zip(view_options, view_labels))[x],
                index=0,
                key=f"{tab_key}_view"
            )
        
        with col2:
            search_term = st.text_input("Search players by name:", "", key=f"{tab_key}_search", placeholder="Enter player name...")

        # Get current data
        current_data = player_data.get(selected_position, {}).get(selected_view, pd.DataFrame())
        current_data = reorder_columns(current_data, player_orders[selected_position])

        if not current_data.empty:
            # Filter data based on search
            if search_term:
                mask = (current_data['first_name'].str.contains(search_term, case=False, na=False) | 
                       current_data['second_name'].str.contains(search_term, case=False, na=False))
                filtered_data = current_data[mask]
            else:
                filtered_data = current_data

            # Display data table
            st.markdown("### Player Data")
            st.markdown('<div class="modern-table">', unsafe_allow_html=True)
            st.dataframe(
                filtered_data,
                use_container_width=True,
                hide_index=True,
                height=400
            )
            st.markdown('</div>', unsafe_allow_html=True)

            # Top performers visualization
            if len(current_data) > 0 and 'total_points' in current_data.columns:
                st.markdown("### Top 10 Performers")
                top_10 = current_data.nlargest(10, 'total_points')

                # Create chart with dark theme colors from design system
                fig = px.bar(
                    top_10,
                    x='total_points',
                    y=top_10['first_name'] + ' ' + top_10['second_name'],
                    orientation='h',
                    title=f"Top 10 {position_name} by Total Points",
                    color='total_points',
                    color_continuous_scale=[
                        [0, 'rgb(255, 84, 89)'],    # red-400
                        [0.5, 'rgb(230, 129, 97)'], # orange-400  
                        [1, 'rgb(50, 184, 198)']    # teal-300
                    ]
                )
                
                fig.update_layout(
                    height=450,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(38, 40, 40, 1)',  # charcoal-800
                    font=dict(family="Inter, sans-serif", size=12, color='rgb(245, 245, 245)'), # gray-200
                    title=dict(font=dict(size=16, color='rgb(245, 245, 245)')),
                    margin=dict(l=20, r=20, t=60, b=20),
                    xaxis=dict(gridcolor='rgba(119, 124, 124, 0.3)', color='rgb(245, 245, 245)'),
                    yaxis=dict(
                        categoryorder='total ascending',
                        gridcolor='rgba(119, 124, 124, 0.3)',
                        color='rgb(245, 245, 245)'
                    ),
                    coloraxis_colorbar=dict(
                        title=dict(text="Points", font=dict(color='rgb(245, 245, 245)')),
                        tickfont=dict(color='rgb(245, 245, 245)')
                    )
                )
                
                fig.update_traces(
                    marker_line_color='rgba(0,0,0,0.1)',
                    marker_line_width=1
                )
                
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.warning(f"No data available for {position_name} - {dict(zip(view_options, view_labels))[selected_view]}")

    # Render each position tab
    with pos_tab1:
        render_player_tab("Goalkeepers", "goalkeepers", "gk")

    with pos_tab2:
        render_player_tab("Defenders", "defenders", "def")

    with pos_tab3:
        render_player_tab("Midfielders", "midfielders", "mid")

    with pos_tab4:
        render_player_tab("Attackers", "attackers", "att")

# Tab 2: Teams
with tab2:
    st.markdown('<h2 class="section-header">Team Statistics</h2>', unsafe_allow_html=True)

    # Team view selection
    team_view_options = ["all_matches", "all_home_matches", "all_away_matches", 
                        "last5_matches", "last5_home_matches", "last5_away_matches"]
    team_view_labels = ["All Matches", "Home Matches", "Away Matches", 
                       "Last 5 Matches", "Home Last 5", "Away Last 5"]

    selected_team_view = st.selectbox(
        "Select Team Data View",
        team_view_options,
        format_func=lambda x: dict(zip(team_view_options, team_view_labels))[x],
        index=0
    )

    # Get current team data
    current_team_data = team_data.get(selected_team_view, pd.DataFrame())
    current_team_data = reorder_columns(current_team_data, team_order)

    if not current_team_data.empty:
        # Team data table
        st.markdown("### Team Performance Data")
        st.markdown('<div class="modern-table">', unsafe_allow_html=True)
        st.dataframe(
            current_team_data,
            use_container_width=True,
            hide_index=True,
            height=500
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Charts section
        chart_col1, chart_col2 = st.columns(2)

        # Design system colors for charts
        chart_colors = [
            'rgb(255, 84, 89)',   # red-400
            'rgb(230, 129, 97)',  # orange-400  
            'rgb(50, 184, 198)'   # teal-300
        ]

        # Chart background and text colors
        chart_bg = 'rgba(38, 40, 40, 1)'  # charcoal-800
        chart_text = 'rgb(245, 245, 245)' # gray-200
        chart_grid = 'rgba(119, 124, 124, 0.3)' # gray-400 with opacity

        # Non-Penalty xG vs Non-Penalty xGA Scatter Plot
        if 'npxG' in current_team_data.columns and 'npxGA' in current_team_data.columns:
            with chart_col1:
                st.markdown("### Attack vs Defense Analysis")

                fig = px.scatter(
                    current_team_data,
                    x='npxG',
                    y='npxGA',
                    text='team',
                    title='Non-Penalty xG vs xGA',
                    labels={
                        'npxG': 'Non-Penalty xG',
                        'npxGA': 'Non-Penalty xGA'
                    },
                    color='pts' if 'pts' in current_team_data.columns else None,
                    size='scored' if 'scored' in current_team_data.columns else None,
                    color_continuous_scale=chart_colors,
                    hover_data=['team', 'pts', 'scored', 'conceded'] if all(col in current_team_data.columns for col in ['pts', 'scored', 'conceded']) else ['team']
                )

                # Add diagonal line
                min_val = min(current_team_data['npxG'].min(), current_team_data['npxGA'].min())
                max_val = max(current_team_data['npxG'].max(), current_team_data['npxGA'].max())

                fig.add_trace(
                    go.Scatter(
                        x=[min_val, max_val],
                        y=[min_val, max_val],
                        mode='lines',
                        line=dict(dash='dash', color='rgb(255, 84, 89)', width=2),
                        name='Balance Line',
                        showlegend=True
                    )
                )

                fig.update_traces(textposition='top center', textfont_size=10, textfont_color=chart_text)
                fig.update_layout(
                    height=450,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor=chart_bg,
                    font=dict(family="Inter, sans-serif", size=11, color=chart_text),
                    title=dict(font=dict(size=14, color=chart_text)),
                    margin=dict(l=20, r=20, t=60, b=20),
                    xaxis=dict(gridcolor=chart_grid, color=chart_text),
                    yaxis=dict(gridcolor=chart_grid, color=chart_text),
                    legend=dict(font=dict(color=chart_text)),
                    coloraxis_colorbar=dict(
                        title=dict(text="Points", font=dict(color=chart_text)),
                        tickfont=dict(color=chart_text)
                    )
                )

                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        # Expected vs Actual Goals
        if 'xG' in current_team_data.columns and 'scored' in current_team_data.columns:
            with chart_col2:
                st.markdown("### Expected vs Actual Goals")

                fig_goals = px.scatter(
                    current_team_data,
                    x='xG',
                    y='scored',
                    text='team',
                    title='xG vs Goals Scored',
                    labels={'xG': 'Expected Goals', 'scored': 'Actual Goals'},
                    color='pts' if 'pts' in current_team_data.columns else None,
                    color_continuous_scale=chart_colors
                )

                # Add diagonal line for perfect prediction
                min_g = min(current_team_data['xG'].min(), current_team_data['scored'].min())
                max_g = max(current_team_data['xG'].max(), current_team_data['scored'].max())

                fig_goals.add_trace(
                    go.Scatter(
                        x=[min_g, max_g],
                        y=[min_g, max_g],
                        mode='lines',
                        line=dict(dash='dash', color='rgba(167, 169, 169, 0.8)', width=2),
                        name='Perfect Prediction',
                        showlegend=True
                    )
                )

                fig_goals.update_traces(textposition='top center', textfont_size=10, textfont_color=chart_text)
                fig_goals.update_layout(
                    height=450,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor=chart_bg,
                    font=dict(family="Inter, sans-serif", size=11, color=chart_text),
                    title=dict(font=dict(size=14, color=chart_text)),
                    margin=dict(l=20, r=20, t=60, b=20),
                    xaxis=dict(gridcolor=chart_grid, color=chart_text),
                    yaxis=dict(gridcolor=chart_grid, color=chart_text),
                    legend=dict(font=dict(color=chart_text)),
                    coloraxis_colorbar=dict(
                        title=dict(text="Points", font=dict(color=chart_text)),
                        tickfont=dict(color=chart_text)
                    )
                )

                st.plotly_chart(fig_goals, use_container_width=True, config={'displayModeBar': False})

        # Goal difference analysis
        if 'scored' in current_team_data.columns and 'conceded' in current_team_data.columns:
            st.markdown("### Goal Difference Analysis")
            
            current_team_data_copy = current_team_data.copy()
            current_team_data_copy['goal_difference'] = current_team_data_copy['scored'] - current_team_data_copy['conceded']

            fig_diff = px.bar(
                current_team_data_copy.sort_values('goal_difference', ascending=True),
                x='goal_difference',
                y='team',
                orientation='h',
                title='Goal Difference by Team',
                color='goal_difference',
                color_continuous_scale=chart_colors
            )
            
            fig_diff.update_layout(
                height=500,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor=chart_bg,
                font=dict(family="Inter, sans-serif", size=12, color=chart_text),
                title=dict(font=dict(size=16, color=chart_text)),
                margin=dict(l=20, r=20, t=60, b=20),
                xaxis=dict(gridcolor=chart_grid, color=chart_text),
                yaxis=dict(gridcolor=chart_grid, color=chart_text),
                coloraxis_colorbar=dict(
                    title=dict(text="Goal Difference", font=dict(color=chart_text)),
                    tickfont=dict(color=chart_text)
                )
            )
            
            fig_diff.update_traces(
                marker_line_color='rgba(0,0,0,0.1)',
                marker_line_width=1
            )
            
            st.plotly_chart(fig_diff, use_container_width=True, config={'displayModeBar': False})

    else:
        st.warning(f"No team data available for {dict(zip(team_view_options, team_view_labels))[selected_team_view]}")

# Tab 3: Team Optimizer
with tab3:
    st.markdown('<h2 class="section-header">Team Optimizer</h2>', unsafe_allow_html=True)
    
    # Check if transfer algorithm file exists
    transfer_file = "data/TransferAlgorithm.csv"
    if not os.path.exists(transfer_file):
        st.error(f"Transfer algorithm data file '{transfer_file}' not found. Please ensure the file is in the root directory.")
        st.info("This tab requires the TransferAlgorithm.csv file to function properly.")
    else:
        # Load transfer algorithm data
        try:
            df = pd.read_csv(transfer_file, encoding='ISO-8859-1', sep=',').drop("No.", axis=1, errors='ignore')
            # Clean ALL columns that might contain numeric data
            for col in df.columns:
                # Skip obviously text columns
                if col in ['Player', 'Team', 'Position']:
                    continue
                    
                # For all other columns, clean problematic values
                df[col] = df[col].astype(str).replace(['-', 'Sum', 'N/A', 'nan', '', 'NULL'], '0')
                
                # Try to convert to numeric
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)   

            # Filters section
            st.markdown("### Data Filters")
            
            modify = st.checkbox("Add position filter")
            
            if modify:
                position = st.selectbox('Position', ['F', 'M', 'D', 'GK'], key='Position')
                df_table = df[df["Position"] == position]
                st.markdown("#### Filtered Players")
                st.dataframe(df_table, use_container_width=True, hide_index=True)
            else:
                st.markdown("#### All Players")
                st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Team selection section
            z = st.expander("🔧 **Team Builder & Optimizer**", expanded=True)
            z.markdown("**Select a complete team to optimize your transfers and visualize your squad on the pitch.**")
            z.markdown("")
            
            # Team selection layout
            col1, col2 = z.columns(2)
            
            with col1:
                st.markdown("**Goalkeepers**")
                _, g1, g2, _ = st.columns([1, 2, 2, 1])
                stg = g1.multiselect("Starting GK", list(df[df.Position=='GK'].Player), max_selections=1, key="start_gk")
                sug = g2.multiselect("Bench GK", [each for each in df[df.Position=='GK'].Player if each not in stg], max_selections=1, key="bench_gk")
                
                st.markdown("**Defenders**")
                _, d1, d2, _ = st.columns([1, 2, 2, 1])
                std = d1.multiselect("Starting DEF (5)", list(df[df.Position=='D'].Player), max_selections=5, key="start_def")
                sud = d2.multiselect("Bench DEF", [each for each in df[df.Position=='D'].Player if each not in std], max_selections=2, key="bench_def")
            
            with col2:
                st.markdown("**Midfielders**")
                _, m1, m2, _ = st.columns([1, 2, 2, 1])
                stm = m1.multiselect("Starting MID (5)", list(df[df.Position=='M'].Player), max_selections=5, key="start_mid")
                sum = m2.multiselect("Bench MID", [each for each in df[df.Position=="M"].Player if each not in stm], max_selections=3, key="bench_mid")
                
                st.markdown("**Forwards**")
                _, f1, f2, _ = st.columns([1, 2, 2, 1])
                stf = f1.multiselect("Starting FWD (3)", list(df[df.Position=='F'].Player), max_selections=3, key="start_fwd")
                suf = f2.multiselect("Bench FWD", [each for each in df[df.Position=='F'].Player if each not in stf], max_selections=2, key="bench_fwd")
            
            # Team settings
            _, cp, gw, _ = z.columns([2, 2, 2, 2])
            captain = cp.selectbox("Captain", stg + std + stm + stf, key="captain_select")
            available_gameweeks = []
            for col in df.columns:
                try:
                    gw_num = int(col)
                    if 1 <= gw_num < 39:  # Valid gameweek range
                        available_gameweeks.append(gw_num)
                except (ValueError, TypeError):
                    continue

            if available_gameweeks:
                GW = str(gw.selectbox("Gameweek", sorted(available_gameweeks), key="gameweek_select"))
            else:
                st.error("No valid gameweek columns found in the data")
                GW = None
            
            # Process team selection
            _names = stg + sug + std + sud + stm + sum + stf + suf
            _positions = (['GK'] * len(stg + sug)) + \
                        (['D'] * len(std + sud)) + \
                        (['M'] * len(stm + sum)) + \
                        (['F'] * len(stf + suf))
            _statuses = (["starting"] * len(stg)) + (["bench"] * len(sug)) + \
                        (["starting"] * len(std)) + (["bench"] * len(sud)) + \
                        (["starting"] * len(stm)) + (["bench"] * len(sum)) + \
                        (["starting"] * len(stf)) + (["bench"] * len(suf))
            
            team_df = pd.DataFrame({"name": _names, "position": _positions, "status": _statuses})
            select_df = pd.merge(df, team_df, how='left',
                                left_on=["Position", "Player"],
                                right_on=["position", "name"])
            
            # Team validation
            assert_picks = assert_team(select_df[select_df.status.isin(['starting', 'bench'])])
            select_df = select_df[select_df.status.isin(['starting', 'bench'])].drop(columns=['name', 'position'], axis=1)
            
            if all(assert_picks.values()):
                select_df = select_df.replace(' ', '', regex=True)
                select_df = select_df.replace('-', '0', regex=True)
                select_df[GW] = select_df[GW].astype(float)
                
                # Optimize button
                if z.button("🚀 **Optimize Team**", help="Automatically select the best starting XI based on projected points"):
                    starting_players = (select_df[select_df["Position"]=='GK'].nlargest(1, GW)["Player"].to_list() + 
                                        select_df[select_df["Position"]=='D'].nlargest(3, GW)["Player"].to_list() + 
                                        select_df[select_df["Position"]=='M'].nlargest(2, GW)["Player"].to_list() + 
                                        select_df[select_df["Position"]=='F'].nlargest(1, GW)["Player"].to_list())
                    starting_players = starting_players + select_df[(~select_df["Player"].isin(starting_players)) & 
                                                                    (select_df["Position"] != "GK")].nlargest(4, GW)["Player"].to_list()
                    captain = select_df.nlargest(1, GW)["Player"].tolist()[0]
                    select_df["status"] = np.where(select_df["Player"].isin(starting_players), "starting", "bench")
                
                # Display team
                team_tab, data_tab = z.tabs(["🏆 Team Visualization", "📊 Team Data"])
                
                # Apply captain multiplier
                select_df_display = select_df.copy()
                select_df_display.loc[select_df_display['Player'] == captain, GW] *= 2
                
                with team_tab:
                    # Total score display
                    total_score = select_df_display.loc[select_df_display['status'] == 'starting', GW].sum()
                    st.markdown(f'<div class="total-score">Total Team Score: {total_score:.1f} points</div>', 
                                unsafe_allow_html=True)
                    
                    # Generate and display pitch
                    pitch = generate_pitch(select_df_display, GW)
                    st.markdown(pitch, unsafe_allow_html=True)
                
                with data_tab:
                    # Display team data
                    display_columns = ['Player', 'Team', 'Position', 'status', ' BCV ', ' PPG - longer term ', GW]
                    available_columns = [col for col in display_columns if col in select_df.columns]
                    st.dataframe(select_df[available_columns], use_container_width=True, hide_index=True)
                
            else:
                z.error("⚠️ **Team selection incomplete!**\nPlease ensure your team follows FPL rules:\n- 2 Goalkeepers (1 starting, 1 bench)\n- 5 Defenders\n- 5 Midfielders\n- 3 Forwards\n- Max 3 players from any team")
            
            # Source attribution
            st.markdown("**Source:** [Transfer Algorithm](https://www.patreon.com/TransferAlgorithm)")
            
        except Exception as e:
            st.error(f"Error loading transfer algorithm data: {e}")
            st.info("Please check that the TransferAlgorithm.csv file is properly formatted.")

# Tab 4: Player Comparison
# Tab 4: Player Comparison
with tab4:
    st.markdown('<h2 class="section-header comparison-title">Player Comparison</h2>', unsafe_allow_html=True)
    
    # Position tabs for comparison
    comp_tab1, comp_tab2, comp_tab3, comp_tab4 = st.tabs(["Goalkeepers", "Defenders", "Midfielders", "Attackers"])
    
    # Function to render comparison tab content
    def render_comparison_tab(position_name, selected_position, tab_key):
        # View selection and data controls
        view_options = ["all", "home", "away", "last5", "home_last5", "away_last5"]
        view_labels = ["All Matches", "Home Matches", "Away Matches", "Last 5 Matches", "Home Last 5", "Away Last 5"]
        
        selected_view = st.selectbox(
                "Select Data View",
                view_options,
                format_func=lambda x: dict(zip(view_options, view_labels))[x],
                index=0,
                key=f"{tab_key}_comp_view"
            )

        # Get current data
        current_data = player_data.get(selected_position, {}).get(selected_view, pd.DataFrame())
        
        if not current_data.empty:
            current_data = reorder_columns(current_data, player_orders[selected_position])
            
            # Create player selection list (combining first and last names)
            if not current_data.empty:
                player_names = (current_data['first_name'].fillna('') + ' ' + 
                              current_data['second_name'].fillna('')).str.strip().tolist()
                
                # Player multiselect
                st.markdown('<div class="player-multiselect">', unsafe_allow_html=True)
                selected_players = st.multiselect(
                    f'Select {position_name.lower()} to compare',
                    player_names,
                    help=f"Choose multiple {position_name.lower()} to compare their statistics",
                    key=f"{tab_key}_comp_multiselect"
                )
                st.markdown('</div>', unsafe_allow_html=True)
                
                if selected_players:
                    st.markdown('<div class="compare-button">', unsafe_allow_html=True)
                    if st.button(f"Compare {position_name}", key=f"compare_{tab_key}"):
                        with st.spinner(f"Analyzing {position_name.lower()} data..."):
                            # Filter data for selected players
                            selected_mask = (current_data['first_name'].fillna('') + ' ' + 
                                           current_data['second_name'].fillna('')).str.strip().isin(selected_players)
                            comparison_data = current_data[selected_mask].copy()
                            
                            if not comparison_data.empty:
                                st.markdown('<div class="comparison-results">', unsafe_allow_html=True)
                                st.markdown(f"### {position_name} Comparison Results")
                                
                                # Prepare data for comparison
                                # Create player identifier
                                comparison_data['player_name'] = (comparison_data['first_name'].fillna('') + ' ' + 
                                                                comparison_data['second_name'].fillna('')).str.strip()
                                
                                # Position-specific key metrics from your player_orders
                                if selected_position == 'goalkeepers':
                                    key_metrics = [
                                        'player_name', 'minutes', 'xGC', 'total_points', 'xPoints', 
                                        'clean_sheets', 'goals_conceded', 'saves', 'bonus', 'form', 
                                        'penalties_saved', 'yellow_cards', 'red_cards'
                                    ]
                                elif selected_position == 'defenders':
                                    key_metrics = [
                                        'player_name', 'minutes', 'xGC', 'total_points', 'xPoints', 
                                        'goals_scored', 'assists', 'clean_sheets', 'goals_conceded', 
                                        'xG', 'xA', 'defensive_points', 'clearances_blocks_interceptions',
                                        'recoveries', 'tackles', 'defensive_contribution', 'bonus', 
                                        'form', 'yellow_cards', 'red_cards'
                                    ]
                                elif selected_position == 'midfielders':
                                    key_metrics = [
                                        'player_name', 'minutes', 'xG', 'xA', 'xGC', 'total_points', 
                                        'xPoints', 'goals_scored', 'assists', 'clean_sheets', 
                                        'goals_conceded', 'defensive_points', 'clearances_blocks_interceptions',
                                        'recoveries', 'tackles', 'defensive_contribution', 'bonus', 
                                        'form', 'yellow_cards', 'red_cards'
                                    ]
                                else:  # attackers
                                    key_metrics = [
                                        'player_name', 'minutes', 'xG', 'xA', 'total_points', 'xPoints', 
                                        'goals_scored', 'assists', 'bonus', 'form', 'defensive_contribution', 
                                        'defensive_points', 'yellow_cards', 'red_cards'
                                    ]
                                
                                # Add available metrics that exist in the data
                                available_metrics = [col for col in key_metrics if col in comparison_data.columns or col == 'player_name']
                                
                                # Create comparison dataframe
                                comparison_df = comparison_data[available_metrics].copy()
                                
                                # Round numerical columns
                                numeric_cols = comparison_df.select_dtypes(include=[np.number]).columns
                                comparison_df[numeric_cols] = comparison_df[numeric_cols].round(2)
                                
                                # Set player name as index for better display
                                comparison_df = comparison_df.set_index('player_name')
                                
                                # Display transposed table for better comparison
                                st.markdown('<div class="comparison-table">', unsafe_allow_html=True)
                                st.dataframe(comparison_df)
                                st.markdown('</div>', unsafe_allow_html=True)
                                
                            else:
                                st.markdown(
                                    '<div class="comparison-empty-state">'
                                    '<div class="comparison-empty-state-icon">No Data</div>'
                                    '<div>No data available for selected players.</div>'
                                    '</div>', 
                                    unsafe_allow_html=True
                                )
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.markdown(
                        f'<div class="selection-prompt">Please select {position_name.lower()} to compare their performance statistics.</div>', 
                        unsafe_allow_html=True
                    )
            else:
                st.markdown(
                    '<div class="comparison-empty-state">'
                    '<div class="comparison-empty-state-icon">No Results</div>'
                    '<div>No players found matching your search criteria.</div>'
                    '</div>', 
                    unsafe_allow_html=True
                )
        else:
            st.warning(f"No data available for {position_name} - {dict(zip(view_options, view_labels))[selected_view]}")
    
    # Render each comparison position tab
    with comp_tab1:
        render_comparison_tab("Goalkeepers", "goalkeepers", "gk")

    with comp_tab2:
        render_comparison_tab("Defenders", "defenders", "def")

    with comp_tab3:
        render_comparison_tab("Midfielders", "midfielders", "mid")

    with comp_tab4:
        render_comparison_tab("Attackers", "attackers", "att")

# Footer
st.markdown(
    '<div class="footer-text">'
    'FPL Statistics Dashboard'
    '</div>', 
    unsafe_allow_html=True
)