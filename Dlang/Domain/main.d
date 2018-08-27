module main;

import core.time;
import etc.c.curl : CurlOption;
import std.array;
import std.conv;
import std.exception;
import std.file;
import std.json;
import std.net.curl;
import std.parallelism;
import std.random;
import std.stdio;
import std.string;
import core.sys.windows.windows;
import core.stdc.string;

void run(string user)
{
	try
	{
		writeln("Begin Checking Account! " ~ user);
		bool working = false;
		auto conn = HTTP();
		conn.handle.set(CurlOption.ssl_verifypeer, false);
		conn.handle.set(CurlOption.proxy, "127.0.0.1:8888");
		conn.operationTimeout(dur!"seconds"(10));
		auto html = get("http://freedomainapi.com/?key=bofod4pg2k&domain=" ~ user ~ ".com", conn);
		auto js = parseJSON(html);
		if (js["available"].toString == "true") {
			writeln("Domain " ~ user ~ " is not registered!");
			std.file.append("./Working.txt", user ~ "\r\n");
		}
	} catch (Exception e) {
		writeln(e.msg);
		core.thread.Thread.sleep(dur!("seconds")(1));
	}
}

void main(string[] args)
{
	auto accounts = readText("./domains.txt").splitLines();
	auto work = new TaskPool(128);
	foreach (account; work.parallel(accounts))
	{
		run(account);
	}
}