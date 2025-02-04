import tkinter as tk
from tkinter import ttk, messagebox
import math


def calcular_perda_carga():
    try:
        # Captura os valores dos campos de entrada
        Q = float(entry_vazao.get()) / 3600  # Conversão para m³/s
        D = float(entry_diametro.get()) / 1000  # Conversão para metros
        L = float(entry_comprimento.get())
        comp_equivalente = float(entry_comp_equivalente.get())
        material = combo_material.get().strip().lower()

        if Q <= 0 or D <= 0 or L <= 0 or comp_equivalente < 0:
            messagebox.showerror("Erro", "Todos os valores devem ser positivos.")
            return

        # Coeficiente de Hazen-Williams
        coeficientes = {'PVC': 140, 'Cobre': 130, 'Aço': 100}
        C = coeficientes.get(material, 140)

        # Cálculo da perda de carga linear (Hf)
        Hf = 10.67 * (Q ** 1.85) / (C ** 1.85 * D ** 4.87) * L

        # Cálculo da perda de carga localizada (Hl)
        Hl = Hf * (comp_equivalente / L)

        # Cálculo da perda de carga total
        perda_total = Hf + Hl
        area = math.pi * (D ** 2) / 4
        velocidade = Q / area

        # Exibição dos resultados
        resultado_texto = (
            f"Perda de carga linear (Hf): {Hf:.3f} mca\n"
            f"Perda de carga localizada (Hl): {Hl:.3f} mca\n"
            f"Perda de carga TOTAL (ΔH): {perda_total:.3f} mca\n"
            f"Velocidade da água: {velocidade:.2f} m/s\n"
        )

        # Verificações de segurança
        if velocidade > 3.0:
            resultado_texto += "\nALERTA: Velocidade acima de 3.0 m/s! Risco de erosão e ruído."
        elif velocidade < 1.5:
            resultado_texto += "\nAVISO: Velocidade abaixo de 1.5 m/s. Pode haver acúmulo de partículas."

        resultado_texto += (
            "\nRecomendações de segurança:\n"
            f"- Adicione +10% de margem: {perda_total * 1.10:.3f} mca\n"
            f"- Adicione +20% de margem: {perda_total * 1.20:.3f} mca"
        )

        resultado_label.config(text=resultado_texto)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")


# Configuração da interface gráfica
root = tk.Tk()
root.title("Cálculo de Perda de Carga")
root.geometry("400x450")

# Campos de entrada
ttK = ttk.Label(root, text="Vazão (m³/h):")
ttK.pack()
entry_vazao = ttk.Entry(root)
entry_vazao.pack()

ttK = ttk.Label(root, text="Diâmetro interno da tubulação (mm):")
ttK.pack()
entry_diametro = ttk.Entry(root)
entry_diametro.pack()

ttK = ttk.Label(root, text="Comprimento reto da tubulação (m):")
ttK.pack()
entry_comprimento = ttk.Entry(root)
entry_comprimento.pack()

ttK = ttk.Label(root, text="Comprimento equivalente total dos acessórios (m):")
ttK.pack()
entry_comp_equivalente = ttk.Entry(root)
entry_comp_equivalente.pack()

ttK = ttk.Label(root, text="Material da tubulação:")
ttK.pack()
combo_material = ttk.Combobox(root, values=["PVC", "Cobre", "Aço"])
combo_material.pack()
combo_material.current(0)

# Botão de cálculo
calcular_btn = ttk.Button(root, text="Calcular", command=calcular_perda_carga)
calcular_btn.pack(pady=10)

# Resultado
resultado_label = ttk.Label(root, text="", justify="left")
resultado_label.pack()

root.mainloop()

