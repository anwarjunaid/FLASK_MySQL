function deleteTodo(sno) {
    fetch(`/delete/${sno}`, {
        method: 'DELETE',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        // Optionally, refresh the list of todos or update the UI as needed
        const todoRow = document.querySelector(`#todo-${sno}`);
        if (todoRow) {
            todoRow.remove();
        } else {
            console.error(`Todo with sno ${sno} not found in DOM`);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function updateTodo(sno){
    console.log("hua bhai")
    document.getElementById('updateForm').addEventListener('submit', function(event) {
        event.preventDefault();
        
        const title = document.getElementById('title').value;
        const desc = document.getElementById('desc').value;
        const newData = {
            title: title,
            desc: desc,
        };
    
        updateTodo2(sno, newData);
    });
}

function updateTodo2(sno, newData) {
    fetch(`/update/${sno}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(newData),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Todo updated successfully:', data);
        // Optionally, update the UI or perform any other action upon successful update
        window.location.href = '/';
    })
    .catch(error => {
        console.error('Error updating todo:', error);
    });
}


function changePassword(sno){
    console.log("method called");
    console.log(sno);
    document.getElementById('passwordForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const oldpwd = document.getElementById('oldpwd').value;
        const newpwd = document.getElementById('newpwd').value;
        fetch(`/changepwd/${sno}`, {
            method : 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ oldpwd: oldpwd, newpwd: newpwd })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('password changed successfully:', data);
            // Optionally, update the UI or perform any other action upon successful update
        })
        .catch(error => {
            console.error('Error updating password:', error);
        });
    });  
}