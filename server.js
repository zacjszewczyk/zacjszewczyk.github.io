var http = require("http");
var url = require('url');
var fs = require('fs');

http.createServer(function (req, res) {
    var q = url.parse(req.url, true);
    var filename = q.pathname;
    // console.log(typeof(filename));
    var year_literal = /blog\/[0-9]{4}$/g;
    var month_literal = /blog\/[0-9]{4}\/[0-9]{2}$/g;
    if (filename == "/favicon.ico") {
        return;
    }
    else if (filename == "/") {
        filename = "home.html";
        filename = "templates/"+filename;
        console.log(filename);
    }
    else if (filename == "/blog") {
        filename = "templates"+filename+".html";
        console.log(filename);
    }
    else if (filename == "/archives") {
        filename = "templates"+filename+".html";
        console.log(filename);
    }
    else if (filename == "/projects") {
        filename = "templates"+filename+".html";
        console.log(filename);
    }
    else if (year_literal.test(filename)) {
        filename = filename.replace("/blog/", "templates/")+".html";
        console.log(filename);
    }
    else if (month_literal.test(filename)) {
        filename = filename.split("/");
        filename = "templates/"+filename[2]+"-"+filename[3]+".html";
        console.log(filename);
    }
    else if (filename.startsWith("/static") || filename == "/rss") {
        console.log("static: "+filename);
    }
    else {
        if (!filename.endsWith("/main.css")) {
            console.log(filename);
            filename = "templates/"+filename.split("/")[2]+".html";
            console.log(filename);
        }
    }

    if (filename.endsWith("/main.css")) {
        res.writeHead(200, {'Content-type' : 'text/css'});
        res.write(fs.readFileSync('./static/main.css', {encoding: 'utf8'}));
        res.end();
    }
    else if (filename == "/rss") {
        res.writeHead(200, {'Content-type' : 'text/xml'});
        res.write(fs.readFileSync('./static/Main_feed.xml', {encoding: 'utf8'}));
        res.end();
    }
    else
    {
        fs.readFile("./"+filename, function(err, data) {
            if (err) {
              res.writeHead(404, {'Content-Type': 'text/html'});
              res.write(fs.readFileSync('./templates/system/error.html', {encoding: 'utf8'}));
              return res.end();
            }  
            res.writeHead(200, {'Content-Type': 'text/html'});
            res.write(data);
            return res.end();
        });
    }
}).listen(8080);