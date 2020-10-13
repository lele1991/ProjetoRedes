//framework website frontend backend "link"
var app = require('express')();
//coneccao do ip ao programa
var http = require('http').Server(app);
var io = require('socket.io')(http);
var awsIot = require('aws-iot-device-sdk');
var port = process.env.PORT || 3000;

//mostra a pg pra quem se conecta
app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});
/*
io.on('connection', function(socket){
  socket.on('chat message', function(msg){
    io.emit('chat message', msg);
  });
});
*/

//escuta a porta "3000"
http.listen(port, function(){
  console.log('listening on *:' + port);
});


var device = awsIot.device({
  keyPath: "./Cert/private.pem.key",
  certPath: "./Cert/certificate.pem.crt",
  caPath: "./Cert/ca.crt",
  clientId: "EDPStorage",
  region: "us-east-1",
  host: "a25kfjnhv6wcrv-ats.iot.us-east-1.amazonaws.com",
  port: 8883
});


device.on("connect", function() {
  console.log("conected");
  device.subscribe('monitoramentoPlanta/#'); //wildcard
});

device.on("error", function(err) {
  console.log(err);
});

//msg mqtt
device.on('message', function(topic, payload) {
  console.log('message', topic, payload.toString());
  if(topic == "monitoramentoPlanta/temperatura"){
    io.emit('temperatura', payload.toString());
  }
  if(topic == "monitoramentoPlanta/umidade"){
    io.emit('umidade', payload.toString());
  }
    
});
