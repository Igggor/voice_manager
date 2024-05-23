document.querySelectorAll('.status-toggle').forEach(el => {
    fetch(`/api/smartdevices/${el.id.slice(6)}`).then(r => r.json()
        .then(data => {
            if (data.status === 1) {
                el.classList.add('status-toggle-active')
            }
        }))
    el.addEventListener('click', (e) => {
        el.classList.toggle('status-toggle-active')
        fetch(`/api/smartdevices/${el.id.slice(6)}`, {
            method: 'PUT',
            body: JSON.stringify({
                action: 'changeStatus',
                status: el.classList.contains('status-toggle-active'),
            }),
            headers: {'Content-Type': 'application/json'}
        }).then(r => r.json())
    })
})

document.querySelector('#addDevice').addEventListener('click', (e) => {
    document.querySelector('.new-device-form').style.display = 'inherit'
})

document.querySelector('#newDeviceSubmitBtn').addEventListener('click', async (e) => {
    let response = await fetch('/devices', {
        method: 'POST',
        body: JSON.stringify({
            operationType: 'addDevice',
            hashKey: document.querySelector('#hashKey').value
        }),
        headers: {'Content-Type': 'application/json'}
    })
    window.location.replace('')
})