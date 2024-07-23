function validateForm() {
    console.log('111');
    // Remove any existing error messages
    removeErrorMessages();

    // Get form elements
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    // Email validation: ensure it's in a valid format
    const emailPattern = /^[a-zA-Z0-9]+@[a-z]+\.[a-z]{2,5}$/;
    console.log("123");
    if (!emailPattern.test(email)) {
        addErrorMessage("email", "Invalid email")
        return false;
    }

    // Password validation: ensuring that it's at least 6 characters long
    if (password.length < 6) {
        addErrorMessage("password", "Must be at least of 6 characters")
        return false;
    }
    
    console.log("validation");
    window.location.href = '/profile';
    // If all validations pass, returned true
    return true;
}



// Function to add an error message next to a form field
function addErrorMessage(fieldId, message) {
    const field = document.getElementById(fieldId);
    const errorMessage = document.createElement("span");
    errorMessage.className = "error";
    errorMessage.innerHTML = message;
    field.parentNode.appendChild(errorMessage);
}


// Function to remove all error messages
function removeErrorMessages() {
    var errorMessages = document.querySelectorAll(".error");
    errorMessages.forEach(function(element) {
        element.parentNode.removeChild(element);
    });
}

