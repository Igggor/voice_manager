document.querySelector('#helpSubmitBtn').addEventListener('click', (e) => {
    fetch(`/help`, {
        method: 'POST',
        body: JSON.stringify({
            theme: document.querySelector('#theme').value,
            question: document.querySelector('#question').value,
        }),
        headers: {'Content-Type': 'application/json'}
    }).then(r => console.log(r))
    document.querySelector('#theme').value = ''
    document.querySelector('#question').value = ''

})