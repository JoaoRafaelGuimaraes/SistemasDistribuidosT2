#!/bin/bash

echo "Encerrando todos os processos da simulação..."

# Mata todos os scripts Python relacionados à simulação
pkill -f supplier_redis.py
pkill -f warehouse_redis.py
pkill -f line_redis.py
pkill -f factory_redis.py
pkill -f product_stock_redis.py
pkill -f kanban_web.py

echo "Todos os processos foram encerrados."

