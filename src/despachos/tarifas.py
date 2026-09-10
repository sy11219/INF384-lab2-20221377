"""Calculo de tarifas de despacho."""

from __future__ import annotations

from dataclasses import dataclass

TARIFA_BASE = 12.50
COSTO_POR_KILO = 1.80
RECARGO_ZONA_ALEJADA = 0.35
UMBRAL_ENVIO_GRATIS = 250.00

ZONAS_ALEJADAS = {"selva", "sierra_alta", "frontera"}


class ZonaDesconocida(Exception):
    """La zona indicada no esta en el tarifario."""


ZONAS = {
    "lima_metropolitana": 1.00,
    "costa_norte": 1.20,
    "costa_sur": 1.20,
    "sierra": 1.45,
    "sierra_alta": 1.65,
    "selva": 1.80,
    "frontera": 2.10,
}


@dataclass
class Envio:
    zona: str
    peso_kg: float
    valor_declarado: float
    urgente: bool = False


def factor_zona(zona: str) -> float:
    if zona not in ZONAS:
        raise ZonaDesconocida(f"zona no reconocida: {zona}")
    return ZONAS[zona]


def costo_peso(peso_kg: float) -> float:
    if peso_kg <= 0:
        return 0.0
    return round(peso_kg * COSTO_POR_KILO, 2)


def aplica_envio_gratis(envio: Envio) -> bool:
    if envio.urgente:
        return False
    if envio.zona in ZONAS_ALEJADAS:
        return False
    return envio.valor_declarado >= UMBRAL_ENVIO_GRATIS


def calcular(envio: Envio) -> float:
    if aplica_envio_gratis(envio):
        return 0.0

    total = TARIFA_BASE + costo_peso(envio.peso_kg)
    total = total * factor_zona(envio.zona)

    if envio.zona in ZONAS_ALEJADAS:
        total = total * (1 + RECARGO_ZONA_ALEJADA)

    if envio.urgente:
        total = total * 1.5

    return round(total, 2)


def clasificar_riesgo_envio(envio: Envio) -> str:
    """Clasifica el riesgo logistico de un envio segun zona, peso y valor.
 
    Devuelve una de: "bajo", "medio", "alto", "critico".
    """
    puntaje = 0
 
    if envio.zona in ZONAS_ALEJADAS:
        puntaje += 2
    elif envio.zona in {"sierra", "costa_sur"}:
        puntaje += 1
 
    if envio.peso_kg > 50:
        puntaje += 3
    elif envio.peso_kg > 20:
        puntaje += 2
    elif envio.peso_kg > 5:
        puntaje += 1
 
    if envio.valor_declarado > 1000:
        puntaje += 3
    elif envio.valor_declarado > 300:
        puntaje += 1
 
    if envio.urgente:
        puntaje += 1
 
    if puntaje >= 7:
        return "critico"
    if puntaje >= 4:
        return "alto"
    if puntaje >= 2:
        return "medio"
    return "bajo"


def desglose(envio: Envio) -> dict[str, float]:
    base = TARIFA_BASE
    peso = costo_peso(envio.peso_kg)
    factor = factor_zona(envio.zona)
    return {
        "base": base,
        "peso": peso,
        "factor_zona": factor,
        "total": calcular(envio),
    }
