async function handleSignin() {
    const signupData = {
        email: document.getElementById("floatingInput").value,
        password: document.getElementById("floatingPassword").value
    }
    //signupData는 자바스크립트 오브젝트 json으로 바꿔줘야함

    console.log(signupData)

    const response = await fetch('http://192.168.200.102:5000/signup', {
        method: 'POST',
        body: JSON.stringify(signupData)
    })
    console.log(response)
}