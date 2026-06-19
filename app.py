from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# AI API 配置（兼容 OpenAI 格式）
AI_API_URL = "https://api.openai.com/v1/chat/completions"
AI_API_KEY = "your-api-key-here"

def call_ai(prompt, system_msg="你是一个有用的AI助手"):
    """调用 AI API"""
    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    try:
        resp = requests.post(AI_API_URL, headers=headers, json=data, timeout=30)
        result = resp.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"错误: {str(e)}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/optimize", methods=["POST"])
def optimize_text():
    """文本优化"""
    text = request.json.get("text", "")
    mode = request.json.get("mode", "polish")
    
    prompts = {
        "polish": f"请润色以下文本，保持原意但让表达更优美：\n\n{text}",
        "rewrite": f"请改写以下文本，用不同的表达方式：\n\n{text}",
        "translate_en": f"请将以下文本翻译成英文：\n\n{text}",
        "translate_zh": f"请将以下文本翻译成中文：\n\n{text}"
    }
    
    result = call_ai(prompts.get(mode, prompts["polish"]))
    return jsonify({"result": result})

@app.route("/api/prompt", methods=["POST"])
def generate_prompt():
    """生成 AI 绘画提示词"""
    desc = request.json.get("description", "")
    style = request.json.get("style", "realistic")
    
    prompt = f"""请根据以下描述生成一个高质量的AI绘画提示词（英文）：
    
描述: {desc}
风格: {style}

要求：
1. 包含主体、细节、光线、构图等要素
2. 使用常见的AI绘画关键词
3. 输出格式：正面提示词 + 负面提示词"""
    
    result = call_ai(prompt, system_msg="你是一个专业的AI绘画提示词生成专家")
    return jsonify({"result": result})

@app.route("/api/code", methods=["POST"])
def generate_code():
    """生成代码片段"""
    desc = request.json.get("description", "")
    lang = request.json.get("language", "python")
    
    prompt = f"请用 {lang} 编写以下功能的代码：\n\n{desc}\n\n要求：代码简洁、有注释、可直接运行。"
    
    result = call_ai(prompt, system_msg="你是一个资深程序员")
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
