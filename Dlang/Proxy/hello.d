module main;

import std.stdio;
import etc.c.curl : CurlOption, CurlInfo;
import std.exception;
import std.net.curl;
import core.time;
import std.file;
import std.parallelism;
import std.string;
import std.random;
import std.conv;

void run(string proxy)
{
    bool working = true;
    try
    {
        auto conn = HTTP();
        conn.handle.set(CurlOption.ssl_verifypeer, 0);
        conn.operationTimeout(dur!"seconds"(25));
        conn.handle.set(CurlOption.proxy, proxy);
        auto rand = uniform(99999999999999, 99999999999999999);
        conn.setCookieJar(tempDir() ~ to!string(rand));
        conn.addRequestHeader("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8");
        conn.addRequestHeader("Accept-Language", "en-US,en;q=0.8");
        conn.addRequestHeader("Origin", "https://www.amazon.co.uk");
        conn.addRequestHeader("User-Agent", "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2251.0 Safari/537.36");

        auto html = get("https://www.amazon.co.uk/ap/signin?_encoding=UTF8&accountStatusPolicy=P1&openid.assoc_handle=gbflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.co.uk%2Fgp%2Fcss%2Forder-history%3Fie%3DUTF8%26ref_%3Dnav_gno_yam_yrdrs&pageId=webcs-yourorder&showRmrMe=1", conn);
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
        writeln("Proxy Works! " ~ proxy);
        std.file.append("./working.txt", proxy ~ "\r\n");
    }
}

int main(string[] args)
{
    int threads = 256;
    auto proxies = readText(getcwd() ~ "/proxies.txt").splitLines();
    auto work = new TaskPool(threads);
    writeln("Using (" ~ to!string(threads) ~ ") Threads!");
    foreach (proxy; work.parallel(proxies))
    {
        run(proxy);
    }
	return 0;
}
