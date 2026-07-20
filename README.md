# 1. 서비스 소개

## "복잡하고 머리 아픈 자산 설계는 이제 그만!"
'맡겨봐!'는 사용자의 기본 정보(나이, 자산운용금액, 투자 성향)를 바탕으로 최적의 자산 배분 포트폴리오를 단 몇 초 만에 제안해 주는 AI 기반 웹 서비스입니다.

- **핵심 가치**: 금융 지식이 부족한 초보자도 전문가 수준의 포트폴리오를 쉽게 받아보고 즉각적인 투자 방향을 설정할 수 있습니다.
  
- **차별화 포인트 (트렌디한 자산 배분)**: 전통적인 주식과 채권 위주의 배분을 넘어, 최신 투자 트렌드에 맞게 비트코인 등 디지털 자산을 리스크 헷징 및 수익 극대화 수단으로 논리적으로 편입하여 제안합니다.

- **사용자 경험 (UX/UI)**: 신뢰감을 주면서도 직관적인 사용을 위해, 여백이 넉넉하고 부드러운 애니메이션이 적용된 '애플(Apple) 스타일의 클린 라이트 모드' UI를 적용했습니다.



# 2. 기술 스택

## Frontend

- HTML5 / CSS3: 반응형 웹 디자인 및 애플 스타일 UI/UX 구현 (순수 바닐라 환경)
- JavaScript (Vanilla): Single Page Application(SPA) 형태의 부드러운 화면 전환 및 비동기 API 통신(Fetch) 처리

## Backend & AI

- Python (3.14.6 Version): BaseHTTPRequestHandler를 활용한 API 엔드포인트 구축
- Google Gemini 2.5 Flash: 빠르고 강력한 최신 LLM을 활용한 맞춤형 프롬프트 엔지니어링 및 응답 생성 (google-genai 라이브러리 사용)
- Vercel Serverless Functions: 별도의 서버 구축 없이 파이썬 백엔드 코드를 서버리스 환경에서 구동 (api/ 디렉토리 라우팅)

## Version Control & Deployment

- Git / GitHub / SourceTree: 소스 코드 버전 관리 및 원격 저장소 연동
- Vercel: 프론트엔드 호스팅 및 백엔드 서버리스 통합 배포, CI/CD 자동



# 3. 실행 및 배포 방법

## 로컬 환경 실행 방법 (Local Development)

1. 저장소를 클론(Clone)하거나 다운로드합니다.
2. 프로젝트 최상단 루트 디렉토리에 .env 파일을 생성하고 발급받은 API 키를 입력합니다. (상세 내용은 하단 '환경 변수 설정' 참고)
3. 로컬에서 웹 서버를 실행하여 index.html을 열고 프론트엔드 UI를 확인합니다. (단, 파이썬 서버리스 함수 테스트를 위해서는 Vercel CLI 설치가 필요할 수 있습니다.)

## Vercel 배포 방법 (Deployment)

1. Vercel에 접속하여 깃허브 계정으로 로그인합니다.
2. Add New -> Project를 선택하고, 본 프로젝트의 깃허브 저장소를 Import 합니다.
3. Application Preset 항목을 반드시 Python이 아닌 Other로 설정합니다.
4. Environment Variables 항목에 API 키를 등록합니다.
5. [Deploy] 버튼을 눌러 배포를 완료합니다.


# 4. 배포 URL
- 서비스 바로가기: codyssey2-a3-1-29mg.vercel.app


  
# 5. 환경 변수(키) 설정 방법
본 서비스는 구글 Gemini API를 사용하며, 보안을 위해 API 키는 소스 코드에 직접 노출하지 않고 환경 변수로 분리하여 안전하게 관리합니다.

## 로컬 작업 시 설정 (.env)

1. 프로젝트 최상단 폴더에 .env 라는 이름의 텍스트 파일을 생성합니다.
2. 파일 내부에 아래와 같이 변수명과 API 키를 작성하고 저장합니다.
  GEMINI_API_KEY="본인의_실제_구글_제미나이_API_키_입력"
3. 주의: API 키 유출을 막기 위해 .gitignore 파일에 .env가 반드시 포함되어 있어야 합니다.
   
## Vercel 배포 시 설정 (Dashboard)

1. Vercel 배포 화면(또는 배포된 프로젝트의 Settings -> Environment Variables 탭)으로 이동합니다.
2. 아래와 같이 Key와 Value를 정확히 입력하고 [Add] 버튼을 눌러 저장합니다.
- Key: GEMINI_API_KEY
- Value: 본인의_실제_구글_제미나이_API_키
3. 설정이 완료된 후, 변경 사항을 적용하기 위해 [Redeploy](재배포)를 수행하면 AI 기능이 정상적으로 활성화됩니다.
