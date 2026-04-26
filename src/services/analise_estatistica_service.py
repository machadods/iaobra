"""
Serviço de Análise Estatística Avançada
Cálculos de estatística, regressão, tendências e previsões
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from scipy import stats as scipy_stats
from scipy.interpolate import interp1d
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import logging
from loguru import logger

class AnalisadorEstatisto:
    """Análise estatística avançada de dados de obra"""
    
    def __init__(self):
        self.logger = logger
        self.logger.add("logs/analise_estatistica.log", rotation="500 MB")
    
    # ============================================================
    # ANÁLISE DE TENDÊNCIAS
    # ============================================================
    
    def calcular_tendencia_progresso(
        self, 
        datas: List[datetime], 
        valores_progresso: List[float]
    ) -> Dict[str, Any]:
        """
        Calcula tendência de progresso com regressão linear
        
        Args:
            datas: Lista de timestamps
            valores_progresso: Lista de percentuais de progresso (0-100)
        
        Returns:
            Dict com slope, intercept, r², velocidade média, previsão
        """
        if len(datas) < 2:
            return {"erro": "Dados insuficientes"}
        
        # Converter datas para dias (numérico)
        data_base = datas[0]
        X = np.array([(d - data_base).days for d in datas]).reshape(-1, 1)
        y = np.array(valores_progresso)
        
        # Regressão Linear
        modelo = LinearRegression()
        modelo.fit(X, y)
        
        y_pred = modelo.predict(X)
        r2 = 1 - (np.sum((y - y_pred)**2) / np.sum((y - np.mean(y))**2))
        
        slope = modelo.coef_[0]  # % por dia
        
        # Previsão de conclusão
        dias_faltantes = (100 - y[-1]) / slope if slope > 0 else float('inf')
        data_conclusao = datas[-1] + timedelta(days=int(dias_faltantes))
        
        return {
            "velocidade_percentual_por_dia": round(slope, 4),
            "r_quadrado": round(r2, 4),
            "dias_faltantes_previstos": int(dias_faltantes),
            "data_conclusao_prevista": data_conclusao,
            "confianca_previsao": round(r2 * 100, 2),  # R² como confiança
            "progresso_atual": y[-1],
            "progresso_inicial": y[0]
        }
    
    # ============================================================
    # ANÁLISE DE DISTRIBUIÇÃO TEMPORAL
    # ============================================================
    
    def analisar_distribuicao_atividade(
        self, 
        timestamps: List[datetime]
    ) -> Dict[str, Any]:
        """
        Analisa padrão de atividade ao longo do tempo
        """
        if not timestamps:
            return {}
        
        df = pd.DataFrame({"timestamp": timestamps})
        df["hora"] = df["timestamp"].dt.hour
        df["dia_semana"] = df["timestamp"].dt.dayofweek
        df["data"] = df["timestamp"].dt.date
        
        # Atividade por hora
        atividade_hora = df.groupby("hora").size().to_dict()
        pico_hora = max(atividade_hora, key=atividade_hora.get) if atividade_hora else None
        
        # Atividade por dia da semana
        dias = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]
        atividade_dia = df.groupby("dia_semana").size().to_dict()
        dia_mais_ativo = dias[max(atividade_dia, key=atividade_dia.get)] if atividade_dia else None
        
        # Atividade por data
        atividade_data = df.groupby("data").size()
        media_por_dia = atividade_data.mean()
        desvio_por_dia = atividade_data.std()
        
        return {
            "pico_atividade_hora": f"{pico_hora:02d}:00" if pico_hora else None,
            "dia_mais_produtivo": dia_mais_ativo,
            "media_atividade_por_dia": round(media_por_dia, 2),
            "variancia_atividade": round(desvio_por_dia**2, 2),
            "desvio_padrao_atividade": round(desvio_por_dia, 2),
            "atividade_por_hora": atividade_hora,
            "atividade_por_dia_semana": atividade_dia
        }
    
    # ============================================================
    # DETECÇÃO DE ANOMALIAS
    # ============================================================
    
    def detectar_anomalias_atividade(
        self, 
        valores: List[float],
        metodo: str = "zscore",
        limiar: float = 3.0
    ) -> Dict[str, Any]:
        """
        Detecta anomalias em sequência de valores usando Z-score
        
        Args:
            valores: Lista de valores (ex: atividade por dia)
            metodo: 'zscore', 'iqr', ou 'isolation_forest'
            limiar: Limiar para zscore (padrão 3.0)
        
        Returns:
            Dict com índices de anomalias, valores atípicos e confiança
        """
        valores = np.array(valores)
        
        if metodo == "zscore":
            z_scores = np.abs(scipy_stats.zscore(valores))
            anomalias = np.where(z_scores > limiar)[0].tolist()
            confianca = float(np.mean(z_scores[anomalias])) if anomalias else 0
        
        elif metodo == "iqr":
            Q1 = np.percentile(valores, 25)
            Q3 = np.percentile(valores, 75)
            IQR = Q3 - Q1
            limite_inf = Q1 - 1.5 * IQR
            limite_sup = Q3 + 1.5 * IQR
            anomalias = np.where((valores < limite_inf) | (valores > limite_sup))[0].tolist()
            confianca = 0.85 if anomalias else 0
        
        else:
            anomalias = []
            confianca = 0
        
        return {
            "indices_anomalias": anomalias,
            "valores_atipicos": valores[anomalias].tolist() if anomalias else [],
            "confianca_deteccao": round(confianca, 3),
            "total_anomalias": len(anomalias)
        }
    
    # ============================================================
    # ANÁLISE DE QUALIDADE E CONFIANÇA
    # ============================================================
    
    def calcular_metricas_qualidade(
        self, 
        confiancas: List[float]
    ) -> Dict[str, Any]:
        """
        Calcula estatísticas de qualidade/confiança
        """
        if not confiancas:
            return {}
        
        confiancas = np.array(confiancas)
        
        return {
            "confianca_media": round(np.mean(confiancas), 4),
            "confianca_mediana": round(np.median(confiancas), 4),
            "confianca_minima": round(np.min(confiancas), 4),
            "confianca_maxima": round(np.max(confiancas), 4),
            "desvio_padrao": round(np.std(confiancas), 4),
            "variancia": round(np.var(confiancas), 4),
            "percentil_25": round(np.percentile(confiancas, 25), 4),
            "percentil_75": round(np.percentile(confiancas, 75), 4),
            "iqr": round(
                np.percentile(confiancas, 75) - np.percentile(confiancas, 25), 
                4
            )
        }
    
    # ============================================================
    # ANÁLISE DE CORRELAÇÃO
    # ============================================================
    
    def calcular_correlacao(
        self, 
        dados: Dict[str, List[float]]
    ) -> Dict[str, Dict[str, float]]:
        """
        Calcula matriz de correlação entre variáveis
        
        Args:
            dados: Dict com nomes e listas de valores
        
        Returns:
            Matriz de correlação
        """
        df = pd.DataFrame(dados)
        correlacao = df.corr()
        
        return correlacao.to_dict()
    
    # ============================================================
    # INTERPOLAÇÃO E SUAVIZAÇÃO
    # ============================================================
    
    def interpolar_progresso(
        self, 
        datas: List[datetime], 
        valores: List[float]
    ) -> Dict[str, Any]:
        """
        Interpola valores de progresso para preenchimento de gaps
        """
        if len(datas) < 2:
            return {"erro": "Dados insuficientes"}
        
        # Converter para dias numéricos
        data_base = datas[0]
        x = np.array([(d - data_base).days for d in datas])
        y = np.array(valores)
        
        # Interpolação linear
        f = interp1d(x, y, kind='linear', fill_value='extrapolate')
        
        # Gerar pontos interpolados
        x_novo = np.arange(x.min(), x.max() + 1, 1)
        y_novo = f(x_novo)
        
        return {
            "x_interpolado": x_novo.tolist(),
            "y_interpolado": np.clip(y_novo, 0, 100).tolist()
        }
    
    # ============================================================
    # ANÁLISE DE VELOCIDADE / MOMENTUM
    # ============================================================
    
    def analisar_velocidade_progresso(
        self, 
        valores: List[float]
    ) -> Dict[str, Any]:
        """
        Analisa velocidade e aceleração de progresso
        """
        if len(valores) < 3:
            return {"erro": "Dados insuficientes"}
        
        valores = np.array(valores)
        
        # Velocidade (primeira derivada)
        velocidade = np.diff(valores)
        velocidade_media = np.mean(velocidade)
        
        # Aceleração (segunda derivada)
        aceleracao = np.diff(velocidade)
        aceleracao_media = np.mean(aceleracao)
        
        # Momentum
        momentos_positivos = np.sum(velocidade > 0)
        momentos_negativos = np.sum(velocidade < 0)
        percentual_positivo = (momentos_positivos / len(velocidade)) * 100
        
        # Status
        if aceleracao_media > 0:
            status = "acelerando"
        elif aceleracao_media < -0.1:
            status = "desacelerando"
        else:
            status = "constante"
        
        return {
            "velocidade_media": round(velocidade_media, 4),
            "aceleracao_media": round(aceleracao_media, 4),
            "momentos_positivos": int(momentos_positivos),
            "momentos_negativos": int(momentos_negativos),
            "percentual_momentum_positivo": round(percentual_positivo, 2),
            "status_momentum": status
        }
    
    # ============================================================
    # CLUSTERING / SEGMENTAÇÃO TEMPORAL
    # ============================================================
    
    def segmentar_fases_obra(
        self, 
        valores_progresso: List[float]
    ) -> Dict[str, Any]:
        """
        Segmenta obra em fases baseado em mudanças de velocidade
        """
        if len(valores_progresso) < 3:
            return {"erro": "Dados insuficientes"}
        
        # Calcular velocidade
        velocidade = np.diff(valores_progresso)
        
        # Identificar pontos de mudança (change points)
        mudancas = np.where(np.abs(np.diff(velocidade)) > np.std(velocidade))[0]
        
        fases = []
        inicio = 0
        
        for mudanca in mudancas:
            fases.append({
                "indice_inicio": int(inicio),
                "indice_fim": int(mudanca),
                "progresso_inicial": float(valores_progresso[inicio]),
                "progresso_final": float(valores_progresso[mudanca]),
                "velocidade_media": float(np.mean(velocidade[inicio:mudanca]))
            })
            inicio = mudanca
        
        # Última fase
        fases.append({
            "indice_inicio": int(inicio),
            "indice_fim": int(len(valores_progresso) - 1),
            "progresso_inicial": float(valores_progresso[inicio]),
            "progresso_final": float(valores_progresso[-1]),
            "velocidade_media": float(np.mean(velocidade[inicio:]))
        })
        
        return {"fases": fases, "total_fases": len(fases)}
    
    # ============================================================
    # ESTATÍSTICAS DESCRITIVAS GENÉRICAS
    # ============================================================
    
    def resumo_estatistico(
        self, 
        valores: List[float]
    ) -> Dict[str, float]:
        """
        Calcula resumo estatístico completo
        """
        valores = np.array(valores)
        
        return {
            "media": round(np.mean(valores), 4),
            "mediana": round(np.median(valores), 4),
            "moda": round(float(scipy_stats.mode(valores, keepdims=True).mode), 4),
            "minimo": round(np.min(valores), 4),
            "maximo": round(np.max(valores), 4),
            "amplitude": round(np.max(valores) - np.min(valores), 4),
            "desvio_padrao": round(np.std(valores), 4),
            "variancia": round(np.var(valores), 4),
            "coeficiente_variacao": round((np.std(valores) / np.mean(valores)) * 100, 4),
            "assimetria": round(scipy_stats.skew(valores), 4),
            "curtose": round(scipy_stats.kurtosis(valores), 4),
            "percentil_25": round(np.percentile(valores, 25), 4),
            "percentil_50": round(np.percentile(valores, 50), 4),
            "percentil_75": round(np.percentile(valores, 75), 4),
            "percentil_90": round(np.percentile(valores, 90), 4),
            "percentil_95": round(np.percentile(valores, 95), 4)
        }
    
    # ============================================================
    # TESTES ESTATÍSTICOS
    # ============================================================
    
    def teste_normalidade(
        self, 
        valores: List[float]
    ) -> Dict[str, Any]:
        """
        Testa se valores seguem distribuição normal (Shapiro-Wilk)
        """
        valores = np.array(valores)
        
        if len(valores) < 3:
            return {"erro": "Amostra muito pequena"}
        
        stat, p_value = scipy_stats.shapiro(valores)
        
        return {
            "teste": "Shapiro-Wilk",
            "estatistica": round(stat, 4),
            "p_value": round(p_value, 4),
            "normal": p_value > 0.05
        }
    
    def teste_tendencia(
        self, 
        valores: List[float]
    ) -> Dict[str, Any]:
        """
        Testa se há tendência significativa (Mann-Kendall)
        """
        valores = np.array(valores)
        
        if len(valores) < 4:
            return {"erro": "Amostra muito pequena"}
        
        # Mann-Kendall simplified
        n = len(valores)
        s = 0
        for i in range(n-1):
            for j in range(i+1, n):
                s += np.sign(valores[j] - valores[i])
        
        # Variância
        var_s = n * (n - 1) * (2 * n + 5) / 18
        
        # Z-score
        z = s / np.sqrt(var_s) if var_s > 0 else 0
        p_value = 2 * (1 - scipy_stats.norm.cdf(abs(z)))
        
        return {
            "teste": "Mann-Kendall",
            "estatistica_s": int(s),
            "z_score": round(z, 4),
            "p_value": round(p_value, 4),
            "tendencia_significativa": p_value < 0.05
        }

# Instância global
analisador = AnalisadorEstatisto()
