function deleteRequest(requestId) {
    if (confirm("Вы уверены, что хотите удалить эту заявку?")) {
        fetch(`/delete_request/${requestId}`, {
            method: "DELETE",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"), // Передача CSRF-токена
                "Content-Type": "application/json"
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка удаления заявки');
            }
            // Обновить страницу или удалить карточку из DOM
            location.reload();
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
    }
}

// Функция для получения значения CSRF-токена из куки
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}