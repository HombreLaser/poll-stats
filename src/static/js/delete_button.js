async function sendDeleteRequest(event) {
    event.preventDefault();
    await fetch(event.target.href, {
        headers: {
         "X-CSRF-Token": token
        },
        method: "DELETE",
        mode: "same-origin",
        credentials: "same-origin",
        redirect: "follow"
    }).then((response) => {
        if(response.redirected)
            window.location = response.url;
    });
}


function listenForDeleteButtonClick() {
    const anchors = document.querySelectorAll('.delete-button');

    for (anchor of anchors)
        anchor.addEventListener("click", sendDeleteRequest);
}


const token = document.head.querySelector("[name~=token][content]").content;
listenForDeleteButtonClick();