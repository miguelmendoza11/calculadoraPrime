"""
Calculadora de Cálculo Multivariable
Desarrollado con Streamlit, NumPy, SymPy, Plotly, y SciPy
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
    layout="wide"
)

# Título principal
st.title("📊 Calculadora de Cálculo Multivariable")
st.markdown("---")

# Menú lateral
menu = st.sidebar.selectbox(
    "Selecciona una funcionalidad:",
    [
        "🏠 Inicio",
        "📈 Visualización de Superficies",
        "🔍 Dominio, Rango y Límites",
        "∂ Derivadas Parciales y Gradientes",
        "🎯 Optimización con Restricciones",
        "∫ Integración Doble y Triple"
    ]
)

# Variables simbólicas
x, y, z, t = symbols('x y z t', real=True)

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def evaluar_funcion_segura(funcion_str, x_val, y_val):
    """Evalúa una función de manera segura con manejo de errores"""
    try:
        expr = sympify(funcion_str)
        f = lambdify((x, y), expr, 'numpy')
        resultado = f(x_val, y_val)
        # Reemplazar infinitos y NaN
        resultado = np.where(np.isfinite(resultado), resultado, np.nan)
        return resultado
    except Exception as e:
        st.error(f"Error al evaluar la función: {str(e)}")
        return None

def calcular_dominio(funcion_str):
    """Analiza y describe el dominio de una función"""
    try:
        expr = sympify(funcion_str)
        dominio_info = []

        # Verificar denominadores (división por cero)
        denominadores = []
        if expr.as_numer_denom()[1] != 1:
            denom = expr.as_numer_denom()[1]
            dominio_info.append(f"El denominador no puede ser cero: {latex(denom)} ≠ 0")

        # Verificar raíces cuadradas (debe ser no negativo)
        for arg in expr.atoms(sp.Pow):
            if arg.exp == sp.Rational(1, 2) or (arg.exp.is_rational and arg.exp < 1 and arg.exp > 0):
                dominio_info.append(f"Debe cumplirse: {latex(arg.base)} ≥ 0")

        # Verificar logaritmos (argumento debe ser positivo)
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
# PÁGINA DE INICIO
# ============================================================================

if menu == "🏠 Inicio":
    st.header("Bienvenido a la Calculadora de Cálculo Multivariable")

    st.markdown("""
    Esta aplicación te permite realizar diversos cálculos y visualizaciones relacionadas con
    el cálculo multivariable. Utiliza el menú lateral para navegar entre las diferentes funcionalidades:

    ### 📈 Visualización de Superficies
    - Visualiza funciones de dos variables en 3D
    - Gráficos interactivos de superficies
    - Curvas de nivel

    ### 🔍 Dominio, Rango y Límites
    - Análisis automático del dominio
    - Cálculo numérico del rango
    - Evaluación de límites en puntos específicos

    ### ∂ Derivadas Parciales y Gradientes
    - Cálculo de derivadas parciales
    - Visualización del vector gradiente
    - Evaluación en puntos específicos

    ### 🎯 Optimización con Restricciones
    - Método de multiplicadores de Lagrange
    - Optimización con restricciones de igualdad
    - Visualización de puntos críticos

    ### ∫ Integración Doble y Triple
    - Integración doble para áreas y volúmenes
    - Integración triple para volúmenes en 3D
    - Cálculo de centros de masa
    """)

    st.markdown("---")
    st.info("💡 **Consejo:** Usa sintaxis de Python/SymPy para las funciones. Por ejemplo: `x**2 + y**2`, `sin(x)*cos(y)`, `exp(x*y)`")

# ============================================================================
# VISUALIZACIÓN DE SUPERFICIES
# ============================================================================

elif menu == "📈 Visualización de Superficies":
    st.header("Visualización de Funciones de Dos Variables")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Configuración")
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
        st.subheader("Información de la Función")
        try:
            expr = sympify(funcion_input)
            st.latex(f"f(x, y) = {latex(expr)}")

            # Información del dominio
            st.write("**Dominio:**")
            dominio_info = calcular_dominio(funcion_input)
            for info in dominio_info:
                st.write(f"- {info}")
        except Exception as e:
            st.error(f"Error al procesar la función: {str(e)}")

    if st.button("🎨 Generar Visualización", type="primary"):
        try:
            # Crear malla de puntos
            x_vals = np.linspace(x_min, x_max, n_points)
            y_vals = np.linspace(y_min, y_max, n_points)
            X, Y = np.meshgrid(x_vals, y_vals)
            Z = evaluar_funcion_segura(funcion_input, X, Y)

            if Z is not None:
                if tipo_grafico in ["Superficie 3D", "Ambos"]:
                    st.subheader("Superficie 3D")
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
                    st.subheader("Curvas de Nivel")
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
                st.subheader("📊 Estadísticas")
                z_valid = Z[np.isfinite(Z)]
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Mínimo", f"{np.min(z_valid):.4f}")
                with col2:
                    st.metric("Máximo", f"{np.max(z_valid):.4f}")
                with col3:
                    st.metric("Media", f"{np.mean(z_valid):.4f}")
                with col4:
                    st.metric("Desv. Est.", f"{np.std(z_valid):.4f}")

        except Exception as e:
            st.error(f"Error al generar la visualización: {str(e)}")

# ============================================================================
# DOMINIO, RANGO Y LÍMITES
# ============================================================================

elif menu == "🔍 Dominio, Rango y Límites":
    st.header("Análisis de Dominio, Rango y Límites")

    funcion_input = st.text_input(
        "Ingresa la función f(x, y):",
        value="sqrt(9 - x**2 - y**2)",
        help="Ejemplos: sqrt(x), 1/(x-y), log(x*y)"
    )

    try:
        expr = sympify(funcion_input)
        st.latex(f"f(x, y) = {latex(expr)}")
    except:
        st.error("Error al procesar la función")

    tab1, tab2, tab3 = st.tabs(["📐 Dominio", "📊 Rango", "🎯 Límites"])

    with tab1:
        st.subheader("Análisis del Dominio")
        if st.button("Calcular Dominio"):
            dominio_info = calcular_dominio(funcion_input)
            st.write("**Restricciones del dominio:**")
            for info in dominio_info:
                st.write(f"- {info}")

    with tab2:
        st.subheader("Cálculo del Rango")
        col1, col2 = st.columns(2)
        with col1:
            x_min_r = st.number_input("x mínimo:", value=-3.0, step=0.5, key="x_min_rango")
            x_max_r = st.number_input("x máximo:", value=3.0, step=0.5, key="x_max_rango")
        with col2:
            y_min_r = st.number_input("y mínimo:", value=-3.0, step=0.5, key="y_min_rango")
            y_max_r = st.number_input("y máximo:", value=3.0, step=0.5, key="y_max_rango")

        if st.button("Calcular Rango Numérico"):
            rango = calcular_rango_numerico(funcion_input, [x_min_r, x_max_r], [y_min_r, y_max_r])
            st.success(rango)

    with tab3:
        st.subheader("Evaluación de Límites")
        st.write("Evalúa límites cuando (x, y) → (a, b)")

        col1, col2 = st.columns(2)
        with col1:
            a = st.number_input("Valor de a:", value=0.0, step=0.1)
            b = st.number_input("Valor de b:", value=0.0, step=0.1)

        if st.button("Calcular Límite"):
            try:
                expr = sympify(funcion_input)
                # Primero límite en x, luego en y
                limite_x = limit(expr, x, a)
                limite_final = limit(limite_x, y, b)

                st.write(f"**Límite cuando (x, y) → ({a}, {b}):**")
                st.latex(f"\\lim_{{(x,y) \\to ({a},{b})}} {latex(expr)} = {latex(limite_final)}")

                # Evaluar por varios caminos
                st.write("**Verificación por diferentes caminos:**")

                # Camino 1: y = 0, x → a
                try:
                    expr_y0 = expr.subs(y, 0)
                    lim_camino1 = limit(expr_y0, x, a)
                    st.write(f"- Camino y = 0: {latex(lim_camino1)}")
                except:
                    st.write("- Camino y = 0: No evaluable")

                # Camino 2: x = 0, y → b
                try:
                    expr_x0 = expr.subs(x, 0)
                    lim_camino2 = limit(expr_x0, y, b)
                    st.write(f"- Camino x = 0: {latex(lim_camino2)}")
                except:
                    st.write("- Camino x = 0: No evaluable")

                # Camino 3: y = x, ambos → punto
                try:
                    expr_yx = expr.subs(y, x)
                    lim_camino3 = limit(expr_yx, x, a)
                    st.write(f"- Camino y = x: {latex(lim_camino3)}")
                except:
                    st.write("- Camino y = x: No evaluable")

            except Exception as e:
                st.error(f"Error al calcular el límite: {str(e)}")

# ============================================================================
# DERIVADAS PARCIALES Y GRADIENTES
# ============================================================================

elif menu == "∂ Derivadas Parciales y Gradientes":
    st.header("Derivadas Parciales y Gradientes")

    funcion_input = st.text_input(
        "Ingresa la función f(x, y):",
        value="x**2*y + y**3",
        help="Ejemplos: x**2 + y**2, x*exp(y), sin(x)*cos(y)"
    )

    try:
        expr = sympify(funcion_input)
        st.latex(f"f(x, y) = {latex(expr)}")

        # Calcular derivadas parciales
        df_dx = diff(expr, x)
        df_dy = diff(expr, y)

        st.subheader("Derivadas Parciales")
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Derivada parcial respecto a x:**")
            st.latex(f"\\frac{{\\partial f}}{{\\partial x}} = {latex(df_dx)}")

        with col2:
            st.write("**Derivada parcial respecto a y:**")
            st.latex(f"\\frac{{\\partial f}}{{\\partial y}} = {latex(df_dy)}")

        # Derivadas de segundo orden
        st.subheader("Derivadas Parciales de Segundo Orden")
        df_dxx = diff(df_dx, x)
        df_dyy = diff(df_dy, y)
        df_dxy = diff(df_dx, y)
        df_dyx = diff(df_dy, x)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.write("**f_xx:**")
            st.latex(f"{latex(df_dxx)}")
        with col2:
            st.write("**f_yy:**")
            st.latex(f"{latex(df_dyy)}")
        with col3:
            st.write("**f_xy:**")
            st.latex(f"{latex(df_dxy)}")
        with col4:
            st.write("**f_yx:**")
            st.latex(f"{latex(df_dyx)}")

        # Evaluación en un punto
        st.subheader("Evaluación del Gradiente en un Punto")
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            x0 = st.number_input("Valor de x₀:", value=1.0, step=0.1)
        with col2:
            y0 = st.number_input("Valor de y₀:", value=1.0, step=0.1)
        with col3:
            st.write("")
            st.write("")
            calcular_grad = st.button("Calcular Gradiente", type="primary")

        if calcular_grad:
            try:
                # Evaluar gradiente en el punto
                grad_x = float(df_dx.subs([(x, x0), (y, y0)]))
                grad_y = float(df_dy.subs([(x, x0), (y, y0)]))
                f_val = float(expr.subs([(x, x0), (y, y0)]))

                st.write(f"**En el punto ({x0}, {y0}):**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("f(x₀, y₀)", f"{f_val:.4f}")
                with col2:
                    st.metric("∂f/∂x", f"{grad_x:.4f}")
                with col3:
                    st.metric("∂f/∂y", f"{grad_y:.4f}")

                st.latex(f"\\nabla f({x0}, {y0}) = ({grad_x:.4f}, {grad_y:.4f})")

                magnitud = np.sqrt(grad_x**2 + grad_y**2)
                st.write(f"**Magnitud del gradiente:** {magnitud:.4f}")

                # Visualización del gradiente
                st.subheader("Visualización del Gradiente")

                # Crear superficie
                x_range = np.linspace(x0 - 2, x0 + 2, 50)
                y_range = np.linspace(y0 - 2, y0 + 2, 50)
                X, Y = np.meshgrid(x_range, y_range)
                Z = evaluar_funcion_segura(funcion_input, X, Y)

                # Gráfico de curvas de nivel con vector gradiente
                fig = go.Figure()

                # Curvas de nivel
                fig.add_trace(go.Contour(
                    x=x_range, y=y_range, z=Z,
                    colorscale='Viridis',
                    name='f(x,y)',
                    showscale=True
                ))

                # Punto de evaluación
                fig.add_trace(go.Scatter(
                    x=[x0], y=[y0],
                    mode='markers',
                    marker=dict(size=12, color='red'),
                    name=f'Punto ({x0}, {y0})'
                ))

                # Vector gradiente
                escala = 0.5
                fig.add_trace(go.Scatter(
                    x=[x0, x0 + escala * grad_x],
                    y=[y0, y0 + escala * grad_y],
                    mode='lines+markers',
                    line=dict(color='red', width=3),
                    marker=dict(size=8, symbol='arrow', angleref='previous'),
                    name='∇f'
                ))

                fig.update_layout(
                    title="Curvas de nivel con vector gradiente",
                    xaxis_title='x',
                    yaxis_title='y',
                    width=700,
                    height=600,
                    showlegend=True
                )

                st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Error al calcular el gradiente: {str(e)}")

    except Exception as e:
        st.error(f"Error al procesar la función: {str(e)}")

# ============================================================================
# OPTIMIZACIÓN CON RESTRICCIONES
# ============================================================================

elif menu == "🎯 Optimización con Restricciones":
    st.header("Optimización con Multiplicadores de Lagrange")

    st.markdown("""
    Resuelve problemas de optimización del tipo:
    - **Optimizar:** f(x, y)
    - **Sujeto a:** g(x, y) = 0
    """)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Función Objetivo")
        funcion_objetivo = st.text_input(
            "f(x, y) =",
            value="x**2 + y**2",
            help="Función a optimizar"
        )

        tipo_opt = st.radio("Tipo de optimización:", ["Minimizar", "Maximizar"])

    with col2:
        st.subheader("Restricción")
        restriccion = st.text_input(
            "g(x, y) = 0, donde g(x, y) =",
            value="x + y - 1",
            help="Restricción de igualdad (se igualará a cero)"
        )

    if st.button("🔍 Resolver con Multiplicadores de Lagrange", type="primary"):
        try:
            # Parsear funciones
            f = sympify(funcion_objetivo)
            g = sympify(restriccion)

            st.subheader("Formulación del Problema")
            st.latex(f"{tipo_opt.lower()} \\quad f(x, y) = {latex(f)}")
            st.latex(f"\\text{{sujeto a}} \\quad g(x, y) = {latex(g)} = 0")

            # Crear función de Lagrange
            lam = symbols('lambda', real=True)
            L = f - lam * g

            st.subheader("Función de Lagrange")
            st.latex(f"\\mathcal{{L}}(x, y, \\lambda) = {latex(f)} - \\lambda ({latex(g)})")
            st.latex(f"\\mathcal{{L}} = {latex(L)}")

            # Calcular derivadas parciales
            dL_dx = diff(L, x)
            dL_dy = diff(L, y)
            dL_dlam = diff(L, lam)

            st.subheader("Sistema de Ecuaciones")
            st.write("Derivadas parciales igualadas a cero:")
            st.latex(f"\\frac{{\\partial \\mathcal{{L}}}}{{\\partial x}} = {latex(dL_dx)} = 0")
            st.latex(f"\\frac{{\\partial \\mathcal{{L}}}}{{\\partial y}} = {latex(dL_dy)} = 0")
            st.latex(f"\\frac{{\\partial \\mathcal{{L}}}}{{\\partial \\lambda}} = {latex(dL_dlam)} = 0")

            # Resolver sistema
            soluciones = sp.solve([dL_dx, dL_dy, dL_dlam], [x, y, lam])

            if soluciones:
                st.subheader("Puntos Críticos")

                # Si hay una sola solución, convertirla a lista
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

                        # Solo considerar soluciones reales
                        if abs(x_val.imag) < 1e-10 and abs(y_val.imag) < 1e-10:
                            x_val = x_val.real
                            y_val = y_val.real
                            lam_val = lam_val.real

                            f_val = float(f.subs([(x, x_val), (y, y_val)]))

                            st.write(f"**Punto {i}:**")
                            st.write(f"- x = {x_val:.6f}")
                            st.write(f"- y = {y_val:.6f}")
                            st.write(f"- λ = {lam_val:.6f}")
                            st.write(f"- f(x, y) = {f_val:.6f}")
                            st.write("---")

                            resultados.append((x_val, y_val, f_val))
                    except:
                        continue

                if resultados:
                    # Encontrar óptimo
                    if tipo_opt == "Minimizar":
                        optimo = min(resultados, key=lambda r: r[2])
                        texto_opt = "Mínimo"
                    else:
                        optimo = max(resultados, key=lambda r: r[2])
                        texto_opt = "Máximo"

                    st.success(f"**{texto_opt} encontrado:**")
                    st.write(f"- Punto: ({optimo[0]:.6f}, {optimo[1]:.6f})")
                    st.write(f"- Valor: f = {optimo[2]:.6f}")

                    # Visualización
                    st.subheader("Visualización")

                    # Determinar rango para visualización
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

                    # Curvas de nivel de la función objetivo
                    fig.add_trace(go.Contour(
                        x=x_range, y=y_range, z=Z,
                        colorscale='Viridis',
                        name='f(x,y)',
                        showscale=True,
                        contours=dict(showlabels=True)
                    ))

                    # Restricción g(x,y) = 0
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

                    # Puntos críticos
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

                # Intentar optimización numérica
                st.info("Intentando optimización numérica...")

                try:
                    f_num = lambdify((x, y), f, 'numpy')
                    g_num = lambdify((x, y), g, 'numpy')

                    # Restricción en forma de diccionario
                    restriccion_dict = {'type': 'eq', 'fun': lambda vars: g_num(vars[0], vars[1])}

                    # Punto inicial
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

                        st.success(f"**Solución numérica encontrada:**")
                        st.write(f"- x = {x_opt:.6f}")
                        st.write(f"- y = {y_opt:.6f}")
                        st.write(f"- f(x, y) = {f_opt:.6f}")
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
    st.header("Integración Doble y Triple")

    tipo_integral = st.radio(
        "Selecciona el tipo de integral:",
        ["Integral Doble ∫∫", "Integral Triple ∫∫∫"]
    )

    if tipo_integral == "Integral Doble ∫∫":
        st.subheader("Integral Doble")
        st.latex(r"\int_{y_1}^{y_2} \int_{x_1}^{x_2} f(x, y) \, dx \, dy")

        funcion_input = st.text_input(
            "Ingresa el integrando f(x, y):",
            value="x*y",
            help="Función a integrar"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Límites para x:**")
            x_inf = st.text_input("Límite inferior de x:", value="0", key="x_inf")
            x_sup = st.text_input("Límite superior de x:", value="1", key="x_sup")

        with col2:
            st.write("**Límites para y:**")
            y_inf = st.text_input("Límite inferior de y:", value="0", key="y_inf")
            y_sup = st.text_input("Límite superior de y:", value="1", key="y_sup")

        metodo = st.radio(
            "Método de cálculo:",
            ["Simbólico (exacto)", "Numérico (aproximado)"]
        )

        if st.button("Calcular Integral Doble", type="primary"):
            try:
                expr = sympify(funcion_input)

                st.write("**Integral a calcular:**")
                st.latex(f"\\int_{{{y_inf}}}^{{{y_sup}}} \\int_{{{x_inf}}}^{{{x_sup}}} {latex(expr)} \\, dx \\, dy")

                if metodo == "Simbólico (exacto)":
                    # Integración simbólica
                    x_inf_sym = sympify(x_inf)
                    x_sup_sym = sympify(x_sup)
                    y_inf_sym = sympify(y_inf)
                    y_sup_sym = sympify(y_sup)

                    # Primera integración (respecto a x)
                    integral_x = sp.integrate(expr, (x, x_inf_sym, x_sup_sym))
                    st.write("**Paso 1: Integrar respecto a x**")
                    st.latex(f"\\int_{{{x_inf}}}^{{{x_sup}}} {latex(expr)} \\, dx = {latex(integral_x)}")

                    # Segunda integración (respecto a y)
                    resultado = sp.integrate(integral_x, (y, y_inf_sym, y_sup_sym))
                    st.write("**Paso 2: Integrar respecto a y**")
                    st.latex(f"\\int_{{{y_inf}}}^{{{y_sup}}} {latex(integral_x)} \\, dy = {latex(resultado)}")

                    # Resultado final
                    resultado_num = float(resultado.evalf())
                    st.success(f"**Resultado:** {resultado_num:.8f}")

                else:
                    # Integración numérica
                    f_num = lambdify((x, y), expr, 'numpy')
                    x_inf_num = float(sympify(x_inf))
                    x_sup_num = float(sympify(x_sup))
                    y_inf_num = float(sympify(y_inf))
                    y_sup_num = float(sympify(y_sup))

                    resultado, error = integrate.dblquad(
                        f_num,
                        y_inf_num, y_sup_num,
                        x_inf_num, x_sup_num
                    )

                    st.success(f"**Resultado:** {resultado:.8f}")
                    st.info(f"**Error estimado:** {error:.2e}")

                # Visualización de la región de integración
                st.subheader("Región de Integración")

                try:
                    x_inf_plot = float(sympify(x_inf))
                    x_sup_plot = float(sympify(x_sup))
                    y_inf_plot = float(sympify(y_inf))
                    y_sup_plot = float(sympify(y_sup))

                    # Crear superficie
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
        st.subheader("Integral Triple")
        st.latex(r"\int_{z_1}^{z_2} \int_{y_1}^{y_2} \int_{x_1}^{x_2} f(x, y, z) \, dx \, dy \, dz")

        funcion_input = st.text_input(
            "Ingresa el integrando f(x, y, z):",
            value="x*y*z",
            help="Función a integrar"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("**Límites para x:**")
            x_inf = st.text_input("Límite inferior de x:", value="0", key="x_inf_3")
            x_sup = st.text_input("Límite superior de x:", value="1", key="x_sup_3")

        with col2:
            st.write("**Límites para y:**")
            y_inf = st.text_input("Límite inferior de y:", value="0", key="y_inf_3")
            y_sup = st.text_input("Límite superior de y:", value="1", key="y_sup_3")

        with col3:
            st.write("**Límites para z:**")
            z_inf = st.text_input("Límite inferior de z:", value="0", key="z_inf_3")
            z_sup = st.text_input("Límite superior de z:", value="1", key="z_sup_3")

        metodo = st.radio(
            "Método de cálculo:",
            ["Simbólico (exacto)", "Numérico (aproximado)"],
            key="metodo_triple"
        )

        if st.button("Calcular Integral Triple", type="primary"):
            try:
                expr = sympify(funcion_input)

                st.write("**Integral a calcular:**")
                st.latex(f"\\int_{{{z_inf}}}^{{{z_sup}}} \\int_{{{y_inf}}}^{{{y_sup}}} \\int_{{{x_inf}}}^{{{x_sup}}} {latex(expr)} \\, dx \\, dy \\, dz")

                if metodo == "Simbólico (exacto)":
                    # Integración simbólica
                    x_inf_sym = sympify(x_inf)
                    x_sup_sym = sympify(x_sup)
                    y_inf_sym = sympify(y_inf)
                    y_sup_sym = sympify(y_sup)
                    z_inf_sym = sympify(z_inf)
                    z_sup_sym = sympify(z_sup)

                    # Primera integración (respecto a x)
                    integral_x = sp.integrate(expr, (x, x_inf_sym, x_sup_sym))
                    st.write("**Paso 1: Integrar respecto a x**")
                    st.latex(f"{latex(integral_x)}")

                    # Segunda integración (respecto a y)
                    integral_y = sp.integrate(integral_x, (y, y_inf_sym, y_sup_sym))
                    st.write("**Paso 2: Integrar respecto a y**")
                    st.latex(f"{latex(integral_y)}")

                    # Tercera integración (respecto a z)
                    resultado = sp.integrate(integral_y, (z, z_inf_sym, z_sup_sym))
                    st.write("**Paso 3: Integrar respecto a z**")
                    st.latex(f"{latex(resultado)}")

                    # Resultado final
                    resultado_num = float(resultado.evalf())
                    st.success(f"**Resultado:** {resultado_num:.8f}")

                else:
                    # Integración numérica
                    f_num = lambdify((x, y, z), expr, 'numpy')
                    x_inf_num = float(sympify(x_inf))
                    x_sup_num = float(sympify(x_sup))
                    y_inf_num = float(sympify(y_inf))
                    y_sup_num = float(sympify(y_sup))
                    z_inf_num = float(sympify(z_inf))
                    z_sup_num = float(sympify(z_sup))

                    resultado, error = integrate.tplquad(
                        f_num,
                        z_inf_num, z_sup_num,
                        y_inf_num, y_sup_num,
                        x_inf_num, x_sup_num
                    )

                    st.success(f"**Resultado:** {resultado:.8f}")
                    st.info(f"**Error estimado:** {error:.2e}")

                # Interpretación geométrica
                st.subheader("Interpretación Geométrica")
                st.write(f"""
                Esta integral triple calcula el volumen bajo la superficie f(x, y, z) = {funcion_input}
                en la región:
                - {x_inf} ≤ x ≤ {x_sup}
                - {y_inf} ≤ y ≤ {y_sup}
                - {z_inf} ≤ z ≤ {z_sup}
                """)

            except Exception as e:
                st.error(f"Error al calcular la integral: {str(e)}")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Calculadora de Cálculo Multivariable | Desarrollado con Streamlit, SymPy, NumPy, Plotly y SciPy</p>
    <p>Miguel Mendoza | miguel.mendozaj@campusucc.edu.co</p>
</div>
""", unsafe_allow_html=True)
