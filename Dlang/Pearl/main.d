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
import core.stdc.string;

void run()
{
	auto conn = HTTP();
	conn.handle.set(CurlOption.ssl_verifypeer, 0);
	conn.handle.set(CurlOption.proxy, "127.0.0.1:8888");
	auto rand = uniform(99999999999999, 99999999999999999);
	conn.setCookieJar(tempDir() ~ to!string(rand));
	conn.addRequestHeader("Cookie", "_ga=GA1.2.1280053819.1424989843; _gat=1; laravel_session=eyJpdiI6IkdJRnVLZ2d5XC93WUk4SzZ4N0NcL2V1UT09IiwidmFsdWUiOiJVSlJ3bVFMYmhTWUgwWTVMZ2ZWRVFHSUQzeUlqUEZJZVFUTk52YlVKb0NuUjhEbkVteTk1S3ZwTXl0OVJ0blZqSlZUdVF0UjN1bmdBdkhudTBWQ2RFZz09IiwibWFjIjoiZjEzYTFkMzlkYzY1MzczMmY5MGM5ZDE3MGQ4ODhkNmVkZTRhZDUyNGMzYWZkMDkwNTAyZDMwZjEwMTM4YjIxMCJ9");
	conn.addRequestHeader("X-Requested-With", "XMLHttpRequest");
	auto html = post("http://www.captain-pearl.com/roll", "amount=1&winchance=70", conn);
	writeln(html);
}

void main(string[] args)
{
	while(true) {
		run();
	}
}

