// Functions
function writeHTTPHeader(path, type) {
    return {'Date' : d.getUTCFullYear()+"/"+d.getUTCMonth()+"/"+d.getUTCDate()+" "+d.getUTCHours()+":"+d.getUTCMinutes()+":"+d.getUTCSeconds()+":"+d.getUTCMilliseconds(),
    'Server' : '',
    'Content-length' : fs.statSync(path).size,
    'Content-type' : type,
    'Cache-control' : 'max-age=2592000',
    'Connection' : 'keep-alive'};
}

// Modules
//  - http: Handle HTTP requests
//  - url: Handle URL manipulation
//  - fd: Filesystem access
var http = require("http");
var url = require('url');
var fs = require('fs');
var d = new Date();

http.createServer(function (req, res) {
    console.log("["+d.getFullYear()+"/"+d.getMonth()+"/"+d.getDate()+" "+d.getHours()+":"+d.getMinutes()+":"+d.getSeconds()+":"+d.getMilliseconds()+"] "+req.method+" "+req.url+" REF: "+req.headers.referer+" via ["+req.connection.remoteFamily+" "+req.connection.remoteAddress+" port "+req.connection.remotePort+"]");
    
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
        res.writeHead(200, writeHTTPHeader("Static/favicon.ico","image/ico"));
        res.write(fs.readFileSync("Static/favicon.ico"));
        return res.end();
    }
    // Return the home page
    else if (filename == "/") {
        filename = "home";
    }
    // Return the blog
    else if (filename == "/blog" || filename == "/blog/") {
        filename = "blog";
    }
    // Return the Post Archives page
    else if (filename == "/archives" || filename == "/archives/") {
        filename = "archives";
    }
    // Return the Projects page
    else if (filename == "/projects" || filename == "/projects/") {
        filename = "projects";
    }
    // Return the MTV demo page
    else if (filename == "/MTV") {
        filename = "Static/MTV.html"
    }
    // Return a post archives page for a specified year
    else if (year_literal.test(filename)) {
        filename = filename.substr(6);
    }
    // Return a post archives page for a specified month
    else if (month_literal.test(filename)) {
        filename = filename.split("/");
        filename = filename[2]+"-"+filename[3];
    }
    // Static resource
    else if (filename.startsWith("/Static") || filename == "/rss") { }
    // Main service worker
    else if (filename.endsWith("sw.js")) { }
    // Return a structure file
    else {
        console.log("Finel else: "+filename);
    }
    // Return a CSS document with the appropriate header
    if (filename.endsWith(".css")) {
        res.writeHead(200, writeHTTPHeader("Static/"+filename.split("/")[2],"text/css"));
        res.write(fs.readFileSync("Static/"+filename.split("/")[2], {encoding: 'utf8'}));
        return res.end();
    }
    // Return the main Service Worker with the appropriate header
    else if (filename.endsWith("sw.js")) {
        res.writeHead(200, writeHTTPHeader(filename.split("/")[1],"text/javascript"));
        res.write(fs.readFileSync(filename.split("/")[1], {encoding: 'utf8'}));
        return res.end();
    }
    // Return a Javascript document with the appropriate header
    else if (filename.endsWith(".js")) {
        res.writeHead(200, writeHTTPHeader("Static/"+filename.split("/")[2],"text/javascript"));
        res.write(fs.readFileSync("Static/"+filename.split("/")[2], {encoding: 'utf8'}));
        return res.end();
    }
    // Return a PNG image with the appropriate header
    else if (filename.endsWith(".png")) {
        res.writeHead(200, writeHTTPHeader("Static/Images/"+filename.split("/")[3], "image/png"));
        res.write(fs.readFileSync("Static/Images/"+filename.split("/")[3]));
        return res.end();
    }
    // Return a WebP image with the appropriate header
    else if (filename.endsWith(".webp")) {
        res.writeHead(200, writeHTTPHeader("Static/Images/"+filename.split("/")[3], "image/webp"));
        res.write(fs.readFileSync("Static/Images/"+filename.split("/")[3]));
        return res.end();
    }
    // Return a JPG image with the appropriate header
    else if (filename.endsWith(".jpg")) {
        res.writeHead(200, writeHTTPHeader("Static/Images/"+filename.split("/")[3], "image/jpg"));
        res.write(fs.readFileSync("Static/Images/"+filename.split("/")[3]));
        return res.end();
    }
    // Return an ICO image with the appropriate header
    else if (filename.endsWith(".ico")) {
        res.writeHead(200, writeHTTPHeader("./"+filename, "image/ico"));
        res.write(fs.readFileSync("./"+filename));
        return res.end();
    }
    // Return an XML document, the RSS feed, with the appropriate header
    else if (filename == "/rss") {
        res.writeHead(200, writeHTTPHeader("./Static/Main_feed.xml", "text/xml"));
        res.write(fs.readFileSync('./Static/Main_feed.xml', {encoding: 'utf8'}));
        return res.end();
    }
    // Return a JSON file with the appropriate header
    else if (filename.endsWith(".json")) {
        res.writeHead(200, writeHTTPHeader("Static/"+filename.split("/")[2], "text/json"));
        res.write(fs.readFileSync("Static/"+filename.split("/")[2]));
        return res.end();
    }
    // Return a static resource
    else if (filename.startsWith("Static") && filename.endsWith(".html")) {
        res.writeHead(200, writeHTTPHeader(filename, "text/html"));
        res.write(fs.readFileSync(filename, {encoding: 'utf8'}));
        return res.end();
    }
    // Final else, for structure files and the error page
    else
    {
        console.log("Second final else.");
        filename = "./Structure/"+filename.replace("/blog/", "")+".html"
        console.log(filename);
        fs.readFile(filename, function(err, data) {
            if (err) {
              res.writeHead(404, writeHTTPHeader('./Structure/system/error.html',"text/html"));
              res.write(fs.readFileSync('./Structure/system/error.html', {encoding: 'utf8'}));
              return res.end();
            }
            res.writeHead(200, writeHTTPHeader(filename, "text/html"));;
            res.write(data);
            return res.end();
        });
    }
}).listen(8080);