document.getElementById('reg-form').addEventListener('submit', async(e)=>{
  e.preventDefault();
  const firstName = document.getElementById('firstName').value;
  const lastName = document.getElementById('lastName').value;
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  const year = document.getElementById('Dropdown').value;
  const confirmPassword = document.getElementById('cpassword').value;

  
  if(!firstName || !lastName || !email || !password || !year || !confirmPassword){
    showErrorMessage('Please enter all credentials');
  }
  if(password.length < 8){
    showErrorMessage('password must be at least 8 characters')
  }
  if(password !== confirmPassword){
    showErrorMessage('Password and confirm password should match');
  }
})
// Function to show success message
function showSuccessMessage(message) {
  Toastify({
      text: message || "Operation completed successfully!",
      duration: 3000,
      close: true,
      background:"green",
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

const form = document.getElementById('reg-form');
const message = document.getElementById('message');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = new FormData(form);
  const response = await fetch('/register', {
    method: 'POST',
    body: JSON.stringify(Object.fromEntries(formData)),
    headers: {
      'Content-Type': 'application/json'
    }
  });
  const data = await response.json();
  message.textContent = data.message;
});