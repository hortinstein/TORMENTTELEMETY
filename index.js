const fs = require('fs');

const runnerIds = [
    'd8eea9c2-d2f2-4a0b-b4e1-3508809fd951',
    '60188132-b459-4b15-bdd6-9f0259a28926',
    'f08743dd-1fcf-4001-8e27-d97e03152b6e',
  ];
  

function printSplits(data) {
    if (data.result && data.result.splits && data.result.splits.length > 0) {
      console.log('Splits:');
      data.result.splits.forEach((split, index) => {
        console.log(`\t${split.name}: - Pace: ${split.pace} - Time: ${split.time}`);
        // console.log(JSON.stringify(split, null, 2));
      });
    } else {
      console.log('No splits found in the data.');
    }
  }
async function fetchDataAndPrint(runnerId) {
  try {
    const url = `https://api.enmotive.grepcv.com/prod/events/2023-uw-medicine-seattle-marathon-and-half-marathon/${runnerId}`;

    const response = await fetch(url, {
      headers: {
        accept: "application/json, text/plain, */*",
        "accept-language": "en-AU,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
        "sec-ch-ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        Referer: "https://raceday.enmotive.com/",
        "Referrer-Policy": "strict-origin-when-cross-origin",
      },
      body: null,
      method: "GET",
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const responseData = await response.json();
    // Parse the JSON string in the 'body' field into a data structure
    const bodyData = JSON.parse(responseData.body);
    
    // Construct the filename using lastname and confirmation_number
    const filename = `${bodyData.lastname}_${bodyData.confirmation_number}.json`;
    
    // Write the data to the file
    fs.writeFileSync(filename, JSON.stringify(bodyData, null, 2));
    // Print the entire object
    console.log('Runner:', bodyData.lastname);
    printSplits(bodyData)
  } catch (error) {
    console.error('Error:', error);
  }
}

// Call the function for each runnerId in the array
for (const runnerId of runnerIds) {
    fetchDataAndPrint(runnerId);
}