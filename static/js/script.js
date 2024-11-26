async function uploadImage() {
    const input = document.getElementById('imageInput');
    const resultDiv = document.getElementById('result');

    resultDiv.textContent = '';

    if (input.files.length === 0) {
        resultDiv.textContent = 'Please select an image.';
        return;
    }

    const formData = new FormData();
    formData.append('file', input.files[0]);

    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            resultDiv.textContent = `Error: ${errorData.error}`;
            return;
        }

        const data = await response.json();
        resultDiv.textContent = `Prediction: ${data.prediction}`;
    } catch (error) {
        resultDiv.textContent = 'Error connecting to server.';
    }
}
