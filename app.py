# ==========================
# FitSUS - Serviço Python (API)
# ==========================
# Este serviço FastAPI faz análises simuladas de tratamentos fitoterápicos.
# Integra-se com o painel PHP para registrar e obter resultados.

from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
import datetime
import random
import uvicorn

# Inicializa o app FastAPI
app = FastAPI(title="FitSUS RWE Analysis Service")

# ==========================
# Rota principal (teste rápido)
# ==========================
@app.get("/")
def home():
    return {"message": "API FitSUS em execução 🚀", "status": "online"}

# ==========================
# Modelo de dados esperado no POST /analyze
# ==========================
class TreatmentPayload(BaseModel):
    treatment_id: int
    user_id: int
    product_id: int
    condition: Optional[str] = None
    dose: Optional[str] = None
    route: Optional[str] = None
    start_date: Optional[str] = None
    notes: Optional[str] = None

# ==========================
# Endpoint principal: /analyze
# ==========================
@app.post("/analyze")
def analyze(payload: TreatmentPayload):
    """
    Analisa um tratamento e retorna um score de risco.
    (Simulação — em produção, seria um modelo preditivo real)
    """

    note = "Sem observações críticas"
    score = 0.1

    # Regras simuladas
    if payload.dose and 'alta' in payload.dose.lower():
        score += 0.4
        note = "Dose alta informada - sugerir acompanhamento"

    if payload.condition and 'dor' in payload.condition.lower():
        score += 0.2

    # Adiciona variação aleatória para simular incerteza
    score += random.uniform(0, 0.2)
    score = round(min(score, 1.0), 3)

    # Resultado
    result = {
        "treatment_id": payload.treatment_id,
        "analysis_date": datetime.datetime.utcnow().isoformat(),
        "risk_score": score,
        "message": note,
        "recommendation": (
            "Agendar acompanhamento com profissional de saúde"
            if score > 0.4 else
            "Acompanhar evolução"
        )
    }

    return result

# ==========================
# Execução local (modo manual)
# ==========================
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
