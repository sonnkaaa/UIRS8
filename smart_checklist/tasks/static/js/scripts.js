<script>
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.complete-task').forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            const taskId = this.dataset.taskId;
            if (this.checked) {
                fetch(`/task/${taskId}/complete/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                    }
                }).then(res => {
                    if (res.ok) {
                        location.reload();
                    }
                });
            }
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
</script>
