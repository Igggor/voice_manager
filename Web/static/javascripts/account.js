

function exitFromAccount() {
    fetch('/account', {
        method: 'POST',
        body: JSON.stringify({
            operationType: 'exit',
        }),
        headers: {'Content-Type': 'application/json'}
    }).then((data) => {
        window.location.replace('/account/login')
    })
}