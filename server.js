// Modules
//  - http: Handle HTTP requests
//  - url: Handle URL manipulation
//  - fd: Filesystem access
var http = require("http");
var url = require('url');
var fs = require('fs');
var d = new Date();

http.createServer(function (req, res) {
    console.log("["+d.getFullYear()+"/"+d.getMonth()+"/"+d.getDate()+" "+d.getHours()+":"+d.getMinutes()+":"+d.getSeconds()+":"+d.getMilliseconds()+"] "+req.method+" "+req.url+" REF: "+req.headers.referer);
    
    // q: URL request
    // filename: Path to the requested resource
    var q = url.parse(req.url, true);
    var filename = q.pathname;

    // year_literal: Regex for year requests
    // month_literal: Regex for month requests
    var year_literal = /blog\/[0-9]{4}$/g;
    var month_literal = /blog\/[0-9]{4}\/[0-9]{2}$/g;
    
    // Return the favicon
    if (filename == "/favicon.ico") {
        res.writeHead(200, {'Content-type' : 'image/ico'});
        res.write(fs.readFileSync("Static/favicon.ico"));
        return res.end();
    }
    // Return the home page
    else if (filename == "/") {
        filename = "Structure/home.html";
        // console.log(filename);
    }
    // Return the blog
    else if (filename == "/blog") {
        filename = "Structure"+filename+".html";
        // console.log(filename);
    }
    // Return the Post Archives page
    else if (filename == "/archives") {
        filename = "Structure"+filename+".html";
        // console.log(filename);
    }
    // Return the Projects page
    else if (filename == "/projects") {
        filename = "Structure"+filename+".html";
        // console.log(filename);
    }
    // Return the MTV demo page
    else if (filename == "/MTV") {
        filename = "Static/MTV.html"
        // console.log("MTV: "+filename)
    }
    // Return a post archives page for a specified year
    else if (year_literal.test(filename)) {
        filename = filename.replace("/blog/", "Structure/")+".html";
        // console.log(filename);
    }
    // Return a post archives page for a specified month
    else if (month_literal.test(filename)) {
        filename = filename.split("/");
        filename = "Structure/"+filename[2]+"-"+filename[3]+".html";
    }
    // Static resource
    else if (filename.startsWith("/Static") || filename == "/rss") {
        // console.log("Static: "+filename);
    }
    // Main service worker
    else if (filename.endsWith("sw.js")) {
        // console.log("Main SW: "+filename)
    }
    // Return a structure file
    else {
        if (!filename.endsWith("/main.css")) {
            filename = "Structure/"+filename.split("/")[2]+".html";
            // console.log(filename);
        }
        console.log("Finel else: "+filename);
    }
    // Return a CSS document with the appropriate header
    if (filename.endsWith(".css")) {
        // console.log("Static/"+filename.split("/")[2]);
        res.writeHead(200,
            {'Content-type' : 'text/css',
            'Cache-control' : 'public',
            'Cache-control' : 'max-age=2592000'}
            );
        res.write(fs.readFileSync("Static/"+filename.split("/")[2], {encoding: 'utf8'}));
        return res.end();
    }
    // Return the main Service Worker with the appropriate header
    else if (filename.endsWith("sw.js")) {
        res.writeHead(200,
            {'Content-type' : 'text/javascript',
            'Cache-control' : 'public',
            'Cache-control' : 'max-age=2592000'}
            );
        res.write(fs.readFileSync(filename.split("/")[1], {encoding: 'utf8'}));
        return res.end();
    }
    // Return a Javascript document with the appropriate header
    else if (filename.endsWith(".js")) {
        res.writeHead(200,
            {'Content-type' : 'text/javascript',
            'Cache-control' : 'public',
            'Cache-control' : 'max-age=2592000'}
            );
        res.write(fs.readFileSync("Static/"+filename.split("/")[2], {encoding: 'utf8'}));
        return res.end();
    }
    // Return a PNG image with the appropriate header
    else if (filename.endsWith(".png")) {
        res.writeHead(200,
            {'Content-type' : 'image/png',
            'Cache-control' : 'public',
            'Cache-control' : 'max-age=2592000'}
            );
        res.write(fs.readFileSync("Static/Images/"+filename.split("/")[3]));
        return res.end();
    }
    // Return a WebP image with the appropriate header
    else if (filename.endsWith(".webp")) {
        res.writeHead(200,
            {'Content-type' : 'image/webp',
            'Cache-control' : 'public',
            'Cache-control' : 'max-age=2592000'}
            );
        res.write(fs.readFileSync("Static/Images/"+filename.split("/")[3]));
        return res.end();
    }
    // Return a JPG image with the appropriate header
    else if (filename.endsWith(".jpg")) {
        res.writeHead(200,
            {'Content-type' : 'image/jpg',
            'Cache-control' : 'public',
            'Cache-control' : 'max-age=2592000'}
            );
        res.write(fs.readFileSync("Static/Images/"+filename.split("/")[3]));
        return res.end();
    }
    // Return an XML document, the RSS feed, with the appropriate header
    else if (filename == "/rss") {
        res.writeHead(200, {'Content-type' : 'text/xml'});
        res.write(fs.readFileSync('./Static/Main_feed.xml', {encoding: 'utf8'}));
        return res.end();
    }
    // Return a JSON file with the appropriate header
    else if (filename.endsWith(".json")) {
        res.writeHead(200,
            {'Content-type' : 'text/json',
            'Cache-control' : 'public',
            'Cache-control' : 'max-age=2592000'}
            );
        res.write(fs.readFileSync("Static/"+filename.split("/")[2]));
        return res.end();
    }
    // Final else, for structure files and the error page
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