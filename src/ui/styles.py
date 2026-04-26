"""
UI STYLES - DESIGN SYSTEM PROFISSIONAL
Estilos Streamlit centralizados com suporte a mídia.
"""

import streamlit as st

def load_css():
    """Carrega CSS global MODERNO da aplicação."""
    st.markdown("""
    <style>
    
    /* ==================== DESIGN SYSTEM ==================== */
    :root {
        --primary: #0f172a;
        --primary-light: #1e3a8a;
        --accent: #3b82f6;
        --accent-dark: #1d4ed8;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --bg-dark: #0b0f19;
        --bg-card: #1a202c;
        --bg-hover: #2d3748;
        --text-primary: #ffffff;
        --text-secondary: #b0b9c9;
        --text-tertiary: #8892a8;
        --border: #1f2937;
        --shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* ==================== GLOBAL ==================== */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body {
        background: linear-gradient(135deg, var(--bg-dark) 0%, #0f1923 100%);
        color: var(--text-primary);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
        line-height: 1.6;
    }
    
    /* ==================== TIPOGRAFIA ==================== */
    .h1 {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 1rem;
        color: var(--text-primary);
    }
    
    .h2 {
        font-size: 1.875rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 0.75rem;
        color: var(--text-primary);
    }
    
    .h3 {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: var(--text-primary);
    }
    
    .subtitle {
        font-size: 0.95rem;
        color: var(--text-secondary);
        font-weight: 400;
        margin-bottom: 1.5rem;
    }
    
    .caption {
        font-size: 0.8rem;
        color: var(--text-tertiary);
    }
    
    /* ==================== CARDS ==================== */
    .card {
        background: linear-gradient(135deg, var(--bg-card) 0%, #1f2937 100%);
        border: 1px solid var(--border);
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
    }
    
    .card:hover {
        transform: translateY(-4px);
        border: 1px solid var(--accent);
        box-shadow: 0 12px 48px rgba(59, 130, 246, 0.15);
    }
    
    .card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--border);
    }
    
    .card-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .card-badge {
        display: inline-block;
        background: var(--accent);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    /* ==================== BOTÕES ==================== */
    .btn {
        display: inline-block;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s ease;
        border: none;
        font-size: 0.95rem;
        white-space: nowrap;
    }
    
    .btn-primary {
        background: linear-gradient(90deg, var(--accent) 0%, var(--accent-dark) 100%);
        color: white;
        border: 1px solid var(--accent);
    }
    
    .btn-primary:hover {
        opacity: 0.9;
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
    }
    
    .btn-secondary {
        background: var(--bg-hover);
        color: var(--text-primary);
        border: 1px solid var(--border);
    }
    
    .btn-secondary:hover {
        background: var(--bg-card);
        border-color: var(--accent);
    }
    
    .btn-success {
        background: linear-gradient(90deg, var(--success) 0%, #059669 100%);
        color: white;
        border: none;
    }
    
    .btn-danger {
        background: linear-gradient(90deg, var(--danger) 0%, #dc2626 100%);
        color: white;
        border: none;
    }
    
    /* ==================== INPUTS ==================== */
    input, textarea, select {
        background: var(--bg-hover);
        border: 1px solid var(--border);
        color: var(--text-primary);
        padding: 0.75rem 1rem;
        border-radius: 10px;
        font-family: inherit;
        transition: all 0.2s ease;
    }
    
    input:focus, textarea:focus, select:focus {
        outline: none;
        border-color: var(--accent);
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* ==================== TABELAS ==================== */
    .table-container {
        margin: 1.5rem 0;
        overflow-x: auto;
        border-radius: 12px;
        border: 1px solid var(--border);
    }
    
    table {
        width: 100%;
        border-collapse: collapse;
        background: var(--bg-card);
    }
    
    thead {
        background: var(--bg-hover);
        border-bottom: 2px solid var(--accent);
    }
    
    th {
        padding: 1rem;
        text-align: left;
        font-weight: 600;
        color: var(--accent);
        text-transform: uppercase;
        font-size: 0.85rem;
        letter-spacing: 0.5px;
    }
    
    td {
        padding: 1rem;
        border-bottom: 1px solid var(--border);
    }
    
    tbody tr:hover {
        background: var(--bg-hover);
    }
    
    /* ==================== MEDIA (VÍDEO, ÁUDIO) ==================== */
    .media-container {
        position: relative;
        width: 100%;
        max-width: 100%;
        margin: 1.5rem 0;
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid var(--border);
        background: var(--bg-hover);
    }
    
    .media-player {
        width: 100%;
        height: auto;
        min-height: 300px;
    }
    
    .audio-player {
        width: 100%;
        margin: 1rem 0;
    }
    
    .media-thumbnail {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 10px;
        cursor: pointer;
        transition: transform 0.3s ease;
    }
    
    .media-thumbnail:hover {
        transform: scale(1.02);
    }
    
    .media-info {
        padding: 1rem;
        background: var(--bg-card);
        font-size: 0.9rem;
        color: var(--text-secondary);
    }
    
    .media-badge {
        display: inline-block;
        background: var(--accent);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 8px;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 0 0.5rem 0 0;
    }
    
    /* ==================== GRÁFICOS ==================== */
    .chart-container {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        box-shadow: var(--shadow);
    }
    
    .chart-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 1rem;
    }
    
    /* ==================== STATS/KPI ==================== */
    .stat-box {
        background: linear-gradient(135deg, var(--accent) 0%, var(--accent-dark) 100%);
        border-radius: 12px;
        padding: 1.5rem;
        color: white;
        box-shadow: var(--shadow);
        text-align: center;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 800;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* ==================== ALERTAS ==================== */
    .alert {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid;
    }
    
    .alert-success {
        background: rgba(16, 185, 129, 0.1);
        border-color: var(--success);
        color: var(--success);
    }
    
    .alert-warning {
        background: rgba(245, 158, 11, 0.1);
        border-color: var(--warning);
        color: var(--warning);
    }
    
    .alert-danger {
        background: rgba(239, 68, 68, 0.1);
        border-color: var(--danger);
        color: var(--danger);
    }
    
    .alert-info {
        background: rgba(59, 130, 246, 0.1);
        border-color: var(--accent);
        color: var(--accent);
    }
    
    /* ==================== BADGES/TAGS ==================== */
    .badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .badge-primary {
        background: var(--accent);
        color: white;
    }
    
    .badge-success {
        background: var(--success);
        color: white;
    }
    
    .badge-warning {
        background: var(--warning);
        color: var(--bg-dark);
    }
    
    .badge-danger {
        background: var(--danger);
        color: white;
    }
    
    /* ==================== SIDEBAR ==================== */
    .sidebar-menu {
        background: var(--bg-card);
        border-radius: 12px;
        padding: 0;
    }
    
    .sidebar-item {
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        border-radius: 8px;
        transition: all 0.2s ease;
        border-left: 3px solid transparent;
        color: var(--text-secondary);
    }
    
    .sidebar-item:hover {
        background: var(--bg-hover);
        color: var(--text-primary);
    }
    
    .sidebar-item.active {
        background: var(--accent);
        color: white;
        border-left-color: white;
    }
    
    /* ==================== ANIMAÇÕES ==================== */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.3s ease-in-out;
    }
    
    .slide-in {
        animation: slideIn 0.3s ease-in-out;
    }
    
    /* ==================== LOADING ==================== */
    .spinner {
        display: inline-block;
        width: 30px;
        height: 30px;
        border: 3px solid var(--border);
        border-radius: 50%;
        border-top-color: var(--accent);
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* ==================== RESPONSIVIDADE ==================== */
    @media (max-width: 768px) {
        .h1 { font-size: 1.75rem; }
        .h2 { font-size: 1.5rem; }
        .h3 { font-size: 1.25rem; }
        
        .card {
            padding: 1rem;
        }
        
        table {
            font-size: 0.9rem;
        }
        
        th, td {
            padding: 0.75rem;
        }
        
        .stat-box {
            padding: 1rem;
        }
        
        .stat-value {
            font-size: 1.5rem;
        }
    }
    
    </style>
    """, unsafe_allow_html=True)
