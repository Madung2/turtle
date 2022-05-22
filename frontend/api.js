async function handleSignin() {
    const signupData = {
        email: document.getElementById("floatingInput").value,
        password: document.getElementById("floatingPassword").value
    }
    //signupData는 자바스크립트 오브젝트 json으로 바꿔줘야함

    const response = await fetch('http://192.168.123.104:5002/signup', {
        method: 'POST',
        body: JSON.stringify(signupData)
    })
    console.log(response.status)
    // response_json = await response.json()
    // console.log(response_json)
    if (response.status == 200) {
        window.location.replace("http://127.0.0.1:5501/frontend/login.html")
    }
}