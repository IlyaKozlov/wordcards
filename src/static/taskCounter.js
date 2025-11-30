let completed = sessionStorage.getItem('completed_tasks') || 0;
document.getElementById('counter').textContent = `Task №: ${completed}`;



function getNewTask() {
    window.location.replace("/static/task_experimental.html");
}

const taskUrl = '/tasks/tasks';


function getTaskContent(taskType) {
    let taskContent = sessionStorage.getItem('task_content');
    let taskContentParsed = null;
    try {
        taskContentParsed = JSON.parse(taskContent);
    } catch (Exception) {
        console.log(Exception.message);
        taskContent = null;
    }

    if (taskContentParsed !== null) {
        return taskContentParsed;
    }

    console.log(
        'Task content is null. Fetching new task from server...'
    )

    const url = new URL(taskUrl, window.location.origin);
    url.searchParams.append('task_type', taskType);
    return fetch(url)
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json(); // Return JSON data
        })
        .catch(error => {
          alert('An error occurred: ' + error.message); // Raise alert on error
          return null; // Return null or handle as needed
        });
}


async function fetchNewTask() {
    fetch(taskUrl)
        .then(response => response.json())
        .then(data => {
            sessionStorage.setItem('next_task_content', JSON.stringify(data));
    });
}

function showHiddenWord() {
    const spoiler = document.getElementById("spoiler");

    // Show the hidden word
    spoiler.classList.remove("hint")
    spoiler.classList.add("hintUnravel")

    // Hide the word again after 5 seconds
    setTimeout(() => {
        spoiler.classList.remove("hint");
    }, 5000);
}
