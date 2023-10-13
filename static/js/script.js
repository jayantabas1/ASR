let mediaRecorder;
let audioChunks = [];
let audioElement = new Audio();
let isRecording = false;

// Start recording
function startRecording() {
  if (!isRecording) {
    navigator.mediaDevices
      .getUserMedia({ audio: true })
      .then(function (stream) {
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.ondataavailable = function (event) {
          audioChunks.push(event.data);
        };

        mediaRecorder.onstop = function () {
          const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
          const audioUrl = URL.createObjectURL(audioBlob);
          // Play the recorded audio
          const audioElement = document.getElementById("audio");
          audioElement.src = audioUrl;
          audioElement.play();
          isRecording = false;
        };

        mediaRecorder.start();
        isRecording = true;
      })
      .catch(function (error) {
        console.error("Error accessing microphone:", error);
      });
  } else {
    mediaRecorder.stop();
  }
}

// Play or pause recorded audio
// function toggleAudio() {
//   if (audioElement.src) {
//     if (audioElement.paused) {
//       audioElement.play();
//     } else {
//       audioElement.pause();
//     }
//   } else {
//     console.error("No recorded audio to play.");
//   }
// }

function translateAudio(translationTextareaId, transcription2TextareaId) {
  const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
  const formData = new FormData();
  formData.append("audio", audioBlob);

  // Send the text to the Flask route using AJAX
  fetch("/upload", {
    // Replace '/translate' with your actual Flask route URL
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      // Handle the response from the Flask route
      const translation_in_english = data.translation1;
      const translation_in_assamese = data.translation2;
      hideLoadingAnimation(); // Pass the ID of the first textarea

      // Set the values of the textareas by their IDs
      document.getElementById(translationTextareaId).textContent =
        translation_in_english;
      document.getElementById(transcription2TextareaId).textContent =
        translation_in_assamese;
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

// Function to show the loading animation
function showLoadingAnimation() {
  document.getElementById("bouncing-loader").style.display = "flex";
}

// Function to hide the loading animation inside a textarea
function hideLoadingAnimation() {
  document.getElementById("bouncing-loader").style.display = "none";
}
$(document).ready(function () {
  $("#recordButton").addClass("notRec");
  // Event handlers for buttons and interactions with HTML elements
  $("#recordButton").click(function () {
    if ($("#recordButton").hasClass("notRec")) {
      $("#recordButton").removeClass("notRec");
      $("#recordButton").addClass("Rec");
      startRecording();
    } else {
      $("#recordButton").removeClass("Rec");
      $("#recordButton").addClass("notRec");
      mediaRecorder.stop(); // This line is outside the if-else block
    }
  });

  $("#translateButton").click(function () {
    translateAudio("translation1", "translation2");
    showLoadingAnimation(); // Pass the ID of the first textarea
  });

  // ... (other DOM-related code)
});
