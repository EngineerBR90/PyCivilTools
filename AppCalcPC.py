import streamlit as st
import math

# Dicionário externo contendo os comprimentos equivalentes (em metros) para cada acessório, material e diâmetro
comprimentos_equivalentes = {
    'Curva 90°': {
        'PVC': {50: 0.6, 75: 1.0, 100: 1.5},
        'Cobre': {50: 0.8, 75: 1.2, 100: 1.7},
        'Aço': {50: 1.0, 75: 1.5, 100: 2.0}
    },
    'Curva 45°': {
        'PVC': {50: 0.4, 75: 0.8, 100: 1.0},
        'Cobre': {50: 0.5, 75: 1.0, 100: 1.3},
        'Aço': {50: 0.7, 75: 1.2, 100: 1.5}
    },
    'T (desvio)': {
        'PVC': {50: 1.0, 75: 1.8, 100: 2.5},
        'Cobre': {50: 1.2, 75: 2.0, 100: 2.8},
        'Aço': {50: 1.5, 75: 2.5, 100: 3.0}
    },
    'Válvula de retenção': {
        'PVC': {50: 2.0, 75: 3.5, 100: 5.0},
        'Cobre': {50: 2.3, 75: 4.0, 100: 5.5},
        'Aço': {50: 2.5, 75: 4.5, 100: 6.0}
    },
    'Registro em cruz': {
        'PVC': {50: 2.5, 75: 4.0, 100: 6.0},
        'Cobre': {50: 2.8, 75: 4.5, 100: 6.5},
        'Aço': {50: 3.0, 75: 5.0, 100: 7.0}
    }
}

def calcular_perda_carga(vazao, diametro, comprimento, comp_equivalente_total, material):
    try:
        Q = float(vazao) / 3600  # Conversão para m³/s
        D = float(diametro) / 1000  # Conversão para metros
        L = float(comprimento)
        comp_equivalente_total = float(comp_equivalente_total)

        if Q <= 0 or D <= 0 or L <= 0 or comp_equivalente_total < 0:
            return "Erro: Todos os valores devem ser positivos."

        coeficientes = {'PVC': 140, 'Cobre': 130, 'Aço': 100}
        C = coeficientes.get(material, 140)

        # Cálculo da perda de carga linear usando Hazen-Williams
        Hf = 10.67 * (Q ** 1.85) / (C ** 1.85 * D ** 4.87) * L
        # Cálculo da perda de carga localizada proporcional ao comprimento equivalente
        Hl = Hf * (comp_equivalente_total / L)
        perda_total = Hf + Hl
        
        area = math.pi * (D ** 2) / 4
        velocidade = Q / area

        resultado_texto = f"""
        **Resultados:**  
        - Perda de carga linear (Hf): `{Hf:.3f} mca`  
        - Perda de carga localizada (Hl): `{Hl:.3f} mca`  
        - Perda de carga TOTAL (ΔH): `{perda_total:.3f} mca`  
        - Velocidade da água: `{velocidade:.2f} m/s`  
        """

        if velocidade > 3.0:
            resultado_texto += "\n⚠️ **ALERTA**: Velocidade acima de 3.0 m/s! Risco de aprisionamento, cavitação e/ou ruído."
        elif velocidade < 1.5:
            resultado_texto += "\nℹ️ **AVISO**: Velocidade abaixo de 1.5 m/s. Pode haver acúmulo de partículas, formação de biofilme e bolsões de ar."

        resultado_texto += f"""
        \n### Recomendações de segurança:
        - Adicione +20% como margem de segurança: {perda_total * 1.20:.3f} mca
        - Adicione ao cálculo a altura geométrica característica da instalação 
          (entre o N.A. e a posição da MB)
        """
        return resultado_texto
    except ValueError:
        return "Erro: Por favor, insira valores numéricos válidos."

# Interface no Streamlit
st.title("Cálculo de Perda de Carga")

st.subheader("Dados da Tubulação")
vazao = st.number_input("Vazão (m³/h):", min_value=0.0, step=0.1)
material = st.selectbox("Material da tubulação:", ["PVC", "Cobre", "Aço"])
diametro = st.selectbox("Diâmetro nominal da tubulação (mm):", [50, 75, 100])
comprimento = st.number_input("Comprimento reto da tubulação (m):", min_value=0.0, step=0.1)

st.subheader("Acessórios e Conexões")
st.markdown("Informe a quantidade de cada acessório instalado:")

comp_equivalente_acessorios = 0.0
for acessorio, materiais in comprimentos_equivalentes.items():
    if material in materiais and diametro in materiais[material]:
        qtd = st.number_input(f"Quantidade de {acessorio}:", min_value=0, step=1, value=0)
        comp_equivalente_acessorios += qtd * materiais[material][diametro]

# Adicionar possibilidade de comprimento equivalente manual
comp_equivalente_manual = st.number_input("Comprimento equivalente adicional (m):", min_value=0.0, step=0.1)
comp_equivalente_total = comp_equivalente_acessorios + comp_equivalente_manual

st.markdown(f"**Comprimento equivalente total dos acessórios:** {comp_equivalente_total:.2f} m")

if st.button("Calcular"):
    resultado = calcular_perda_carga(vazao, diametro, comprimento, comp_equivalente_total, material)
    st.markdown(resultado)

