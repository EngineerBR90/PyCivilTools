import streamlit as st
import math

def calcular_perda_carga(vazao, diametro, comprimento, comp_equivalente, material):
    try:
        Q = float(vazao) / 3600  # Conversão para m³/s
        D = float(diametro) / 1000  # Conversão para metros
        L = float(comprimento)
        comp_equivalente = float(comp_equivalente)

        if Q <= 0 or D <= 0 or L <= 0 or comp_equivalente < 0:
            return "Erro: Todos os valores devem ser positivos."

        coeficientes = {'PVC': 140, 'Cobre': 130, 'Aço': 100}
        C = coeficientes.get(material, 140)

        Hf = 10.67 * (Q ** 1.85) / (C ** 1.85 * D ** 4.87) * L
        Hl = Hf * (comp_equivalente / L)
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
            resultado_texto += "\nℹ️ **AVISO**: Velocidade abaixo de 1.5 m/s. Pode haver acúmulo de partículas, bolsão de ar e formação de biofilme."

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

vazao = st.number_input("Vazão (m³/h):", min_value=0.0, step=0.1)
diametro = st.number_input("Diâmetro interno da tubulação (mm):", min_value=0.0, step=0.1)
comprimento = st.number_input("Comprimento reto da tubulação (m):", min_value=0.0, step=0.1)
comp_equivalente = st.number_input("Comprimento equivalente total dos acessórios (m):", min_value=0.0, step=0.1)

material = st.selectbox("Material da tubulação:", ["PVC", "Cobre"])

if st.button("Calcular"):
    resultado = calcular_perda_carga(vazao, diametro, comprimento, comp_equivalente, material)
    st.markdown(resultado)
