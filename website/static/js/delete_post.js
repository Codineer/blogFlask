// import { show_error_toast, show_success_toast } from "./project";
function delete_post(post_id) {
    fetch(`/delete-post/${post_id}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
            // You can add other headers if needed
        },
        // You can pass data in the body if required
        // body: JSON.stringify({ post_id: postId })
    })
        .then(async response => {
            if (!response.ok) {

                show_error_toast(await response.text())
            }
            if (response.ok) {

                show_success_toast("Post Deleted Successfully")
            }

        }).catch(async error => {
            // Handle error
            show_error_toast("Something went wrong")
        });

    // console.log(res)
};
