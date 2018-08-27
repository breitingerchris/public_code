module main;

import core.time;
import etc.c.curl : CurlOption;
import std.array;
import std.conv;
import std.digest.md;
import std.exception;
import std.file;
import std.json;
import std.net.curl;
import std.parallelism;
import std.random;
import std.regex;
import std.stdio;
import std.string;
import core.sys.windows.windows;
import core.stdc.string;

void run(string user)
{
	while (true) {
		try
		{
			writeln("Begin Checking Account! " ~ user);
			bool working = false;
			char[][] orders;
			string gcb;
			string captchatext;
			auto conn = HTTP();
			conn.handle.set(CurlOption.ssl_verifypeer, false);
			conn.operationTimeout(dur!"seconds"(10));
			
			auto rand = uniform(99999999999999, 99999999999999999);
			conn.setCookieJar(tempDir() ~ to!string(rand));
			conn.addRequestHeader("User-Agent", "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.0 Safari/537.36");
			auto html = get("http://freedomainapi.com/?key=bofod4pg2k&domain=" ~ user ~ ".com", conn);
			auto js = parseJSON(html);
			if (js["available"].toString == "true") {
				writeln("Domain " ~ user ~ " is not registered!");
				std.file.append("./Working.txt", js["available"].toString);
			}
		} catch (Exception e) {
			writeln(e.msg);
			core.thread.Thread.sleep(dur!("seconds")(1));
		}
	}
}

void startRun(string file, int threads, string duser = null, string dpass = null)
{
	auto accounts = readText("./domains.txt").splitLines();
	auto work = new TaskPool(threads);
	foreach (account; work.parallel(accounts))
	{
		run(account);
	}
}