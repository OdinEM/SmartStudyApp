document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("#form");
  const nameInput = document.querySelector("#name");
  const emailInput = document.querySelector("#email");
  const subjectInput = document.querySelector("#subject");
  const messageInput = document.querySelector("#message");

  const resetForm = () => {
      nameInput.value = "";
      emailInput.value = "";
      subjectInput.value = "";
      messageInput.value = "";
  };

  form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const name = nameInput.value.trim();
      const email = emailInput.value.trim();
      const subject = subjectInput.value.trim();
      const message = messageInput.value.trim();

      if (!name || !email || !message || !subject) {
          showErrorMessage("Please fill in all fields");
          return;
      }

      const messageData = {
          name,
          email,
          subject,
          message
      };

      try {
          const response = await fetch('http://localhost:5000/messages', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify(messageData)
          });

          if (response.ok) {
              const responseData = await response.json();
              showSuccessMessage(responseData.message);
              resetForm();
          } else {
              const errorData = await response.json();
              showErrorMessage(errorData.error);
          }
      } catch (error) {
          console.error("Error:", error);
          showErrorMessage("An error occurred. Please try again later.");
      }
  });
});



// Function to show success message
function showSuccessMessage(message) {
  Toastify({
      text: message || "Operation completed successfully!",
      duration: 3000,
      close: true,
      backgroundColor:"green",
      className: "toastify-success"
  }).showToast();
}

// Function to show error message
function showErrorMessage(message) {
  Toastify({
      text: message || "Error: Something went wrong!",
      duration: 3000,
      close: true,
      backgroundColor:"red",
      className: "toastify-error"
  }).showToast();
}
