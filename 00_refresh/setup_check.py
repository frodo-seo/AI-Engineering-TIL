"""Day 2. 환경이 제대로 세팅됐는지 확인한다.

- .env에서 ANTHROPIC_API_KEY를 읽어오는가?
- anthropic SDK가 설치돼 있는가?
- 실제 API에 ping이 가는가? (아주 짧은 메시지 1회)
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("[FAIL] ANTHROPIC_API_KEY가 .env에 없음. .env.example을 복사해서 채워넣어라.")
    sys.exit(1)

print(f"[OK] API key loaded (prefix: {api_key[:10]}...)")

try:
    from anthropic import Anthropic
except ImportError:
    print("[FAIL] anthropic 패키지 없음. `pip install -r requirements.txt` 실행.")
    sys.exit(1)

print("[OK] anthropic SDK import 성공")

client = Anthropic()

resp = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=32,
    messages=[{"role": "user", "content": "Say 'pong' and nothing else."}],
)

print(f"[OK] API 응답: {resp.content[0].text}")
print(f"     input_tokens={resp.usage.input_tokens}, output_tokens={resp.usage.output_tokens}")
print("\n셋업 완료. Day 3로 가자.")
