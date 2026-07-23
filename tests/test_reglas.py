"""Casos límite: conservar evidencia, no completar teléfonos y separar zonas."""
import unittest
from pathlib import Path

import pandas as pd

from src.comun import cargar, texto
from src.limpieza import limpiar, telefono
from src.duplicados import detectar
from src.validacion import validar

ROOT = Path(__file__).resolve().parents[1]


class Reglas(unittest.TestCase):
    def test_telefonos_sin_imputar(self):
        cases = {
            "2220-1723": ("22201723", "VALIDO"),
            "22207754, 22207755": ("22207754;22207755", "MULTIPLE"),
            "+502 22201723": ("22201723", "VALIDO"),
            "22202870-73": ("22202870", "PARCIAL"),
            "2517748 2384159": ("", "INVALIDO"),
            "00000000": ("", "INVALIDO"),
            "SIN DATO": ("", "AUSENTE"),
        }
        for value, expected in cases.items():
            with self.subTest(value=value):
                self.assertEqual(telefono(value)[:2], expected)

    def test_unicode_idempotente_sin_perder_tildes(self):
        result = texto("  Jose\u0301\u200b   de la Cruz  ")
        self.assertEqual(result, "JOSÉ DE LA CRUZ")
        self.assertEqual(texto(result), result)

    def test_capital_conserva_codigo_y_separa_zona(self):
        raw = cargar(ROOT)
        sample = raw.loc[raw.DEPARTAMENTO.eq("CIUDAD CAPITAL")].iloc[:2].copy().reset_index(drop=True)
        clean, audit = limpiar(sample, ROOT)
        self.assertEqual(clean.CODIGO.tolist(), sample.CODIGO.tolist())
        self.assertTrue(clean.CODIGO_MUNICIPIO.eq("0101").all())
        self.assertTrue(clean.MUNICIPIO.eq("GUATEMALA").all())
        self.assertTrue(clean.MUNICIPIO_ORIGINAL.str.startswith("ZONA ").all())
        self.assertTrue(clean.ZONA_CAPITAL.ne("").all())
        self.assertTrue(validar(sample, clean, ROOT)["aprobada"])

    def test_distrito_incompleto_no_se_completa(self):
        raw = cargar(ROOT).iloc[:1].copy().reset_index(drop=True)
        raw.loc[0, "DISTRITO"] = "01-"
        clean, audit = limpiar(raw, ROOT)
        self.assertEqual(clean.loc[0, "DISTRITO"], "")
        self.assertEqual(clean.loc[0, "DISTRITO_ORIGINAL"], "01-")
        self.assertEqual(clean.loc[0, "ESTADO_DISTRITO"], "INCOMPLETO")

    def test_similitud_no_elimina_jornadas_distintas(self):
        df = pd.DataFrame([
            {"CODIGO": "01-01-0001-46", "CODIGO_MUNICIPIO": "0101", "ESTABLECIMIENTO": "COLEGIO CENTRAL", "DIRECCION": "ZONA 1", "TELEFONO": "22201723", "JORNADA": "MATUTINA", "PLAN": "DIARIO(REGULAR)"},
            {"CODIGO": "01-01-0002-46", "CODIGO_MUNICIPIO": "0101", "ESTABLECIMIENTO": "COLEGIO CENTRAL", "DIRECCION": "ZONA 1", "TELEFONO": "22201723", "JORNADA": "VESPERTINA", "PLAN": "DIARIO(REGULAR)"},
        ], dtype="string")
        result = detectar(df)
        self.assertEqual(len(df), 2)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0].decision, "CONSERVAR_SERVICIOS_DISTINTOS")


if __name__ == "__main__":
    unittest.main()
