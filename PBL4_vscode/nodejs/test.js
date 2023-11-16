var http = require('http');
var url = require('url');
var fs = require('fs');

// http.createServer(function (req, res) {
//   var q = url.parse(req.url, true);
//   var filename = "./html/" + q.pathname;
//   fs.readFile(filename, function(err, data) {
//     if (err) {
//       res.writeHead(404, {'Content-Type': 'text/html'});
//       return res.end("404 Not Found");
//     } 
//     res.writeHead(200, {'Content-Type': 'text/html'});
//     res.write(data);
//     return res.end();
//   });
// }).listen(5000);

const server = http.createServer((req, res) => {
  // set path to html file
  var path = url.parse(req.url, true);
  // set header
  res.setHeader('Content-Type', 'text/html');
  // read file
  var filename = './view/' + path.pathname;
  fs.readFile(filename, function(err, data) {
    if(err) {
      res.statusCode = 404;
      return res.end("404 Not Found");
    }
    res.statusCode = 200;
    //res.write(data);
    res.end(data);
  });
});

const port = 5000;
// localhost is the default value for 2nd argument
const host = 'localhost' //'0.0.0.0'
server.listen(port, host, () => {
  console.log('listening for requests on port ', port);
});