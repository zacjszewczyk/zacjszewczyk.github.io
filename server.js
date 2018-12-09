// Modules
//  - http: Handle HTTP requests
//  - url: Handle URL manipulation
//  - fd: Filesystem access
var http = require("http");
var url = require('url');
var fs = require('fs');

http.createServer(function (req, res) {
    // q: URL request
    // filename: Path to the requested resource
    var q = url.parse(req.url, true);
    var filename = q.pathname;

    // year_literal: Regex for year requests
    // month_literal: Regex for month requests
    var year_literal = /blog\/[0-9]{4}$/g;
    var month_literal = /blog\/[0-9]{4}\/[0-9]{2}$/g;
    
    if (filename == "/favicon.ico") {
        res.writeHead(200, {'Content-type' : 'image/ico'});
        res.write(fs.readFileSync("Static/favicon.ico"));
        return res.end();
    }
    else if (filename == "/") {
        filename = "home.html";
        filename = "Structure/"+filename;
        console.log(filename);
    }
    else if (filename == "/blog") {
        filename = "Structure"+filename+".html";
        console.log(filename);
    }
    else if (filename == "/archives") {
        filename = "Structure"+filename+".html";
        console.log(filename);
    }
    else if (filename == "/projects") {
        filename = "Structure"+filename+".html";
        console.log(filename);
    }
    else if (filename == "/MTV") {
        filename = "Static/MTV.html"
        console.log("MTV: "+filename)
    }
    else if (year_literal.test(filename)) {
        filename = filename.replace("/blog/", "Structure/")+".html";
        console.log(filename);
    }
    else if (month_literal.test(filename)) {
        filename = filename.split("/");
        filename = "Structure/"+filename[2]+"-"+filename[3]+".html";
    }
    else if (filename.startsWith("/Static") || filename == "/rss") {
        console.log("Static: "+filename);
    }
    else {
        if (!filename.endsWith("/main.css")) {
            filename = "Structure/"+filename.split("/")[2]+".html";
            console.log(filename);
        }
        console.log("Finel else: "+filename);
    }
    if (filename.endsWith(".css")) {
        // console.log("Static/"+filename.split("/")[2]);
        res.writeHead(200, {'Content-type' : 'text/css'});
        res.write(fs.readFileSync("Static/"+filename.split("/")[2], {encoding: 'utf8'}));
        return res.end();
    }
    else if (filename.endsWith(".js")) {
        res.writeHead(200, {'Content-type' : 'text/javascript'});
        res.write(fs.readFileSync("Static/"+filename.split("/")[2], {encoding: 'utf8'}));
        return res.end();
    }
    else if (filename.endsWith(".png")) {
        res.writeHead(200, {'Content-type' : 'image/png'});
        res.write(fs.readFileSync("Static/Images/"+filename.split("/")[3]));
        return res.end();
    }
    else if (filename == "/rss") {
        res.writeHead(200, {'Content-type' : 'text/xml'});
        res.write(fs.readFileSync('./Static/Main_feed.xml', {encoding: 'utf8'}));
        return res.end();
    }
    else
    {
        fs.readFile("./"+filename, function(err, data) {
            if (err) {
              res.writeHead(404, {'Content-Type': 'text/html'});
              res.write(fs.readFileSync('./Structure/system/error.html', {encoding: 'utf8'}));
              return res.end();
            }
            res.writeHead(200, {'Content-Type': 'text/html'});
            res.write(data);
            return res.end();
        });
    }
}).listen(8080);