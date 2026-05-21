// js/app.js

// Render music cards based on current search/filter
function renderMusic(filterFn = null) {
    const musicList = getMusic();
    const container = document.getElementById('musicGrid');
    if (!container) return;
    container.innerHTML = '';
    const userId = getCurrentUser();
    const userLikes = userId ? getUserLikes(userId) : [];
    const filtered = filterFn ? musicList.filter(filterFn) : musicList;
    filtered.forEach(m => {
        const card = document.createElement('div');
        card.className = 'music-card fade-in';
        // Image src – use placeholder if actual not found
        const imgSrc = m.image || 'images/album.png';
        const likeCount = getMusicLikeCount(m.id);
        const isLiked = userLikes.includes(m.id);
        card.innerHTML = `
            <div class="card-top">
                <img src="${imgSrc}" alt="Album" class="album-art" />
                <div class="music-info">
                    <h3><a href="#" onclick="alert('Details for ${m.title}'); return false;">${m.title}</a></h3>
                    <p>${m.artist}</p>
                    <div class="hashtags">
                        ${m.hashtags.map(tag => `<span class="hashtag" onclick="filterByTag('${tag}')">#${tag}</span>`).join('')}
                    </div>
                </div>
            </div>
            <div class="like-btn-container">
                <button class="like-btn ${isLiked ? 'liked' : ''}" onclick="handleLike(${m.id}, this)">
                    <i class="fa ${isLiked ? 'fa-heart' : 'fa-heart-o'}"></i>
                </button>
                <span class="likes-count" id="like-count-${m.id}">${likeCount}</span>
            </div>
        `;
        container.appendChild(card);
    });
}

function handleLike(musicId, btn) {
    if (!isLoggedIn()) {
        alert('로그인 후에 좋아요를 누를 수 있습니다.');
        return;
    }
    const userId = getCurrentUser();
    const likedNow = toggleLike(userId, musicId);
    // Update UI
    const countSpan = document.getElementById(`like-count-${musicId}`);
    const newCount = getMusicLikeCount(musicId);
    countSpan.textContent = newCount;
    if (likedNow) {
        btn.classList.add('liked');
        btn.innerHTML = '<i class="fa fa-heart"></i>';
    } else {
        btn.classList.remove('liked');
        btn.innerHTML = '<i class="fa fa-heart-o"></i>';
    }
}

function filterByTag(tag) {
    renderMusic(m => m.hashtags.includes(tag));
}

function filterBySearch(query) {
    const q = query.toLowerCase();
    renderMusic(m => {
        return m.title.toLowerCase().includes(q) ||
               m.artist.toLowerCase().includes(q) ||
               m.hashtags.some(t => t.toLowerCase().includes(q));
    });
}

// Hook up search input
document.getElementById('searchInput')?.addEventListener('keyup', function(e) {
    const val = e.target.value.trim();
    if (val === '') {
        renderMusic();
    } else {
        filterBySearch(val);
    }
});

// If page is Top Likes or Hashtag page, they will call specific render functions from their own scripts.
