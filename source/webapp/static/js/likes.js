async function makeRequest(url, method = "POST", body) {
    let token = await getCookie('token')
    let headers = {}
    headers['Authorization'] = `Token ${token}`
    headers['Content-Type'] = 'application/json'
    const response = await fetch(url,
        {
            "method": method,
            "headers": headers,
            "body": JSON.stringify(body)
        }
    );
    if (response.ok) {
        return await response.json();
    } else {
        let error = new Error(response.text());
        console.log(error);
        throw error;
    }
}

async function onClickLike(event) {
    event.preventDefault();
    let button = event.currentTarget;
    let postId = button.dataset.postId;
    let action = button.dataset.action;
    let url = `/api/v1/posts/${postId}/${action}/`;
    try {
        let data = await makeRequest(url);
        if (action === 'like') {
            button.classList.remove('btn-primary');
            button.classList.add('btn-danger');
            button.querySelector('i').classList.remove('bi-heart');
            button.querySelector('i').classList.add('bi-heart-fill');
            button.dataset.action = 'unlike';
        } else if (action === 'unlike') {
            button.classList.remove('btn-danger');
            button.classList.add('btn-primary');
            button.querySelector('i').classList.remove('bi-heart-fill');
            button.querySelector('i').classList.add('bi-heart');
            button.dataset.action = 'like';
        }
        let likesCountElement = document.getElementById(`likes-count-${postId}`);
        if (likesCountElement) {
            likesCountElement.innerText = `${data.likes_count} likes`;
        }
    } catch (error) {
        console.error('Error handling like button click:', error);
    }
}

function onLoad() {
    let likeButtons = document.querySelectorAll('[data-js="like-button"]');
    for (let button of likeButtons) {
        button.addEventListener('click', onClickLike);
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

window.addEventListener('load', onLoad);