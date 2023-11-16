const usernamefield = document.querySelector("#usernamefield");
const feedbackArea = document.querySelector(".invalid-feedback");
const emailfield = document.querySelector("#emailfield");
const emailFeedbackArea = document.querySelector(".invalid-feedback2")
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const emailSuccessOutput = document.querySelector(".emailSuccessOutput");
const passwordfield = document.querySelector("#passwordfield");
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const submitBtn = document.querySelector(".submitBtn");


const handleToggleInput=(e)=>{
    if(showPasswordToggle.textContent==="SHOW"){
        showPasswordToggle.textContent= "HIDE";
        passwordfield.setAttribute("type", "text");
    }
    else{
        showPasswordToggle.textContent = "SHOW";
        passwordfield.setAttribute("type", "password");
    }
};
showPasswordToggle.addEventListener('click', handleToggleInput)


usernamefield.addEventListener("keyup", (e) =>{
    const usernameVal = e.target.value;
    usernameSuccessOutput.textContent=`Checking ${usernameVal}`


    usernameSuccessOutput.style.display="block"
    usernamefield.classList.remove("is-invalid");
    feedbackArea.style.display = "none";
    
    if(usernameVal.length > 0){
        fetch("/validate_username/",{
            body: JSON.stringify({username : usernameVal}),
            method : "POST",
        })
            .then((res) => res.json())
            .then((data)=>{
                console.log("data", data);
                usernameSuccessOutput.style.display="none"
                if(data.username_error){

                    submitBtn.disabled = true;
                    usernamefield.classList.add("is-invalid");
                    feedbackArea.style.display = "block";
                    feedbackArea.innerHTML = `<p>${data.username_error}</p>`;
                }
                else{
                    submitBtn.removeAttribute("disabled")
                }
            });
    }
    

    
});


emailfield.addEventListener("keyup", (e) =>{
    const emailVal = e.target.value;
    emailSuccessOutput.textContent= `Checking ${emailVal} `

    emailSuccessOutput.style.display="block";
    emailfield.classList.remove("is-invalid");
    emailFeedbackArea.style.display = "none";


    if (emailVal.length>0){
        fetch("/validate_email/",{
            body : JSON.stringify({email:emailVal}),
            method : "POST",
        })
            .then((res)=> res.json())
            .then((data)=>{
                console.log("data",data);
                emailSuccessOutput.style.display="none";
                if(data.email_error){
                    submitBtn.setAttribute("disabled", "disabled");
                    submitBtn.disabled = true;
                    emailfield.classList.add("is-invalid");
                    emailFeedbackArea.style.display = "block";
                    emailFeedbackArea.innerHTML=`<p>${data.email_error}</p>`

                }
                else{
                    submitBtn.removeAttribute("disabled")
                }
            })
    }
});