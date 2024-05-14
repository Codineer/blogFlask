
document.getElementById("signupform").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the default form submission behavior

    const formData = new FormData(event.target);

    if (formData.get('password') !== formData.get('password2')) {
        alert('password and confirm password not matches')
        return
    }
    let isValid = true;

    for (let [key, value] of formData) {
        console.log(key, value)
        if (value.trim() === '') {
            isValid = false;
            alert("Fill all the required fields.")
            break; // Exit the loop early if a field is empty
        }
    }
    if (!isValid) {
        return
    }
    // Send the data using fetch or XMLHttpRequest
    fetch("/sign-up", {
        method: "POST",
        body: formData,
    }).then(async response => {

        if (response.redirected) {
            // If redirected, extract the redirect URL
            const redirectUrl = response.url;
            // Redirect the user to the specified URL
            window.location.href = redirectUrl;
        }
        if (response.redirected === false) {

            show_error_toast(await response.text())

        }

    }).catch(async error => {
        // Handle error
        show_error_toast("Something went wrong")
    });

    // console.log(res)
});
