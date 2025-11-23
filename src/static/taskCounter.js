let completed = sessionStorage.getItem('completed_tasks') || 0;
document.getElementById('counter').textContent = `Task №: ${completed}`;



function getNewTask() {
    window.location.replace("/static/task_experimental.html");
}

const taskUrl = '/tasks/tasks';


function getTaskContent(taskType) {
    let taskContent = sessionStorage.getItem('task_content');

    if (taskContent == null) {
        const url = new URL(taskUrl, window.location.origin);
        url.searchParams.append('task_type', taskType);
        taskContent = fetch(url).text;
    }
    return JSON.parse(taskContent);
}


async function fetchNewTask() {
    fetch(taskUrl)
        .then(response => response.json())
        .then(data => {
            sessionStorage.setItem('next_task_content', JSON.stringify(data));
    });
}

