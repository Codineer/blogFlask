document.getElementById("postform").addEventListener("submit", async function (event) {
    event.preventDefault();

    const formData = new FormData(event.target);

    let isValid = true;

    for (let [key, value] of formData) {
        console.log(key, value)
        if (value.trim() === '') {
            isValid = false;
            alert("Fill all the required fields.")
            break;
        }
    }
    if (!isValid) {
        return
    }

    fetch("/create-post", {
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
        show_error_toast("something went wrong")

    });

    // console.log(res)
});

function back() {
    window.location.href = document.referrer
}