document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  //function to send out email
  document.querySelector('#compose-form').addEventListener('submit', () => send_email());
});


function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#specific-email').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}


function load_specific_email(id,mailbox){
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);

      //getting details for recipients, sender, timestamp, subject, body
      recipients = email.recipients;
      sender = email.sender;
      timestamp = email.timestamp;
      subject = email.subject;
      body = email.body;


      //hiding compose and main email view, but show this email
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector('#specific-email').style.display = 'block';

      console.log(mailbox, email.archived);
      document.querySelector('#specific-email').innerHTML = `
        <div>
          <h5>From: ${sender} </h5>
          <h5>To: ${recipients}</h5>
          <h5>Subject: ${subject}</h5>
          <h5>Timestamp: ${timestamp}</h5>
        </div>
        <button class="btn btn-sm btn-outline-primary" id="Reply">Reply</button>
        ${mailbox === 'inbox' && !email.archived ? '<button id="archivebutton" class="btn btn-sm btn-outline-primary">Archive</button>' : ''}
        ${mailbox === 'archive' && email.archived ? '<button id="unarchivebutton" class="btn btn-sm btn-outline-primary">Unarchive</button>' : ''}
        <hr id="horizontal-line">
        <div>
          <h5>${body}</h5>
        </div>
      `;
      /* lines 60 and 61 use ternary operator to display archive and unarchive buttons */

      //event listener for clicking the reply button
      document.querySelector('#Reply').addEventListener('click',()=>reply_email(email));

      if (document.querySelector('#archivebutton')){
        document.querySelector('#archivebutton').addEventListener('click', ()=> archive_email(email));
      }

      if (document.querySelector('#unarchivebutton')){
        document.querySelector('#unarchivebutton').addEventListener('click', ()=> unarchive_email(email));
      }

        //making API call to update email as read
        if (!email.read){
          fetch(`/emails/${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                read: true
            })
          });
        }
  });
}  

function reply_email(email){
        //only show compose-view
        document.querySelector('#emails-view').style.display = 'none';
        document.querySelector('#compose-view').style.display = 'block';
        document.querySelector('#specific-email').style.display = 'none';

        document.querySelector('#compose-recipients').value = `${email.sender}`; 
        document.querySelector('#compose-subject').value = `Re: ${email.subject}`; 
        document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`; 

}


function archive_email(email){
  //updating archive status to true for email
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: true
    })
  }).then(() => {
    // Wait for the archive operation to complete before reloading the mailbox
    setTimeout(() => load_mailbox('inbox'), 500);
  });
}

function unarchive_email(email){
  console.log("Unarchiving email:", email);
  //updating archive status to true for email
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: false
    })
  }).then(() => {
    console.log("Email unarchived successfully");
    // Wait for the archive operation to complete before reloading the mailbox
    setTimeout(() => load_mailbox('inbox'), 500);
  }).catch(error => {
    console.log("Error unarchiving email:", error);
  });
}





function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#specific-email').style.display = 'none';

  // setting the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //calling the API to display all the emails in a particular mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      if(emails.length === 0){
        const newemail = document.createElement('div');
        newemail.innerHTML = "No emails";
        document.querySelector('#emails-view').append(newemail);
      } else{

        //looping through all the emails 
        emails.forEach(email=>{

          //creating a div for each email
          const newemail = document.createElement('div');
          //adding a boostrap CSS class of "list-group-item" to the email
          newemail.className = "list-group-item border-style";
          newemail.innerHTML = `
            <div style="display: flex; justify-content: space-between;">
              <h5>${email.sender}</h5>
              <h5>${email.subject} </h5>
              <h5>${email.timestamp}</h5>
            </div>`;
          newemail.style.border = "3px solid bisque"; //add a border
          newemail.style.borderRadius = "3px";

          if (email.read){
            newemail.style.backgroundColor = "lightgrey";
          } else{
            newemail.style.backgroundColor = "white";
          }
        
          newemail.addEventListener('click', () => {
            load_specific_email(email.id,mailbox);
            email.read = true;
          });
          document.querySelector('#emails-view').append(newemail);
        })
      }
  });
}


//function to send email when form for composing email is submitted
function send_email(){

  //getting the value of recipients, subject and body input fields
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  //send data to backend
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body,
    })
  })
  .then(response => response.json())
  .then(result => {
  // Print result
  console.log(result);
  //redirect user to sent mailbox
  load_mailbox('sent');
  });

}

