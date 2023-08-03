document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

// Send the email when the submit button is clicked
function send_email(event) {

  // Get the values
  const recipients = document.querySelector("#compose-recipients").value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;
  
  // Create JSON with required fields
  const email_json = {"recipients": recipients, "subject": subject, "body": body};

  fetch("/emails", {
    method: "POST",
    body: JSON.stringify(email_json)
  })
  .then(response => response.json())
  .then(data => load_mailbox("sent"));
  event.preventDefault();
}

// Fill the compose email form with default 'reply' values
function reply(recipient, subject, body) {

  compose_email();
  document.querySelector('#compose-recipients').value = recipient;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = body;
}

// PUT request to archive the email
function archive(email_id) {

  fetch(`/emails/${email_id}`, {
    method: "PUT",
    body: JSON.stringify({
      archived: true,
    })
  })
  .then(data => load_mailbox("inbox"));
}


// PUT request to unarchive the email
function unarchive(email_id) {

  fetch(`/emails/${email_id}`, {
    method: "PUT",
    body: JSON.stringify({
      archived: false,
    })
  })
  .then(data => load_mailbox("inbox"));
}

// Load an email
function see_email(id, mailbox) {

  // Get the email
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email_info => {

    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';

    // Set the top part of email: sender, recipient(s), subject and timestamp
    let email_info_top = `<p><b>From:</b> ${email_info.sender} <br> <b>To:</b> ${email_info.recipients} <br> <b>Subject:</b> ${email_info.subject} <br> <b>Timestamp:</b> ${email_info.timestamp}</p>`;

    // Allow user to archive/unarchive emails(unless from 'sent' mailbox)
    if (mailbox !== "sent") {
      let email_buttons = "<button class='btn btn-sm btn-outline-primary' id='reply'>Reply</button>";
      if (email_info.archived) {
        email_buttons += "<button class='btn btn-sm btn-outline-primary' id='unarchive'>Unarchive</button>";
      }
      else {
        email_buttons += "<button class='btn btn-sm btn-outline-primary' id='archive'>Archive</button>";
      }
      let email_info_bottom = `<p>${email_info.body}</p>`;
      // Set the email html(in this case for recieved emails in 'inbox' or 'archived')
      document.querySelector('#email-view').innerHTML = email_info_top + email_buttons + "<hr>" + email_info_bottom;
    }
    else {
      let email_info_bottom = `<p>${email_info.body}</p>`;
      // Set the email html(in this case for sent emails)
      document.querySelector('#email-view').innerHTML = email_info_top + "<hr>" + email_info_bottom;
    }

    // Set parameters to reply to email
    let sender = email_info.sender;
    let body = `On ${email_info.timestamp} ${email_info.sender} wrote: ${email_info.body}`;
    let subject;
    if (email_info.subject.slice(0, 4) === "Re: ") {
      subject = email_info.subject;
    }
    else {
      subject = "Re: " + email_info.subject;
    }

    // Add event listeners to reply and archive/unarchive buttons
    if (mailbox !== "sent") {
      document.querySelector("#reply").addEventListener('click', () => reply(sender, subject, body));
      if (email_info.archived) {
        document.querySelector("#unarchive").addEventListener('click', () => unarchive(email_info.id));
      }
      else {
        document.querySelector("#archive").addEventListener('click', () => archive(email_info.id));
      }

      // If email has been opened for first time, set its 'read' property to true
      if (!email_info.read) {
        fetch(`/emails/${id}`, {
          method: "PUT",
          body: JSON.stringify({
            read: true
          })
        })
      }
    }
  })
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  let emails_view = document.querySelector('#emails-view');
  emails_view.style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  emails_view.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get the emails in that mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Creat a table to display the emails
    let email_table = "<table style='width: 100%;'>";
    let row;
    emails.forEach(email => {
      
      // Add each email into the table as a row(tr) element

      // If the email has been read, make it grey, else make it white
      if (email.read) {
        row = `<tr class='email-read' id='${email.id}'><td style='font-weight: bold;'>${email.sender}</td><td>${email.subject}</td><td class='timestamp'>${email.timestamp}</td></tr>`;
      }
      else {
        row = `<tr class='email-unread' id='${email.id}'><td style='font-weight: bold;'>${email.sender}</td><td>${email.subject}</td><td class='timestamp'>${email.timestamp}</td></tr>`;
      }
      email_table += row;
    });
    
    // Add the table to the html
    email_table += "</table>";
    emails_view.innerHTML += email_table;

    // Add event listeners to each row(email) that show the email details when clicked
    let rows = document.querySelectorAll("tr");
    rows.forEach(row => row.addEventListener("click", () => see_email(row.id, mailbox)));
  })
  
}