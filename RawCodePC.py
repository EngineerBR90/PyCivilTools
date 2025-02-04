import math

def validar_entrada_positiva(mensagem):
    """
    Valida entradas numéricas positivas com tratamento de erros
    Retorna: Valor float positivo válido
    """
    while True:
        try:
            valor = float(input(mensagem))
            if valor <= 0:
                raise ValueError("O valor deve ser positivo")
            return valor
        except ValueError as e:
            print(f"Erro: {str(e)}. Tente novamente.")

def calcular_perda_carga():
    """
    Calcula a perda de carga em tubulações de piscinas utilizando a fórmula de Hazen-Williams
    Considera normas ABNT e inclui verificações de segurança
    """
    print("\n=== Cálculo de Perda de Carga em Tubulações de Piscinas ===")
    print("(Baseado na fórmula de Hazen-Williams e normas ABNT)\n")

    try:
        # Entradas validadas com tratamento de erros
        Q = validar_entrada_positiva("Digite a vazão (m³/h): ") / 3600  # Conversão para m³/s
        D = validar_entrada_positiva("Digite o diâmetro interno da tubulação (mm): ") / 1000  # Para metros
        L = validar_entrada_positiva("Digite o comprimento reto da tubulação (m): ")
        material = input("Material da tubulação (PVC, Cobre, Aço): ").strip().lower()
        comp_equivalente = validar_entrada_positiva("Digite o comprimento equivalente total dos acessórios (m): ")

        # Coeficiente de Hazen-Williams com verificação
        coeficientes = {'pvc': 140, 'cobre': 130, 'aço': 100}
        C = coeficientes.get(material, 140)
        if material not in coeficientes:
            print("\nAviso: Material não reconhecido. Usando coeficiente padrão do PVC (C=140).")

        # Cálculo da perda de carga linear (Hf)
        Hf = 10.67 * (Q ** 1.85) / (C ** 1.85 * D ** 4.87) * L  # Coeficiente ajustado para 10.67

        # Cálculo da perda de carga localizada (Hl)
        Hl = Hf * (comp_equivalente / L)  # L já validado como >0

        # Cálculos finais
        perda_total = Hf + Hl
        area = math.pi * (D ** 2) / 4
        velocidade = Q / area  # Em m/s

        # Resultados detalhados
        print("\n=== RESULTADOS ===")
        print(f"- Perda de carga linear (Hf): {Hf:.3f} mca")
        print(f"- Perda de carga localizada (Hl): {Hl:.3f} mca")
        print(f"- Perda de carga TOTAL (ΔH): {perda_total:.3f} mca")
        print(f"- Velocidade da água: {velocidade:.2f} m/s")

        # Verificação de velocidade conforme NBR 5626
        if velocidade > 3.0:
            print("\nALERTA: Velocidade acima de 3.0 m/s! Risco de erosão e ruído. Aumente o diâmetro.")
        elif velocidade < 1.5:
            print("\nAVISO: Velocidade abaixo de 1.5 m/s. Pode haver acumulo de partículas.")

        # Margens de segurança calculadas
        print("\nRecomendações de segurança:")
        print(f"- Adicione +10% de margem: {perda_total * 1.10:.3f} mca")
        print(f"- Adicione +20% de margem: {perda_total * 1.20:.3f} mca")

    except Exception as e:
        print(f"\nErro inesperado: {str(e)}")
        print("Verifique os valores inseridos e tente novamente.")

# Execução do programa
if __name__ == "__main__":
    calcular_perda_carga()
    input("\nPressione Enter para sair...")
