// js/db.js

const INIT_USERS = [
    { id: 'user1', password: 'password' },
    { id: 'user2', password: 'password' }
];

const INIT_MUSIC = [
    { id: 1, title: 'Ditto', artist: 'NewJeans', image: 'images/album.png', hashtags: ['Kpop', 'Dance'] },
    { id: 2, title: 'VIBE (feat. Jimin of BTS)', artist: 'TAEYANG', image: 'images/album.png', hashtags: ['Kpop', 'HipHop', 'R&B'] },
    { id: 3, title: 'Attention', artist: 'NewJeans', image: 'images/album.png', hashtags: ['Kpop'] },
    { id: 4, title: 'Teddy Bear', artist: 'STAYC', image: 'images/album.png', hashtags: ['Kpop', 'Dance', 'Indie'] },
    { id: 5, title: 'Pink Venom', artist: 'BLACKPINK', image: 'images/album.png', hashtags: ['Kpop', 'Dance'] },
    { id: 6, title: 'Shut Down', artist: 'BLACKPINK', image: 'images/album.png', hashtags: [] },
    { id: 7, title: 'After LIKE', artist: 'IVE', image: 'images/album.png', hashtags: ['Kpop', 'Pop'] },
    { id: 8, title: 'LOVE DIVE', artist: 'IVE', image: 'images/album.png', hashtags: ['Kpop', 'Pop', 'Rock'] },
    { id: 9, title: 'Hype Boy', artist: 'NewJeans', image: 'images/album.png', hashtags: ['Kpop', 'Dance'] },
    { id: 10, title: 'Cookie', artist: 'NewJeans', image: 'images/album.png', hashtags: ['Kpop', 'Dance', 'HipHop'] }
];

function initDB() {
    if (!localStorage.getItem('users')) {
        localStorage.setItem('users', JSON.stringify(INIT_USERS));
    }
    if (!localStorage.getItem('music')) {
        localStorage.setItem('music', JSON.stringify(INIT_MUSIC));
    }
    if (!localStorage.getItem('likes')) {
        localStorage.setItem('likes', JSON.stringify({})); // { userId: [musicId1, musicId2] }
    }
}

function getMusic() {
    return JSON.parse(localStorage.getItem('music')) || [];
}

function getUsers() {
    return JSON.parse(localStorage.getItem('users')) || [];
}

function getLikes() {
    return JSON.parse(localStorage.getItem('likes')) || {};
}

function getUserLikes(userId) {
    const likes = getLikes();
    return likes[userId] || [];
}

function toggleLike(userId, musicId) {
    const likes = getLikes();
    if (!likes[userId]) {
        likes[userId] = [];
    }
    
    const index = likes[userId].indexOf(musicId);
    let isLiked = false;
    
    if (index > -1) {
        // Unlike
        likes[userId].splice(index, 1);
    } else {
        // Like
        likes[userId].push(musicId);
        isLiked = true;
    }
    
    localStorage.setItem('likes', JSON.stringify(likes));
    return isLiked;
}

function getMusicLikeCount(musicId) {
    const likes = getLikes();
    let count = 0;
    for (const userId in likes) {
        if (likes[userId].includes(musicId)) {
            count++;
        }
    }
    return count;
}

// Initialize on script load
initDB();
