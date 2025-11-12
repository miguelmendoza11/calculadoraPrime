"""
Calculadora de Cálculo Multivariable
Desarrollado con Streamlit, NumPy, SymPy, Plotly, y SciPy
Versión con interfaz mejorada
"""

import streamlit as st
import numpy as np
import sympy as sp
from sympy import symbols, sympify, lambdify, diff, latex, limit, oo
from sympy.vector import gradient, CoordSys3D
import plotly.graph_objects as go
import plotly.express as px
from scipy import optimize, integrate
from scipy.optimize import minimize
import warnings
warnings.filterwarnings('ignore')

# Configuración de la página
st.set_page_config(
    page_title="Calculadora de Cálculo Multivariable",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"  # Sidebar siempre visible
)

# ============================================================================
# ESTILOS CSS PERSONALIZADOS
# ============================================================================

def aplicar_estilos():
    st.markdown("""
    <style>
    :root {
        --ucc-blue: #00a5b5;
        --ucc-green: #84bd00;
        --gray-100: #f7fafc;
        --gray-200: #edf2f7;
        --gray-300: #e2e8f0;
        --gray-400: #cbd5e0;
        --gray-500: #a0aec0;
        --gray-600: #718096;
        --gray-700: #4a5568;
        --gray-800: #2d3748;
        --gray-900: #1a202c;
    }

    /* Estilos generales */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Título principal */
    .main-title {
        background: linear-gradient(135deg, #00a5b5 0%, #84bd00 100%);
        color: white;
        padding: 2rem;
        border-radius: 0.5rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        margin-bottom: 2rem;
    }

    .main-title h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }

    /* Cards educativos */
    .educational-card {
        background-color: white;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        overflow: hidden;
        margin-bottom: 2rem;
        border: 2px solid #e2e8f0;
    }

    .educational-card-header {
        background: linear-gradient(135deg, #00a5b5 0%, #0095a3 100%);
        color: white;
        padding: 1.5rem;
        border-bottom: 3px solid #84bd00;
    }

    .educational-card-header h2 {
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0;
    }

    /* Info panels */
    .info-panel {
        background-color: #f7fafc;
        border-left: 4px solid #00a5b5;
        border-radius: 0.375rem;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
    }

    .info-panel.success {
        border-left-color: #84bd00;
        background-color: #f0fdf4;
    }

    .info-panel.warning {
        border-left-color: #f97316;
        background-color: #fffbeb;
    }

    /* Botones personalizados */
    .stButton > button {
        background: linear-gradient(135deg, #00a5b5 0%, #0095a3 100%);
        color: white;
        border: none;
        border-radius: 0.375rem;
        padding: 0.75rem 2rem;
        font-weight: 600;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #0095a3 0%, #00848f 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }

    /* Stats cards */
    .stat-card {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 0.5rem;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s;
    }

    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    .stat-label {
        color: #718096;
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }

    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00a5b5 0%, #84bd00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    /* Feature cards */
    .feature-card {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 0.5rem;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s;
        height: 100%;
    }

    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 16px rgba(0, 165, 181, 0.15);
        border-color: #00a5b5;
    }

    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }

    .feature-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }

    .feature-description {
        color: #718096;
        font-size: 0.9rem;
        line-height: 1.6;
    }

    /* Sidebar personalizado */
    .css-1d391kg {
        background: linear-gradient(180deg, #f7fafc 0%, #edf2f7 100%);
    }

    /* Métricas de Streamlit */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #00a5b5;
        font-weight: 700;
    }

    /* Tabs personalizados */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #f7fafc;
        border-radius: 0.375rem 0.375rem 0 0;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00a5b5 0%, #0095a3 100%);
        color: white;
    }

    /* Input fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border: 2px solid #e2e8f0;
        border-radius: 0.375rem;
        padding: 0.75rem;
        transition: border-color 0.3s;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #00a5b5;
        box-shadow: 0 0 0 3px rgba(0, 165, 181, 0.1);
    }

    /* Expander personalizado */
    .streamlit-expanderHeader {
        background-color: #f7fafc;
        border-radius: 0.375rem;
        font-weight: 600;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
        color: white;
        border-radius: 0.5rem;
        margin-top: 3rem;
    }

    /* Selectbox personalizado */
    .stSelectbox > div > div {
        border: 2px solid #e2e8f0;
        border-radius: 0.375rem;
    }

    /* Radio buttons */
    .stRadio > div {
        background-color: #f7fafc;
        padding: 1rem;
        border-radius: 0.375rem;
    }

    /* Sidebar fijo y mejorado */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f7fafc 0%, #edf2f7 100%);
        border-right: 2px solid #e2e8f0;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, #f7fafc 0%, #edf2f7 100%);
    }
    
    /* Forzar sidebar siempre visible - IMPORTANTE */
    section[data-testid="stSidebar"] {
        display: block !important;
        visibility: visible !important;
        width: 21rem !important;
        min-width: 21rem !important;
    }
    
    /* Ocultar botón de colapsar sidebar */
    button[kind="header"] {
        display: none !important;
    }
    
    /* Ajustar contenido principal para sidebar fijo */
    .main .block-container {
        padding-left: 1rem;
    }
    
    /* Mejorar selectbox en sidebar */
    [data-testid="stSidebar"] .stSelectbox > label {
        font-weight: 600;
        color: #2d3748;
        font-size: 1rem;
    }
    
    /* Slider personalizado */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #00a5b5 0%, #84bd00 100%);
    }

    /* Help section */
    .help-section {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin-top: 2rem;
        border: 2px solid #e2e8f0;
    }

    .help-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    </style>
    """, unsafe_allow_html=True)

aplicar_estilos()

# Variables simbólicas
x, y, z, t = symbols('x y z t', real=True)

# Diccionario de símbolos para sympify (IMPORTANTE para que reconozca las variables)
simbolos = {'x': x, 'y': y, 'z': z, 't': t,
            'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
            'exp': sp.exp, 'log': sp.log, 'sqrt': sp.sqrt,
            'pi': sp.pi, 'e': sp.E}

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def evaluar_funcion_segura(funcion_str, x_val, y_val):
    """Evalúa una función de manera segura con manejo de errores"""
    try:
        expr = sympify(funcion_str, locals=simbolos)
        f = lambdify((x, y), expr, 'numpy')
        resultado = f(x_val, y_val)
        resultado = np.where(np.isfinite(resultado), resultado, np.nan)
        return resultado
    except Exception as e:
        st.error(f"Error al evaluar la función: {str(e)}")
        return None

def calcular_dominio(funcion_str):
    """Analiza y describe el dominio de una función"""
    try:
        expr = sympify(funcion_str, locals=simbolos)
        dominio_info = []

        if expr.as_numer_denom()[1] != 1:
            denom = expr.as_numer_denom()[1]
            dominio_info.append(f"El denominador no puede ser cero: {latex(denom)} ≠ 0")

        for arg in expr.atoms(sp.Pow):
            if arg.exp == sp.Rational(1, 2) or (arg.exp.is_rational and arg.exp < 1 and arg.exp > 0):
                dominio_info.append(f"Debe cumplirse: {latex(arg.base)} ≥ 0")

        for arg in expr.atoms(sp.log):
            dominio_info.append(f"Debe cumplirse: {latex(arg.args[0])} > 0")

        if not dominio_info:
            dominio_info.append("El dominio es todo ℝ²")

        return dominio_info
    except Exception as e:
        return [f"Error al calcular dominio: {str(e)}"]

def calcular_rango_numerico(funcion_str, x_range, y_range, n_points=100):
    """Calcula el rango numérico de una función"""
    try:
        x_vals = np.linspace(x_range[0], x_range[1], n_points)
        y_vals = np.linspace(y_range[0], y_range[1], n_points)
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = evaluar_funcion_segura(funcion_str, X, Y)

        if Z is not None:
            z_valid = Z[np.isfinite(Z)]
            if len(z_valid) > 0:
                return f"Rango aproximado: [{np.min(z_valid):.4f}, {np.max(z_valid):.4f}]"
        return "No se pudo calcular el rango"
    except Exception as e:
        return f"Error: {str(e)}"

# ============================================================================
# TÍTULO PRINCIPAL CON DISEÑO MEJORADO
# ============================================================================

st.markdown("""
<div class="main-title">
    <h1>📊 Calculadora de Cálculo Multivariable</h1>
    <p style="margin-top: 0.5rem; font-size: 1.1rem; opacity: 0.95;">
        Herramienta interactiva para visualización y análisis matemático
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# MENÚ LATERAL MEJORADO
# ============================================================================

st.sidebar.image("https://via.placeholder.com/300x100/00a5b5/ffffff?text=UCC+Matemáticas", use_container_width=True)
st.sidebar.markdown("---")

menu = st.sidebar.selectbox(
    "🎯 Selecciona una funcionalidad:",
    [
        "🏠 Inicio",
        "📈 Visualización de Superficies",
        "🔍 Dominio, Rango y Límites",
        "∂ Derivadas Parciales y Gradientes",
        "🎯 Optimización con Restricciones",
        "∫ Integración Doble y Triple"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 💡 Ayuda Rápida
- **Sintaxis**: Usa notación Python/SymPy
- **Ejemplos**: `x**2 + y**2`, `sin(x)*cos(y)`
- **Funciones**: `exp()`, `log()`, `sqrt()`
""")

# ============================================================================
# PÁGINA DE INICIO
# ============================================================================

if menu == "🏠 Inicio":
    st.markdown("""
    <div class="educational-card">
        <div class="educational-card-header">
            <h2>🎓 Bienvenido a la Calculadora de Cálculo Multivariable</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    Esta aplicación te permite realizar diversos cálculos y visualizaciones relacionadas con
    el cálculo multivariable. Una herramienta completa para estudiantes y profesores.
    """)

    # Grid de características
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <div class="feature-title">Visualización 3D</div>
            <div class="feature-description">
                Gráficos interactivos de superficies y curvas de nivel con alta resolución
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">∂</div>
            <div class="feature-title">Derivadas Parciales</div>
            <div class="feature-description">
                Cálculo automático de gradientes y derivadas de cualquier orden
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Optimización</div>
            <div class="feature-description">
                Método de Lagrange y optimización con restricciones de igualdad
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">Análisis de Dominio</div>
            <div class="feature-description">
                Determinación automática de dominio y rango de funciones
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">∫</div>
            <div class="feature-title">Integración Múltiple</div>
            <div class="feature-description">
                Integración doble y triple con métodos simbólicos y numéricos
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Estadísticas</div>
            <div class="feature-description">
                Análisis estadístico detallado de las funciones evaluadas
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Panel informativo
    st.markdown("""
    <div class="info-panel success">
        <div class="info-title">💡 Consejo de uso</div>
        <div class="info-text">
            Utiliza sintaxis de Python/SymPy para las funciones. Por ejemplo: <code>x**2 + y**2</code>, 
            <code>sin(x)*cos(y)</code>, <code>exp(x*y)</code>. La aplicación soporta todas las funciones 
            matemáticas estándar.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sección de ayuda
    st.markdown("""
    <div class="help-section">
        <div class="help-title">📚 Funciones Disponibles</div>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1rem;">
            <div>
                <strong>Trigonométricas:</strong><br>
                sin, cos, tan, asin, acos, atan
            </div>
            <div>
                <strong>Exponenciales:</strong><br>
                exp, log, ln, log10, sqrt
            </div>
            <div>
                <strong>Otros:</strong><br>
                abs, floor, ceil, factorial
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# VISUALIZACIÓN DE SUPERFICIES
# ============================================================================

elif menu == "📈 Visualización de Superficies":
    st.markdown("""
    <div class="educational-card">
        <div class="educational-card-header">
            <h2>📈 Visualización de Funciones de Dos Variables</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### ⚙️ Configuración")
        funcion_input = st.text_input(
            "Ingresa la función f(x, y):",
            value="x**2 + y**2",
            help="Ejemplos: x**2 + y**2, sin(x)*cos(y), exp(-(x**2 + y**2))"
        )

        x_min = st.number_input("x mínimo:", value=-5.0, step=0.5)
        x_max = st.number_input("x máximo:", value=5.0, step=0.5)
        y_min = st.number_input("y mínimo:", value=-5.0, step=0.5)
        y_max = st.number_input("y máximo:", value=5.0, step=0.5)

        n_points = st.slider("Resolución:", min_value=20, max_value=200, value=50)

        tipo_grafico = st.radio(
            "Tipo de gráfico:",
            ["Superficie 3D", "Curvas de Nivel", "Ambos"]
        )

    with col2:
        st.markdown("### 📋 Información de la Función")
        try:
            expr = sympify(funcion_input, locals=simbolos)
            st.latex(f"f(x, y) = {latex(expr)}")

            st.markdown("""
            <div class="info-panel">
                <div class="info-title">🔍 Análisis del Dominio</div>
            </div>
            """, unsafe_allow_html=True)
            
            dominio_info = calcular_dominio(funcion_input)
            for info in dominio_info:
                st.write(f"• {info}")
        except Exception as e:
            st.error(f"Error al procesar la función: {str(e)}")

    if st.button("🎨 Generar Visualización", type="primary"):
        try:
            x_vals = np.linspace(x_min, x_max, n_points)
            y_vals = np.linspace(y_min, y_max, n_points)
            X, Y = np.meshgrid(x_vals, y_vals)
            Z = evaluar_funcion_segura(funcion_input, X, Y)

            if Z is not None:
                if tipo_grafico in ["Superficie 3D", "Ambos"]:
                    st.markdown("### 🎨 Superficie 3D")
                    fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='Viridis')])
                    fig.update_layout(
                        scene=dict(
                            xaxis_title='x',
                            yaxis_title='y',
                            zaxis_title='f(x, y)',
                            camera=dict(eye=dict(x=1.5, y=1.5, z=1.3))
                        ),
                        width=700,
                        height=600,
                        title=f"Superficie: f(x, y) = {funcion_input}"
                    )
                    st.plotly_chart(fig, use_container_width=True)

                if tipo_grafico in ["Curvas de Nivel", "Ambos"]:
                    st.markdown("### 🗺️ Curvas de Nivel")
                    fig = go.Figure(data=[go.Contour(x=x_vals, y=y_vals, z=Z, colorscale='Viridis')])
                    fig.update_layout(
                        xaxis_title='x',
                        yaxis_title='y',
                        width=700,
                        height=600,
                        title=f"Curvas de nivel: f(x, y) = {funcion_input}"
                    )
                    st.plotly_chart(fig, use_container_width=True)

                # Estadísticas
                st.markdown("### 📊 Estadísticas de la Función")
                z_valid = Z[np.isfinite(Z)]
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-label">Mínimo</div>
                        <div class="stat-value">{np.min(z_valid):.4f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-label">Máximo</div>
                        <div class="stat-value">{np.max(z_valid):.4f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-label">Media</div>
                        <div class="stat-value">{np.mean(z_valid):.4f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-label">Desv. Est.</div>
                        <div class="stat-value">{np.std(z_valid):.4f}</div>
                    </div>
                    """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error al generar la visualización: {str(e)}")

# ============================================================================
# DOMINIO, RANGO Y LÍMITES
# ============================================================================

elif menu == "🔍 Dominio, Rango y Límites":
    st.markdown("""
    <div class="educational-card">
        <div class="educational-card-header">
            <h2>🔍 Análisis de Dominio, Rango y Límites</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

    funcion_input = st.text_input(
        "Ingresa la función f(x, y):",
        value="sqrt(9 - x**2 - y**2)",
        help="Ejemplos: sqrt(x), 1/(x-y), log(x*y)"
    )

    try:
        expr = sympify(funcion_input, locals=simbolos)
        st.latex(f"f(x, y) = {latex(expr)}")
    except:
        st.error("Error al procesar la función")

    tab1, tab2, tab3 = st.tabs(["📐 Dominio", "📊 Rango", "🎯 Límites"])

    with tab1:
        st.markdown("### 📐 Análisis del Dominio")
        if st.button("🔍 Calcular Dominio", key="btn_dominio"):
            dominio_info = calcular_dominio(funcion_input)
            st.markdown("""
            <div class="info-panel success">
                <div class="info-title">Restricciones del dominio:</div>
            </div>
            """, unsafe_allow_html=True)
            for info in dominio_info:
                st.write(f"• {info}")

    with tab2:
        st.markdown("### 📊 Cálculo del Rango")
        col1, col2 = st.columns(2)
        with col1:
            x_min_r = st.number_input("x mínimo:", value=-3.0, step=0.5, key="x_min_rango")
            x_max_r = st.number_input("x máximo:", value=3.0, step=0.5, key="x_max_rango")
        with col2:
            y_min_r = st.number_input("y mínimo:", value=-3.0, step=0.5, key="y_min_rango")
            y_max_r = st.number_input("y máximo:", value=3.0, step=0.5, key="y_max_rango")

        if st.button("📊 Calcular Rango Numérico", key="btn_rango"):
            rango = calcular_rango_numerico(funcion_input, [x_min_r, x_max_r], [y_min_r, y_max_r])
            st.markdown(f"""
            <div class="info-panel success">
                <div class="info-title">{rango}</div>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.markdown("### 🎯 Evaluación de Límites")
        st.info("Evalúa límites cuando (x, y) → (a, b)")

        col1, col2 = st.columns(2)
        with col1:
            a = st.number_input("Valor de a:", value=0.0, step=0.1)
        with col2:
            b = st.number_input("Valor de b:", value=0.0, step=0.1)

        if st.button("🎯 Calcular Límite", key="btn_limite"):
            try:
                expr = sympify(funcion_input, locals=simbolos)
                limite_x = limit(expr, x, a)
                limite_final = limit(limite_x, y, b)

                st.markdown(f"""
                <div class="info-panel success">
                    <div class="info-title">Límite cuando (x, y) → ({a}, {b})</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.latex(f"\\lim_{{(x,y) \\to ({a},{b})}} {latex(expr)} = {latex(limite_final)}")

                st.markdown("**📍 Verificación por diferentes caminos:**")

                # Camino 1: y = 0, x → a
                try:
                    expr_y0 = expr.subs(y, 0)
                    lim_camino1 = limit(expr_y0, x, a)
                    st.write(f"• Camino y = 0: {latex(lim_camino1)}")
                except:
                    st.write("• Camino y = 0: No evaluable")

                # Camino 2: x = 0, y → b
                try:
                    expr_x0 = expr.subs(x, 0)
                    lim_camino2 = limit(expr_x0, y, b)
                    st.write(f"• Camino x = 0: {latex(lim_camino2)}")
                except:
                    st.write("• Camino x = 0: No evaluable")

                # Camino 3: y = x
                try:
                    expr_yx = expr.subs(y, x)
                    lim_camino3 = limit(expr_yx, x, a)
                    st.write(f"• Camino y = x: {latex(lim_camino3)}")
                except:
                    st.write("• Camino y = x: No evaluable")

            except Exception as e:
                st.error(f"Error al calcular el límite: {str(e)}")

# ============================================================================
# DERIVADAS PARCIALES Y GRADIENTES
# ============================================================================

elif menu == "∂ Derivadas Parciales y Gradientes":
    st.markdown("""
    <div class="educational-card">
        <div class="educational-card-header">
            <h2>∂ Derivadas Parciales y Gradientes</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

    funcion_input = st.text_input(
        "Ingresa la función f(x, y):",
        value="x**2*y + y**3",
        help="Ejemplos: x**2 + y**2, x*exp(y), sin(x)*cos(y)"
    )

    # Intentar parsear la función
    expr = None
    try:
        expr = sympify(funcion_input, locals=simbolos)
        st.markdown("### 📝 Función Ingresada")
        st.latex(f"f(x, y) = {latex(expr)}")
    except Exception as e:
        st.error(f"❌ Error al procesar la función: {str(e)}")
        st.info("💡 Asegúrate de usar sintaxis correcta. Ejemplos: `x**2 + y**2`, `sin(x)*cos(y)`, `exp(x*y)`")

    # Si la función se parseó correctamente, calcular derivadas
    if expr is not None:
        try:
            # Calcular derivadas parciales de primer orden
            st.markdown("### ∂ Derivadas Parciales de Primer Orden")
            
            with st.spinner("Calculando derivadas parciales..."):
                df_dx = diff(expr, x)
                df_dy = diff(expr, y)
            
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("""
                <div class="info-panel">
                    <div class="info-title">Derivada parcial respecto a x</div>
                </div>
                """, unsafe_allow_html=True)
                st.latex(f"\\frac{{\\partial f}}{{\\partial x}} = {latex(df_dx)}")

            with col2:
                st.markdown("""
                <div class="info-panel">
                    <div class="info-title">Derivada parcial respecto a y</div>
                </div>
                """, unsafe_allow_html=True)
                st.latex(f"\\frac{{\\partial f}}{{\\partial y}} = {latex(df_dy)}")

            # Derivadas de segundo orden
            st.markdown("### ∂² Derivadas Parciales de Segundo Orden")
            
            with st.spinner("Calculando derivadas de segundo orden..."):
                df_dxx = diff(df_dx, x)
                df_dyy = diff(df_dy, y)
                df_dxy = diff(df_dx, y)
                df_dyx = diff(df_dy, x)

            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("**f_xx (∂²f/∂x²)**")
                st.latex(f"{latex(df_dxx)}")
                
            with col2:
                st.markdown("**f_yy (∂²f/∂y²)**")
                st.latex(f"{latex(df_dyy)}")
                
            with col3:
                st.markdown("**f_xy (∂²f/∂x∂y)**")
                st.latex(f"{latex(df_dxy)}")
                
            with col4:
                st.markdown("**f_yx (∂²f/∂y∂x)**")
                st.latex(f"{latex(df_dyx)}")

            # Verificar teorema de Schwarz
            if df_dxy == df_dyx:
                st.success("✅ Se cumple el teorema de Schwarz (Clairaut): f_xy = f_yx")
            else:
                st.warning("⚠️ Las derivadas cruzadas son diferentes")

            # Evaluación en un punto
            st.markdown("---")
            st.markdown("### 📍 Evaluación del Gradiente en un Punto")
            
            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                x0 = st.number_input("Valor de x₀:", value=1.0, step=0.1, key="x0_grad")
            with col2:
                y0 = st.number_input("Valor de y₀:", value=1.0, step=0.1, key="y0_grad")
            with col3:
                st.write("")
                st.write("")
                calcular_grad = st.button("🔍 Calcular Gradiente", type="primary")

            if calcular_grad:
                try:
                    with st.spinner("Evaluando gradiente en el punto..."):
                        grad_x = float(df_dx.subs([(x, x0), (y, y0)]))
                        grad_y = float(df_dy.subs([(x, x0), (y, y0)]))
                        f_val = float(expr.subs([(x, x0), (y, y0)]))

                    st.markdown(f"""
                    <div class="info-panel success">
                        <div class="info-title">✅ Resultados en el punto ({x0}, {y0})</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("f(x₀, y₀)", f"{f_val:.6f}")
                    with col2:
                        st.metric("∂f/∂x", f"{grad_x:.6f}")
                    with col3:
                        st.metric("∂f/∂y", f"{grad_y:.6f}")

                    st.markdown("**Vector Gradiente:**")
                    st.latex(f"\\nabla f({x0}, {y0}) = \\left({grad_x:.6f}, {grad_y:.6f}\\right)")

                    magnitud = np.sqrt(grad_x**2 + grad_y**2)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.info(f"**📏 Magnitud del gradiente:** ||∇f|| = {magnitud:.6f}")
                    with col2:
                        if magnitud > 0:
                            direccion_x = grad_x / magnitud
                            direccion_y = grad_y / magnitud
                            st.info(f"**🧭 Dirección unitaria:** ({direccion_x:.6f}, {direccion_y:.6f})")
                        else:
                            st.info("**🧭 Punto crítico:** ∇f = 0")

                    # Visualización del gradiente
                    st.markdown("---")
                    st.markdown("### 🎨 Campo Vectorial del Gradiente")

                    with st.spinner("Generando campo vectorial..."):
                        # Parámetros del campo vectorial
                        col1, col2 = st.columns(2)
                        with col1:
                            densidad = st.slider("Densidad de vectores:", min_value=5, max_value=20, value=12, 
                                               help="Cantidad de vectores a mostrar")
                        with col2:
                            escala_vectores = st.slider("Escala de triángulos:", min_value=5, max_value=20, value=10, step=1,
                                                       help="Tamaño de los triángulos")
                        
                        # Crear malla de puntos para el campo vectorial
                        x_range_campo = np.linspace(x0 - 2, x0 + 2, densidad)
                        y_range_campo = np.linspace(y0 - 2, y0 + 2, densidad)
                        
                        # Crear superficie para curvas de nivel
                        x_range = np.linspace(x0 - 2, x0 + 2, 50)
                        y_range = np.linspace(y0 - 2, y0 + 2, 50)
                        X, Y = np.meshgrid(x_range, y_range)
                        Z = evaluar_funcion_segura(funcion_input, X, Y)

                        if Z is not None:
                            fig = go.Figure()

                            # Curvas de nivel
                            fig.add_trace(go.Contour(
                                x=x_range, y=y_range, z=Z,
                                colorscale='Viridis',
                                name='f(x,y)',
                                showscale=True,
                                contours=dict(showlabels=True),
                                opacity=0.8
                            ))

                            # Calcular y graficar campo vectorial del gradiente (SOLO TRIÁNGULOS)
                            vectores_x = []
                            vectores_y = []
                            angulos = []
                            magnitudes = []
                            
                            for xi in x_range_campo:
                                for yi in y_range_campo:
                                    try:
                                        # Calcular gradiente en cada punto
                                        gx = float(df_dx.subs([(x, xi), (y, yi)]))
                                        gy = float(df_dy.subs([(x, xi), (y, yi)]))
                                        mag = np.sqrt(gx**2 + gy**2)
                                        
                                        if np.isfinite(gx) and np.isfinite(gy) and mag > 0.01:
                                            vectores_x.append(xi)
                                            vectores_y.append(yi)
                                            # Calcular ángulo del gradiente
                                            angulo = np.degrees(np.arctan2(gy, gx))
                                            angulos.append(angulo)
                                            magnitudes.append(mag)
                                    except:
                                        continue
                            
                            # Dibujar solo triángulos (sin líneas)
                            if len(vectores_x) > 0:
                                # Normalizar colores por magnitud
                                max_mag = max(magnitudes) if magnitudes else 1
                                min_mag = min(magnitudes) if magnitudes else 0
                                
                                # Crear lista de colores basados en magnitud
                                colores = []
                                for mag in magnitudes:
                                    # Normalizar entre 0 y 1
                                    if max_mag > min_mag:
                                        intensity = (mag - min_mag) / (max_mag - min_mag)
                                    else:
                                        intensity = 0.5
                                    
                                    # Color de verde oscuro a rojo
                                    r = int(255 * intensity)
                                    g = int(150 * (1 - intensity))
                                    b = 50
                                    colores.append(f'rgb({r}, {g}, {b})')
                                
                                # Dibujar SOLO triángulos (puntas de flecha)
                                fig.add_trace(go.Scatter(
                                    x=vectores_x,
                                    y=vectores_y,
                                    mode='markers',
                                    marker=dict(
                                        size=escala_vectores,
                                        color=colores,
                                        symbol='arrow',
                                        angle=angulos,
                                        line=dict(width=1, color='white')
                                    ),
                                    name='∇f (gradiente)',
                                    hovertemplate='<b>Punto:</b> (%{x:.2f}, %{y:.2f})<br>' +
                                                '<b>Magnitud:</b> %{text:.3f}<extra></extra>',
                                    text=magnitudes
                                ))
                                
                                # Punto de evaluación principal (destacado)
                                fig.add_trace(go.Scatter(
                                    x=[x0], y=[y0],
                                    mode='markers+text',
                                    marker=dict(size=20, color='yellow', symbol='star',
                                              line=dict(color='black', width=2)),
                                    text=[f'  ({x0}, {y0})'],
                                    textposition='top right',
                                    textfont=dict(size=12, color='black', family='Arial Black'),
                                    name=f'Punto evaluado',
                                    hovertemplate=f'<b>Punto:</b> ({x0}, {y0})<br>' +
                                                f'<b>f =</b> {f_val:.4f}<br>' +
                                                f'<b>∇f =</b> ({grad_x:.4f}, {grad_y:.4f})<br>' +
                                                f'<b>||∇f|| =</b> {magnitud:.4f}<extra></extra>'
                                ))

                            fig.update_layout(
                                title="Campo Vectorial del Gradiente - Dirección de Máximo Crecimiento",
                                xaxis_title='x',
                                yaxis_title='y',
                                width=900,
                                height=800,
                                showlegend=True,
                                hovermode='closest',
                                plot_bgcolor='rgba(240,240,240,0.5)'
                            )

                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Información adicional
                            st.markdown("""
                            <div class="info-panel">
                                <div class="info-title">💡 Interpretación del Campo Vectorial</div>
                                <div class="info-text">
                                    • Cada <strong>triángulo</strong> representa la dirección del <strong>gradiente ∇f</strong> en ese punto<br>
                                    • La <strong>dirección</strong> del triángulo indica hacia dónde crece más rápido la función<br>
                                    • El <strong>color</strong> indica la magnitud del gradiente (verde→naranja→rojo = lento→rápido)<br>
                                    • Los triángulos son <strong>perpendiculares a las curvas de nivel</strong><br>
                                    • La estrella ⭐ amarilla es el punto de evaluación principal
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Estadísticas del campo
                            if magnitudes:
                                st.markdown("### 📊 Estadísticas del Campo")
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Magnitud Mínima", f"{min(magnitudes):.4f}")
                                with col2:
                                    st.metric("Magnitud Máxima", f"{max(magnitudes):.4f}")
                                with col3:
                                    st.metric("Magnitud Promedio", f"{np.mean(magnitudes):.4f}")

                except Exception as e:
                    st.error(f"❌ Error al evaluar el gradiente: {str(e)}")
                    st.exception(e)

        except Exception as e:
            st.error(f"❌ Error al calcular las derivadas: {str(e)}")
            st.exception(e)

# ============================================================================
# OPTIMIZACIÓN CON RESTRICCIONES
# ============================================================================

elif menu == "🎯 Optimización con Restricciones":
    st.markdown("""
    <div class="educational-card">
        <div class="educational-card-header">
            <h2>🎯 Optimización con Multiplicadores de Lagrange</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-panel">
        <div class="info-title">📚 Método de Lagrange</div>
        <div class="info-text">
            Resuelve problemas de optimización del tipo:<br>
            <strong>Optimizar:</strong> f(x, y)<br>
            <strong>Sujeto a:</strong> g(x, y) = 0
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 🎯 Función Objetivo")
        funcion_objetivo = st.text_input(
            "f(x, y) =",
            value="x**2 + y**2",
            help="Función a optimizar"
        )

        tipo_opt = st.radio("Tipo de optimización:", ["Minimizar", "Maximizar"])

    with col2:
        st.markdown("### 🔒 Restricción")
        restriccion = st.text_input(
            "g(x, y) = 0, donde g(x, y) =",
            value="x + y - 1",
            help="Restricción de igualdad (se igualará a cero)"
        )

    if st.button("🔍 Resolver con Multiplicadores de Lagrange", type="primary"):
        try:
            f = sympify(funcion_objetivo, locals=simbolos)
            g = sympify(restriccion, locals=simbolos)

            st.markdown("### 📋 Formulación del Problema")
            st.latex(f"{tipo_opt.lower()} \\quad f(x, y) = {latex(f)}")
            st.latex(f"\\text{{sujeto a}} \\quad g(x, y) = {latex(g)} = 0")

            lam = symbols('lambda', real=True)
            L = f - lam * g

            st.markdown("### ℒ Función de Lagrange")
            st.latex(f"\\mathcal{{L}}(x, y, \\lambda) = {latex(f)} - \\lambda ({latex(g)})")
            st.latex(f"\\mathcal{{L}} = {latex(L)}")

            dL_dx = diff(L, x)
            dL_dy = diff(L, y)
            dL_dlam = diff(L, lam)

            st.markdown("### 📐 Sistema de Ecuaciones")
            st.markdown("""
            <div class="info-panel">
                <div class="info-title">Derivadas parciales igualadas a cero</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.latex(f"\\frac{{\\partial \\mathcal{{L}}}}{{\\partial x}} = {latex(dL_dx)} = 0")
            st.latex(f"\\frac{{\\partial \\mathcal{{L}}}}{{\\partial y}} = {latex(dL_dy)} = 0")
            st.latex(f"\\frac{{\\partial \\mathcal{{L}}}}{{\\partial \\lambda}} = {latex(dL_dlam)} = 0")

            soluciones = sp.solve([dL_dx, dL_dy, dL_dlam], [x, y, lam])

            if soluciones:
                st.markdown("### ✅ Puntos Críticos")

                if isinstance(soluciones, dict):
                    soluciones = [soluciones]

                resultados = []
                for i, sol in enumerate(soluciones, 1):
                    try:
                        if isinstance(sol, dict):
                            x_val = complex(sol[x])
                            y_val = complex(sol[y])
                            lam_val = complex(sol[lam]) if lam in sol else 0
                        else:
                            x_val = complex(sol[0])
                            y_val = complex(sol[1])
                            lam_val = complex(sol[2]) if len(sol) > 2 else 0

                        if abs(x_val.imag) < 1e-10 and abs(y_val.imag) < 1e-10:
                            x_val = x_val.real
                            y_val = y_val.real
                            lam_val = lam_val.real

                            f_val = float(f.subs([(x, x_val), (y, y_val)]))

                            st.markdown(f"""
                            <div class="info-panel">
                                <div class="info-title">Punto {i}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("x", f"{x_val:.6f}")
                            with col2:
                                st.metric("y", f"{y_val:.6f}")
                            with col3:
                                st.metric("λ", f"{lam_val:.6f}")
                            with col4:
                                st.metric("f(x, y)", f"{f_val:.6f}")

                            resultados.append((x_val, y_val, f_val))
                    except:
                        continue

                if resultados:
                    if tipo_opt == "Minimizar":
                        optimo = min(resultados, key=lambda r: r[2])
                        texto_opt = "Mínimo"
                    else:
                        optimo = max(resultados, key=lambda r: r[2])
                        texto_opt = "Máximo"

                    st.markdown(f"""
                    <div class="info-panel success">
                        <div class="info-title">🎉 {texto_opt} encontrado</div>
                        <div class="info-text">
                            <strong>Punto:</strong> ({optimo[0]:.6f}, {optimo[1]:.6f})<br>
                            <strong>Valor:</strong> f = {optimo[2]:.6f}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Visualización
                    st.markdown("### 🎨 Visualización")

                    x_vals_opt = [r[0] for r in resultados]
                    y_vals_opt = [r[1] for r in resultados]
                    x_center = np.mean(x_vals_opt)
                    y_center = np.mean(y_vals_opt)
                    rango = max(3, max(abs(x_center), abs(y_center)) + 2)

                    x_range = np.linspace(x_center - rango, x_center + rango, 100)
                    y_range = np.linspace(y_center - rango, y_center + rango, 100)
                    X, Y = np.meshgrid(x_range, y_range)
                    Z = evaluar_funcion_segura(funcion_objetivo, X, Y)

                    fig = go.Figure()

                    fig.add_trace(go.Contour(
                        x=x_range, y=y_range, z=Z,
                        colorscale='Viridis',
                        name='f(x,y)',
                        showscale=True,
                        contours=dict(showlabels=True)
                    ))

                    try:
                        Z_g = evaluar_funcion_segura(restriccion, X, Y)
                        fig.add_trace(go.Contour(
                            x=x_range, y=y_range, z=Z_g,
                            contours=dict(
                                start=0,
                                end=0,
                                size=1,
                                showlabels=True,
                                coloring='lines'
                            ),
                            line=dict(color='red', width=3),
                            showscale=False,
                            name='Restricción g(x,y)=0'
                        ))
                    except:
                        pass

                    for i, (x_val, y_val, f_val) in enumerate(resultados):
                        fig.add_trace(go.Scatter(
                            x=[x_val], y=[y_val],
                            mode='markers+text',
                            marker=dict(size=12, color='red' if (x_val, y_val) == optimo[:2] else 'orange'),
                            text=[f'P{i+1}'],
                            textposition='top center',
                            name=f'Punto {i+1}'
                        ))

                    fig.update_layout(
                        title="Función objetivo con restricción y puntos críticos",
                        xaxis_title='x',
                        yaxis_title='y',
                        width=800,
                        height=700,
                        showlegend=True
                    )

                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No se encontraron soluciones reales.")
            else:
                st.warning("No se encontraron puntos críticos.")

                st.info("🔄 Intentando optimización numérica...")

                try:
                    f_num = lambdify((x, y), f, 'numpy')
                    g_num = lambdify((x, y), g, 'numpy')

                    restriccion_dict = {'type': 'eq', 'fun': lambda vars: g_num(vars[0], vars[1])}

                    x0 = [0.0, 0.0]

                    if tipo_opt == "Minimizar":
                        resultado = minimize(lambda vars: f_num(vars[0], vars[1]),
                                           x0, constraints=restriccion_dict, method='SLSQP')
                    else:
                        resultado = minimize(lambda vars: -f_num(vars[0], vars[1]),
                                           x0, constraints=restriccion_dict, method='SLSQP')

                    if resultado.success:
                        x_opt, y_opt = resultado.x
                        f_opt = f_num(x_opt, y_opt)

                        st.markdown(f"""
                        <div class="info-panel success">
                            <div class="info-title">✅ Solución numérica encontrada</div>
                            <div class="info-text">
                                <strong>x:</strong> {x_opt:.6f}<br>
                                <strong>y:</strong> {y_opt:.6f}<br>
                                <strong>f(x, y):</strong> {f_opt:.6f}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("La optimización numérica no convergió.")
                except Exception as e:
                    st.error(f"Error en optimización numérica: {str(e)}")

        except Exception as e:
            st.error(f"Error al resolver el problema: {str(e)}")

# ============================================================================
# INTEGRACIÓN DOBLE Y TRIPLE
# ============================================================================

elif menu == "∫ Integración Doble y Triple":
    st.markdown("""
    <div class="educational-card">
        <div class="educational-card-header">
            <h2>∫ Integración Doble y Triple</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tipo_integral = st.radio(
        "Selecciona el tipo de integral:",
        ["Integral Doble ∫∫", "Integral Triple ∫∫∫"]
    )

    if tipo_integral == "Integral Doble ∫∫":
        st.markdown("### ∫∫ Integral Doble")
        st.latex(r"\int_{y_1}^{y_2} \int_{x_1}^{x_2} f(x, y) \, dx \, dy")

        funcion_input = st.text_input(
            "Ingresa el integrando f(x, y):",
            value="x*y",
            help="Función a integrar"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Límites para x:**")
            x_inf = st.text_input("Límite inferior de x:", value="0", key="x_inf")
            x_sup = st.text_input("Límite superior de x:", value="1", key="x_sup")

        with col2:
            st.markdown("**Límites para y:**")
            y_inf = st.text_input("Límite inferior de y:", value="0", key="y_inf")
            y_sup = st.text_input("Límite superior de y:", value="1", key="y_sup")

        metodo = st.radio(
            "Método de cálculo:",
            ["Simbólico (exacto)", "Numérico (aproximado)"]
        )

        if st.button("🧮 Calcular Integral Doble", type="primary"):
            try:
                expr = sympify(funcion_input, locals=simbolos)

                st.markdown("### 📐 Integral a calcular")
                st.latex(f"\\int_{{{y_inf}}}^{{{y_sup}}} \\int_{{{x_inf}}}^{{{x_sup}}} {latex(expr)} \\, dx \\, dy")

                if metodo == "Simbólico (exacto)":
                    x_inf_sym = sympify(x_inf, locals=simbolos)
                    x_sup_sym = sympify(x_sup, locals=simbolos)
                    y_inf_sym = sympify(y_inf, locals=simbolos)
                    y_sup_sym = sympify(y_sup, locals=simbolos)

                    st.markdown("### 📝 Proceso de Integración")
                    
                    integral_x = sp.integrate(expr, (x, x_inf_sym, x_sup_sym))
                    st.markdown("""
                    <div class="info-panel">
                        <div class="info-title">Paso 1: Integrar respecto a x</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.latex(f"\\int_{{{x_inf}}}^{{{x_sup}}} {latex(expr)} \\, dx = {latex(integral_x)}")

                    resultado = sp.integrate(integral_x, (y, y_inf_sym, y_sup_sym))
                    st.markdown("""
                    <div class="info-panel">
                        <div class="info-title">Paso 2: Integrar respecto a y</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.latex(f"\\int_{{{y_inf}}}^{{{y_sup}}} {latex(integral_x)} \\, dy = {latex(resultado)}")

                    resultado_num = float(resultado.evalf())
                    st.markdown(f"""
                    <div class="info-panel success">
                        <div class="info-title">✅ Resultado Final</div>
                        <div class="stat-value">{resultado_num:.8f}</div>
                    </div>
                    """, unsafe_allow_html=True)

                else:
                    f_num = lambdify((x, y), expr, 'numpy')
                    x_inf_num = float(sympify(x_inf, locals=simbolos))
                    x_sup_num = float(sympify(x_sup, locals=simbolos))
                    y_inf_num = float(sympify(y_inf, locals=simbolos))
                    y_sup_num = float(sympify(y_sup, locals=simbolos))

                    resultado, error = integrate.dblquad(
                        f_num,
                        y_inf_num, y_sup_num,
                        x_inf_num, x_sup_num
                    )

                    st.markdown(f"""
                    <div class="info-panel success">
                        <div class="info-title">✅ Resultado Numérico</div>
                        <div class="stat-value">{resultado:.8f}</div>
                        <div class="info-text">Error estimado: {error:.2e}</div>
                    </div>
                    """, unsafe_allow_html=True)

                # Visualización
                st.markdown("### 🎨 Región de Integración")

                try:
                    x_inf_plot = float(sympify(x_inf, locals=simbolos))
                    x_sup_plot = float(sympify(x_sup, locals=simbolos))
                    y_inf_plot = float(sympify(y_inf, locals=simbolos))
                    y_sup_plot = float(sympify(y_sup, locals=simbolos))

                    x_range = np.linspace(x_inf_plot, x_sup_plot, 50)
                    y_range = np.linspace(y_inf_plot, y_sup_plot, 50)
                    X, Y = np.meshgrid(x_range, y_range)
                    Z = evaluar_funcion_segura(funcion_input, X, Y)

                    fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='Viridis')])
                    fig.update_layout(
                        scene=dict(
                            xaxis_title='x',
                            yaxis_title='y',
                            zaxis_title='f(x, y)',
                            camera=dict(eye=dict(x=1.5, y=1.5, z=1.3))
                        ),
                        width=700,
                        height=600,
                        title="Volumen bajo la superficie"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                except:
                    pass

            except Exception as e:
                st.error(f"Error al calcular la integral: {str(e)}")

    else:  # Integral Triple
        st.markdown("### ∫∫∫ Integral Triple")
        st.latex(r"\int_{z_1}^{z_2} \int_{y_1}^{y_2} \int_{x_1}^{x_2} f(x, y, z) \, dx \, dy \, dz")

        funcion_input = st.text_input(
            "Ingresa el integrando f(x, y, z):",
            value="x*y*z",
            help="Función a integrar"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Límites para x:**")
            x_inf = st.text_input("Límite inferior de x:", value="0", key="x_inf_3")
            x_sup = st.text_input("Límite superior de x:", value="1", key="x_sup_3")

        with col2:
            st.markdown("**Límites para y:**")
            y_inf = st.text_input("Límite inferior de y:", value="0", key="y_inf_3")
            y_sup = st.text_input("Límite superior de y:", value="1", key="y_sup_3")

        with col3:
            st.markdown("**Límites para z:**")
            z_inf = st.text_input("Límite inferior de z:", value="0", key="z_inf_3")
            z_sup = st.text_input("Límite superior de z:", value="1", key="z_sup_3")

        metodo = st.radio(
            "Método de cálculo:",
            ["Simbólico (exacto)", "Numérico (aproximado)"],
            key="metodo_triple"
        )

        if st.button("🧮 Calcular Integral Triple", type="primary"):
            try:
                expr = sympify(funcion_input, locals=simbolos)

                st.markdown("### 📐 Integral a calcular")
                st.latex(f"\\int_{{{z_inf}}}^{{{z_sup}}} \\int_{{{y_inf}}}^{{{y_sup}}} \\int_{{{x_inf}}}^{{{x_sup}}} {latex(expr)} \\, dx \\, dy \\, dz")

                if metodo == "Simbólico (exacto)":
                    x_inf_sym = sympify(x_inf, locals=simbolos)
                    x_sup_sym = sympify(x_sup, locals=simbolos)
                    y_inf_sym = sympify(y_inf, locals=simbolos)
                    y_sup_sym = sympify(y_sup, locals=simbolos)
                    z_inf_sym = sympify(z_inf, locals=simbolos)
                    z_sup_sym = sympify(z_sup, locals=simbolos)

                    st.markdown("### 📝 Proceso de Integración")

                    integral_x = sp.integrate(expr, (x, x_inf_sym, x_sup_sym))
                    st.markdown("""
                    <div class="info-panel">
                        <div class="info-title">Paso 1: Integrar respecto a x</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.latex(f"{latex(integral_x)}")

                    integral_y = sp.integrate(integral_x, (y, y_inf_sym, y_sup_sym))
                    st.markdown("""
                    <div class="info-panel">
                        <div class="info-title">Paso 2: Integrar respecto a y</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.latex(f"{latex(integral_y)}")

                    resultado = sp.integrate(integral_y, (z, z_inf_sym, z_sup_sym))
                    st.markdown("""
                    <div class="info-panel">
                        <div class="info-title">Paso 3: Integrar respecto a z</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.latex(f"{latex(resultado)}")

                    resultado_num = float(resultado.evalf())
                    st.markdown(f"""
                    <div class="info-panel success">
                        <div class="info-title">✅ Resultado Final</div>
                        <div class="stat-value">{resultado_num:.8f}</div>
                    </div>
                    """, unsafe_allow_html=True)

                else:
                    f_num = lambdify((x, y, z), expr, 'numpy')
                    x_inf_num = float(sympify(x_inf, locals=simbolos))
                    x_sup_num = float(sympify(x_sup, locals=simbolos))
                    y_inf_num = float(sympify(y_inf, locals=simbolos))
                    y_sup_num = float(sympify(y_sup, locals=simbolos))
                    z_inf_num = float(sympify(z_inf, locals=simbolos))
                    z_sup_num = float(sympify(z_sup, locals=simbolos))

                    resultado, error = integrate.tplquad(
                        f_num,
                        z_inf_num, z_sup_num,
                        y_inf_num, y_sup_num,
                        x_inf_num, x_sup_num
                    )

                    st.markdown(f"""
                    <div class="info-panel success">
                        <div class="info-title">✅ Resultado Numérico</div>
                        <div class="stat-value">{resultado:.8f}</div>
                        <div class="info-text">Error estimado: {error:.2e}</div>
                    </div>
                    """, unsafe_allow_html=True)

                # Interpretación geométrica
                st.markdown("### 📐 Interpretación Geométrica")
                st.markdown(f"""
                <div class="info-panel">
                    <div class="info-text">
                        Esta integral triple calcula el volumen bajo la superficie f(x, y, z) = {funcion_input}
                        en la región:<br>
                        • {x_inf} ≤ x ≤ {x_sup}<br>
                        • {y_inf} ≤ y ≤ {y_sup}<br>
                        • {z_inf} ≤ z ≤ {z_sup}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error al calcular la integral: {str(e)}")

# ============================================================================
# FOOTER MEJORADO
# ============================================================================

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    <h3 style="margin-bottom: 1rem;">📊 Calculadora de Cálculo Multivariable</h3>
    <p style="margin-bottom: 0.5rem;">Desarrollado con Streamlit, SymPy, NumPy, Plotly y SciPy</p>
    <p style="margin-bottom: 0; opacity: 0.9;">
        <strong>Miguel Mendoza</strong> | miguel.mendozaj@campusucc.edu.co
    </p>
    <p style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">
        Universidad Cooperativa de Colombia © 2024
    </p>
</div>
""", unsafe_allow_html=True)
