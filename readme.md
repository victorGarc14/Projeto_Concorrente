# 🚦 Simulação de Tráfego com Threads em Python

Este projeto implementa uma simulação de tráfego urbano utilizando **threads** em Python, onde múltiplos veículos (carros e ambulância) trafegam simultaneamente por uma malha de ruas com cruzamentos controlados por semáforos.

A simulação possui interface gráfica simples usando **Tkinter**, com suporte a sprites e animação básica.

---

## 🎯 Objetivo

Demonstrar conceitos de:

- Concorrência com threads
- Sincronização (locks e condições)
- Problemas clássicos (acesso a recursos compartilhados)
- Visualização gráfica de estados concorrentes

---

## 🧠 Conceitos Aplicados

- Threads (`threading.Thread`)
- Locks
- Exclusão mútua
- Simulação baseada em tempo (clock global)

---

## 🚗 Tipos de Veículos

- **CR** → Carro rápido (vermelho)
- **CM** → Carro médio (laranja)
- **CL** → Carro lento (amarelo)
- **AM** → Ambulância (prioridade)

---

## 🚦 Semáforos

Os semáforos controlam o fluxo nos cruzamentos:

- **L** → Libera tráfego horizontal (linhas)
- **C** → Libera tráfego vertical (colunas)

A ambulância pode forçar a abertura do semáforo.

---

## 🖥️ Interface Gráfica

A interface mostra:

- A malha de ruas
- Veículos em tempo real
- Estado dos semáforos

Atualização baseada em:

```python
root.after(100, atualizar)
```

## 🎮 Funcionamento

- Cada veículo é uma thread independente
- O Clock sincroniza o tempo global
- Os veículos consultam a malha para decidir movimentos
- Semáforos controlam acesso a cruzamentos
- A GUI renderiza o estado atual continuamente

## Executar o projeto


---

### 🔹 1. Clonar ou baixar o projeto

Via Git:

```bash
git clone <repo-url>
cd Projeto_Concorrente
```

---

### 🔹 2 (Opcional) Criar ambiente virtual

No terminal (PowerShell ou CMD):

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

### 🔹 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

### 🔹 4. Executar o projeto

```bash
cd Projeto_Concorrente
python main.py
```

---

## 👨‍💻 Autores
