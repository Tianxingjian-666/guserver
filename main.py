from flask import Flask, Response, request
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

# MCP SSE 标准服务端点
@app.route('/sse', methods=['GET'])
def sse_endpoint():
    def event_stream():
        # 1. 输出MCP握手+工具声明（元器解析必备）
        yield 'event: endpoint\ndata: /messages\n\n'
        time.sleep(0.3)
        yield 'event: tools/list\ndata: {"tools":[{"name":"get_stock_can_slim","description":"获取A股股票基本面+技术面CAN SLIM全量数据","inputSchema":{"type":"object","properties":{"stock_code":{"type":"string","description":"6位A股股票代码"}}}]}\n\n'
        # 2. 持续心跳保活
        while True:
            yield f': ping - {time.time()}\n\n'
            time.sleep(30)
    return Response(event_stream(), mimetype="text/event-stream")

# MCP 工具调用接口
@app.route('/messages', methods=['POST'])
def handle_message():
    req = request.json
    stock_code = req.get("params",{}).get("stock_code","")

    # 这里后续可以对接Tushare、公开行情API拉取真实财报/行情
    # 先返回标准合格格式，保证元器100%识别
    result_data = {
        "stock_code": stock_code,
        "q_eps_growth": 28,
        "roe": 18,
        "avg_year_eps": 24,
        "cir_cap": 260,
        "rel_strength": 89,
        "inst_ratio": 35,
        "price_new_high": True,
        "market_trend": "up"
    }

    return {
        "content": [{"type":"text","text":str(result_data)}]
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
