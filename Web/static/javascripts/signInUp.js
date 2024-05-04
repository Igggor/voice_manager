async function cryptText(message, algo) {
    if (algo == null) {
        algo = "SHA-256";
    }

    const msgUint8 = new TextEncoder().encode(message)                          // encode as (utf-8) Uint8Array
    const hashBuffer = await crypto.subtle.digest(algo, msgUint8)              // hash the message
    const hashArray = Array.from(new Uint8Array(hashBuffer))                     // convert buffer to byte array
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('')     // convert bytes to hex string
}

async function sendLoginForm() {
    fetch('/account/login', {
        method: 'POST',
        body: JSON.stringify({
            password: await cryptText(document.querySelector('#password').value),
            operationType: 'login',
            email: document.querySelector('#email').value
        }),
        headers: {'Content-Type': 'application/json'}
    }).then(r => r.json()
        .then(data => {
            if (data.correct) {
                window.location.replace('/account')

            } else {
                document.querySelector('#loginErr').style.display = 'inherit'
            }
        }))
}

async function sendSignupForm() {
    document.querySelector('#signupErr1').style.display = 'none'
    document.querySelector('#signupErr2').style.display = 'none'

    if (document.querySelector('#password').value === document.querySelector('#passwordSecond').value) {
        fetch('/account/signup', {
            method: 'POST',
            body: JSON.stringify({
                operationType: 'signup',
                userData: {
                    email: document.querySelector('#email').value,
                    password: await cryptText(document.querySelector('#password').value),
                    name: document.querySelector('#name').value,
                    surname: document.querySelector('#surname').value,
                }
            }),
            headers: {'Content-Type': 'application/json'}
        }).then(r => {
            if (r.status === 400) {
                document.querySelector('#signupErr2').style.display = 'inherit'
            }
            else if (r.status === 200) {
                window.location.replace('/account')
            }
            })
    }
    else {
        document.querySelector('#signupErr1').style.display = 'inherit'
    }
}
