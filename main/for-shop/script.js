let buy_btn = document.getElementById("buy");
let tg = window.Telegram.WebApp;
tg.expand()
buy_btn.addEventListener("click", () => {
    let name = document.getElementById('user_name').value;
    let telegram_id = document.getElementById('telegram_id').value;
    let email = document.getElementById('email').value;
    let text = document.getElementById('text').value;
    let time = 0


    if (document.getElementById("three-day").checked){
        time = 3
    }
    if (document.getElementById("seven-day").checked){
        time = 7
    }
    if (document.getElementById("three-week").checked){
        time = 21
    }
    if (document.getElementById("none-day").checked){
        time = 100
    }

    document.getElementById("user_name").style.border = "1px solid #ADD8E6"
    document.getElementById("telegram_id").style.border = "1px solid #ADD8E6"
    document.getElementById("email").style.border = "1px solid #ADD8E6"

    let data1 = {
        name:name,
        telegram_id:telegram_id,
        email:email,
        text:text,
        time:time
    }
    let warn = 0
    if(name.length < 3){
        warn = 1
        document.getElementById("user_name").style.border = "2px solid red"
    }
    if(telegram_id.length < 1){
        warn = 1
        document.getElementById("telegram_id").style.border = "2px solid red"
    }
    if(email < 5){
        warn = 1
        document.getElementById("email").style.border = "2px solid red"
    }

    if (warn != 1){
        if(time != 0){
            alert('Спасибо. С вами свяжутся')
            tg.sendData(JSON.stringify(data1));
            setInterval( () => tg.close(),3000);
        }else{
            alert('Не выбран срок готовности')
        }
    }
});

