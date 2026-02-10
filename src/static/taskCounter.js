const uid = getUid();

let completed = sessionStorage.getItem('completed_tasks') || 0;
document.getElementById('counter').textContent = `Task №: ${completed}`;

const taskUrl = '/tasks/tasks' + "?uid=" + encodeURIComponent(uid);

function updateTaskStatistics(wordTuples) {
    // Accepts an array of tuples: [[word1, true], [word2, false], ...]
    if (!Array.isArray(wordTuples) || wordTuples.length === 0) {
        return Promise.resolve(null);
    }

    // Save raw tuples to localStorage
    try {
        localStorage.setItem('task_statistics', JSON.stringify(wordTuples));
    } catch (e) {
        console.error('Failed to save task statistics to localStorage:', e);
    }
}

function commitTaskStatistics(wordTuples) {
    const payload = {"statistics": wordTuples.map(t => ({word: t[0], is_true: t[1]}))};
    console.log('Committing task statistics:', payload);
    return fetch('/tasks/update_statistics' + "?uid=" + encodeURIComponent(uid), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(payload)
        })
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


function getTaskContent(taskType, verificationFunction = null) {
    // If there are saved statistics in localStorage, send them and then set to null
    try {
        const statsRaw = localStorage.getItem('task_statistics');
        if (statsRaw !== null && statsRaw !== 'null') {
            localStorage.removeItem('task_statistics')
            commitTaskStatistics(JSON.parse(statsRaw));
        }
    } catch (e) {
        console.error('Error handling localStorage statistics:', e);
    }

    let taskContent = sessionStorage.getItem('task_content');
    let taskContentParsed = null;
    try {
        taskContentParsed = JSON.parse(taskContent);
        if (verificationFunction !== null && !verificationFunction(taskContentParsed)) {
            taskContentParsed = null;
            console.log('Task content is invalid. Fetching new task from server...');
        }
    } catch (e) {
        // parsing failed or taskContent is null
        if (e && e.message) {
            console.log(e.message);
        }
        taskContentParsed = null;
    }

    if (taskContentParsed !== null) {
        return Promise.resolve(taskContentParsed);
    }

    console.log('Task content is null. Fetching new task from server...');

    const url = new URL(taskUrl, window.location.origin);
    url.searchParams.append('task_type', taskType);
    url.searchParams.append('uid', uid);
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
