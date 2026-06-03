"""Módulo de modelado no supervisado para perfiles criminales estatales."""

from __future__ import annotations

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from src import config


class CrimeClusteringPipeline:
    """Pipeline para procesar y agrupar entidades por Bien Jurídico Afectado.

    Encapsula el pivoteo de datos a nivel macro (7 categorías), la 
    estandarización con StandardScaler, el cálculo de métricas de agrupación
    y la reducción con PCA (2D) exclusivamente para la visualización del scatter plot.
    """

    def __init__(self) -> None:
        self.scaler = StandardScaler()
        # Fijamos a 2 componentes porque solo lo usaremos para proyectar la gráfica final en 2D
        self.pca = PCA(n_components=2, random_state=config.SEED)
        
        self.features_names: list[str] = []
        self.states_names: list[str] = []
        self.X_scaled: np.ndarray | None = None
        self.X_pca: np.ndarray | None = None
        self._model: KMeans | None = None

    def prepare_matrix(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transforma el dataset plano en una matriz de proporciones por Bien Jurídico.
        
        Agrupa el volumen delictivo en las 7 categorías principales y las normaliza
        en porcentajes de participación por entidad federativa para mitigar el sesgo poblacional.
        """
        # Cambiamos el pivoteo para agrupar por los Bienes Jurídicos Afectados (7 columnas)
        matrix = df.groupby(["entidad", "bien_juridico_afectado"])["incidencia_delictiva"].sum().unstack(fill_value=0)
        
        self.states_names = list(matrix.index)
        self.features_names = list(matrix.columns)
        
        # Convertir a proporciones (porcentaje de cada macro-delito sobre el total del estado)
        row_totals = matrix.sum(axis=1) + 1e-9
        matrix_pct = matrix.div(row_totals, axis=0)
        
        return matrix_pct

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preprocesa la matriz: pivotea por bien jurídico y estandariza las variables.
        
        Retorna la matriz escalada original de 7 dimensiones lista para entrenar KMeans.
        """
        # Crear matriz de proporciones (32 estados x 7 bienes jurídicos)
        matrix_pct = self.prepare_matrix(df)
        
        # Estandarizar las columnas (Media=0, Varianza=1)
        self.X_scaled = self.scaler.fit_transform(matrix_pct)
        
        # Calculamos el PCA de forma anticipada para tener listas las coordenadas de visualización
        self.X_pca = self.pca.fit_transform(self.X_scaled)
        
        print(f"[Clustering] Matriz macro preparada con {matrix_pct.shape[0]} estados y {matrix_pct.shape[1]} variables (Bienes Jurídicos).")
        print(f"[Clustering] El plano visual (PCA 2D) captura el {sum(self.pca.explained_variance_ratio_)*100:.2f}% de la varianza total de estas categorías.")
        
        return matrix_pct

    def evaluate_k_options(self, max_k: int = 10) -> dict[str, list[float]]:
        """Calcula la Inercia y la Silueta evaluando en el espacio real de 7 dimensiones.
        
        Garantiza que el agrupamiento se calcule con los datos puros sin perder información.
        """
        if self.X_scaled is None:
            raise RuntimeError("Primero debes ejecutar `fit_transform()` sobre los datos.")
            
        inertias = []
        silhouettes = []
        k_values = list(range(2, max_k + 1))
        
        for k in k_values:
            km = KMeans(n_clusters=k, random_state=config.SEED, n_init=10)
            # Entrenamos en la matriz escalada real (las 7 dimensiones)
            labels = km.fit_predict(self.X_scaled)
            
            inertias.append(km.inertia_)
            silhouettes.append(silhouette_score(self.X_scaled, labels))
            
        return {"k": k_values, "inertia": inertias, "silhouette": silhouettes}

    def fit_final_model(self, n_clusters: int) -> pd.DataFrame:
        """Entrena el KMeans definitivo en el espacio de 7D y mapea los resultados a las coordenadas PCA."""
        if self.X_scaled is None or self.X_pca is None:
            raise RuntimeError("Primero debes ejecutar `fit_transform()` sobre los datos.")
            
        # El modelo agrupa usando las 7 variables reales
        self._model = KMeans(n_clusters=n_clusters, random_state=config.SEED, n_init=10)
        labels = self._model.fit_predict(self.X_scaled)
        
        # Mapeamos a un DataFrame que incluye las coordenadas 2D del PCA para el scatter plot
        results = pd.DataFrame({
            "entidad": self.states_names,
            "pca_1": self.X_pca[:, 0],
            "pca_2": self.X_pca[:, 1],
            "cluster": labels
        })
        
        return results