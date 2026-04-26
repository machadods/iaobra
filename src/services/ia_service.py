"""
IA SERVICE - OpenRouter
Modelos gratuitos em ordem de preferencia.
"""

import requests
import html
import re
from config import OPENROUTER_API_KEY, OPENROUTER_MODEL, OPENROUTER_BASE_URL

MODELOS_GRATUITOS = [OPENROUTER_MODEL]
_modelos_cache: list = []


def _buscar_modelos_gratuitos(api_key: str) -> list:
    """Consulta a API do OpenRouter e retorna IDs dos modelos gratuitos disponíveis."""
    global _modelos_cache
    if _modelos_cache:
        return _modelos_cache
    try:
        resp = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10,
        )
        if resp.status_code == 200:
            modelos = resp.json().get("data", [])
            _modelos_cache = [
                m["id"] for m in modelos
                if str(m.get("pricing", {}).get("prompt", "1")) == "0"
                and str(m.get("pricing", {}).get("completion", "1")) == "0"
            ]
            return _modelos_cache
    except Exception:
        pass
    return [OPENROUTER_MODEL]


def _sanitizar(texto: str) -> str:
    texto = html.escape(texto)
    texto = re.sub(r"[<>{};`]", "", texto)
    return texto[:4000]


class IAService:
    def __init__(self):
        self.api_key = OPENROUTER_API_KEY
        self._modelo_atual = None

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://iaobras.app",
            "X-Title": "IAObras",
        }

    def _chamar_ia(self, mensagens: list, temperatura: float = 0.7,
                   id_usuario: int = None, descricao_debito: str = "Chamada IA") -> str:
        if not self.api_key:
            return "Chave OPENROUTER_API_KEY nao configurada no arquivo .env"

        # Verifica e debita credito antes de chamar
        if id_usuario:
            from src.services.creditos_service import CreditosService
            cred = CreditosService()
            if not cred.tem_creditos(id_usuario):
                return "Sem creditos de IA. Acesse Planos para recarregar."
            cred.debitar(id_usuario, descricao_debito)

        # Busca modelos gratuitos disponíveis na conta e tenta cada um
        modelos = _buscar_modelos_gratuitos(self.api_key)
        if not modelos:
            modelos = MODELOS_GRATUITOS
        ultimo_erro = ""

        for modelo in modelos:
            try:
                resp = requests.post(
                    OPENROUTER_BASE_URL,
                    headers=self._headers(),
                    json={
                        "model": modelo,
                        "messages": mensagens,
                        "temperature": temperatura,
                        "max_tokens": 1500,
                    },
                    timeout=45,
                )
                if resp.status_code == 200:
                    self._modelo_atual = modelo
                    return resp.json()["choices"][0]["message"]["content"]
                else:
                    ultimo_erro = f"Modelo {modelo}: HTTP {resp.status_code} — {resp.text[:200]}"
            except requests.exceptions.Timeout:
                ultimo_erro = f"Modelo {modelo}: timeout"
            except Exception as e:
                ultimo_erro = f"Modelo {modelo}: {str(e)}"

        return f"Nenhum modelo disponivel respondeu. Ultimo erro: {ultimo_erro}"

    def analisar_registro(self, texto: str, nome_obra: str, id_usuario: int = None) -> str:
        texto = _sanitizar(texto)
        nome_obra = _sanitizar(nome_obra)
        prompt = f"""Voce e um assistente especialista em construcao civil brasileira.
O mestre de obras registrou o seguinte progresso da obra "{nome_obra}":

"{texto}"

Responda em portugues do Brasil com:

AUDITORIA DO DIA:
(Avalie o que foi feito, pontos de atencao)

PROXIMAS ETAPAS SUGERIDAS:
(Liste 3 a 5 acoes praticas e objetivas)

ALERTA:
(Algum risco identificado? Se nao houver escreva "Nenhum alerta.")

Seja direto e use linguagem simples para o mestre de obras."""
        return self._chamar_ia([{"role": "user", "content": prompt}], 0.5,
                               id_usuario=id_usuario, descricao_debito="Analise de registro")

    def gerar_cronograma(self, descricao: str, nome_obra: str, id_usuario: int = None) -> str:
        descricao = _sanitizar(descricao)
        nome_obra = _sanitizar(nome_obra)
        prompt = f"""Especialista em construcao civil brasileira.
Crie um cronograma simples para a obra "{nome_obra}":

"{descricao}"

Formato de tabela: Etapa | Duracao estimada | Descricao resumida
Maximo 10 etapas. Linguagem simples. Responda em portugues do Brasil."""
        return self._chamar_ia([{"role": "user", "content": prompt}], 0.4,
                               id_usuario=id_usuario, descricao_debito="Cronograma IA")

    def consultar_precos(self, material: str, regiao: str = "Brasil", id_usuario: int = None) -> str:
        material = _sanitizar(material)
        regiao = _sanitizar(regiao)
        prompt = f"""Especialista em materiais de construcao civil brasileira.
Estimativa de preco para: {material} — Regiao: {regiao}

Inclua: faixa de preco (R$), unidade, onde encontrar, dica para economizar.
Avise que sao estimativas e podem variar. Portugues do Brasil."""
        return self._chamar_ia([{"role": "user", "content": prompt}], 0.3,
                               id_usuario=id_usuario, descricao_debito="Consulta preco IA")

    def chat_estudos(self, pergunta: str, historico: list = None, id_usuario: int = None) -> str:
        pergunta = _sanitizar(pergunta)
        msgs = [{
            "role": "system",
            "content": "Voce e um professor especialista em construcao civil brasileira. Ajude mestres de obras com duvidas tecnicas, normas NBR, materiais e gestao. Seja didatico e use linguagem acessivel. Responda em portugues do Brasil.",
        }]
        if historico:
            for m in historico[-10:]:  # maximo 10 mensagens de historico
                msgs.append({"role": m["role"], "content": _sanitizar(m["content"])})
        msgs.append({"role": "user", "content": pergunta})
        return self._chamar_ia(msgs, 0.7,
                               id_usuario=id_usuario, descricao_debito="Chat estudos")

    def resumir_obra(self, registros: list, nome_obra: str) -> str:
        if not registros:
            return "Nenhum registro para resumir."
        nome_obra = _sanitizar(nome_obra)
        textos = "\n".join([f"- {_sanitizar(r)}" for r in registros[-10:]])
        prompt = f"""Gestor de obras, resumo executivo da obra "{nome_obra}":

{textos}

Inclua: SITUACAO ATUAL | PROGRESSO | PENDENCIAS | RECOMENDACAO
Maximo 200 palavras. Portugues do Brasil."""
        return self._chamar_ia([{"role": "user", "content": prompt}], 0.4)

    @property
    def configurada(self) -> bool:
        return bool(self.api_key)

    @property
    def modelo_em_uso(self) -> str:
        return self._modelo_atual or OPENROUTER_MODEL
