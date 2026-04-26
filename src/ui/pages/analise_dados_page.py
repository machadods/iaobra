"""
Página de Análise de Dados - Timeline e Estatísticas Avançadas
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from src.services.analise_estatistica_service import analisador

def render():
    """Renderiza página de análise de dados"""
    
    st.markdown("""
    <div class='h1'>📊 Análise de Dados - Simulador Temporal</div>
    <div class='subtitle'>Estatística avançada, tendências e previsões em tempo real</div>
    """, unsafe_allow_html=True)
    
    # Sidebar com filtros
    with st.sidebar:
        st.markdown("### 🎯 Filtros")
        id_obra = st.selectbox("Selecione a Obra", [1, 2, 3], format_func=lambda x: f"Obra #{x}")
        data_inicio = st.date_input("Data Início", datetime.now() - timedelta(days=30))
        data_fim = st.date_input("Data Fim", datetime.now())
    
    # Gerar dados de exemplo (em produção, vem do banco)
    dados_exemplo = gerar_dados_exemplo(data_inicio, data_fim)
    
    # ==================== TABS ====================
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Tendências",
        "⚡ Velocidade",
        "🎯 Anomalias",
        "📊 Correlação",
        "🔮 Previsão"
    ])
    
    # ==================== TAB 1: TENDÊNCIAS ====================
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Progresso da Obra")
            
            # Gráfico de progresso
            fig_progresso = px.line(
                dados_exemplo,
                x="data",
                y="progresso",
                markers=True,
                title="Progresso Acumulado",
                labels={"progresso": "Progresso (%)", "data": "Data"}
            )
            fig_progresso.update_traces(
                line=dict(color='#3b82f6', width=3),
                marker=dict(size=6)
            )
            fig_progresso.update_layout(
                template="plotly_dark",
                hovermode="x unified"
            )
            st.plotly_chart(fig_progresso, use_container_width=True)
        
        with col2:
            st.markdown("### Análise de Tendência")
            
            # Calcular tendência
            tendencia = analisador.calcular_tendencia_progresso(
                dados_exemplo["data"].tolist(),
                dados_exemplo["progresso"].tolist()
            )
            
            # Exibir métricas
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.metric(
                    "Velocidade",
                    f"{tendencia['velocidade_percentual_por_dia']:.2f}% /dia",
                    delta=f"R²: {tendencia['r_quadrado']:.3f}"
                )
            with col_m2:
                st.metric(
                    "Conclusão Prevista",
                    tendencia["data_conclusao_prevista"].strftime("%d/%m/%Y"),
                    delta=f"Confiança: {tendencia['confianca_previsao']:.0f}%"
                )
            
            # Detalhes
            with st.expander("📋 Detalhes da Tendência"):
                df_tend = pd.DataFrame([tendencia])
                st.dataframe(df_tend, use_container_width=True)
    
    # ==================== TAB 2: VELOCIDADE ====================
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Velocidade de Progresso")
            
            # Calcular velocidade
            velocidade_info = analisador.analisar_velocidade_progresso(
                dados_exemplo["progresso"].tolist()
            )
            
            # Gráfico de velocidade
            velocidade_diaria = np.diff(dados_exemplo["progresso"].values)
            
            fig_velocidade = go.Figure()
            fig_velocidade.add_trace(go.Bar(
                y=velocidade_diaria,
                x=dados_exemplo["data"].iloc[1:],
                marker_color=['#10b981' if v > 0 else '#ef4444' for v in velocidade_diaria],
                name="Progresso/dia"
            ))
            fig_velocidade.update_layout(
                title="Velocidade Diária",
                template="plotly_dark",
                xaxis_title="Data",
                yaxis_title="Progresso (%)"
            )
            st.plotly_chart(fig_velocidade, use_container_width=True)
        
        with col2:
            st.markdown("### Momentum e Aceleração")
            
            # Métricas de velocidade
            col_v1, col_v2 = st.columns(2)
            with col_v1:
                st.metric(
                    "Velocidade Média",
                    f"{velocidade_info['velocidade_media']:.2f}%",
                    "por dia"
                )
            with col_v2:
                st.metric(
                    "Aceleração",
                    f"{velocidade_info['aceleracao_media']:.3f}",
                    f"Status: {velocidade_info['status_momentum']}"
                )
            
            # Momentum
            st.markdown(f"""
            - **Momentum Positivo**: {velocidade_info['percentual_momentum_positivo']:.1f}%
            - **Momentos Positivos**: {velocidade_info['momentos_positivos']}
            - **Momentos Negativos**: {velocidade_info['momentos_negativos']}
            """)
    
    # ==================== TAB 3: ANOMALIAS ====================
    with tab3:
        st.markdown("### 🚨 Detecção de Anomalias")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            metodo_anomalia = st.selectbox(
                "Método de Detecção",
                ["Z-Score", "IQR", "Isolation Forest"]
            )
            limiar = st.slider("Limiar de Sensibilidade", 1.0, 5.0, 3.0)
        
        with col2:
            # Detectar anomalias
            anomalias = analisador.detectar_anomalias_atividade(
                dados_exemplo["atividade"].tolist(),
                metodo="zscore",
                limiar=limiar
            )
            
            # Gráfico com anomalias destacadas
            fig_anomalia = go.Figure()
            fig_anomalia.add_trace(go.Scatter(
                y=dados_exemplo["atividade"],
                x=dados_exemplo["data"],
                mode='lines+markers',
                name="Atividade",
                line=dict(color='#3b82f6')
            ))
            
            if anomalias["indices_anomalias"]:
                fig_anomalia.add_trace(go.Scatter(
                    y=[dados_exemplo["atividade"].iloc[i] for i in anomalias["indices_anomalias"]],
                    x=[dados_exemplo["data"].iloc[i] for i in anomalias["indices_anomalias"]],
                    mode='markers',
                    name="Anomalias",
                    marker=dict(color='#ef4444', size=12, symbol='star')
                ))
            
            fig_anomalia.update_layout(
                template="plotly_dark",
                title="Detecção de Anomalias",
                hovermode="x unified"
            )
            st.plotly_chart(fig_anomalia, use_container_width=True)
        
        # Resumo de anomalias
        st.markdown("#### 📍 Anomalias Detectadas")
        if anomalias["total_anomalias"] > 0:
            col_a1, col_a2, col_a3 = st.columns(3)
            with col_a1:
                st.metric("Total de Anomalias", anomalias["total_anomalias"])
            with col_a2:
                st.metric("Confiança", f"{anomalias['confianca_deteccao']:.2%}")
            with col_a3:
                st.metric("Valores Atípicos", len(anomalias["valores_atipicos"]))
        else:
            st.success("✅ Nenhuma anomalia detectada!")
    
    # ==================== TAB 4: CORRELAÇÃO ====================
    with tab4:
        st.markdown("### 🔗 Correlação entre Variáveis")
        
        # Dados para correlação
        dados_correlacao = {
            "Progresso": dados_exemplo["progresso"].tolist(),
            "Atividade": dados_exemplo["atividade"].tolist(),
            "Qualidade": dados_exemplo["qualidade"].tolist(),
            "Uploads": dados_exemplo["uploads"].tolist()
        }
        
        corr_matrix = analisador.calcular_correlacao(dados_correlacao)
        df_corr = pd.DataFrame(corr_matrix)
        
        # Heatmap
        fig_corr = go.Figure(data=go.Heatmap(
            z=df_corr.values,
            x=df_corr.columns,
            y=df_corr.index,
            colorscale='Blues'
        ))
        fig_corr.update_layout(template="plotly_dark", title="Matriz de Correlação")
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Tabela de correlação
        st.dataframe(df_corr.round(3), use_container_width=True)
    
    # ==================== TAB 5: PREVISÃO ====================
    with tab5:
        st.markdown("### 🔮 Previsões e Projeções")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Interpolação para suavização
            interpolacao = analisador.interpolar_progresso(
                dados_exemplo["data"].tolist(),
                dados_exemplo["progresso"].tolist()
            )
            
            # Gráfico com previsão
            fig_previsao = go.Figure()
            
            # Dados reais
            fig_previsao.add_trace(go.Scatter(
                x=dados_exemplo["data"],
                y=dados_exemplo["progresso"],
                mode='markers',
                name="Dados Reais",
                marker=dict(color='#3b82f6', size=8)
            ))
            
            # Linha interpolada
            fig_previsao.add_trace(go.Scatter(
                x=pd.date_range(start=dados_exemplo["data"].min(), periods=len(interpolacao["x_interpolado"]), freq='D'),
                y=interpolacao["y_interpolado"],
                mode='lines',
                name="Tendência",
                line=dict(color='#10b981', width=2, dash='dash')
            ))
            
            fig_previsao.update_layout(
                template="plotly_dark",
                title="Previsão de Progresso",
                hovermode="x unified"
            )
            st.plotly_chart(fig_previsao, use_container_width=True)
        
        with col2:
            st.markdown("#### 📊 Estatísticas")
            
            # Resumo estatístico
            resumo = analisador.resumo_estatistico(dados_exemplo["progresso"].tolist())
            
            st.metric("Média", f"{resumo['media']:.1f}%")
            st.metric("Mediana", f"{resumo['mediana']:.1f}%")
            st.metric("Desvio Padrão", f"{resumo['desvio_padrao']:.2f}%")
            st.metric("Min/Max", f"{resumo['minimo']:.1f}% / {resumo['maximo']:.1f}%")
    
    # ==================== RODAPÉ ====================
    st.markdown("---")
    st.markdown("""
    <div class='subtitle'>
    💡 **Dicas**: Use os filtros para analisar períodos específicos. 
    Os dados são recalculados em tempo real usando estatística avançada.
    </div>
    """, unsafe_allow_html=True)

def gerar_dados_exemplo(data_inicio, data_fim):
    """Gera dados de exemplo para demonstração"""
    dates = pd.date_range(start=data_inicio, end=data_fim, freq='D')
    
    progresso = np.linspace(0, 85, len(dates)) + np.random.normal(0, 2, len(dates))
    progresso = np.clip(progresso, 0, 100)
    
    atividade = np.random.poisson(15, len(dates))
    qualidade = 0.7 + 0.2 * np.sin(np.linspace(0, 4*np.pi, len(dates))) + np.random.normal(0, 0.05, len(dates))
    qualidade = np.clip(qualidade, 0.5, 0.95)
    uploads = np.random.poisson(8, len(dates))
    
    return pd.DataFrame({
        "data": dates,
        "progresso": progresso,
        "atividade": atividade,
        "qualidade": qualidade,
        "uploads": uploads
    })
