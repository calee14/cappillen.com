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
    listItem.textContent = inputValue;
    
    // Add the list item to the list
    document.getElementById('ticker-list').appendChild(listItem);
    
    // Clear the input field
    document.getElementById('inputField').value = '';

    updateTickerList();
}

function updateTickerList() {
    // Get all the list items and build an array of strings
    const listItems = document.querySelectorAll('#ticker-list li');
    const listDataArray = Array.from(listItems).map(item => item.innerHTML);
    
    // Set the hidden input field's value to the JSON representation of the array
    document.getElementById('content-ticker-list').value = JSON.stringify(listDataArray);

    console.log(document.getElementById('content-ticker-list').value);
}