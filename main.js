var app = require('app');
app.commandLine.appendSwitch('enable-smooth-scrolling', true);
var BrowserWindow = require('browser-window');
var mainWindow = null;


var j = require('jscloak');
var utils = j.utils;
var sprintf = utils.sprintf;

var log = (msg) => {
   console.log('javscript:')
   console.log(msg)
};

var pyipc = require('./start-service');
var ipc = require('ipc');

app.on('ready', function() {
   // Create the browser window.
   mainWindow = new BrowserWindow({
	  'width' : 802,
	  'height' : 375,
     'center' : true,
	  'frame' : false,
	  'resizable ' : false,
	  'transparent' : false,
	  'overlay-scrollbars' : false,
	  'title-bar-style': 'hidden'
   });

	var wc = mainWindow.webContents;

	var debug = false;
	for (x in process.argv) {
		switch (process.argv[x]) {
		case '--debug':
			debug = true;
			break;
		default:
			break;
		}
	}

	//var cmd = utils.sprintf('init_updater_api(%s);', debug);
	//wc.executeJavaScript(cmd);

   // and load the index.html of the app.
	var url = sprintf('file://%s/index.html', __dirname);
   mainWindow.loadURL(url);

	function onData(data) {
		wc.executeJavaScript(sprintf('onPyMsg(%s);', data));
	}

	pyipc.init(onData);

	ipc.on('pyMsg', function(event, msg) {
		pyipc.send(msg);
	});
	//ipc.send('Hello');


   // Open the DevTools.
   if (debug)
      mainWindow.openDevTools();

   // Emitted when the window is closed.
   mainWindow.on('closed', function() {
      // Dereference the window object, usually you would store windows
      // in an array if your app supports multi windows, this is the time
      // when you should delete the corresponding element.
      //wc = null;
      mainWindow = null;
   });
});

app.on('window-all-closed', function() {
   if (process.platform != 'darwin') {
      app.quit();
   }
});


