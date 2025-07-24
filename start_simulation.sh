#!/bin/bash

echo "=== (Re)criando container redis-sim ==="
# Remove qualquer container antigo (parado ou em execução)
docker rm -f redis-sim >/dev/null 2>&1 || true

# Cria e inicia um novo container, mapeando a porta 6379
docker run -d \
  --name redis-sim \
  -p 6379:6379 \
  redis:7 \
  >/dev/null
echo "→ Container redis-sim criado e rodando (porta 6379 mapeada)"

# Aguarda o Redis ficar disponível dentro do container
echo "=== Aguardando Redis ficar disponível dentro do container ==="
for i in {1..10}; do
  if docker exec redis-sim redis-cli ping 2>/dev/null | grep -q PONG; then
    echo "→ Redis respondeu no container!"
    break
  fi
  echo "→ Tentativa $i: aguardando 1s..."
  sleep 1
done

if ! docker exec redis-sim redis-cli ping 2>/dev/null | grep -q PONG; then
  echo "[ERRO] Redis não respondeu após 10s. Abortando."
  exit 1
fi

# Cria diretório de logs se não existir e limpa logs antigos
mkdir -p debug_logs
rm -f debug_logs/*.log

echo "=== Inicializando dados no Redis ==="
python3 init_redis.py

echo "=== Iniciando serviços Python ==="
# Fornecedor
python3 supplier_redis.py    > debug_logs/supplier.log    &

# Almoxarifado
python3 warehouse_redis.py   > debug_logs/warehouse.log   &

# Linhas da Fábrica 1 (empurrada)
for i in {1..5}; do
  echo "Iniciando linha $i da Fábrica 1 (empurrada)..."
  python3 line_redis.py $i 1 > debug_logs/line1_$i.log &
done

# Linhas da Fábrica 2 (puxada)
for i in {1..8}; do
  echo "Iniciando linha $i da Fábrica 2 (puxada)..."
  python3 line_redis.py $i 2 > debug_logs/line2_$i.log &
done

# Fábricas
echo "Iniciando Fábrica 1 (empurrada)..."
python3 factory_redis.py empurrada 1 5 > debug_logs/factory1.log &

echo "Iniciando Fábrica 2 (puxada)..."
python3 factory_redis.py puxada     2 8 > debug_logs/factory2.log &

# Estoque de produtos acabados (simulador de clientes)
echo "Iniciando estoque de produtos acabados..."
python3 product_stock_redis.py > debug_logs/product_stock.log &

# Kanban Web (Flask)
echo "Iniciando Kanban Web..."
python3 kanban_web.py > debug_logs/kanban_web.log &

echo ">>> Simulação iniciada! Acesse http://localhost:5000 para ver o Kanban."


