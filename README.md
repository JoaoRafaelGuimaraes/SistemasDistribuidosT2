# Warehouse - T2 de sistemas Distribuídos

## Dependências 
```bash
pip3 install -U docker.io redis threading matplotlib numpy random 
```
## Execução

Para **executar** todos os arquivos necessários, basta executar o script **./start_simulation.sh**.
* Na primeira execução, esse processo pode demorar, haja visto que irá baixar a imagem do Redis.

Para **parar** a execução dos processos, basta executar o script **./stop_simulation.sh**.
* Caso não seja executado, o programa continuará sendo executado em paralelo e consumindo memória

## Objetivo
Desenvolver um sistema distribuído de controle de estoque para garantir que não ocorra ruptura na fabricação por falta de partes.

### Cenário:
<img width="633" height="375" alt="Image" src="https://github.com/user-attachments/assets/ab91e20f-8eac-4a9c-acc4-920f48eb459c" />

**2 Fábricas:**
* Fábrica 1 (Fabricação Empurrada): 5 linhas, produção com lote fixo.
* Fábrica 2 (Fabricação Puxada): 8 linhas, produção com lote variável, baseada em demanda de mercado.
  
**5 versões de produto:** Cada uma com uma lista de materiais diferentes.

**100 tipos de peças:**
* Kit base: 43 peças comuns a todos.
* Kit de variação: 20 a 33 peças específicas por versão.

## Demonstração 🎥

Clique na imagem abaixo para assistir à demonstração do projeto no YouTube:

[![Vídeo de demonstração](https://img.youtube.com/vi/CchOLr5CZqo/0.jpg)](https://youtu.be/CchOLr5CZqo)


