let completed = sessionStorage.getItem('completed_tasks') || 0;
document.getElementById('counter').textContent = `Task №: ${completed}`;



function getNewTask() {
    window.location.replace("/static/task.html");
}

const taskUrl = '/tasks/tasks';

function updateTaskStatistics(wordTuples) {
    // Accepts an array of tuples: [[word1, true], [word2, false], ...]
    if (!Array.isArray(wordTuples) || wordTuples.length === 0) {
        return Promise.resolve(null);
    }
    const statistics = wordTuples.map(tuple => {
        if (!Array.isArray(tuple)) {
            // ignore malformed entries
            return null;
        }
        const word = tuple.length > 0 ? String(tuple[0]) : '';
        const is_true = tuple.length > 1 ? !!tuple[1] : false;
        return {word, is_true};
    }).filter(Boolean);
    const payload = {statistics};
    return fetch('/tasks/update_statistics', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(payload)
        })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .catch(error => {
            console.error('Failed to update task statistics:', error);
            return null;
        });
}


function getTaskContent(taskType, verificationFunction=null) {
    let taskContent = sessionStorage.getItem('task_content');
    let taskContentParsed = null;
    try {
        taskContentParsed = JSON.parse(taskContent);
        if (verificationFunction !== null && !verificationFunction(taskContentParsed)) {
            taskContentParsed = null;
        }
        console.log(
            'Task content is invalid. Fetching new task from server...'
        )
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

