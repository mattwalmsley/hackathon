// Function to load and merge data from CSV files
function loadAndMergeData() {
  const dataElement = document.getElementById('data');
  dataElement.innerHTML = '';

  // Array to store the merged data
  let mergedData = [];

  // Array to store the headers
  let headers = [];

  // Function to process each CSV file
  function processCSV(file, index) {
    Papa.parse(file, {
      header: true,
      dynamicTyping: true,
      complete: function (results) {
        const parsedData = results.data;
        mergedData = mergedData.concat(parsedData);

        // Store the headers from the first CSV file
        if (index === 0) {
          headers = results.meta.fields;
        }

        // Check if all CSV files have been processed
        if (index === 2) {
          // Display the merged data with headers
          const headerRow = document.createElement('div');
          headerRow.className = 'row header';
          headers.forEach((header) => {
            const headerCell = document.createElement('span');
            headerCell.textContent = header;
            headerRow.appendChild(headerCell);
          });
          dataElement.appendChild(headerRow);

          mergedData.forEach((entry) => {
            const entryRow = document.createElement('div');
            entryRow.className = 'row';
            headers.forEach((header) => {
              const entryCell = document.createElement('span');
              entryCell.textContent = entry[header];
              entryRow.appendChild(entryCell);
            });
            dataElement.appendChild(entryRow);
          });
        }
      },
    });
  }

  // Load and process each CSV file
  const files = ['deals.csv', 'employees.csv', 'clients.csv'];
  files.forEach((file, index) => {
    const xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          processCSV(xhr.responseText, index);
        } else {
          console.error('Failed to load CSV file:', file);
        }
      }
    };
    xhr.open('GET', file, true);
    xhr.send();
  });
}

// Call the loadAndMergeData function when the page loads
window.addEventListener('load', loadAndMergeData);
