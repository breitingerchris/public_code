module main;

import etc.c.curl : CurlOption, CurlInfo;
import std.conv;
import core.time;
import std.net.curl;
import std.stdio;
import std.json;
import std.regex;
import std.string;
import std.array;
import std.random;
import std.file;
import std.math;

void run()
{
	auto conn = HTTP();
	conn.handle.set(CurlOption.ssl_verifypeer, 0);
	conn.handle.set(CurlOption.proxy, "127.0.0.1:8888");
	conn.addRequestHeader("User-Agent", "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2305.3 Safari/537.36");
	conn.addRequestHeader("Accept", "application/json, text/plain, */*");
	conn.addRequestHeader("Referer", "https://win88.me/");
	conn.addRequestHeader("Cookie", "btc-pid=yshVU1JB9CHYyC/qCmrslWdLdUgJr5uq37fNmSkGTK0Rbc9XTi71AaebPY09VAUER+c0eODuCl/beNrAVKzJ72qbbD8QakvT0v9; _we_wk_ss_lsf_=true; playMpSound=1; playChatSound=false; btc-googid=e5CWljr4DxT-pvinL99HWq3gIXdbe_AvCIRT_sKUmzWeVkcGLV7T4fRC4oQUZifEmaR9eAUWAhQBKaSzxY59BdL17pVvWFkuiqlYdiVdoFU0_40PmWCVV163b3FRBt4PVsjSrCPFjw9qSJwnPUUh9oNg3EDpsxKfx7iKdSDhu_k8bSRIWqI_ObaQyHJXDcmd0a3BOlMqcE0oMHAAcJGsl_9zCTpV9IP-bRNoJ5KhsWuK9M_rAJQGqG147brLUTTp; betsTabIndex=1; betAmount=%220.00000000%22; lastNewsPostId=51; __zlcmid=TVeStyV8NVUnfE");

	double bet = 0.00000050;
	double min = 0.00000050;
	string seed = "qlk3kq51cqou";
	string over = "false";
	double chance = 49.5;
	double profit = 0.00000000;
	double balance = 0.00002000;

	while(true) {
		auto postData = "{\"BetAmount\":\"" ~ format("%#0.8f", bet) ~ "\",\"ClientSeed\":\""~ seed ~ "\",\"Over\":" ~ over ~ ",\"WinChance\":\""~ format("%#0.4f", chance) ~ "\",\"Edge\":99}";
		auto html = post("https://win88.me/dice/play", postData, conn);
		auto js = parseJSON(html);
		writeln("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
		writeln("Winner: " ~ chomp(js["Winner"].toString()) ~ "\nProfit: " ~ format("%#0.8f", profit) ~ "\nBalance: " ~ format("%#0.8f", balance));
		if (over == "false") {
			over = "true";
		} else {
			over = "false";
		}

		if (chomp(js["Winner"].toString()) == "true")
		{
			if (uniform(0, 2) != 1) {
				bet = min;
			}
			profit += to!double(format("%#0.8f", js["Winnings"].toString()));
			balance += to!double(format("%#0.8f", js["Winnings"].toString()));
		}
		else
		{
			if (uniform(0, 2) != 1) {
				bet = balance;
				chance = 90.0;
			}
			profit -= bet;
			balance -= bet;
		}
	}
}

void main(string[] args)
{
	run();
}

