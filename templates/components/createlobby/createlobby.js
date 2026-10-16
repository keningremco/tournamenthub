
const privateCheckbox = document.getElementById("isPrivate");
const passwordField = document.getElementById("passwordField");
const lobbyPassword = document.getElementById("lobbyPassword");

if (privateCheckbox && passwordField && lobbyPassword) {
    function updatePasswordField() {
        passwordField.classList.toggle("show", privateCheckbox.checked);
        lobbyPassword.required = privateCheckbox.checked;

        if (!privateCheckbox.checked) {
            lobbyPassword.value = "";
        }
    }

    privateCheckbox.addEventListener("change", updatePasswordField);
    updatePasswordField();
}
