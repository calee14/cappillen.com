function addTicker() {
    // Get the value from the input field
    const inputValue = document.getElementById('inputField').value;
            
    if (inputValue.trim() === '') {
        alert('Please enter a valid string.');
        return;
    }
    
    // Create a new list item element
    const listItem = document.createElement('li');
    
    // Add the input value as the content of the list item
    const tickerSpan = document.createElement('span');
    tickerSpan.textContent = inputValue
    listItem.appendChild(tickerSpan);

    const deleteButton = document.createElement('button');
    deleteButton.innerText = 'delete';
    deleteButton.addEventListener('click', (event) => {
        event.target.parentElement.remove();
        updateTickerList();
    });
    deleteButton.style.marginLeft = '5px';
    listItem.appendChild(deleteButton);
    
    // Add the list item to the list
    document.getElementById('ticker-list').appendChild(listItem);
    
    // Clear the input field
    document.getElementById('inputField').value = '';

    updateTickerList();
}


function updateTickerList() {
    // Get all the list items and build an array of strings
    const listItems = document.querySelectorAll('#ticker-list li');
    const listDataArray = Array.from(listItems).map(item => item.childNodes[0].textContent);
    
    // Set the hidden input field's value to the JSON representation of the array
    document.getElementById('content-ticker-list').value = JSON.stringify(listDataArray);

    console.log(document.getElementById('content-ticker-list').value);
}

function submitLeperRequest() {
    const url = '/leperbase/api/build';

    const data = {
        'tickerList' : document.getElementById('content-ticker-list').value,
    };
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }

    document.getElementById('leperSubmitButton').disabled = true;

    fetch(url, options)
        .then(response => response.blob())
        .then(blob => {
            const blobUrl = URL.createObjectURL(blob);
            window.location.href = blobUrl;
            document.getElementById('leperSubmitButton').disabled = false;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('leperSubmitButton').disabled = false;
        });
}
