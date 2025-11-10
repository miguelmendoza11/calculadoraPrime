# Calculadora de Cálculo Multivariable

Una aplicación interactiva desarrollada con Streamlit para realizar cálculos y visualizaciones de cálculo multivariable.

## Características

### 📈 Visualización de Superficies
- Visualización 3D de funciones de dos variables
- Curvas de nivel
- Gráficos interactivos con Plotly

### 🔍 Dominio, Rango y Límites
- Cálculo automático del dominio
- Cálculo numérico del rango
- Evaluación de límites en puntos específicos
- Verificación de límites por diferentes caminos

### ∂ Derivadas Parciales y Gradientes
- Cálculo simbólico de derivadas parciales
- Derivadas de segundo orden
- Visualización de vectores gradiente
- Evaluación del gradiente en puntos específicos
- Visualización de curvas de nivel con vectores gradiente

### 🎯 Optimización con Restricciones
- Método de multiplicadores de Lagrange
- Resolución simbólica y numérica
- Visualización de puntos críticos
- Optimización con restricciones de igualdad

### ∫ Integración Doble y Triple
- Integración doble simbólica y numérica
- Integración triple simbólica y numérica
- Cálculo de volúmenes, masas y centros de masa
- Visualización de regiones de integración

## Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/miguelmendoza11/calculadoraPrime.git
cd calculadoraPrime
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

Ejecuta la aplicación con el siguiente comando:

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## Tecnologías Utilizadas

- **Streamlit**: Framework para la interfaz web
- **NumPy**: Cálculos numéricos
- **SymPy**: Cálculos simbólicos
- **Plotly**: Visualizaciones interactivas
- **SciPy**: Optimización e integración numérica
- **Requests**: Peticiones HTTP
- **Flask**: Framework web (incluido para extensiones futuras)

## Ejemplos de Funciones

### Funciones de dos variables:
- `x**2 + y**2` (paraboloide)
- `sin(x)*cos(y)` (función trigonométrica)
- `exp(-(x**2 + y**2))` (campana gaussiana)
- `x**2 - y**2` (silla de montar)
- `sqrt(9 - x**2 - y**2)` (hemisferio)

### Restricciones:
- `x + y - 1` (plano)
- `x**2 + y**2 - 4` (círculo)
- `x*y - 1` (hipérbola)

## Sintaxis de Funciones

Usa la sintaxis de Python/SymPy:
- Potencias: `x**2`, `y**3`
- Raíces: `sqrt(x)`, `x**(1/2)`
- Exponencial: `exp(x)`
- Trigonométricas: `sin(x)`, `cos(y)`, `tan(x)`
- Logaritmos: `log(x)`, `ln(x)`
- Constantes: `pi`, `E`

## Autor

**Miguel Mendoza**
- Email: miguel.mendozaj@campusucc.edu.co
- GitHub: [@miguelmendoza11](https://github.com/miguelmendoza11)

## Licencia

Este proyecto está bajo la Licencia MIT.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request para sugerencias y mejoras.
