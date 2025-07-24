from flask import Flask, render_template
import redis
import threading
import time
from utils import (
    REDIS_HOST,
    REDIS_PORT,
    RED_ALERT_WAREHOUSE,
    YELLOW_ALERT_WAREHOUSE,
    RED_ALERT_PRODUCT_STOCK,
    LOG_RESTOCK_KEY,
    LOG_CONSUMPTION_KEY,
    MAX_LOG
)

app = Flask(__name__)
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# Intervalo de atualização (segundos)
REFRESH_INTERVAL = 2

# Função para obter dia de simulação
def fetch_simulation_day():
    try:
        day = int(r.get("simulation:day") or 0)
    except (redis.exceptions.RedisError, ValueError):
        day = 0
    return day

# Função para ler os dados do Kanban (peças e produtos)
def fetch_kanban_data():
    # Produtos acabados
    product_keys = sorted(r.scan_iter("product:*"))
    products = []
    for key in product_keys:
        name = key.split(':')[-1]
        count = int(r.get(key) or 0)
        color = ('green' if count >= RED_ALERT_PRODUCT_STOCK * 2 else
                 'yellow' if count >= RED_ALERT_PRODUCT_STOCK else
                 'red')
        products.append({'name': name, 'count': count, 'color': color})

    # Peças no almoxarifado
    warehouse_keys = sorted(r.scan_iter("warehouse:part:*"))
    parts = []
    for key in warehouse_keys:
        name = key.split(':')[-1]
        count = int(r.get(key) or 0)
        color = ('green' if count >= YELLOW_ALERT_WAREHOUSE else
                 'yellow' if count >= RED_ALERT_WAREHOUSE else
                 'red')
        parts.append({'name': name, 'count': count, 'color': color})

    return products, parts

# Função para obter logs de requisições de reabastecimento
def fetch_restock_logs():
    # Lista mais recentes no Redis (LPUSH na simulação)
    return r.lrange(LOG_RESTOCK_KEY, 0, MAX_LOG - 1) or []

# Função para obter logs de consumo de produtos
def fetch_consumption_logs():
    return r.lrange(LOG_CONSUMPTION_KEY, 0, MAX_LOG - 1) or []

@app.route("/")
def index():
    sim_day = fetch_simulation_day()
    products, parts = fetch_kanban_data()
    restock_logs = fetch_restock_logs()
    consumption_logs = fetch_consumption_logs()
    return render_template(
        'index.html',
        sim_day=sim_day,
        products=products,
        parts=parts,
        restocks=restock_logs,
        consumptions=consumption_logs,
        refresh=REFRESH_INTERVAL
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)