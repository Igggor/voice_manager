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
    fetch('login', {
        method: 'POST',
        body: JSON.stringify({
            password: await cryptText(document.querySelector('#password').value),
            operationType: 'login',
            email: document.querySelector('#username').value
        }),
        headers: {'Content-Type': 'application/json'}
    }).then(r => r.json()
        .then(data => {
            if (data.correct) {
                // Cookies.set('sessionId', data.sessionId, { expires: 30}) // worked
                Cookies.set('sessionId', 'qwerty123', { expires: 30}) // test
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
        fetch('signup', {
            method: 'POST',
            body: JSON.stringify({
                operationType: 'signup',
                username: document.querySelector('#username').value,
                password: await cryptText(document.querySelector('#password').value)
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
