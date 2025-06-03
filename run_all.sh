#!/bin/bash
#./run_all.sh
echo "🧩 確認並安裝缺少的 Python 套件..."
source /Users/jamie/Desktop/農友日記/venv/bin/activate
pip install --quiet python-multipart

echo "🔧 啟動後端..."
bash /Users/jamie/Desktop/農友日記/run_backend.sh &

# 等待後端啟動穩定
echo "⏳ 等待後端啟動中（3秒）..."
sleep 3

# 啟動前端
FRONTEND_PATH="/Users/jamie/Desktop/農友日記/final_frontend"
if [ -d "$FRONTEND_PATH" ]; then
  echo "🚀 啟動前端..."
  cd "$FRONTEND_PATH" || exit
  npm run dev &
else
  echo "❌ 找不到前端目錄：$FRONTEND_PATH"
  exit 1
fi

echo "✅ 前後端都已啟動！請在瀏覽器中訪問 http://localhost:5173 或 5176（依照你實際設定）"

wait