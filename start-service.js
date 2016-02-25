var child_process = require('child_process')
var child = 0;
//var spawn = child_process.spawn;
var spawn = child_process.exec;

function log(data, lvl) {
   console.log(data);
}

function send(data) {
   if (child == 0)
      log('error: python child is null');
   child.stdin.write(JSON.stringify(data) + '\n');
}

function init(on_data) {
   child = spawn(__dirname + '/py_stdcom.py')
   //child.stdin.write(data);
   child.stderr.on('data', function(data) {
      log('js: got error from python:' + String(data));
   });
   child.stdout.on('data', function(data) {
      var msg = JSON.parse(data);
      if (msg['magic'] != 'gentoo_sicp_rms')
         log('error: bad python message');
      on_data(msg);
   });
}

exports.init = init
exports.send = send
