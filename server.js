var http = require("http");
var url = require('url');
var fs = require('fs');

http.createServer(function (req, res) {
    var q = url.parse(req.url, true);
    var filename = q.pathname;
    // console.log(filename);
    if (filename == "/favicon.ico") {
        return;
    }
    else if (filename == "/") {
        filename = "home.html";
        filename = "templates/"+filename
        console.log(filename);
    }
    else if (filename == "/blog") {
        filename = "templates"+filename+".html"
        console.log(filename);
    }
    else if (filename == "/rss") {
        filename = "templates"+filename+".html"
        console.log(filename);
    }
    else if (filename == "/archives") {
        filename = "templates"+filename+".html"
        console.log(filename);
    }
    else if (filename == "/projects") {
        filename = "templates"+filename+".html"
        console.log(filename);
    }
    else if (filename == "/admin") {
        filename = "templates"+filename+".html"
        console.log(filename);
    }
    else {
        console.log(filename);
    }
    if (filename == "/main.css") {
        res.writeHead(200, {'Content-type' : 'text/css'});
        var fileContents = fs.readFileSync('./static/main.css', {encoding: 'utf8'});
        res.write(fileContents);
        res.end();
    }
    else
    {
        fs.readFile("./"+filename, function(err, data) {
            if (err) {
              res.writeHead(404, {'Content-Type': 'text/html'});
              return res.end("404 Not Found");
            }  
            res.writeHead(200, {'Content-Type': 'text/html'});
            res.write(data);
            return res.end();
        });
    }
}).listen(8080);