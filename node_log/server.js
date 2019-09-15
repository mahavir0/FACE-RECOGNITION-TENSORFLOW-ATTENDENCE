var express = require('express');
var app = express();
const fetch = require('node-fetch');
const http=require("http");
var httpServer = http.createServer(app);
httpServer.listen(8081);
var request = require('ajax-request');
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
    subject: 'test subject',        // Plain text
    //html:    '<b>html text</b>'            // HTML
  });
  app.get('/index',function(req,res) {
    res.sendFile(__dirname+'/index.html');
  })

app.get('/mail', function (req, res) {
  request({
    url: 'http://192.168.137.1:5000/getMail',
    method: 'GET',
  }, function(err, res1, body) {
    request({
      url: 'http://192.168.137.1:5000/attendenceByMonth/02',
      method: 'GET',
    }, function(err, res2, body1) {
      console.log(body+"hi"+body1);
      a=JSON.parse(body).mail;
      b=JSON.parse(body1);
      keys=Object.keys(b);
      var i=0;
      a.forEach(element => {
        console.log("hereeee");
        if(element[0].toString()==keys[i]){
          send({ // Overriding default parameters
            to:   element[1],
            subject: 'Regarding Attendence ',
            text: 'Dear Student <br/> Your Attendance '+b[keys[i]] // Override value set as default
          }, function (err, res) {
            console.log('* [example 1.1] send() callback returned: err:', err, '; res:', res);
          });
          i++;
        }
      });
    });
  });

  res.redirect('/index');
})

