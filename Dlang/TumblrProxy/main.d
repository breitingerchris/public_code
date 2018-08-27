module main;

import std.stdio;
import etc.c.curl : CurlOption, CurlInfo;
import std.exception;
import std.net.curl;
import core.time;
import std.file;
import std.parallelism;
import std.string;
import std.random;
import std.conv;

void run(string proxy)
{
	bool working = true;
	try
	{
		auto conn = HTTP();
		conn.handle.set(CurlOption.ssl_verifypeer, 0);
		conn.operationTimeout(dur!"seconds"(10));
		conn.handle.set(CurlOption.proxy, proxy);
		auto rand = uniform(99999999999999, 99999999999999999);
		conn.setCookieJar(tempDir() ~ to!string(rand));
		conn.addRequestHeader("User-Agent", "Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30");
		
		auto html = get("https://www.tumblr.com/login?from_splash=1", conn);
		
	}
	catch (Exception e)
	{
		writeln("Proxy Does Not Works! " ~ proxy);
		working = false;
	}
	
	if (working)
	{
		writeln("Proxy Works! " ~ proxy);
		std.file.append("./working.txt", proxy ~ "\r\n");
	}
}

int main(string[] args)
{
	int threads = 256;
	auto proxies = readText("./proxies.txt").splitLines();
	auto work = new TaskPool(threads);
	foreach (proxy; work.parallel(proxies))
	{
		run(proxy);
	}
	return 0;
}
