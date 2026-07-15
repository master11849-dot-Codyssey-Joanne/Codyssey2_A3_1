# 이 파일은 "api/recommend.py" 입니다.
# 웹페이지에서 보낸 정보를 받아 OpenAI에게 질문하고, 그 대답을 다시 웹페이지로 돌려보냅니다.

from http.server import BaseHTTPRequestHandler
import json
import os
from openai import OpenAI

# Vercel 환경에서 파이썬을 실행하기 위한 기본 규칙(클래스)입니다.
class handler(BaseHTTPRequestHandler):
    
    # POST 방식(데이터를 숨겨서 안전하게 보내는 방식)으로 요청이 들어왔을 때 실행됩니다.
    def do_POST(self):
        try:
            # 1. 프론트엔드(app.js)에서 보낸 정보(나이, 금액, 성향)를 읽어옵니다.
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            age = data.get('age')
            amount = data.get('amount')
            risk_type = data.get('type')

            # 2. 보안 설정: 깃허브에 올리지 않은 환경변수(비밀 금고)에서 API 키를 몰래 꺼내옵니다.
            api_key = os.environ.get("OPENAI_API_KEY")
            
            # API 키가 없으면 에러를 발생시킵니다.
            if not api_key:
                raise ValueError("API 키가 설정되지 않았습니다.")

            # OpenAI 클라이언트를 준비합니다.
            client = OpenAI(api_key=api_key)
            
            # 3. AI에게 내릴 '지시문(Prompt)'을 작성합니다. (이 부분이 우리 서비스의 핵심 독창성입니다!)
            # 성향에 따라 한국어로 명확하게 변환해 줍니다.
            risk_text = "공격형" if risk_type == 'aggressive' else "안정추구형"
            
            system_prompt = f"""
            당신은 전통 금융 자산과 비트코인 등 디지털 자산의 알고리즘 트레이딩에 정통한 최고 수준의 자산운용 설계사입니다.
            사용자의 나이({age}세), 운용 가능 금액({amount}원), 투자 성향({risk_text})을 바탕으로 최적의 포트폴리오를 구성해주세요.

            [필수 포함 조건]
            1. 주식, 채권뿐만 아니라 '디지털 자산(비트코인 중심)'을 반드시 포함하여 배분할 것. 
               - 안정추구형이더라도 포트폴리오 헷징(방어) 목적으로 비트코인을 1~5% 내외로 논리적으로 편입시킬 것.
            2. 비율(%)뿐만 아니라, 입력받은 금액({amount}원)을 기준으로 **정확한 배분 금액**을 원 단위로 명시할 것.
            3. 각 자산군별 추천 종목(예: S&P500 ETF, 비트코인 등)과 그 추천 사유를 전문적이지만 초보자가 이해하기 쉽게 설명할 것.
            4. 출력은 HTML 태그 없이 깔끔한 텍스트와 번호 매기기, 줄바꿈을 활용하여 가독성 좋게 작성할 것.
            """

            # 4. OpenAI 서버에 질문(프롬프트)을 전송하고 답변을 기다립니다.
            response = client.chat.completions.create(
                model="gpt-3.5-turbo", # 빠르고 가성비 좋은 모델을 사용합니다.
                messages=[
                    {"role": "system", "content": "당신은 냉철하고 분석적인 AI 자산관리사입니다."},
                    {"role": "user", "content": system_prompt}
                ],
                temperature=0.7 # 0에 가까울수록 기계적, 1에 가까울수록 창의적 답변이 나옵니다.
            )
            
            # AI가 준 답변의 텍스트만 쏙 뽑아냅니다.
            ai_result = response.choices[0].message.content
            
            # 5. 성공적으로 답변을 받았다고 프론트엔드에 알려주고(상태코드 200), 결과를 JSON 형태로 돌려보냅니다.
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response_data = {"recommendation": ai_result}
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            
        except Exception as e:
            # [안전장치] 만약 위 과정 중 하나라도 실패하면(에러), 500 에러와 함께 실패 이유를 프론트엔드로 보냅니다.
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_data = {"error": str(e)}
            self.wfile.write(json.dumps(error_data).encode('utf-8'))