const show_error_toast = async (message) => {
    const toastDiv = document.getElementById("toast");
    toastDiv.textContent = message;

    // Clear the content of the "toast" div after 3 seconds
    setTimeout(() => {
        toastDiv.textContent = "";
    }, 3000)

}
const show_success_toast = async (message) => {
    const toastDiv = document.getElementById("toast");
    toastDiv.textContent = message;
    toastDiv.style.backgroundColor = "green"
    // Clear the content of the "toast" div after 3 seconds
    setTimeout(() => {
        toastDiv.style.backgroundColor = "red"
        toastDiv.textContent = "";
        window.location.reload();
    }, 3000)

}


const comment_buttons = document.getElementsByClassName("commentbutton")

for (let i = 0; i < comment_buttons.length; i++) {
    // Access each element using the index i
    const button = comment_buttons[i];

    // Add an event listener to each button
    button.addEventListener('click', function (event) {
        const div_id = event.target.getAttribute('id')

        const comment_div = document.getElementById(`comment${div_id[div_id.length - 1]}`)

        if (comment_div.style.display === "block") {
            comment_div.style.display = "none"
        }
        else {
            comment_div.style.display = "block"
        }
        console.log('Button clicked');
    });
}


function handleCommentSubmit(event, post_id) {
    // Prevent the default form submission behavior
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
    // Your form submission handling code here
    console.log('Form submitted!');
    console.log(formData)
    fetch(`/create-comment/${post_id}`, {
        method: "POST",
        body: formData,
    }).then(async response => {
        if (!response.ok) {

            show_error_toast(await response.text())
        }
        if (response.ok) {

            show_success_toast("Comment added successfully Successfully")
        }
    }).catch(async error => {
        show_error_toast("Something went wrong")
    });

};


// import { show_error_toast, show_success_toast } from "./project";
function delete_comment(comment_id) {
    fetch(`/delete-comment/${comment_id}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
    })
        .then(async response => {
            if (!response.ok) {

                show_error_toast(await response.text())
            }
            if (response.ok) {

                show_success_toast("Comment Deleted Successfully")
            }

        }).catch(async error => {
            show_error_toast("Something went wrong")
        });

};
function like_post(post_id) {
    fetch(`/like-post/${post_id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
    })
        .then(async response => {
            if (!response.ok) {

                show_error_toast(await response.text())
            }
            if (response.ok) {
                let message = await response.text()
                if (message === 'liked') {
                    document.getElementById(`likebutton${post_id}`).setAttribute('fill', 'red')
                }
                else {
                    document.getElementById(`likebutton${post_id}`).setAttribute('fill', 'black')
                }
                const toastDiv = document.getElementById("toast");
                toastDiv.textContent = message + " post";
                toastDiv.style.backgroundColor = "green"
                // Clear the content of the "toast" div after 3 seconds
                setTimeout(() => {
                    toastDiv.style.backgroundColor = "red"
                    toastDiv.textContent = "";

                }, 3000)
            }

        }).catch(async error => {
            console.log(error)
            show_error_toast("Something went wrong")
        });

};
