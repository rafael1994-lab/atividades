<script>

    const usuarios = [
        {usuario: "fredy", senha:"senhaforte123"},
        {usuario: "tonhao", senha:"bastiao123"},
    ];

    document.getElementById("formLogin") .addEventListener("submit",function(log) {
        log.preventDefault();
        const user = document.getElementById("user").value;
        const pass = document.getElementById("pass").value;

        const logado = usuarios.find(x => x.usuario === user && x.senha === pass);


        if(logado){
            sessionStorage.setItem("usuarioLogado", logado.usuario);
            window.location.href = "pages/home.html";
        }else{
            alert("Usuário ou Senha incorretos.")
        }
})

</script>