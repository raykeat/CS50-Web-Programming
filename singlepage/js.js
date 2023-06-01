//javascript allows us to display single page applications,
//as we can use javascript to manipulate the DOM to display different divs and details,
//without having to make requests to a server

document.addEventListener('DOMContentLoaded',()=>{
    document.querySelectorAll('button').forEach(button=>{
        //this refers to the element that received the event
        //in this case, this refers to the button that was clicked on
        //this.dataset.page means for the button that was clicked, access its data properties and data-page attribute
        button.addEventListener('click', showpage(this.dataset.page))
    })
})


function showpage(page){
    document.querySelectorAll('div').forEach(div =>{
        div.style.display = 'none';
    })
    document.querySelector(`#${page}`).style.display = 'block';
}