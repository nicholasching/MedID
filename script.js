const webcam = document.querySelector('#webcamPreview');

//Core
window.navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        webcam.srcObject = stream;
        webcam.onloadedmetadata = (e) => {
            webcam.play();
        };
    })
    .catch( () => {
        alert('Reload the browser and hit allow.');
    });