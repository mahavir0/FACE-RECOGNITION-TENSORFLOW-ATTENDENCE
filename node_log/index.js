console.log('* [example 1.1] sending test email');
 
// Require'ing module and setting default options
 
var send = require('gmail-send')({
//var send = require('../index.js')({
  user: 'mahavirpatel0@gmail.com',
  // user: credentials.user,                  // Your GMail account used to send emails
  pass: 'nikhilpatel',
  // pass: credentials.pass,                  // Application-specific password
  to:   'shahneel1562@gmail.com',
  // to:   credentials.user,                  // Send to yourself
                                           // you also may set array of recipients:
                                           // [ 'user1@gmail.com', 'user2@gmail.com' ]
  // from:    credentials.user,            // from: by default equals to user
  // replyTo: credentials.user,            // replyTo: by default undefined
  // bcc: 'some-user@mail.com',            // almost any option of `nodemailer` will be passed to it
  subject: 'test subject',
  text:    'gmail-send example 1',         // Plain text
  //html:    '<b>html text</b>'            // HTML
});
 
 
// Override any default option and send email
 
console.log('* [example 1.1] sending test email');
 
send({ // Overriding default parameters
  subject: 'attached ' // Override value set as default
}, function (err, res) {
  console.log('* [example 1.1] send() callback returned: err:', err, '; res:', res);
});
 