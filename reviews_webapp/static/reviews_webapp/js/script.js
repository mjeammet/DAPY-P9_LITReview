function ThrowConfirmationAlert(argu){
    alert(argu);
    var confirmation = confirm("Etes-vous sûr.e de vouloir supprimer ce post ?");
    if (confirmation == true){
        console.log(window.location.reload())
        // return window.location.replace()
    } else {
        return 0
    }
}