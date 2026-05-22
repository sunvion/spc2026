// 일단 DOM이 로딩된 다음에
document.addEventListener('DOMContentLoaded', () => {
    const chatInput = document.getElementById('user-input');
    const formInput = document.getElementById('user-input-form');
    const resultDiv = document.getElementById('result');

    formInput.addEventListener('submit', async (ev) => {
        ev.preventDefault();

        const chatMessage = chatInput.value;
        // console.log(chatMessage); // 실무적으론 이렇게 나의 디버그 코드를 올리면 안된다.
        // minifying 도구를 이용해서 해결하거나 모든 주석, 공백 제거 및 변수명은 짧게 치환하고 패키징해서 배포

        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({chatMessage})
        });
        
        const data = await response.json()
        console.log(data)
        // .then(response => response.json()
        // ).then(data => 
        //     console.log(data)
        // )
        // TODO: 응답 받아서 처리하기

        const chatbotReply = document.createElement('p')
        chatbotReply.innerText = data.reply;
        resultDiv.appendChild(chatbotReply);

        // TODO 위에 리팩티로이해서 적절하게 분리, fetch 하는 거 분리하고 응답받아서 DOM에 그리는 것 분리
    })
})