var sys=require('sys'),
    path=require('path'),
    fs=require('fs'),
    url=require('url'),
    http=require('http');

http.createServer(function(req,res){
	var uri=url.parse(req.url).pathname;
	var filename=path.join(process.cwd(),uri);
	path.exists(filename, function(exists){
		if(!exists){
			res.writeHead(404, {'Content-Type':'text/plain'});
			res.write('404 not found\n');
			res.close();
			return;
		}
		fs.readFile(filename,'binary', function(err, data){
			if(err){
				res.writeHead(500, {'Content-Type':'text/plain'});
				res.write(err+'\n');
				res.close();
				return;
			}

			sys.puts('serving request');
			res.writeHead(200);
			res.write(data, 'binary');
			res.close();
			});
		});
}).listen(8080);
sys.puts('server running at http:127.0.0.1:8080/');
