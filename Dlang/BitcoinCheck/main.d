module main;

import core.thread;
import etc.c.curl : CurlOption, CurlInfo;
import std.array;
import std.conv;
import std.file;
import std.net.curl;
import std.parallelism;
import core.time;
import std.regex;
import std.string;
import std.process;
import std.json;
import std.uri;
import std.exception;
import std.stdio;

void run(string addr)
{
	try
	{
		auto conn = HTTP();
		conn.handle.set(CurlOption.ssl_verifypeer, 0);
		conn.operationTimeout(dur!"seconds"(25));
		string url = "https://api.chain.com/v2/bitcoin/addresses/" ~ addr ~ "?api-key-id=323bed4cf04731b14f5223649efc4a25";
		auto html = get(url, conn);
		auto js = parseJSON(html);
		if (html.indexOf("total\":{\"balance\":0") == -1) {
			writeln("Address has balance: " ~ addr);
			std.file.append("./Balance.txt", addr ~ " " ~ html ~ "\r\n");
		}
	} catch (CurlException e) {
		writeln(e.msg);
	}
}

void startRun()
{
	int threads = 100;
	auto addrs = readText("./addrs.txt").splitLines();
	auto work = new TaskPool(threads);
	foreach (addr; work.parallel(addrs))
	{
		auto add = matchFirst(addr, regex("Address: (.*?)$"));
		if (!add[1].empty) {
			run(to!string(chomp(add[1])));
		}
	}
}


void main(string[] args)
{
	while (true) {
		auto thing = spawnProcess("./vanitygen64.exe -k -o output.txt 1");
		Thread.sleep(dur!("seconds")(5));
		kill(thing);
		std.file.rename("output.txt", "addrs.txt");
		startRun();
		std.file.remove("addrs.txt");
	}
}

