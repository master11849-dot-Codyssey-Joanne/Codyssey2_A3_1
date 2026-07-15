/* 이 파일은 "app.js"입니다.
  웹페이지의 버튼 클릭, 화면 전환, 그리고 AI 서버와의 통신을 담당합니다.
*/

// =====================================================================
// 1. HTML에 있는 '방(섹션)'과 '버튼'들을 자바스크립트로 불러와서 이름표를 붙여줍니다.
// =====================================================================
const homeSection = document.getElementById('home-section');
const inputSection = document.getElementById('input-section');
const resultSection = document.getElementById('result-section');

const startBtn = document.getElementById('start-btn');
const submitBtn = document.getElementById('submit-btn');
const retryBtn = document.getElementById('retry-btn');
const menuHome = document.getElementById('menu-home');
const menuInput = document.getElementById('menu-input');

// =====================================================================
// 2. 화면을 부드럽게 전환하는 마법의 함수 만들기
// =====================================================================
// 모든 방을 다 숨기고(hidden 추가), 내가 원하는 방만 보여주는(active 추가) 기능입니다.
function showSection(sectionToShow) {
    // 1) 일단 3개의 방을 모두 숨깁니다.
    homeSection.classList.add('hidden');
    homeSection.classList.remove('active');
    
    inputSection.classList.add('hidden');
    inputSection.classList.remove('active');
    
    resultSection.classList.add('hidden');
    resultSection.classList.remove('active');

    // 2) 내가 띄우고 싶은 방만 다시 보여줍니다.
    sectionToShow.classList.remove('hidden');
    sectionToShow.classList.add('active');

    // 3) 상단 메뉴바의 글씨 색상도 현재 화면에 맞춰서 진하게 바꿔줍니다.
    menuHome.classList.remove('active');
    menuInput.classList.remove('active');
    if (sectionToShow === homeSection) {
        menuHome.classList.add('active');
    } else {
        menuInput.classList.add('active');
    }
}

// =====================================================================
// 3. 단순 버튼 클릭 이벤트 연결하기 (클릭하면 화면 이동)
// =====================================================================
// "내 포트폴리오 설계받기" 버튼 누르면 -> 입력 화면으로 이동
startBtn.addEventListener('click', () => {
    showSection(inputSection);
});

// 상단 "홈" 메뉴 누르면 -> 첫 화면으로 이동
menuHome.addEventListener('click', () => {
    showSection(homeSection);
});

// 상단 "설계하기" 메뉴 누르면 -> 입력 화면으로 이동
menuInput.addEventListener('click', () => {
    showSection(inputSection);
});

// 결과 화면에서 "다시 설계하기" 누르면 -> 입력 화면으로 이동 (입력칸 초기화 포함)
retryBtn.addEventListener('click', () => {
    document.getElementById('age').value = '';     // 나이 빈칸으로
    document.getElementById('amount').value = '';  // 금액 빈칸으로
    showSection(inputSection);
});

// =====================================================================
// 4. (핵심) "포트폴리오 생성하기" 버튼을 눌렀을 때 실행되는 AI 호출 로직
// =====================================================================
// async는 "이 작업은 시간이 좀 걸릴 수 있으니(서버 통신) 기다려주며 처리해라"는 뜻입니다.
submitBtn.addEventListener('click', async () => {
    
    // 사용자가 입력한 값들과 에러/로딩 상자를 불러옵니다.
    const age = document.getElementById('age').value;
    const amount = document.getElementById('amount').value;
    const riskType = document.querySelector('input[name="risk-type"]:checked').value;
    
    const errorMsg = document.getElementById('error-msg');
    const loadingBox = document.getElementById('loading-box');

    // [안전장치 1] 빈 입력값(필수값 누락) 검사
    if (!age || !amount) {
        errorMsg.textContent = "나이와 자산운용금액을 모두 정확하게 입력해 주세요.";
        errorMsg.classList.remove('hidden'); // 에러 상자 보여주기
        return; // 여기서 멈추고 밑으로 안 내려갑니다. (서버로 안 보냄)
    }

    // 에러 상자가 켜져 있었다면 다시 숨깁니다.
    errorMsg.classList.add('hidden');
    
    // [안전장치 2] 로딩 중 표시 & 버튼 중복 클릭 방지 (과금 방지)
    loadingBox.classList.remove('hidden');
    submitBtn.disabled = true; // 사용자가 연타하지 못하게 버튼을 끕니다.
    submitBtn.textContent = "AI 분석 중..."; // 버튼 글씨 변경
    submitBtn.style.opacity = "0.5"; // 버튼을 살짝 투명하게

    try {
        // 백엔드 API로 데이터 보내기 (fetch 함수 사용)
        const response = await fetch('/api/recommend', {
            method: 'POST', // 정보를 숨겨서 안전하게 보냅니다.
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ age: age, amount: amount, type: riskType }) // 입력한 정보를 예쁘게 포장해서 보냅니다.
        });

        // [안전장치 3] API 오류(4xx/5xx) 실패 처리
        if (!response.ok) {
            throw new Error("서버 응답 오류가 발생했습니다."); 
        }

        // 성공적으로 AI의 답변을 받아서 글자로 풉니다.
        const data = await response.json();
        
        // 화면을 결과 창으로 넘기고, AI가 준 텍스트를 화면에 뿌려줍니다.
        document.getElementById('ai-result-content').textContent = data.recommendation;
        showSection(resultSection);

    } catch (error) {
        // [안전장치 4] 지연/타임아웃 등 에러 발생 시 사용자 안내
        errorMsg.textContent = "AI 연결이 지연되거나 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.";
        errorMsg.classList.remove('hidden');
        console.error("API Fetch Error:", error);
    } finally {
        // 결과가 성공했든 실패했든 무조건 마지막에 실행되는 정리 작업입니다.
        loadingBox.classList.add('hidden'); // 로딩 숨기기
        submitBtn.disabled = false; // 버튼 다시 켜주기
        submitBtn.textContent = "포트폴리오 생성하기"; // 버튼 글씨 원래대로
        submitBtn.style.opacity = "1";
    }
});