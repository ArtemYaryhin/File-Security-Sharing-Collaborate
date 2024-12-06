document.getElementById("upload-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById("file-input");
    if (!fileInput.files.length) {
        alert("Please select a file to upload.");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    const response = await fetch("/upload", {
        method: "POST",
        body: formData,
    });

    const resultDiv = document.getElementById("result");
    if (response.ok) {
        const data = await response.json();
        resultDiv.innerHTML = `<p><strong>${data.message}</strong></p><pre>${JSON.stringify(data.result, null, 2)}</pre>`;
    } else {
        const errorData = await response.json();
        resultDiv.innerHTML = `<p style="color: red;"><strong>Error:</strong> ${errorData.error}</p>`;
    }
}); 