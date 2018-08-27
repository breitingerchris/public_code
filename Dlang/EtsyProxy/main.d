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
	bool working = false;
	try
	{
		auto conn = HTTP();
		conn.handle.set(CurlOption.ssl_verifypeer, 0);
		conn.operationTimeout(dur!"seconds"(13));
		conn.handle.set(CurlOption.proxy, proxy);
		conn.addRequestHeader("User-Agent", "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2251.0 Safari/537.36");
		
		auto html = get("https://www.reddit.com/login", conn);
		if (html.indexOf("LOG IN") != -1)
		{
			writeln("Proxy Works! " ~ proxy);
			working = true;
		}
		
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
	return;
}

int main(string[] args)
{
	int threads = 32;
	auto proxies = readText(getcwd() ~ "/proxies.txt").splitLines();
	auto work = new TaskPool();
	writeln("Using (" ~ to!string(threads) ~ ") Threads!");
	foreach (proxy; work.parallel(proxies))
	{
		run(proxy);
	}
	return 0;
}
