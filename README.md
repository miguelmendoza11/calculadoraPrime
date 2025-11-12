# 📊 Calculadora de Cálculo Multivariable

Una aplicación web interactiva desarrollada con Streamlit para realizar cálculos avanzados, visualizaciones 3D y análisis de funciones multivariables. Herramienta educativa completa para estudiantes y profesores de cálculo.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Tabla de Contenidos

- [Características](#características)
- [Instalación](#instalación)
- [Uso](#uso)
- [Ejemplos de Funciones](#ejemplos-de-funciones)
- [Sintaxis de Funciones](#sintaxis-de-funciones)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Contribuciones](#contribuciones)
- [Autor](#autor)
- [Licencia](#licencia)

## ✨ Características

### 📈 Visualización de Superficies
- Visualización 3D interactiva de funciones de dos variables
- Curvas de nivel con múltiples resoluciones (20-200 puntos)
- Gráficos interactivos con Plotly (zoom, rotación, exportación)
- Estadísticas automáticas: mínimo, máximo, media y desviación estándar
- Análisis visual combinado (superficie 3D + curvas de nivel)
- Análisis automático del dominio de la función

### 🔍 Dominio, Rango y Límites
- **Cálculo automático del dominio** con identificación de restricciones
- **Cálculo numérico del rango** en regiones personalizables
- **Evaluación de límites** en puntos específicos
- Verificación de límites por diferentes caminos:
  - Camino y = 0
  - Camino x = 0
  - Camino y = x
- Análisis de continuidad y existencia de límites

### ∂ Derivadas Parciales y Gradientes
- Cálculo simbólico de derivadas parciales de primer orden
- Derivadas parciales de segundo orden (f_xx, f_yy, f_xy, f_yx)
- Verificación del teorema de Schwarz (Clairaut)
- **Campo vectorial del gradiente**:
  - Visualización con triángulos direccionales
  - Mapa de calor por magnitud (verde→naranja→rojo)
  - Densidad de vectores configurable
  - Escala de triángulos ajustable
- Evaluación del gradiente en puntos específicos
- Cálculo de magnitud y dirección unitaria
- Identificación de puntos críticos (∇f = 0)
- Visualización integrada con curvas de nivel

### 🎯 Optimización con Restricciones
- Método de multiplicadores de Lagrange
- Resolución simbólica del sistema de ecuaciones
- Identificación automática de puntos críticos
- Clasificación de máximos y mínimos locales
- Optimización numérica con SLSQP como respaldo
- Visualización interactiva:
  - Curvas de nivel de la función objetivo
  - Gráfica de la restricción g(x,y) = 0
  - Marcadores de puntos críticos
  - Identificación del óptimo global
- Cálculo del valor de λ (multiplicador de Lagrange)

### ∫ Integración Doble y Triple
- **Integración doble**:
  - Método simbólico (exacto) con SymPy
  - Método numérico (aproximado) con SciPy
  - Proceso de integración paso a paso
  - Visualización 3D del volumen bajo la superficie
  - Estimación de error en método numérico
- **Integración triple**:
  - Cálculo simbólico y numérico de volúmenes en 3D
  - Integración iterada en tres variables
  - Interpretación geométrica de la región
  - Estimación de error numérico
- Límites de integración personalizables (constantes o funciones)

## 🚀 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Conexión a internet (para la primera instalación)

### Pasos de Instalación

1. **Clona este repositorio**:
```bash
git clone https://github.com/miguelmendoza11/calculadoraPrime.git
cd calculadoraPrime
```

2. **Crea un entorno virtual (recomendado)**:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Instala las dependencias**:
```bash
pip install -r requirements.txt
```

## 💻 Uso

### Iniciar la Aplicación

Ejecuta la aplicación con el siguiente comando:
```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

### Navegación

Utiliza el **menú lateral** (sidebar) para navegar entre las diferentes funcionalidades:

1. **🏠 Inicio** - Presentación y guía de uso
2. **📈 Visualización de Superficies** - Gráficos 3D y curvas de nivel
3. **🔍 Dominio, Rango y Límites** - Análisis de dominio y límites
4. **∂ Derivadas Parciales y Gradientes** - Cálculo de derivadas y campos vectoriales
5. **🎯 Optimización con Restricciones** - Multiplicadores de Lagrange
6. **∫ Integración Doble y Triple** - Cálculo de integrales múltiples

### Consejos de Uso

- Usa la **sintaxis de Python/SymPy** para ingresar funciones
- Los gráficos son **interactivos**: puedes hacer zoom, rotar y desplazar
- Ajusta la **resolución** para mejorar la calidad (mayor número = mayor detalle)
- Experimenta con diferentes **rangos** para visualizar mejor las funciones
- Los **tooltips** (?) proporcionan ayuda contextual en cada campo

## 📝 Ejemplos de Funciones

### Funciones de Dos Variables
```python
# Paraboloide circular
x**2 + y**2

# Silla de montar (paraboloide hiperbólico)
x**2 - y**2

# Campana gaussiana
exp(-(x**2 + y**2))

# Función trigonométrica
sin(x)*cos(y)

# Onda sinusoidal
sin(sqrt(x**2 + y**2))

# Hemisferio
sqrt(9 - x**2 - y**2)

# Cono
sqrt(x**2 + y**2)

# Función racional
1/(1 + x**2 + y**2)

# Plano inclinado
x + 2*y + 3
```

### Funciones de Tres Variables (para integración triple)
```python
# Volumen simple
x*y*z

# Densidad variable
1 + x + y + z

# Esfera con densidad
x**2 + y**2 + z**2

# Función exponencial
exp(-(x**2 + y**2 + z**2))
```

### Restricciones para Optimización
```python
# Restricción lineal (plano)
x + y - 1

# Restricción circular
x**2 + y**2 - 4

# Restricción hiperbólica
x*y - 1

# Restricción elíptica
x**2/4 + y**2/9 - 1

# Restricción parabólica
y - x**2
```

## 🔧 Sintaxis de Funciones

### Operadores Matemáticos Básicos

| Operación | Sintaxis | Ejemplo | Resultado |
|-----------|----------|---------|-----------|
| Suma | `+` | `x + y` | x + y |
| Resta | `-` | `x - y` | x - y |
| Multiplicación | `*` | `2*x` o `x*y` | 2x o xy |
| División | `/` | `x/y` | x/y |
| Potencia | `**` | `x**2` | x² |
| Paréntesis | `()` | `(x+y)**2` | (x+y)² |

### Funciones Matemáticas Disponibles

#### Trigonométricas
```python
sin(x)      # Seno
cos(x)      # Coseno
tan(x)      # Tangente
asin(x)     # Arcoseno
acos(x)     # Arcocoseno
atan(x)     # Arcotangente
```

#### Exponenciales y Logarítmicas
```python
exp(x)      # e^x
log(x)      # Logaritmo natural (ln)
log10(x)    # Logaritmo base 10
sqrt(x)     # Raíz cuadrada (√x)
```

#### Otras Funciones
```python
abs(x)      # Valor absoluto |x|
floor(x)    # Piso ⌊x⌋
ceil(x)     # Techo ⌈x⌉
```

### Constantes Matemáticas
```python
pi          # π ≈ 3.14159265359
E           # e ≈ 2.71828182846
```

### Ejemplos de Sintaxis Correcta

✅ **Correcto:**
```python
x**2 + y**2
sin(x)*cos(y)
exp(x*y)
sqrt(x**2 + y**2)
log(abs(x*y))
```

❌ **Incorrecto:**
```python
x^2 + y^2          # Usar ** en lugar de ^
sen(x)*cos(y)      # Usar sin en lugar de sen
e^(x*y)            # Usar exp() en lugar de e^
√(x**2 + y**2)     # Usar sqrt() en lugar de √
```

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Streamlit** | 1.28+ | Framework para crear interfaces web interactivas |
| **NumPy** | 1.24+ | Cálculos numéricos eficientes con arrays |
| **SymPy** | 1.12+ | Matemáticas simbólicas, álgebra y cálculo |
| **Plotly** | 5.18+ | Visualizaciones 3D interactivas y gráficos |
| **SciPy** | 1.11+ | Optimización numérica e integración |

### Instalación Individual

Si necesitas instalar las dependencias individualmente:
```bash
pip install streamlit>=1.28.0
pip install numpy>=1.24.0
pip install sympy>=1.12
pip install plotly>=5.18.0
pip install scipy>=1.11.0
```

## 📦 Estructura del Proyecto
```
calculadoraPrime/
│
├── app.py                 # Aplicación principal de Streamlit
├── requirements.txt       # Dependencias del proyecto
├── README.md             # Este archivo (documentación)
│
└── (estructura futura)
    ├── utils/            # Funciones auxiliares
    │   ├── calculus.py   # Funciones de cálculo
    │   └── plotting.py   # Funciones de visualización
    ├── assets/           # Recursos estáticos
    │   └── logo.png      # Logo de la aplicación
    └── tests/            # Pruebas unitarias
        └── test_app.py   # Tests de la aplicación
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas y muy apreciadas. Para contribuir al proyecto:

### Proceso de Contribución

1. **Fork** el proyecto
2. Crea una **rama** para tu feature:
```bash
   git checkout -b feature/NuevaFuncionalidad
```
3. **Commit** tus cambios:
```bash
   git commit -m 'Add: nueva funcionalidad de análisis'
```
4. **Push** a la rama:
```bash
   git push origin feature/NuevaFuncionalidad
```
5. Abre un **Pull Request**

### Áreas de Mejora Sugeridas

- [ ] Añadir más ejemplos predefinidos y plantillas
- [ ] Implementar exportación de resultados a PDF/LaTeX
- [ ] Agregar animaciones de funciones paramétricas
- [ ] Soporte para coordenadas cilíndricas y esféricas
- [ ] Modo oscuro para la interfaz
- [ ] Integración con Jupyter Notebooks
- [ ] Sistema de guardado de sesiones
- [ ] Galería de funciones comunes
- [ ] Tutorial interactivo paso a paso
- [ ] Soporte multiidioma (inglés, portugués)

### Reportar Problemas

Si encuentras un bug o tienes una sugerencia:

1. Verifica que no exista un [Issue](https://github.com/miguelmendoza11/calculadoraPrime/issues) similar
2. Abre un nuevo Issue con:
   - Descripción clara del problema
   - Pasos para reproducirlo
   - Comportamiento esperado vs. comportamiento actual
   - Capturas de pantalla (si aplica)


</div>
