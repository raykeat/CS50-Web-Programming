function search() {
    const input = document.getElementById("input").value;
    if (input){
        window.location.href = "/wiki/" + input;
    }
    


}