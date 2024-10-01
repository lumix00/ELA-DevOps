import tkinter as tk

def create_letter_sidebar(sidebar, letters):
    """Adiciona letras em um sidebar, quebrando linhas conforme necessário."""
    # Cria um Frame para armazenar as letras
    letter_frame = tk.Frame(sidebar, bg="#f0f0f0")

    # Variáveis para controle de largura
    current_width = 0
    max_width = sidebar.winfo_width() - 20  # Margem de 10px em cada lado

    # Adiciona as letras como Labels no Frame
    for letter in letters:
        label = tk.Label(letter_frame, text=letter, font=("Arial", 24), bg="#f0f0f0")
        label.pack(side=tk.LEFT)  # Adiciona os Labels na horizontal

        # Atualiza a largura atual
        current_width += label.winfo_reqwidth()

        # Verifica se a largura atual excede o limite
        if current_width > max_width:
            # Adiciona o Frame da linha anterior ao sidebar
            letter_frame.pack(side=tk.TOP)  # Adiciona uma nova linha
            letter_frame = tk.Frame(sidebar, bg="#f0f0f0")  # Novo Frame para a nova linha
            current_width = label.winfo_reqwidth()  # Reinicia o contador de largura com a nova letra

    # Adiciona o último Frame
    letter_frame.pack(side=tk.TOP, padx=10, pady=10)

# Cria a janela principal
root = tk.Tk()
root.title("Caixa Lateral")
root.geometry("800x600")  # Define o tamanho da janela (largura x altura)

# Define a largura da caixa lateral como 20% da largura da janela
sidebar_width = int(root.winfo_screenwidth() * 0.2)

# Cria a caixa lateral
sidebar = tk.Frame(root, width=sidebar_width, height=root.winfo_height(), bg="#f0f0f0")
sidebar.pack(side=tk.RIGHT, fill=tk.Y)

# Array de letras e espaços
letters = ['A', 'B', 'C', ' ', 'D', 'E', 'F', 'G', ' ', 
           'A', 'B', 'C', ' ', 'D', 'E', 'F', 'G', ' ', 
           'A', 'B', 'C', ' ', 'D', 'E', 'F', 'G', ' ', 
           'A', 'B', 'C', ' ', 'D', 'E', 'F', 'G', ' ', 
           'A', 'B', 'C', ' ', 'D', 'E', 'F', 'G', ' ', 
           'A', 'B', 'C', ' ', 'D', 'E', 'F', 'G', ' ', 
           'A', 'B', 'C', ' ', 'D', 'E', 'F', 'G', ' ', 
           'A', 'B', 'C', ' ', 'D', 'E', 'F', 'G', ' ', 
           'A', 'B', 'C', ' ', 'D', 'E', 'F', 'G', ' ', 
           'A', 'B', 'C', ' ', 'D', 'E', 'F', 'G', ' ', 
           'A', 'B', 'C', ' ', 'D', 'E', 'F', 'G', ' ']

# Chama a função para criar a sidebar com as letras
create_letter_sidebar(sidebar, letters)

# Inicia o loop da interface gráfica
root.mainloop()
