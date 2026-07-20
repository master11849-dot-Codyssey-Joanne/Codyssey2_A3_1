# 이 파일은 "api/recommend.py" 입니다.
# 웹페이지에서 보낸 정보를 받아 최신 'Gemini 2.5 Flash'에게 질문하고, 그 대답을 다시 돌려보냅니다.

from http.server import BaseHTTPRequestHandler
import json
import os
from google import genai # 최신 구글 Gemini 라이브러리를 불러옵니다.

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

            # 2. Vercel 환경변수(비밀 금고)에서 Gemini API 키를 몰래 꺼내옵니다.
            api_key = os.environ.get("GEMINI_API_KEY")
            
            if not api_key:
                raise ValueError("API 키가 설정되지 않았습니다.")

            # 최신 클라이언트 방식으로 Gemini와 연결할 준비를 합니다.
            client = genai.Client(api_key=api_key)
            
            # 3. AI에게 내릴 프롬프트(지시문) 작성 (우리의 핵심 독창성!)
            risk_text = "공격형" if risk_type == 'aggressive' else "안정추구형"
            
            prompt = f"""
            당신은 전통 금융 자산과 비트코인 등 디지털 자산의 알고리즘 트레이딩에 정통한 최고 수준의 자산운용 설계사입니다.
            사용자의 나이({age}세), 운용 가능 금액({amount}원), 투자 성향({risk_text})을 바탕으로 최적의 포트폴리오를 구성해주세요.

            [필수 포함 조건]
            1. 주식, 채권뿐만 아니라 '디지털 자산(비트코인 중심)'을 반드시 포함하여 배분할 것. 
               - 안정추구형이더라도 포트폴리오 헷징(방어) 목적으로 비트코인을 1~5% 내외로 논리적으로 편입시킬 것.
            2. 비율(%)뿐만 아니라, 입력받은 금액({amount}원)을 기준으로 **정확한 배분 금액**을 원 단위로 명시할 것.
            3. 각 자산군별 추천 종목(예: S&P500 ETF, 비트코인 등)과 그 추천 사유를 전문적이지만 초보자가 이해하기 쉽게 설명할 것.
            4. 출력은 HTML 태그 없이 깔끔한 텍스트와 번호 매기기, 줄바꿈을 활용하여 가독성 좋게 작성할 것.
            """

            # 4. Gemini 2.5 Flash 모델에게 질문을 보내고 답변을 기다립니다.
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            ai_result = response.text
            
            # 5. 성공적으로 답변을 받았다고 웹페이지에 알려주고, 결과를 예쁘게 포장(JSON)해서 돌려보냅니다.
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response_data = {"recommendation": ai_result}
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            
        except Exception as e:
            # [안전장치] 만약 에러가 발생하면, 서버가 멈추지 않고 화면에 에러 내용을 알려줍니다.
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_data = {"error": str(e)}
            self.wfile.write(json.dumps(error_data).encode('utf-8'))