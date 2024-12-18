document.getElementById('predictionType').addEventListener('change', function () {
    const type = this.value;
    document.getElementById('batchForm').style.display = type === 'batch' ? 'block' : 'none';
    document.getElementById('individualForm').style.display = type === 'individual' ? 'block' : 'none';
    document.getElementById('result').innerHTML = '';
    document.getElementById('error').innerHTML = '';
});

document.getElementById('batchForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const file = document.getElementById('file').value;
    await makePrediction({ file: file });
});

document.getElementById('individualForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const area = document.getElementById('area').value;
    const year_built = document.getElementById('year_built').value;
    await makePrediction({ area: area, year_built: year_built });
});

async function makePrediction(data) {
    const resultDiv = document.getElementById('result');
    const loadingDiv = document.getElementById('loading');
    const errorDiv = document.getElementById('error');
    
    resultDiv.innerHTML = '';
    errorDiv.innerHTML = '';
    loadingDiv.style.display = 'block';

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            const result = await response.json();
            if (result.average_price) {
                resultDiv.innerHTML = `Average Price: $${result.average_price.toFixed(2)}`;
            } else if (result.message) {
                resultDiv.innerHTML = `Message: ${result.message}`;
            } else {
                resultDiv.innerHTML = 'Unexpected response format.';
            }
        } else {
            errorDiv.innerHTML = 'Error: Could not retrieve data.';
        }
    } catch (error) {
        errorDiv.innerHTML = `Error: ${error.message}`;
    } finally {
        loadingDiv.style.display = 'none';
    }
}
