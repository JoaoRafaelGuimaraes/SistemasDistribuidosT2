# kanban_visualizer_local.py

import redis
import time
import matplotlib.pyplot as plt
from utils import (
    REDIS_HOST,
    REDIS_PORT,
    RED_ALERT_LINE,
    YELLOW_ALERT_LINE,
    RED_ALERT_WAREHOUSE,
    YELLOW_ALERT_WAREHOUSE,
    RED_ALERT_PRODUCT_STOCK,
    NUM_PARTS,
    NUM_PRODUCTS
)

plt.ion()  # Modo interativo

def connect_to_redis():
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        r.ping()
        return r
    except redis.exceptions.ConnectionError:
        print(f"[ERRO] Falha ao conectar no Redis em {REDIS_HOST}:{REDIS_PORT}")
        return None

def get_kanban_color(value, red_limit, yellow_limit):
    if value < red_limit:
        return 'red'
    elif value < yellow_limit:
        return 'orange'
    else:
        return 'green'

def fetch_data(r):
    warehouse_keys = [f"warehouse:part:{i}" for i in range(NUM_PARTS)]
    warehouse_values = list(map(lambda v: int(v or 0), r.mget(warehouse_keys)))

    product_keys = [f"product:{i}" for i in range(NUM_PRODUCTS)]
    product_values = list(map(lambda v: int(v or 0), r.mget(product_keys)))

    return warehouse_values, product_values

def run_visualizer():
    r = connect_to_redis()
    if not r:
        return

    fig, axs = plt.subplots(2, 1, figsize=(12, 7))
    fig.suptitle('Kanban de Estoques (Tempo Real)', fontsize=16)

    while True:
        warehouse_stock, product_stock = fetch_data(r)

        axs[0].cla()
        axs[1].cla()

        # Produtos acabados
        prod_colors = [get_kanban_color(v, RED_ALERT_PRODUCT_STOCK, RED_ALERT_PRODUCT_STOCK * 2) for v in product_stock]
        axs[0].bar([f"P{i+1}" for i in range(NUM_PRODUCTS)], product_stock, color=prod_colors)
        axs[0].set_title("Produtos Acabados")
        axs[0].set_ylim(0, max(product_stock + [RED_ALERT_PRODUCT_STOCK * 3]))
        axs[0].grid(True)

        # Almoxarifado
        sample_parts = warehouse_stock[:20]
        part_colors = [get_kanban_color(v, RED_ALERT_WAREHOUSE, YELLOW_ALERT_WAREHOUSE) for v in sample_parts]
        axs[1].bar([str(i+1) for i in range(20)], sample_parts, color=part_colors)
        axs[1].set_title("Peças no Almoxarifado (1–20)")
        axs[1].set_ylim(0, max(sample_parts + [RED_ALERT_WAREHOUSE * 1.5]))
        axs[1].grid(True)

        plt.pause(2)

if __name__ == "__main__":
    run_visualizer()
