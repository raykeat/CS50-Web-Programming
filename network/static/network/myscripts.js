
//function to display the edit post section
function editpost(event){
    console.log("Clicked on edit anchor tag");

    var editId = event.target.getAttribute('data-edit-id');
    document.querySelector(`#editdiv2-${editId}`).style.display = "block";
    document.querySelectorAll('#div1').forEach(div=>{
        div.style.display = 'None';
    })
    
}

//function to edit the post by sending fetch request to backend
function updatepost(event,id,csrfToken){
    form = event.target;
    newformcontent = form.elements.editpostcontent.value;
    console.log(newformcontent)
    fetch(`/editpost/${id}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            content : newformcontent,
            id:id
        })
      })
    .then(response => response.json())
    .then(data => {
    //hAndle the response data
    //start a console group
    console.group('Update Post Response'); 
    console.error(data);

    
      console.log(data);
      document.querySelector(`#postcontent-${id}`).innerHTML = newformcontent;
      document.querySelector(`#editdiv2-${id}`).style.display = 'None';
      document.querySelectorAll('#div1').forEach(div => {
        div.style.display = 'block';
      });

      
  });
}


function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  
    if (cookieValue) {
      return cookieValue.pop();
    } else {
      return '';
    }
  }
  
function like(postid,userid){
    //retrieve CSRF token from cookie
    const csrftoken = getCookie('csrftoken'); 
    console.log("button clicked")
    fetch(`/like/${postid}/${userid}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            postid : postid,
            userid:userid
        })
      })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        document.querySelector(`#likes-${postid}`).innerHTML=`&#10084; ${data['likecount']}`;

        
        document.querySelector(`#like-${postid}`).style.display = "none";
        document.querySelector(`#unlike-${postid}`).style.display = "block";
    

    })
}

function unlike(postid,userid){
    const csrftoken = getCookie('csrftoken');
    console.log("button clicked")
    fetch(`/unlike/${postid}/${userid}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            postid : postid,
            userid:userid
        })
      })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        document.querySelector(`#likes-${postid}`).innerHTML=`&#10084; ${data['likecount']}`;

        
        document.querySelector(`#like-${postid}`).style.display = "block";
        document.querySelector(`#unlike-${postid}`).style.display = "none";

    })
}

function followuser(currentuser,userprofile){

     //Send AJAX request to follow user
     $.ajax({
        type: "POST",
        url: "/followuser/" + currentuser + "/" + userprofile + "/",
        data: {
            'currentuser': currentuser,
            'userprofile': userprofile,
            'action': 'follow'
        },
        success: function (response) {
            //showing and hiding buttons after successful follow
            $('#follow').hide();
            $('#unfollow').show();
            $('#followmessage').show();
            console.log('success')
        },
        error: function (response) {
            console.log(response);
        }
    });
}

function unfollowuser(currentuser,userprofile){

    //Send AJAX request to follow user
    $.ajax({
       type: "POST",
       url: "/followuser/" + currentuser + "/" + userprofile + "/",
       data: {
           'currentuser': currentuser,
           'userprofile': userprofile,
           'action': 'unfollow'
       },
       success: function (response) {
           //showing and hiding buttons after successful follow
           $('#follow').show();
           $('#unfollow').hide();
           $('#unfollowmessage').show();
       },
       error: function (response) {
           console.log(response);
       }
   });
}




