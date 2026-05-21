/**
 * BOARD VIBE - Premium Client Side Application Logic
 * Powered by Fetch API, Glassmorphic Animations & XSS Protection
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM 요소 캐싱
    const postForm = document.getElementById('post-form');
    const titleInput = document.getElementById('title-input');
    const messageInput = document.getElementById('message-input');
    const submitBtn = document.getElementById('submit-btn');
    const postsContainer = document.getElementById('posts-container');
    const postsLoader = document.getElementById('posts-loader');
    const emptyState = document.getElementById('empty-state');
    const postsCountBadge = document.getElementById('posts-count');
    
    const titleCounter = document.getElementById('title-counter');
    const messageCounter = document.getElementById('message-counter');
    
    // Lucide 아이콘 초기 실행
    lucide.createIcons();

    // 초기 데이터 로딩
    loadPosts();

    // ==========================================================================
    // 1. 이벤트 리스너 설정
    // ==========================================================================
    
    // 폼 서브밋 핸들러
    postForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const title = titleInput.value.trim();
        const message = messageInput.value.trim();
        
        // 간단한 정적 유효성 검사
        if (!title) {
            showToast('제목을 입력해 주세요.', 'error');
            titleInput.focus();
            return;
        }
        if (!message) {
            showToast('내용을 입력해 주세요.', 'error');
            messageInput.focus();
            return;
        }
        
        await createPost(title, message);
    });

    // 제목 글자수 카운터 및 경고 효과
    titleInput.addEventListener('input', () => {
        const length = titleInput.value.length;
        titleCounter.textContent = `${length}/100`;
        
        titleCounter.className = 'char-counter';
        if (length >= 90) {
            titleCounter.classList.add('danger');
        } else if (length >= 70) {
            titleCounter.classList.add('warning');
        }
    });

    // 내용 글자수 카운터 및 경고 효과
    messageInput.addEventListener('input', () => {
        const length = messageInput.value.length;
        messageCounter.textContent = `${length}/1000`;
        
        messageCounter.className = 'char-counter';
        if (length >= 900) {
            messageCounter.classList.add('danger');
        } else if (length >= 700) {
            messageCounter.classList.add('warning');
        }
    });

    // ==========================================================================
    // 2. 핵심 비즈니스 로직 함수
    // ==========================================================================

    // API: 전체 게시글 가져오기 및 렌더링
    async function loadPosts() {
        showLoadingState(true);
        
        try {
            const response = await fetch('/api/posts');
            if (!response.ok) {
                throw new Error('서버 데이터를 가져오는 데 실패했습니다.');
            }
            
            const posts = await response.json();
            updatePostsCountBadge(posts.length);
            
            // 컨테이너 초기화
            postsContainer.innerHTML = '';
            
            if (posts.length === 0) {
                emptyState.classList.remove('hidden');
                postsContainer.classList.add('hidden');
            } else {
                emptyState.classList.add('hidden');
                postsContainer.classList.remove('hidden');
                
                posts.forEach(post => {
                    const cardHTML = createCardElement(post);
                    postsContainer.appendChild(cardHTML);
                });
                
                // 새로 렌더링된 요소들에 대해 Lucide 아이콘 적용
                lucide.createIcons();
            }
        } catch (error) {
            console.error(error);
            showToast(error.message || '게시글 목록을 로드하는 중 오류가 발생했습니다.', 'error');
        } finally {
            showLoadingState(false);
        }
    }

    // API: 신규 게시글 등록
    async function createPost(title, message) {
        setSubmitButtonLoading(true);
        
        try {
            const response = await fetch('/api/posts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title, message })
            });
            
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.error || '게시글 등록에 실패했습니다.');
            }
            
            showToast('생각 카드가 성공적으로 등록되었습니다!', 'success');
            
            // 입력 폼 리셋
            postForm.reset();
            titleCounter.textContent = '0/100';
            titleCounter.className = 'char-counter';
            messageCounter.textContent = '0/1000';
            messageCounter.className = 'char-counter';
            
            // 화면에 새 카드 즉시 추가 (비동기 실시간 렌더링으로 프리미엄 UX 구현)
            const newCard = createCardElement(result);
            
            if (postsContainer.classList.contains('hidden')) {
                postsContainer.classList.remove('hidden');
                emptyState.classList.add('hidden');
            }
            
            // 맨 앞에 새 카드 삽입
            postsContainer.insertBefore(newCard, postsContainer.firstChild);
            
            // 새 카드의 아이콘 초기화
            lucide.createIcons();
            
            // 카드 개수 갱신
            const currentCount = parseInt(postsCountBadge.textContent, 10);
            updatePostsCountBadge(currentCount + 1);
            
        } catch (error) {
            console.error(error);
            showToast(error.message, 'error');
        } finally {
            setSubmitButtonLoading(false);
        }
    }

    // API: 게시글 삭제
    async function deletePost(postId, cardElement) {
        try {
            const response = await fetch(`/api/posts/${postId}`, {
                method: 'DELETE'
            });
            
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.error || '게시글 삭제에 실패했습니다.');
            }
            
            // 삭제 애니메이션 적용 (Fade out & Shrink)
            cardElement.classList.add('fade-out');
            
            // 애니메이션 완료 후 DOM에서 완전히 제거
            cardElement.addEventListener('animationend', () => {
                cardElement.remove();
                
                // 카드 개수 갱신
                const currentCount = parseInt(postsCountBadge.textContent, 10);
                const newCount = Math.max(0, currentCount - 1);
                updatePostsCountBadge(newCount);
                
                // 카드가 하나도 없다면 비어있는 상태 뷰 노출
                if (newCount === 0) {
                    postsContainer.classList.add('hidden');
                    emptyState.classList.remove('hidden');
                }
            });
            
            showToast('생각 카드가 안전하게 삭제되었습니다.', 'success');
            
        } catch (error) {
            console.error(error);
            showToast(error.message, 'error');
        }
    }

    // ==========================================================================
    // 3. UI 헬퍼 함수
    // ==========================================================================

    // XSS 공격 방지를 위한 이스케이프 헬퍼 함수
    function escapeHTML(str) {
        if (!str) return '';
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    // 시간 포맷 헬퍼 함수 (YYYY-MM-DD HH:MM)
    function formatDate(dateString) {
        try {
            // SQLite의 CURRENT_TIMESTAMP는 UTC 기준 포맷(YYYY-MM-DD HH:MM:SS)으로 생성됨
            // 브라우저 현지 시간으로 변환을 진행
            const utcDate = new Date(dateString.replace(' ', 'T') + 'Z');
            
            // 날짜가 잘못되었을 때 폴백
            if (isNaN(utcDate.getTime())) {
                return dateString.substring(0, 16); 
            }
            
            const pad = (n) => n < 10 ? '0' + n : n;
            const year = utcDate.getFullYear();
            const month = pad(utcDate.getMonth() + 1);
            const day = pad(utcDate.getDate());
            const hours = pad(utcDate.getHours());
            const minutes = pad(utcDate.getMinutes());
            
            return `${year}-${month}-${day} ${hours}:${minutes}`;
        } catch (e) {
            return dateString;
        }
    }

    // 카드 요소 DOM 생성
    function createCardElement(post) {
        const card = document.createElement('article');
        card.className = 'glass-card post-card';
        card.setAttribute('data-id', post.id);
        
        // 이스케이프 처리 진행
        const safeTitle = escapeHTML(post.title);
        const safeMessage = escapeHTML(post.message);
        const formattedDate = formatDate(post.created_at);
        
        card.innerHTML = `
            <div class="post-card-header">
                <h3 class="post-card-title">${safeTitle}</h3>
                <div class="card-actions-wrapper">
                    <button class="edit-btn" aria-label="게시글 수정" title="수정하기">
                        <i data-lucide="edit-3" class="edit-icon"></i>
                    </button>
                    <button class="delete-btn" aria-label="게시글 삭제" title="삭제하기">
                        <i data-lucide="trash-2" class="delete-icon"></i>
                    </button>
                </div>
            </div>
            <div class="post-card-body">
                <p class="post-card-text">${safeMessage}</p>
            </div>
            <div class="post-card-footer">
                <div class="post-date-wrapper">
                    <i data-lucide="clock" class="clock-icon"></i>
                    <span>${formattedDate}</span>
                </div>
            </div>
        `;
        
        // 수정 버튼 이벤트 연결
        const editButton = card.querySelector('.edit-btn');
        editButton.addEventListener('click', (e) => {
            e.stopPropagation();
            enterEditMode(post, card);
        });

        // 삭제 버튼 이벤트 연결
        const deleteButton = card.querySelector('.delete-btn');
        deleteButton.addEventListener('click', (e) => {
            e.stopPropagation();
            if (confirm('이 생각 카드를 정말로 삭제할까요?')) {
                deletePost(post.id, card);
            }
        });
        
        return card;
    }

    // 인라인 편집 모드 진입
    function enterEditMode(post, cardElement) {
        // 이미 수정 중인지 체크
        if (cardElement.classList.contains('editing')) return;
        
        cardElement.classList.add('editing');
        
        // 인라인 수정 폼 엘리먼트 생성
        const editForm = document.createElement('form');
        editForm.className = 'card-edit-form';
        
        editForm.innerHTML = `
            <div class="edit-form-header">
                <i data-lucide="edit-3" class="edit-header-icon"></i>
                <span class="edit-header-title">생각 카드 수정</span>
            </div>
            <div class="edit-input-group">
                <label for="edit-title-${post.id}">제목</label>
                <input 
                    type="text" 
                    id="edit-title-${post.id}" 
                    class="edit-title-input" 
                    required 
                    maxlength="100" 
                    value="${escapeHTML(post.title)}"
                    autocomplete="off"
                >
            </div>
            <div class="edit-input-group">
                <label for="edit-message-${post.id}">내용</label>
                <textarea 
                    id="edit-message-${post.id}" 
                    class="edit-message-textarea" 
                    required 
                    maxlength="1000" 
                    rows="4"
                >${escapeHTML(post.message)}</textarea>
            </div>
            <div class="edit-actions">
                <button type="button" class="edit-btn-pill edit-cancel-btn">
                    <i data-lucide="x" class="edit-btn-icon"></i> 취소
                </button>
                <button type="submit" class="edit-btn-pill edit-save-btn">
                    <i data-lucide="check" class="edit-btn-icon"></i> 저장
                </button>
            </div>
        `;
        
        cardElement.appendChild(editForm);
        lucide.createIcons(); // 아이콘 렌더링
        
        // 제목 입력 필드에 포커싱
        const titleInput = editForm.querySelector('.edit-title-input');
        titleInput.focus();
        titleInput.setSelectionRange(titleInput.value.length, titleInput.value.length);
        
        // 취소 버튼 리스너
        const cancelButton = editForm.querySelector('.edit-cancel-btn');
        cancelButton.addEventListener('click', (e) => {
            e.preventDefault();
            exitEditMode(cardElement, editForm);
        });
        
        // 저장 폼 전송 리스너
        editForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const newTitle = editForm.querySelector('.edit-title-input').value.trim();
            const newMessage = editForm.querySelector('.edit-message-textarea').value.trim();
            
            if (!newTitle) {
                showToast('제목을 입력해 주세요.', 'error');
                return;
            }
            if (!newMessage) {
                showToast('내용을 입력해 주세요.', 'error');
                return;
            }
            
            await updatePost(post, newTitle, newMessage, cardElement, editForm);
        });
    }

    // 인라인 편집 모드 탈퇴
    function exitEditMode(cardElement, editForm) {
        cardElement.classList.remove('editing');
        editForm.remove();
    }

    // API: 게시글 수정 반영
    async function updatePost(post, title, message, cardElement, editForm) {
        const saveBtn = editForm.querySelector('.edit-save-btn');
        const cancelBtn = editForm.querySelector('.edit-cancel-btn');
        
        // 버튼 락 설정
        saveBtn.disabled = true;
        cancelBtn.disabled = true;
        saveBtn.innerHTML = `<div class="btn-loader"></div><span>저장 중...</span>`;
        
        try {
            const response = await fetch(`/api/posts/${post.id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title, message })
            });
            
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.error || '게시글 수정에 실패했습니다.');
            }
            
            // 데이터 업데이트
            post.title = result.title;
            post.message = result.message;
            
            // DOM 컨텐츠 갱신
            cardElement.querySelector('.post-card-title').textContent = result.title;
            cardElement.querySelector('.post-card-text').textContent = result.message;
            
            // 시간 포맷 갱신 (선택 사항)
            cardElement.querySelector('.post-date-wrapper span').textContent = formatDate(result.created_at);
            
            // 성공 피드백 알림 및 수정 폼 소멸
            showToast('생각 카드가 세련되게 수정되었습니다.', 'success');
            exitEditMode(cardElement, editForm);
            
        } catch (error) {
            console.error(error);
            showToast(error.message, 'error');
            
            // 상태 원복
            saveBtn.disabled = false;
            cancelBtn.disabled = false;
            saveBtn.innerHTML = `<i data-lucide="check" class="edit-btn-icon"></i> 저장`;
            lucide.createIcons();
        }
    }

    // 등록 버튼 로딩 상태 전환
    function setSubmitButtonLoading(isLoading) {
        if (isLoading) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = `
                <div class="btn-loader"></div>
                <span>등록 중...</span>
            `;
            submitBtn.style.opacity = '0.7';
        } else {
            submitBtn.disabled = false;
            submitBtn.innerHTML = `
                <span>등록하기</span>
                <i data-lucide="arrow-right" class="btn-arrow-icon"></i>
            `;
            submitBtn.style.opacity = '1';
            lucide.createIcons(); // 아이콘 리로드
        }
    }

    // 로딩 스켈레톤 상태 제어
    function showLoadingState(isLoading) {
        if (isLoading) {
            postsLoader.classList.remove('hidden');
            postsContainer.classList.add('hidden');
            emptyState.classList.add('hidden');
        } else {
            postsLoader.classList.add('hidden');
        }
    }

    // 게시글 숫자 배지 업데이트
    function updatePostsCountBadge(count) {
        postsCountBadge.textContent = count;
    }

    // 토스트 알림 생성 및 출력
    function showToast(message, type = 'success') {
        const toastContainer = document.getElementById('toast-container');
        
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        const iconName = type === 'success' ? 'check-circle' : 'alert-circle';
        
        toast.innerHTML = `
            <i data-lucide="${iconName}" class="toast-icon"></i>
            <span class="toast-message">${escapeHTML(message)}</span>
        `;
        
        toastContainer.appendChild(toast);
        lucide.createIcons(); // 토스트 내부 아이콘 렌더링
        
        // 3.5초 뒤 토스트 퇴장 애니메이션 추가 및 소멸
        setTimeout(() => {
            toast.classList.add('fade-out');
            toast.addEventListener('animationend', () => {
                toast.remove();
            });
        }, 3500);
    }
});
